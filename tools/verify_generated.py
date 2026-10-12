"""Human-readable diagnostic: check the generated IES module is faithful to the
ontology - every generated class's bases are real ontology parents and its
init-style (state vs cls) matches its descent from ies_top:State.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import rdflib
from rdflib import RDF, RDFS

sys.path.insert(0, str(Path(__file__).resolve().parent))  # import the sibling generator
from generate_ies import emit_name, py_name  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OWL_CLASS = rdflib.URIRef("http://www.w3.org/2002/07/owl#Class")


def parse_classes(path: Path):
    """name -> (bases list, init style) from a python source file."""
    src = path.read_text()
    out = {}
    for m in re.finditer(r"class\s+(\w+)\(([^)]*)\):(.*?)(?=\nclass |\Z)", src, re.S):
        name = m.group(1)
        bases = [b.strip() for b in m.group(2).split(",") if b.strip()]
        body = m.group(3)
        style = "state" if "_state_init(" in body else ("cls" if "_cls_init(" in body else "?")
        out[name] = (bases, style)
    return out


def ontology_model():
    g = rdflib.Graph()
    g.parse(ROOT / "ies-top.ttl")
    g.parse(ROOT / "ies-core.ttl")
    classes = set()
    for t in (RDFS.Class, OWL_CLASS):
        for s, _, _ in g.triples((None, RDF.type, t)):
            classes.add(str(s))
    parents = {}
    for s, _, o in g.triples((None, RDFS.subClassOf, None)):
        parents.setdefault(str(s), []).append(str(o))

    def full_parents(name_uri):
        return [py_name(p) for p in parents.get(name_uri, []) if py_name(p)]

    # State descent across the whole graph (kept in prefixed internal names)
    pmap = {}
    for c in classes:
        n = py_name(c)
        if n:
            pmap[n] = full_parents(c)

    def descends_state(n, seen=None):
        if n == "IesTop_State":
            return True
        seen = seen or set()
        if n in seen:
            return False
        seen.add(n)
        return any(descends_state(p, seen) for p in pmap.get(n, []))

    # outputs use the bare public names the generated file carries
    all_names = {emit_name(n) for n in pmap}
    core = {}
    for c in classes:
        n = py_name(c)
        if n and n.startswith("IesCore_"):
            core[emit_name(n)] = ({emit_name(p) for p in pmap[n]},
                                  "state" if descends_state(n) else "cls")
    return core, all_names


def main():
    onto, all_names = ontology_model()
    gen = {k: v for k, v in parse_classes(ROOT / "ies_toolkit" / "ies_core_generated.py").items()
           if k in onto}

    print(f"counts: ontology={len(onto)}  generated={len(gen)}")
    problems = 0
    for name, (bases, style) in gen.items():
        if name not in onto:
            print(f"  [not in ontology] {name}"); problems += 1; continue
        onto_parents, onto_style = onto[name]
        for b in bases:
            if b in all_names and b not in onto_parents:
                print(f"  [bad base] {name}: {b} not an ontology parent {sorted(onto_parents)}"); problems += 1
        for p in onto_parents:
            if p not in bases:
                print(f"  [missing base] {name}: ontology parent {p} not in generated bases {sorted(bases)}"); problems += 1
        if style != onto_style:
            print(f"  [init mismatch] {name}: gen={style} onto={onto_style}"); problems += 1
    missing = set(onto) - set(gen)
    for name in sorted(missing):
        print(f"  [missing from generated] {name}"); problems += 1
    print(f"-> {problems} faithfulness problem(s)")


if __name__ == "__main__":
    main()
