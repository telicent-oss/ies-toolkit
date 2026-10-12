"""Tests guarding the ontology -> Python code generation.

These complement the behavioural tests in test_ies_core.py by guarding the
*generator* itself: that the committed generated module is in sync with the
ontologies, that it is faithful to them, and that ontology-derived semantics
(instance_type from ies_top:powertype) are correct.
"""
import importlib.util
from pathlib import Path

import pytest

from ies_toolkit.rdflib_plugin import RdfLibPlugIn
from ies_toolkit import ies_core as ic

ROOT = Path(__file__).resolve().parent.parent.parent  # tests/generator/ -> repo root
GENERATED = ROOT / "ies_toolkit" / "ies_core_generated.py"


def _load(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _norm(text):
    return text.replace("\r\n", "\n")


@pytest.mark.parametrize("target", ["core", "top"])
def test_generated_file_is_up_to_date(target):
    """Each committed *_generated.py must equal a fresh generation from the
    current ontologies. Fails if the ontology changed without regenerating, or
    if the generated file was hand-edited."""
    gen = _load("generate_ies", ROOT / "tools" / "generate_ies.py")
    cfg = gen.TARGETS[target]
    builders = (gen.relations_model(cfg, gen.load_graph(), gen.load_shacl(cfg))
                if cfg.get("shacl_files") else {})
    emit_parents, is_state, emitted, inst_types = gen.build_model(cfg, full_mi=cfg["full_mi"])
    expected = gen.render(cfg, emit_parents, is_state, emitted, inst_types, relation_hosts=set(builders))
    actual = Path(cfg["out"]).read_text(encoding="utf-8")
    assert _norm(actual) == _norm(expected), (
        f"{Path(cfg['out']).name} is out of date - "
        f"run: python tools/generate_ies.py --target {target}"
    )


@pytest.mark.parametrize("target", ["core", "top"])
def test_terms_file_is_up_to_date(target):
    """Each committed per-module terms file (typed namespace + URI registry) must
    equal a fresh render (ontology-derived)."""
    gen = _load("generate_ies", ROOT / "tools" / "generate_ies.py")
    cfg = gen.TARGETS[target]
    expected = gen.render_terms(cfg)
    actual = Path(cfg["terms_out"]).read_text(encoding="utf-8")
    assert _norm(actual) == _norm(expected), (
        f"{Path(cfg['terms_out']).name} is out of date - "
        f"run: python tools/generate_ies.py --target {target}"
    )


def test_namespace_constants_are_the_single_source():
    """ies_toolkit/constants.py is the one definition of the IES namespaces; the
    generator imports them, and they must match the ontology's declared @prefix."""
    import rdflib
    from ies_toolkit import constants
    gen = _load("generate_ies", ROOT / "tools" / "generate_ies.py")
    assert gen.TOP_NS is constants.IES_TOP and gen.CORE_NS is constants.IES_CORE
    declared = {p: str(u) for p, u in gen.load_graph().namespaces()}  # load_graph also guards this
    assert declared["ies_top"] == constants.IES_TOP
    assert declared["ies_core"] == constants.IES_CORE


def test_generation_fails_on_namespace_bump_without_constant_update():
    """The ontology guard: a declared @prefix that disagrees with the constants raises."""
    import rdflib
    gen = _load("generate_ies", ROOT / "tools" / "generate_ies.py")
    g = rdflib.Graph()
    g.bind("ies_top", rdflib.Namespace("http://purl.org/ies/top/v1/ont/"))  # bumped, constant not
    g.bind("ies_core", rdflib.Namespace(gen.CORE_NS))
    with pytest.raises(ValueError, match="ies_top"):
        gen._validate_namespaces(g)


def test_relations_file_is_up_to_date():
    """The committed relations module must equal a fresh render_relations."""
    gen = _load("generate_ies", ROOT / "tools" / "generate_ies.py")
    cfg = gen.TARGETS["core"]
    builders = gen.relations_model(cfg, gen.load_graph(), gen.load_shacl(cfg))
    expected = gen.render_relations(cfg, builders)
    actual = Path(cfg["relations_out"]).read_text(encoding="utf-8")
    assert _norm(actual) == _norm(expected), (
        "ies_core_relations_generated.py is out of date - "
        "run: python tools/generate_ies.py --relations --target core"
    )


def test_generated_classes_are_faithful_to_ontology():
    """Every generated class's bases are real ontology parents and its init
    style matches its State-descent. Guards the generator's correctness
    independently of the drift check."""
    verify = _load("verify_generated", ROOT / "tools" / "verify_generated.py")
    onto, all_names = verify.ontology_model()
    gen = {k: v for k, v in verify.parse_classes(GENERATED).items() if k in onto}

    missing = set(onto) - set(gen)
    assert not missing, f"ontology classes missing from generated module: {sorted(missing)}"

    for name, (bases, style) in gen.items():
        onto_parents, onto_style = onto[name]
        # every generated base that names an ontology class must be a real ontology
        # parent (the woven mixins / *_Relations are not ontology classes, so skip) ...
        for base in bases:
            if base in all_names:
                assert base in onto_parents, f"{name}: base {base} is not an ontology parent"
        # ... and (full-MI) every ontology parent must appear in the bases, so a
        # silently dropped parent (e.g. a future Turtle reserialisation) and the
        # resulting wrong MRO is caught rather than passing CI.
        for parent in onto_parents:
            assert parent in bases, f"{name}: ontology parent {parent} missing from generated bases {bases}"
        assert style == onto_style, f"{name}: init style {style!r} != ontology {onto_style!r}"


# (SetClass, member type) pairs derived from ies_top:powertype. instance_type
# must be the member type, and .instantiate() must mint it. Regression guard for
# the self-referential-instance_type bug.
POWERTYPE_CASES = [
    ("SetOfSigns", "Sign"),
    ("SetOfCharacterStrings", "CharacterString"),
    ("SetOfNames", "Name"),
    ("SetOfRepresentations", "Representation"),
    ("SetOfIndividualDocuments", "IndividualDocument"),
    ("SetOfSetOfSigns", "SetOfSigns"),
    ("SetOfPersons", "Person"),
    ("SetOfLivingOrganisms", "LivingOrganism"),
    ("SetOfInformationProcessingSystems", "InformationProcessingSystem"),
]


@pytest.mark.parametrize("set_cls_name,member_cls_name", POWERTYPE_CASES)
def test_instance_type_matches_powertype(set_cls_name, member_cls_name):
    store = RdfLibPlugIn()
    set_cls = getattr(ic, set_cls_name)
    member_cls = getattr(ic, member_cls_name)
    inst = set_cls(store=store, uri="http://test.org/set")
    assert inst.instance_type is member_cls
    minted = inst.instantiate(uri="http://test.org/member")
    assert isinstance(minted, member_cls)


def test_instantiate_without_uri_mints_a_member():
    """Regression: rdfs.instantiate() with no uri must auto-generate one and
    return a real member (previously returned None - missing call parens)."""
    store = RdfLibPlugIn()
    s = ic.SetOfSigns(store=store, uri="http://test.org/set")
    member = s.instantiate()  # no uri -> store mints one
    assert member is not None, "instantiate() with no uri returned None"
    assert isinstance(member, ic.Sign)
    assert member.uri


# ---------------------------------------------------------------------------
# SHACL faithfulness. The drift tests above pin the generated files byte-for-byte;
# these check the layer above that: that every constrained SHACL property-shape
# is either realized as a builder or a *documented* exclusion, and that each
# builder in the model reaches the generated file as a method. A new or changed
# shape that is neither realized nor documented trips these tests so it gets
# triaged rather than silently dropped.
# ---------------------------------------------------------------------------

# Core targetClass wrapper -> why its constrained SHACL shape emits no reified
# builder. Every entry is a decision to record, not code around; prune an entry
# once its shape is realized or removed (test_no_stale_documented_exclusions).
KNOWN_UNREALIZED = {
    # generic root - the curated ActivityMixin.add_participant covers it
    "IesCore_Participation": "generic root; covered by curated ActivityMixin.add_participant",

    # boundary state whose bounded entity is a top-namespace class; the core weave
    # attaches only core hosts - realized once top-target relations are generated
    "IesCore_Modify": "boundary targets IesTop_State (top namespace); pending top-target relations",

    # plain 1-hop object edges (isPartOf / isTemporalPartOf / hasCharacteristic)
    # that are neither reified participation/boundary nodes nor representations;
    # the generated 1-hop 'Layer A' relations are not implemented
    "IesCore_AccountAdminActivity": "plain structural isPartOf; Layer A (1-hop relations) not implemented",
    "IesCore_CoLocation": "plain structural isPartOf; Layer A not implemented",
    "IesCore_Movement": "plain structural isPartOf; Layer A not implemented",
    "IesCore_PartyInCommunication": "plain structural isPartOf; Layer A not implemented",
    "IesCore_TransactionActivity": "plain structural isPartOf; Layer A not implemented",
    "IesCore_Installed": "plain structural isTemporalPartOf; Layer A not implemented",
    "IesCore_Artefact": "hasName is ThingMixin.add_name; hasCharacteristic is a plain edge (Layer A)",
}


def _relations_state(gen):
    cfg = gen.TARGETS["core"]
    g_shacl = gen.load_shacl(cfg)
    builders = gen.relations_model(cfg, gen.load_graph(), g_shacl)
    return gen.shacl_model(g_shacl), builders


def _realized(gen, model, builders):
    """Set of targetClass wrappers whose shape produced at least one builder -
    either as a minted participation/boundary node, or as a representation host."""
    built_nodes = {s["node"] for specs in builders.values() for s in specs if "node" in s}
    rep_hosts = {h for h, specs in builders.items()
                 if any(s.get("kind") == "representation" for s in specs)}
    realized = set()
    for tc_uri, rows in model.items():
        w = gen.py_name(tc_uri)
        if rows and w and (tc_uri in built_nodes or w in rep_hosts):
            realized.add(w)
    return realized


def test_shacl_shapes_are_realized_or_documented():
    """Every constrained core SHACL shape is realized as a builder or listed in
    KNOWN_UNREALIZED. Fails if a shape appears that is neither."""
    gen = _load("generate_ies", ROOT / "tools" / "generate_ies.py")
    model, builders = _relations_state(gen)
    realized = _realized(gen, model, builders)

    unaccounted = []
    for tc_uri, rows in model.items():
        if not rows:
            continue  # bare targetClass registration, no property constraints
        w = gen.py_name(tc_uri)
        if w is None:
            continue  # foreign class, deliberately dropped by py_name
        if w in realized or w in KNOWN_UNREALIZED:
            continue
        unaccounted.append((w, sorted({r["path_local"] for r in rows})))
    assert not unaccounted, (
        "SHACL property-shapes neither realized as a builder nor documented - "
        "triage each (realize it, or add to KNOWN_UNREALIZED with a reason):\n"
        + "\n".join(f"  {w}: {paths}" for w, paths in sorted(unaccounted)))


def test_no_stale_documented_exclusions():
    """Each KNOWN_UNREALIZED entry must still be an unrealized shape in the model,
    so the ledger is pruned when a shape becomes realized or is removed."""
    gen = _load("generate_ies", ROOT / "tools" / "generate_ies.py")
    model, builders = _relations_state(gen)
    realized = _realized(gen, model, builders)
    shaped = {gen.py_name(tc) for tc, rows in model.items() if rows}

    now_realized = sorted(w for w in KNOWN_UNREALIZED if w in realized)
    assert not now_realized, f"KNOWN_UNREALIZED entries are now realized, remove them: {now_realized}"
    absent = sorted(w for w in KNOWN_UNREALIZED if w not in shaped)
    assert not absent, f"KNOWN_UNREALIZED entries no longer have a SHACL shape, remove them: {absent}"


def test_every_builder_spec_is_emitted_as_a_method():
    """The generated relations module exposes one {Host}_Relations class per model
    host and exactly one add_* method per builder spec - nothing dropped, nothing
    invented."""
    gen = _load("generate_ies", ROOT / "tools" / "generate_ies.py")
    _, builders = _relations_state(gen)
    from ies_toolkit import ies_core_relations_generated as rel

    # model hosts are internal (prefixed) keys; emitted classes carry the bare
    # public name, so bridge with emit_name.
    emitted = {n[:-len("_Relations")] for n in vars(rel) if n.endswith("_Relations")}
    expected = {gen.emit_name(h) for h in builders}
    assert emitted == expected, (
        f"relations classes != model hosts; extra={sorted(emitted - expected)} "
        f"missing={sorted(expected - emitted)}")

    for host, specs in builders.items():
        cls = getattr(rel, f"{gen.emit_name(host)}_Relations")
        methods = [n for n, v in vars(cls).items() if callable(v) and n.startswith("add_")]
        assert len(methods) == len(specs), (
            f"{gen.emit_name(host)}_Relations has {len(methods)} add_* methods but the "
            f"model has {len(specs)} builder specs")


def test_validate_shacl_targets_flags_undeclared_class():
    """generate_relations fails fast when a constrained SHACL shape targets a
    class the ontology does not declare (an orphan shape / missing class)."""
    gen = _load("generate_ies", ROOT / "tools" / "generate_ies.py")
    core = "http://purl.org/ies/core/v0/ont/"
    shaped = {core + "Ghost": [{"path_local": "isPartOf"}]}

    with pytest.raises(ValueError, match="not declared"):
        gen.validate_shacl_targets(shaped, set())              # undeclared -> raises
    gen.validate_shacl_targets(shaped, {core + "Ghost"})       # declared -> passes
    gen.validate_shacl_targets({core + "Ghost": []}, set())    # bare shape, no rows -> ignored
    gen.validate_shacl_targets({"http://x.org/Foreign": [{"path_local": "p"}]}, set())  # foreign -> ignored


def test_validate_emit_names_flags_clashes():
    """Dropping the module prefix must fail fast if it would collapse two classes
    to one public name, or hit a Python keyword/builtin."""
    import rdflib
    from rdflib import RDF, RDFS
    gen = _load("generate_ies", ROOT / "tools" / "generate_ies.py")

    def graph(*locals_):
        g = rdflib.Graph()
        for ns, local in locals_:
            g.add((rdflib.URIRef(ns + local), RDF.type, RDFS.Class))
        return g

    # top:Foo and core:Foo both emit as "Foo"
    with pytest.raises(ValueError, match="collides"):
        gen.validate_emit_names(graph((gen.TOP_NS, "Foo"), (gen.CORE_NS, "Foo")))
    # a class whose bare name shadows a Python builtin
    with pytest.raises(ValueError, match="builtin"):
        gen.validate_emit_names(graph((gen.CORE_NS, "type")))
    # distinct local names across modules are fine
    gen.validate_emit_names(graph((gen.TOP_NS, "Foo"), (gen.CORE_NS, "Bar")))
