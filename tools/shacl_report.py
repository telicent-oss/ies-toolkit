"""Dry-run report for the SHACL-driven autogeneration pass (Phase 1, step 1).

Read-only. Parses the exported SHACL shapes and prints the method inventory the
generator WOULD emit - general engines, the specialisation trees projected from
the class subsumption hierarchy, and the inferred host class for each builder -
without touching any generated file. The point is to validate the design against
every SHACL constraint and pin the host/participant heuristic before the emitter
is written. `shacl_model()` here is the function that later moves into
generate_ies.py to drive emission.

Usage:  python tools/shacl_report.py
"""
from __future__ import annotations

import sys
from collections import defaultdict, namedtuple
from pathlib import Path

import rdflib
from rdflib.collection import Collection

sys.path.insert(0, str(Path(__file__).resolve().parent))  # import the sibling generator
from generate_ies import CORE_NS, ROOT, TOP_NS, load_graph, py_name, subclass_parents  # noqa: E402

SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
SHACL_FILES = ["ies-core-shacl.ttl", "ies-top-shacl.ttl"]
PARTICIPATION = "IesCore_Participation"

# one shaped edge of a NodeShape: predicate, its typed target(s), message, nodekind
PropShape = namedtuple("PropShape", "path targets message nodekind")


def local(uri) -> str:
    """Bare local name for display (Activity, isPartOf), stripped of namespace."""
    s = str(uri)
    for ns in (CORE_NS, TOP_NS):
        if s.startswith(ns):
            return s[len(ns):]
    return s.rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def disp(wrapper: str) -> str:
    """IesCore_AccountHolder -> AccountHolder (for readable report output)."""
    return wrapper.split("_", 1)[1] if wrapper and "_" in wrapper else wrapper


def snake(name: str) -> str:
    """CamelCase local name -> snake_case method fragment (AccountHolder -> account_holder)."""
    out: list[str] = []
    for i, ch in enumerate(name):
        boundary = ch.isupper() and i and (
            not name[i - 1].isupper() or (i + 1 < len(name) and name[i + 1].islower())
        )
        if boundary:
            out.append("_")
        out.append(ch.lower())
    s = "".join(out).replace("-", "_")
    while "__" in s:
        s = s.replace("__", "_")
    return s.strip("_")


def load_shacl():
    """Combined SHACL graph + which files parsed and which were skipped (Phase 0)."""
    g = rdflib.Graph()
    loaded, skipped = [], []
    for f in SHACL_FILES:
        p = ROOT / f
        if not p.exists():
            continue
        try:
            part = rdflib.Graph()
            part.parse(p)
        except Exception as e:  # unparsable export (e.g. ies-top-shacl Phase-0 bug)
            skipped.append((f, str(e).splitlines()[0]))
            continue
        g += part
        loaded.append(f)
    return g, loaded, skipped


def shacl_model(g: rdflib.Graph) -> dict[str, list[PropShape]]:
    """targetClass wrapper-name -> its property shapes. The core extraction pass."""
    model: dict[str, list[PropShape]] = defaultdict(list)
    for shape, _, tc in g.triples((None, SH.targetClass, None)):
        key = py_name(str(tc)) or local(tc)
        for _, _, pn in g.triples((shape, SH.property, None)):
            path = g.value(pn, SH.path)
            msg = g.value(pn, SH.message)
            nk = g.value(pn, SH.nodeKind)
            targets: list[str] = []
            c = g.value(pn, SH["class"])
            if c is not None:
                targets.append(local(c))
            orn = g.value(pn, SH["or"])
            if orn is not None:
                for item in Collection(g, orn):
                    ic = g.value(item, SH["class"])
                    if ic is not None:
                        targets.append(local(ic))
            model[key].append(PropShape(local(path) if path else None, targets,
                                        str(msg) if msg else None,
                                        local(nk) if nk else None))
    return dict(model)


def property_model(g: rdflib.Graph):
    """property local-name -> (domain class, range class) from the
    sh:targetSubjectsOf / sh:targetObjectsOf shapes. A property with a domain but
    no object-range is literal-valued (e.g. representationValue, iso8601*)."""
    dom, rng = {}, {}
    for sh, _, prop in g.triples((None, SH.targetSubjectsOf, None)):
        c = g.value(sh, SH["class"])
        if c is not None:
            dom[local(prop)] = local(c)
    for sh, _, prop in g.triples((None, SH.targetObjectsOf, None)):
        c = g.value(sh, SH["class"])
        if c is not None:
            rng[local(prop)] = local(c)
    return dom, rng


def ancestry(parents: dict[str, list[str]]):
    def ancestors(w, seen=None):
        seen = seen if seen is not None else set()
        for p in parents.get(w, []):
            if p not in seen:
                seen.add(p)
                ancestors(p, seen)
        return seen
    children: dict[str, list[str]] = defaultdict(list)
    for c, ps in parents.items():
        for p in ps:
            children[p].append(c)

    def descendants(root, seen=None):
        seen = seen if seen is not None else []
        for c in sorted(children.get(root, [])):
            if c not in seen:
                seen.append(c)
                descendants(c, seen)
        return seen
    return ancestors, descendants


def infer_roles(shapes: list[PropShape]):
    """Host/participant heuristic: isTemporalPartOf endpoint = the participant
    argument; the other shaped endpoint(s) = the host class(es) the builder
    attaches to. Returns (participant_targets, host_targets, other_edges)."""
    participant, hosts, other = [], [], []
    for ps in shapes:
        if ps.path == "isTemporalPartOf":
            participant += ps.targets
        elif ps.path == "isPartOf":
            hosts += ps.targets
        else:
            other.append(ps)
    return participant, hosts, other


def main():
    g, loaded, skipped = load_shacl()
    model = shacl_model(g)
    onto = load_graph()
    parents = subclass_parents(onto)
    ancestors, descendants = ancestry(parents)

    ACTIVITY = "IesCore_Activity"

    def is_activity(localname: str) -> bool:
        w = "IesCore_" + localname
        return w == ACTIVITY or ACTIVITY in ancestors(w)

    n_constraints = sum(len(v) for v in model.values())
    print("=" * 78)
    print("SHACL autogeneration dry-run report  (read-only; no files emitted)")
    print("=" * 78)
    print(f"parsed shapes: {', '.join(loaded) or '(none)'}")
    for f, err in skipped:
        print(f"  SKIPPED {f}: {err}")
    print(f"targetClasses with shapes: {len(model)}    property-shape constraints: {n_constraints}")

    # ---- classify each shaped targetClass --------------------------------------
    def is_participation(w):
        return w == PARTICIPATION or PARTICIPATION in ancestors(w)

    participation = {w for w in model if is_participation(w)}
    boundary_paths = ("isAStartOf", "isAFinishOf", "isAnEndOf")
    lifecycle = {w for w in model if w not in participation
                 and any(ps.path in boundary_paths for ps in model[w])}
    identifier = {w for w in model if w not in participation | lifecycle
                  and any(ps.path == "isIdentifiedBy" for ps in model[w])}
    structural = set(model) - participation - lifecycle - identifier

    # ---- 1. participation specialisation tree ----------------------------------
    print("\n" + "-" * 78)
    print("1. PARTICIPATION  (reified; engine + specialisation tree from subClassOf)")
    print("-" * 78)
    print(f"  root engine:  add_participant(participant, role_class=...)   [{disp(PARTICIPATION)}]")
    tree = [PARTICIPATION] + list(descendants(PARTICIPATION))
    for w in tree:
        if w not in model:
            note = "no shape -> would inherit the generic engine" if w != PARTICIPATION else ""
            if w != PARTICIPATION:
                print(f"    - {disp(w):28} (no SHACL shape)  {note}")
            continue
        part, hosts, other = infer_roles(model[w])
        act_hosts = [h for h in dict.fromkeys(hosts) if is_activity(h)]
        non_act = [h for h in dict.fromkeys(hosts) if not is_activity(h)]
        method = "add_participant" if w == PARTICIPATION else f"add_{snake(disp(w))}"
        host_s = "|".join(act_hosts) or "<<no Activity host>>"
        part_s = "|".join(dict.fromkeys(part)) or "(explicit arg)"
        print(f"    {method}()")
        print(f"        host (Activity): {host_s}   participant: {part_s}")
        if non_act:
            print(f"        + non-Activity isPartOf endpoint(s): {'|'.join(non_act)}")
        for ps in other:
            print(f"        + extra edge {ps.path} -> {'|'.join(ps.targets) or '?'}")

    # ---- 2. lifecycle / boundary states ----------------------------------------
    print("\n" + "-" * 78)
    print("2. LIFECYCLE / BOUNDARY STATES  (isAStartOf / isAFinishOf shaped edges)")
    print("-" * 78)
    boundary_kind = {"isAStartOf": "start", "isAFinishOf": "finish", "isAnEndOf": "end"}
    for w in sorted(lifecycle):
        for ps in model[w]:
            if ps.path in boundary_kind:
                tgt = "|".join(ps.targets) or "?"
                print(f"    {disp(w):20} {ps.path} -> {tgt:18} ({boundary_kind[ps.path]}-boundary of {tgt})")

    # ---- 3. typed identifiers ---------------------------------------------------
    print("\n" + "-" * 78)
    print("3. TYPED IDENTIFIERS  (isIdentifiedBy shaped edges -> add_identifier specialisation)")
    print("-" * 78)
    for w in sorted(identifier):
        idts = []
        for ps in model[w]:
            if ps.path == "isIdentifiedBy":
                idts += ps.targets
        print(f"    {disp(w):20} -> {', '.join(dict.fromkeys(idts))}")

    # ---- 4. other structural 1-hop ---------------------------------------------
    print("\n" + "-" * 78)
    print("4. OTHER STRUCTURAL 1-HOP  (direct add_<path> methods)")
    print("-" * 78)
    for w in sorted(structural):
        edges = "; ".join(f"{ps.path}->{'|'.join(ps.targets) or '?'}" for ps in model[w])
        print(f"    {disp(w):24} {edges}")

    # ---- 4b. property domain/range (the 1-hop layer) ---------------------------
    print("\n" + "-" * 78)
    print("4b. PROPERTY DOMAIN/RANGE  (sh:targetSubjectsOf / sh:targetObjectsOf)")
    print("-" * 78)
    dom, rng = property_model(g)
    props = sorted(set(dom) | set(rng))
    obj_props = [p for p in props if p in rng]
    lit_props = [p for p in props if p not in rng and p in dom]
    print("  object-valued (range is a class) -> add_<prop>(target):")
    for p in obj_props:
        print(f"      {p:30} {dom.get(p, '?')} -> {rng[p]}")
    print("  literal-valued (domain, no object-range) -> set_<prop>(value):")
    for p in lit_props:
        print(f"      {p:30} {dom[p]} -> <literal>")

    # ---- 5. reified roots with NO shape (literal chains) ------------------------
    print("\n" + "-" * 78)
    print("5. REIFIED ROOTS WITH NO SHACL SHAPE  (literal-valued; derived from subClassOf)")
    print("-" * 78)
    for root in ("IesCore_Representation",):
        chain = [root] + descendants(root)
        present = [disp(w) for w in chain]
        shaped = [disp(w) for w in chain if w in model]
        print(f"    {disp(root)} chain: {' / '.join(present)}")
        print(f"        in SHACL: {shaped or '(none - all literal-valued, as expected)'}")
        print("        => add_representation engine + add_name/add_identifier from the subclass tree")

    # ---- 6. heuristic stress / ambiguities -------------------------------------
    print("\n" + "-" * 78)
    print("6. AMBIGUITIES / HEURISTIC STRESS  (decide before writing the emitter)")
    print("-" * 78)
    flags = 0
    for w in participation:
        if w == PARTICIPATION:
            continue
        part, hosts, _ = infer_roles(model[w])
        act_hosts = [h for h in dict.fromkeys(hosts) if is_activity(h)]
        if not act_hosts:
            print(f"    [no Activity host] {disp(w)}: isPartOf has no Activity-descended target - needs curation")
            flags += 1
        elif len(act_hosts) > 1:
            print(f"    [multi-Activity-host] {disp(w)}: {'|'.join(act_hosts)} (both Activities - pick primary)")
            flags += 1
        if not part:
            print(f"    [no participant edge] {disp(w)}: no isTemporalPartOf - participant arg unshaped")
            flags += 1
    for w, shapes in model.items():
        for ps in shapes:
            if not ps.targets:
                print(f"    [untyped target] {disp(w)}.{ps.path}: no sh:class/sh:or - target type unknown")
                flags += 1
            if ps.path is None:
                print(f"    [no path] {disp(w)}: property shape without sh:path")
                flags += 1
        seen_paths = [ps.path for ps in shapes]
        for p in set(seen_paths):
            if seen_paths.count(p) > 1:
                print(f"    [repeated predicate] {disp(w)}.{p} x{seen_paths.count(p)}: target-type ambiguous")
                flags += 1
    print(f"    -> {flags} flag(s)")

    # ---- appendix: full raw inventory ------------------------------------------
    print("\n" + "-" * 78)
    print("APPENDIX: full raw SHACL inventory")
    print("-" * 78)
    for w in sorted(model):
        print(f"  {disp(w)}")
        for ps in model[w]:
            tgt = "|".join(ps.targets) or "(untyped)"
            print(f"      {ps.path} -> {tgt}   [{ps.nodekind}]")


if __name__ == "__main__":
    main()
