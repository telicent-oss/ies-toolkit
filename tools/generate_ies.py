"""Generate IES Python wrapper classes from the source ontologies.

Reads ``ies-top.ttl`` and ``ies-core.ttl`` and emits, per target, a fully
generated module of wrapper classes (one per ontology class). Generated files
are overwritten wholesale on every run and must never be hand-edited; custom
behaviour lives in the hand-written overlay / *_custom mixin modules.

Usage:
    python tools/generate_ies.py                    # core, single-parent
    python tools/generate_ies.py --target top       # ies-top
    python tools/generate_ies.py --full-mi          # honour full multiple inheritance

Faithfulness is verified separately by tools/verify_generated.py.
"""
from __future__ import annotations

import argparse
import builtins
import keyword
import sys
from pathlib import Path

import rdflib
from rdflib import RDF, RDFS
from rdflib.collection import Collection

SHACL = rdflib.Namespace("http://www.w3.org/ns/shacl#")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))  # make the ies_toolkit package importable when run as a script
from ies_toolkit.constants import IES_CORE as CORE_NS  # noqa: E402 (needs the path shim above)
from ies_toolkit.constants import IES_TOP as TOP_NS  # noqa: E402

OWL_CLASS = rdflib.URIRef("http://www.w3.org/2002/07/owl#Class")
POWERTYPE = f"{TOP_NS}powertype"

# Foreign-namespace parents that the generator deliberately drops (no Python
# wrapper exists for these yet). Extend if/when wrappers are added.
FOREIGN_DROP_PREFIXES = ("http://www.opengis.net/ont/geosparql#",)

# Per-target configuration. Everything that cannot be derived from the ontology
# lives here as small, documented, regeneration-safe config (LinkML-style
# injection) rather than as protected regions in the generated file.
TARGETS = {
    "core": {
        "prefix": "IesCore_",
        "const": "IES_CORE",
        "overlay": "ies_core.py",
        "out": ROOT / "ies_toolkit" / "ies_core_generated.py",
        "full_mi": True,              # honour every rdfs:subClassOf parent (derived-first)
        "custom_module": "ies_core_custom",
        "shacl_files": ["ies-core-shacl.ttl"],
        "reified_engine": "ReifiedBuilderMixin",
        "relations_out": ROOT / "ies_toolkit" / "ies_core_relations_generated.py",
        "terms_out": ROOT / "ies_toolkit" / "ies_core_terms_generated.py",
        "mixins": {                   # class -> (MixinName, "replace"|"extend")
            "IesCore_RecurringTimespan": ("RecurringTimespanMixin", "extend"),
            "IesCore_Activity": ("ActivityMixin", "extend"),
            "IesCore_LivingOrganism": ("LivingOrganismMixin", "extend"),
        },
        # ancestor -> {params, call, replaces_temporal}: applied to it + descendants.
        # replaces_temporal drops start/finish from __init__ (the params supersede them).
        "construction_mixins": {
            "IesCore_LivingOrganism": {
                "params": "date_of_birth: str | None = None, place_of_birth=None, "
                          "date_of_death: str | None = None, place_of_death=None",
                "call": "self.add_lifespan(date_of_birth, place_of_birth, date_of_death, place_of_death)",
                "replaces_temporal": True,
            },
        },
        "instance_type_extra": {},    # values the ontology omits from powertype
        "no_temporal": set(),         # State-descended classes that hide start/finish
    },
    "top": {
        "prefix": "IesTop_",
        "const": "IES_TOP",
        "overlay": "ies_top.py / ies_top_custom.py",
        "out": ROOT / "ies_toolkit" / "ies_top_generated.py",
        "terms_out": ROOT / "ies_toolkit" / "ies_top_terms_generated.py",
        "custom_module": "ies_top_custom",
        # full MI is REQUIRED here: IesTop_Set must inherit Rdfs_Class (for
        # .instantiate()), which single-parent mode would drop.
        "full_mi": True,
        "mixins": {
            "IesTop_Thing": ("ThingMixin", "extend"),
            "IesTop_State": ("StateMixin", "replace"),
            "IesTop_Tuple": ("TupleMixin", "extend"),
            "IesTop_ThreePlaceTuple": ("ThreePlaceTupleMixin", "extend"),
            "IesTop_FourPlaceTuple": ("FourPlaceTupleMixin", "extend"),
        },
        # The ontology has no ies_top:powertype triple for these Set classes, so
        # their member type cannot be derived; supply it explicitly.
        "instance_type_extra": {
            "IesTop_Set": "IesTop_Thing",
            "IesTop_SetOfDisjointSpatiotemporalExtents": "IesTop_SpatiotemporalExtent",
            "IesTop_SetOfOverlappingSpatiotemporalExtents": "IesTop_SpatiotemporalExtent",
        },
        "no_temporal": {"IesTop_Universe"},
    },
}


def py_name(uri: str) -> str | None:
    """Map an ontology class URI to its Python wrapper name, or None to drop it."""
    if uri.startswith(TOP_NS):
        return "IesTop_" + uri[len(TOP_NS):]
    if uri.startswith(CORE_NS):
        return "IesCore_" + uri[len(CORE_NS):]
    if uri == "http://www.w3.org/2000/01/rdf-schema#Class":
        return "Rdfs_Class"
    if uri == "http://www.w3.org/2000/01/rdf-schema#Resource":
        return "Rdfs_Resource"
    for pfx in FOREIGN_DROP_PREFIXES:
        if uri.startswith(pfx):
            return None
    return None  # unknown foreign namespace -> drop


def emit_name(wrapper: str) -> str:
    """Internal wrapper key -> public class name: drop the IesTop_/IesCore_ prefix
    (IesCore_Person -> Person). Rdfs_* keep their prefix. The internal key stays
    prefixed everywhere else, so it is unique across modules and reconstructs its
    URI; only the emitted/imported name is bare."""
    if wrapper.startswith("IesTop_"):
        return wrapper[len("IesTop_"):]
    if wrapper.startswith("IesCore_"):
        return wrapper[len("IesCore_"):]
    return wrapper


def _validate_namespaces(g: rdflib.Graph) -> None:
    """Fail fast if the ontology's declared ies_top / ies_core @prefix disagrees with
    the namespace constants. ies_toolkit/constants.py is the single definition; on a
    namespace bump, update it there and this guard confirms the ontology agrees."""
    declared = {p: str(u) for p, u in g.namespaces()}
    for prefix, expected in (("ies_top", TOP_NS), ("ies_core", CORE_NS)):
        if declared.get(prefix) != expected:
            raise ValueError(
                f"ontology @prefix {prefix}: <{declared.get(prefix)}> does not match "
                f"ies_toolkit/constants.py <{expected}>")


def validate_emit_names(g: rdflib.Graph) -> None:
    """Fail fast if dropping the module prefix would make two classes share a public
    name, or if a public name is a Python keyword or shadows a builtin. Runs from
    load_graph, so every generation is guarded."""
    seen: dict[str, str] = {}
    for uri in declared_classes(g):
        internal = py_name(str(uri))
        if internal is None:
            continue
        public = emit_name(internal)
        if public in seen and seen[public] != internal:
            raise ValueError(
                f"dropping the module prefix collides {seen[public]} and {internal}: "
                f"both emit as '{public}' - disambiguate at the ontology source")
        seen[public] = internal
        if keyword.iskeyword(public) or hasattr(builtins, public):
            kind = "keyword" if keyword.iskeyword(public) else "builtin"
            raise ValueError(f"{internal} emits as '{public}', a Python {kind} - rename at the ontology source")


def load_graph() -> rdflib.Graph:
    g = rdflib.Graph()
    g.parse(ROOT / "ies-top.ttl")
    g.parse(ROOT / "ies-core.ttl")
    _validate_namespaces(g)
    validate_emit_names(g)
    return g


def declared_classes(g: rdflib.Graph) -> set[str]:
    classes: set[str] = set()
    for cls_type in (RDFS.Class, OWL_CLASS):
        for s, _, _ in g.triples((None, RDF.type, cls_type)):
            classes.add(str(s))
    return classes


def subclass_parents(g: rdflib.Graph) -> dict[str, list[str]]:
    """child wrapper-name -> its rdfs:subClassOf parent wrapper-names, read from
    rdflib so any Turtle serialisation (single statements, object-lists,
    predicate-lists) is handled. Foreign-namespace parents (py_name -> None) are
    dropped. Parents are name-sorted because rdflib does not guarantee triple
    order and generation must be deterministic; full multiple inheritance is
    re-ordered most-derived-first at emission, so the only effect of this sort is
    a stable tiebreak between equal-depth parents."""
    edges: dict[str, set[str]] = {}
    for s, _, o in g.triples((None, RDFS.subClassOf, None)):
        cn, pn = py_name(str(s)), py_name(str(o))
        if cn and pn:
            edges.setdefault(cn, set()).add(pn)
    return {cn: sorted(ps) for cn, ps in edges.items()}


def instance_types(g: rdflib.Graph, cfg: dict) -> dict[str, str]:
    """Each Set class's .instantiate() member type, derived from the ontology's
    `<member> ies_top:powertype <SetClass>` triples and restricted to this
    target's namespace, plus any explicit overrides the ontology omits."""
    prefix = cfg["prefix"]
    out: dict[str, str] = {}
    pwr = rdflib.URIRef(POWERTYPE)
    for member, _, set_cls in g.triples((None, pwr, None)):
        sn, mn = py_name(str(set_cls)), py_name(str(member))
        if sn and mn and sn.startswith(prefix):
            out[sn] = mn
    out.update(cfg["instance_type_extra"])
    return out


def _local(uri: str) -> str:
    return uri.rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def _snake(local: str) -> str:
    """CamelCase local name -> snake_case (AccountHolder -> account_holder)."""
    out: list[str] = []
    for i, ch in enumerate(local):
        if ch.isupper() and i and (not local[i - 1].isupper()
                                   or (i + 1 < len(local) and local[i + 1].islower())):
            out.append("_")
        out.append(ch.lower())
    s = "".join(out).replace("-", "_")
    while "__" in s:
        s = s.replace("__", "_")
    return s.strip("_")


def declared_properties(g: rdflib.Graph) -> dict[str, str]:
    """local-name -> declared property URI (rdf:type rdf:Property)."""
    out: dict[str, str] = {}
    for s, _, _ in g.triples((None, RDF.type, RDF.Property)):
        out.setdefault(_local(str(s)), str(s))
    return out


def load_shacl(cfg: dict) -> rdflib.Graph:
    g = rdflib.Graph()
    for fname in cfg.get("shacl_files", ()):
        p = ROOT / fname
        if not p.exists():
            raise FileNotFoundError(f"SHACL file not found: {p}")
        g.parse(p)
    return g


def shacl_model(g_shacl: rdflib.Graph) -> dict[str, list[dict]]:
    """targetClass URI -> [{pred, path_local, targets, message}] with full URIs."""
    model: dict[str, list[dict]] = {}
    for shape, _, tc in g_shacl.triples((None, SHACL.targetClass, None)):
        rows = model.setdefault(str(tc), [])
        for _, _, pn in g_shacl.triples((shape, SHACL.property, None)):
            path = g_shacl.value(pn, SHACL.path)
            if path is None:
                continue
            targets: list[str] = []
            c = g_shacl.value(pn, SHACL["class"])
            if c is not None:
                targets.append(str(c))
            orn = g_shacl.value(pn, SHACL["or"])
            if orn is not None:
                for item in Collection(g_shacl, orn):
                    ic = g_shacl.value(item, SHACL["class"])
                    if ic is not None:
                        targets.append(str(ic))
            msg = g_shacl.value(pn, SHACL.message)
            rows.append({"pred": str(path),
                         "path_local": _local(str(path)),
                         "targets": targets,
                         "message": str(msg) if msg else None})
    return model


def property_model(g_shacl: rdflib.Graph) -> tuple[dict[str, str], dict[str, str]]:
    """(domain, range) URI maps keyed by property local-name, from the
    sh:targetSubjectsOf / sh:targetObjectsOf shapes."""
    dom, rng = {}, {}
    for sh, _, prop in g_shacl.triples((None, SHACL.targetSubjectsOf, None)):
        c = g_shacl.value(sh, SHACL["class"])
        if c is not None:
            dom[_local(str(prop))] = str(c)
    for sh, _, prop in g_shacl.triples((None, SHACL.targetObjectsOf, None)):
        c = g_shacl.value(sh, SHACL["class"])
        if c is not None:
            rng[_local(str(prop))] = str(c)
    return dom, rng


def _uri_of(wrapper: str) -> str:
    if wrapper.startswith("IesCore_"):
        return CORE_NS + wrapper[len("IesCore_"):]
    if wrapper.startswith("IesTop_"):
        return TOP_NS + wrapper[len("IesTop_"):]
    return wrapper


def _ancestry(parents: dict[str, list[str]]):
    cache: dict[str, set[str]] = {}

    def anc(w: str) -> set[str]:
        if w in cache:
            return cache[w]
        cache[w] = set()  # guard cycles
        s: set[str] = set()
        for p in parents.get(w, []):
            s.add(p)
            s |= anc(p)
        cache[w] = s
        return s
    return anc


# reified-builder construction (participation + lifecycle boundary states)
PARTICIPATION = "IesCore_Participation"
ACTIVITY = "IesCore_Activity"
REPRESENTATION = "IesCore_Representation"
REP_ROOTS = {"IesCore_Representation", "IesCore_Name", "IesCore_Identifier"}
BOUNDARY_LOCALS = {"isAStartOf", "isAFinishOf", "isAnEndOf"}


def relations_model(cfg: dict, g_onto: rdflib.Graph, g_shacl: rdflib.Graph) -> dict[str, list[dict]]:
    """host wrapper-name -> [builder spec]. A builder mints a reified node
    (participation role or boundary state) and wires its shaped edges; the host is
    the Activity it isPartOf (participation) or the entity it bounds (boundary)."""
    prefix = cfg["prefix"]
    model = shacl_model(g_shacl)
    parents = subclass_parents(g_onto)
    anc = _ancestry(parents)

    def is_part(w):
        return w == PARTICIPATION or PARTICIPATION in anc(w)

    def is_act(w):
        return w == ACTIVITY or ACTIVITY in anc(w)

    def is_rep(w):
        return w == REPRESENTATION or REPRESENTATION in anc(w)

    # predicate local-name -> its range URI, for predicates whose range is a
    # Representation (hasName, isIdentifiedBy, isRepresentedAs) - these drive the
    # typed representation/identifier builders.
    _, prop_range = property_model(g_shacl)
    rep_preds = {ln: rng for ln, rng in prop_range.items()
                 if py_name(rng) and is_rep(py_name(rng))}

    builders: dict[str, list[dict]] = {}

    def add_builder(host, node_uri, host_pred, edges_for_args, node_w, kind):
        args = []
        for pred, tw, ploc in edges_for_args:
            args.append({"pred": pred, "type": tw, "ploc": ploc})
        builders.setdefault(host, []).append({
            "method_base": _snake(node_w[len(prefix):]),
            "node": node_uri, "host_pred": host_pred, "args": args, "kind": kind})

    def add_rep_builder(host, target_uri, host_pred, range_root_uri):
        target_w = py_name(target_uri)
        if target_w in REP_ROOTS:
            return  # the generic roots are covered by ThingMixin.add_name/identifier/representation
        if target_w and is_rep(target_w):
            mint_type, category = target_uri, None            # a real Representation subclass
        else:
            mint_type, category = range_root_uri, target_uri  # a SKOS category concept on the range root
        builders.setdefault(host, []).append({
            "method_base": _snake(_local(target_uri)), "mint_type": mint_type,
            "host_pred": host_pred, "category": category, "kind": "representation"})

    for tc_uri, rows in model.items():
        node_w = py_name(tc_uri)
        if node_w is None:
            continue
        # flatten edges: (path_local, pred_uri, [target wrappers])
        edges = [(r["path_local"], r["pred"], [py_name(t) for t in r["targets"]]) for r in rows]

        if is_part(node_w):
            if node_w == PARTICIPATION:
                continue  # generic add_participant comes from the curated ActivityMixin
            host_preds = {}  # host wrapper -> pred uri (the isPartOf to an Activity)
            for ploc, pred, tws in edges:
                if ploc == "isPartOf":
                    for tw in tws:
                        if tw and is_act(tw):
                            host_preds.setdefault(tw, pred)
            for host, host_pred in host_preds.items():
                if not host.startswith(prefix):
                    continue
                arg_edges = []
                for ploc, pred, tws in edges:
                    for tw in tws:
                        if ploc == "isPartOf" and tw == host:
                            continue  # the host edge itself
                        if tw:
                            arg_edges.append((pred, tw, ploc))
                add_builder(host, tc_uri, host_pred, arg_edges, node_w, "participation")

        elif any(ploc in BOUNDARY_LOCALS for ploc, _, _ in edges):
            for ploc, pred, tws in edges:
                if ploc not in BOUNDARY_LOCALS:
                    continue
                for host in tws:
                    if not host or not host.startswith(prefix):
                        continue
                    arg_edges = []
                    for ploc2, pred2, tws2 in edges:
                        if ploc2 == ploc and host in tws2:
                            continue  # the boundary (host) edge itself
                        for tw in tws2:
                            if tw:
                                arg_edges.append((pred2, tw, ploc2))
                    add_builder(host, tc_uri, pred, arg_edges, node_w, "boundary")

        # representation / identifier specialisations: the targetClass is the host,
        # pointing via a representation-ranged predicate at a typed node + literal value
        if node_w.startswith(prefix):
            for r in rows:
                root = rep_preds.get(r["path_local"])
                if root is None:
                    continue
                for target_uri in r["targets"]:
                    add_rep_builder(node_w, target_uri, r["pred"], root)
    return builders


def validate_relation_predicates(builders: dict, declared: dict[str, str]) -> None:
    """Raise ValueError listing any predicate a builder would emit that is not a
    declared ontology property, with a same-local-name hint where one exists."""
    declared_uris = set(declared.values())
    by_local: dict[str, list[str]] = {}
    for uri in declared_uris:
        by_local.setdefault(_local(uri), []).append(uri)

    bad: dict[str, set[str]] = {}
    for host, specs in builders.items():
        for s in specs:
            for pred in [s["host_pred"]] + [a["pred"] for a in s.get("args", [])]:
                if pred not in declared_uris:
                    bad.setdefault(pred, set()).add(f"{host}.add_{s['method_base']}")
    if not bad:
        return

    lines = ["SHACL references properties not declared in the ontology:"]
    for pred in sorted(bad):
        hint = by_local.get(_local(pred))
        hint_s = (f"same local name IS declared as {hint[0]}" if hint
                  else "no property of this local name is declared anywhere")
        users = sorted(bad[pred])
        shown = ", ".join(users[:6]) + ("" if len(users) <= 6 else f" (+{len(users) - 6} more)")
        lines.append(f"  {pred}\n      [{hint_s}]\n      used by: {shown}")
    raise ValueError("\n".join(lines))


def validate_relation_classes(builders: dict, declared_class_uris: set[str]) -> None:
    """Raise if a builder's host targetClass, or a class it would instantiate, is
    not a declared ontology class."""
    bad_hosts: dict[str, list[str]] = {}
    bad_minted: dict[str, set[str]] = {}
    for host, specs in builders.items():
        if _uri_of(host) not in declared_class_uris:
            bad_hosts[host] = sorted(f"add_{s['method_base']}" for s in specs)
        for s in specs:
            minted = s.get("node") or s.get("mint_type")
            if minted and minted not in declared_class_uris:
                bad_minted.setdefault(minted, set()).add(f"{host}.add_{s['method_base']}")
    if not bad_hosts and not bad_minted:
        return

    lines = ["SHACL targets classes not declared in the ontology:"]
    for host in sorted(bad_hosts):
        lines.append(f"  host {_uri_of(host)} is not a declared class  (builders: {', '.join(bad_hosts[host])})")
    for cls in sorted(bad_minted):
        lines.append(f"  minted class {cls} is not declared  (used by: {', '.join(sorted(bad_minted[cls]))})")
    raise ValueError("\n".join(lines))


def validate_shacl_targets(model: dict, declared_class_uris: set[str]) -> None:
    """Raise if a SHACL shape that carries property constraints targets a class the
    ontology does not declare - an orphan shape, or a class missing from the
    ontology. Such a shape can never yield a valid builder, so fail at generation
    rather than let it fall through the relations model silently."""
    bad: dict[str, list[str]] = {}
    for tc_uri, rows in model.items():
        if not rows:
            continue  # bare targetClass registration, no constraints to realize
        if py_name(tc_uri) is None:
            continue  # foreign class, dropped by design
        if tc_uri not in declared_class_uris:
            bad[tc_uri] = sorted({r["path_local"] for r in rows})
    if not bad:
        return
    lines = ["SHACL shapes constrain classes not declared in the ontology:"]
    for tc in sorted(bad):
        lines.append(f"  {tc} is not a declared class  (shaped paths: {', '.join(bad[tc])})")
    raise ValueError("\n".join(lines))


def _uri_to_source(uri: str) -> str:
    """How to write this URI in the generated module. For an IES URI, an f-string
    on the namespace constant, e.g. f"{IES_CORE}Assessor" (so the module holds the
    local name, not the full URL); for a foreign URI, a quoted string literal."""
    if uri.startswith(CORE_NS):
        return f'f"{{IES_CORE}}{uri[len(CORE_NS):]}"'
    if uri.startswith(TOP_NS):
        return f'f"{{IES_TOP}}{uri[len(TOP_NS):]}"'
    return f'"{uri}"'


def _dedup_name(base: str, used_names: set[str], collide_suffix: str) -> str:
    name = base
    if name in used_names:
        name = f"{base}_{collide_suffix}"
    i = 2
    while name in used_names:
        name = f"{base}_{i}"
        i += 1
    used_names.add(name)
    return name


def _emit_rep_builder(spec: dict, host: str, used_names: set[str]):
    """A typed representation/identifier builder: mint the node (a Representation
    subclass, or the predicate's range root + an ies_core:category for SKOS
    concepts) and set its literal value, via ThingMixin._add_representation."""
    mint_local = _local(spec["mint_type"])
    name = _dedup_name("add_" + spec["method_base"], used_names, _local(spec["host_pred"]).lower())
    body = [f'rep = self._add_representation(value, {_uri_to_source(spec["mint_type"])}, '
            f'{_uri_to_source(spec["host_pred"])}, '
            f'"{spec["method_base"]}", "{REPRESENTATION}", None, representation_uri)']
    if spec["category"]:
        body.append(f'rep._apply_categories([{_uri_to_source(spec["category"])}])')
    body.append("return rep")
    target = _local(spec["category"]) if spec["category"] else mint_local
    article = "an" if target[:1].lower() in "aeiou" else "a"
    doc = f"Add {article} {target} to this {_strip_prefix(host)} ({_local(spec['host_pred'])} + representationValue)."
    return name, ["self", "value", "representation_uri=None"], doc, body


def _emit_builder(spec: dict, host: str, used_names: set[str]):
    """Return (method_name, params, docstring, body_lines) for one reified builder."""
    if spec["kind"] == "representation":
        return _emit_rep_builder(spec, host, used_names)
    node_local = _local(spec["node"])
    base = "add_" + spec["method_base"]
    name = base
    if name in used_names:  # two boundary edges of the same node on one host
        name = f"{base}_{_snake(_local(spec['host_pred']))}"
    i = 2
    while name in used_names:
        name = f"{base}_{i}"
        i += 1
    used_names.add(name)

    uri_param = "participation_uri" if spec["kind"] == "participation" else "state_uri"
    body = [f'node = self._mint_node({_uri_to_source(spec["node"])}, "{_snake(node_local)}", {uri_param})',
            f'self._wire(node, {_uri_to_source(spec["host_pred"])}, self.uri)']
    required, optional, used_params = [], [], set()
    # one non-host edge -> required; a choice of several -> all optional
    single = len(spec["args"]) == 1
    for a in sorted(spec["args"], key=lambda a: 0 if a["ploc"] == "isTemporalPartOf" else 1):
        tw = a["type"]
        pbase = _snake(tw.split("_", 1)[1] if "_" in tw else tw)
        pname, j = pbase, 2
        while pname in used_params:
            pname = f"{pbase}_{j}"
            j += 1
        used_params.add(pname)
        if single:
            required.append(pname)
            body.append(f'self._wire(node, {_uri_to_source(a["pred"])}, {pname})')
        else:
            optional.append(pname)
            body.append(f'if {pname} is not None:')
            body.append(f'    self._wire(node, {_uri_to_source(a["pred"])}, {pname})')
    body.append("return node")

    params = ["self"] + required + [f"{p}=None" for p in optional] + [f"{uri_param}=None"]
    article = "an" if node_local[:1].lower() in "aeiou" else "a"
    doc = f"Mint {article} {node_local} ({_local(spec['host_pred'])} this {_strip_prefix(host)})."
    return name, params, doc, body


def _strip_prefix(wrapper: str) -> str:
    return wrapper.split("_", 1)[1] if "_" in wrapper else wrapper


def render_relations(cfg: dict, builders: dict) -> str:
    engine, custom = cfg["reified_engine"], cfg["custom_module"]
    lines = ['"""Relationship / reified builders generated from the SHACL shapes.',
             "",
             "DO NOT EDIT BY HAND. Regenerate with:  python tools/generate_ies.py --relations",
             f"The reified-node engine lives in the hand-written overlay ({custom}.{engine}).",
             '"""',
             f"from .{custom} import {engine}",
             "from .constants import IES_CORE, IES_TOP",
             "",
             ""]
    for host in sorted(builders):
        lines.append(f"class {emit_name(host)}_Relations({engine}):")
        used: set[str] = set()
        for spec in sorted(builders[host], key=lambda s: s["method_base"]):
            name, params, doc, body = _emit_builder(spec, host, used)
            lines.append(f"    def {name}({', '.join(params)}):")
            lines.append(f'        """{doc}"""')
            lines.extend("        " + b for b in body)
            lines.append("")
        lines.append("")
    lines.append("__all__ = [")
    for host in sorted(builders):
        lines.append(f'    "{emit_name(host)}_Relations",')
    lines.append("]")
    return "\n".join(lines).rstrip() + "\n"


def build_model(cfg: dict, full_mi: bool):
    prefix = cfg["prefix"]
    g = load_graph()
    classes = declared_classes(g)
    inst_types = instance_types(g, cfg)

    raw_parents = subclass_parents(g)
    valid_names = {py_name(c) for c in classes} | {"Rdfs_Class", "Rdfs_Resource"}

    # full parent set (foreign dropped), used for both base selection and
    # State-descent (which must see all parents regardless of the MI flag).
    full_parent_map: dict[str, list[str]] = {}
    for uri in classes:
        name = py_name(uri)
        if name is None:
            continue
        full_parent_map[name] = [p for p in raw_parents.get(name, []) if p in valid_names]

    depth_cache: dict[str, int] = {}

    def depth(n: str) -> int:
        if n in depth_cache:
            return depth_cache[n]
        ps = full_parent_map.get(n, [])
        depth_cache[n] = 0 if not ps else 1 + max(depth(p) for p in ps)
        return depth_cache[n]

    def safe_depth(n: str) -> int:
        return depth(n) if n in full_parent_map else 0

    def is_state(n: str, seen=None) -> bool:
        """Whether n transitively descends from ies_top:State (-> _state_init)."""
        if n == "IesTop_State":
            return True
        seen = seen or set()
        if n in seen:
            return False
        seen.add(n)
        return any(is_state(p, seen) for p in full_parent_map.get(n, []))

    # choose emitted bases per MI flag
    #
    # Derived-first ordering (most-derived parent first) is a heuristic that
    # keeps Python's C3 MRO happy: a base must never precede one of its own
    # descendants, so ordering by descending depth avoids the common conflict
    # (e.g. listing SetOfStates before its subclass SetOfPersons). It is not a
    # guarantee for every conceivable hierarchy - a pathological shape could
    # still be un-linearizable, but that fails LOUDLY at import (TypeError:
    # Cannot create a consistent MRO), which the drift/faithfulness tests catch.
    emit_parents: dict[str, list[str]] = {}
    for name, ps in full_parent_map.items():
        if not ps:
            bases = ["IesTop_Thing"]  # safety net; ontology currently has no orphans
        elif full_mi:
            bases = sorted(ps, key=lambda p: -safe_depth(p))  # derived-first, name tiebreak
        else:
            bases = [ps[0]]  # single-parent mode: first parent by name (unused; targets are full-MI)
        emit_parents[name] = bases

    # topological emission order (parents before children), alpha within tier
    target_names = sorted(n for n in emit_parents if n.startswith(prefix))
    emitted: list[str] = []
    placed: set[str] = set()

    def place(n: str):
        if n in placed or not n.startswith(prefix):
            return
        for p in emit_parents.get(n, []):
            place(p)
        placed.add(n)
        emitted.append(n)

    for n in target_names:
        place(n)

    return emit_parents, is_state, emitted, inst_types


def _header(cfg: dict) -> str:
    return (
        '"""IES wrapper classes generated from ies-top.ttl and ies-core.ttl.\n'
        "\n"
        "DO NOT EDIT BY HAND. Regenerate with:  python tools/generate_ies.py\n"
        f"Custom methods belong in the hand-written overlay ({cfg['overlay']}), not here.\n"
        '"""\n'
        "import datetime\n"
        "\n"
        f"from .constants import {cfg['const']}\n"
        "from .rdf_plugin import RDFPlugin\n"
    )


def render(cfg: dict, emit_parents, is_state, emitted, inst_types, relation_hosts=None) -> str:
    prefix, const, mixins = cfg["prefix"], cfg["const"], cfg["mixins"]
    no_temporal = cfg["no_temporal"]
    relation_hosts = relation_hosts or set()
    construction = cfg.get("construction_mixins", {})

    def _construction(name):
        fam, stack = {name}, list(emit_parents.get(name, []))
        while stack:
            p = stack.pop()
            if p not in fam:
                fam.add(p)
                stack.extend(emit_parents.get(p, []))
        for ancestor, spec in construction.items():
            if ancestor in fam:
                return spec
        return None

    # collect non-own names that need importing (parents + instance_type members)
    foreign = set()
    used_mixins = set()
    used_relations = set()
    for name in emitted:
        for b in emit_parents[name]:
            if not b.startswith(prefix):
                foreign.add(b)
        member = inst_types.get(name)
        if member and not member.startswith(prefix):
            foreign.add(member)
        if name in mixins:
            used_mixins.add(mixins[name][0])
        if name in relation_hosts:
            used_relations.add(f"{emit_name(name)}_Relations")
    top_imports = sorted(emit_name(b) for b in foreign if b.startswith("IesTop_"))
    rdfs_imports = sorted(b for b in foreign if b.startswith("Rdfs_"))

    lines = [_header(cfg)]
    if top_imports:
        lines.append("from .ies_top import " + ", ".join(top_imports))
    if rdfs_imports:
        lines.append("from .rdfs import " + ", ".join(rdfs_imports))
    if used_mixins:
        lines.append(f"from .{cfg['custom_module']} import " + ", ".join(sorted(used_mixins)))
    if used_relations:
        lines.append(f"from .{cfg['relations_out'].stem} import " + ", ".join(sorted(used_relations)))
    lines.append("")
    lines.append("__all__ = [")
    for name in emitted:
        lines.append(f'    "{emit_name(name)}",')
    lines.append("]")
    lines.append("")
    lines.append("")

    state_sig = ("    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, "
                 "classes: list[str] | None = None, start: datetime.datetime | None = None, "
                 "finish: datetime.datetime | None = None, categories: list[str] | None = None):")
    cls_sig = ("    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, "
               "classes: list[str] | None = None, categories: list[str] | None = None):")

    for name in emitted:
        frag = name[len(prefix):]
        type_uri = 'f"{' + const + '}' + frag + '"'
        base_list = [emit_name(b) for b in emit_parents[name]]
        extra = []
        mixin = mixins.get(name)
        if mixin:
            extra.append(mixin[0])
        if name in relation_hosts:
            extra.append(f"{emit_name(name)}_Relations")
        base_list = extra + base_list
        lines.append(f"class {emit_name(name)}({', '.join(base_list)}):")

        if mixin and mixin[1] == "replace":
            lines.append("    pass")          # constructor + methods come from the mixin
            lines.append("")
            continue

        life = _construction(name)
        if name in no_temporal:               # State-descended but hides start/finish
            lines.append(cls_sig)
            lines.append(f"        self._state_init(classes,{type_uri},store,uri,None,None)")
        elif life and life.get("replaces_temporal"):
            lines.append(cls_sig[:-2] + ", " + life["params"] + "):")
            lines.append(f"        self._state_init(classes,{type_uri},store,uri,None,None)")
        elif is_state(name):
            lines.append(state_sig[:-2] + ", " + life["params"] + "):" if life else state_sig)
            lines.append(f"        self._state_init(classes,{type_uri},store,uri,start,finish)")
        else:
            lines.append(cls_sig)
            lines.append(f"        self._cls_init(classes,{type_uri},store,uri)")
        lines.append("        self._apply_categories(categories)")
        if life:
            lines.append(f"        {life['call']}")
        if name in inst_types:
            lines.append(f"        self.instance_type = {emit_name(inst_types[name])}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_terms(cfg: dict) -> str:
    """This module's declared IES terms (classes + properties), generated from the
    ontology and namespace-filtered to this target, in two forms:
      * a DefinedNamespace (IesCore / IesTop) for typed, typo-safe term access
        (IesCore.Person -> URIRef; an unknown term raises AttributeError);
      * frozensets IES_CLASS_URIS / IES_PROPERTY_URIS (the URI registry) for the
        non-IES warning (ies_terms.IesTermsMixin), which needs the class/property split.
    The base URI is the single-source namespace constant."""
    prefix, const = cfg["prefix"], cfg["const"]      # "IesCore_", "IES_CORE"
    ns_class = prefix.rstrip("_")                     # "IesCore"
    target = ns_class.replace("Ies", "").lower()      # "core"
    g = load_graph()
    class_uris = sorted(str(c) for c in declared_classes(g)
                        if (n := py_name(str(c))) and n.startswith(prefix))
    prop_uris = sorted(u for u in declared_properties(g).values()
                       if (n := py_name(u)) and n.startswith(prefix))
    terms = sorted({_local(u) for u in class_uris} | {_local(u) for u in prop_uris})
    lines = [f'"""Declared {ns_class} terms: a typed namespace + a URI registry.',
             "",
             f"DO NOT EDIT BY HAND. Regenerate with:  python tools/generate_ies.py --target {target}",
             '"""',
             "from rdflib import URIRef",
             "from rdflib.namespace import DefinedNamespace, Namespace",
             f"from .constants import {const}",
             "",
             "",
             f"class {ns_class}(DefinedNamespace):",
             f"    _NS = Namespace({const})",
             "    _fail = True",
             ""]
    lines += [f"    {t}: URIRef" for t in terms]
    lines += ["", "", "IES_CLASS_URIS = frozenset({"]
    lines += [f'    "{u}",' for u in class_uris]
    lines += ["})", "", "IES_PROPERTY_URIS = frozenset({"]
    lines += [f'    "{u}",' for u in prop_uris]
    lines.append("})")
    return "\n".join(lines) + "\n"


def generate_terms(cfg: dict) -> None:
    cfg["terms_out"].write_text(render_terms(cfg), encoding="utf-8")
    print(f"Generated {cfg['prefix'].rstrip('_')} terms -> {cfg['terms_out']}")


def generate_relations(cfg: dict) -> dict:
    """Emit the SHACL-derived relationship/reified builders for a target and
    return the builder model (host wrapper-name -> builder specs)."""
    g_onto = load_graph()
    g_shacl = load_shacl(cfg)
    builders = relations_model(cfg, g_onto, g_shacl)
    declared = {str(c) for c in declared_classes(g_onto)}
    validate_shacl_targets(shacl_model(g_shacl), declared)
    validate_relation_predicates(builders, declared_properties(g_onto))
    validate_relation_classes(builders, declared)
    out = render_relations(cfg, builders)
    cfg["relations_out"].write_text(out, encoding="utf-8")
    n = sum(len(v) for v in builders.values())
    print(f"Generated {n} relationship builders over {len(builders)} host classes -> {cfg['relations_out']}")
    return builders


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", choices=sorted(TARGETS), default="core")
    ap.add_argument("--full-mi", action="store_true",
                    help="force full multiple inheritance even if the target defaults to single-parent")
    ap.add_argument("--relations", action="store_true",
                    help="generate only the SHACL-derived relationship/reified builders")
    ap.add_argument("-o", "--out", default=None)
    args = ap.parse_args()

    cfg = TARGETS[args.target]
    generate_terms(cfg)           # this module's terms: namespace + URI registry
    if args.relations:
        generate_relations(cfg)
        return
    builders = generate_relations(cfg) if cfg.get("shacl_files") else {}
    full_mi = args.full_mi or cfg["full_mi"]
    emit_parents, is_state, emitted, inst_types = build_model(cfg, full_mi=full_mi)
    out = render(cfg, emit_parents, is_state, emitted, inst_types, relation_hosts=set(builders))
    out_path = Path(args.out) if args.out else cfg["out"]
    out_path.write_text(out, encoding="utf-8")
    mode = "full-MI" if full_mi else "single-parent"
    print(f"Generated {len(emitted)} {args.target} classes ({mode}) -> {out_path}")


if __name__ == "__main__":
    main()
