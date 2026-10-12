"""Shared SPARQL assertion helpers for tests that check produced RDF.

Queries run against the store's rdflib graph (RdfLibPlugIn exposes `.graph`), with
the IES prefixes pre-bound. String literals are stored as ^^xsd:string, and rdflib
SPARQL does not equate a bare "x" with "x"^^xsd:string - match values with
"x"^^xsd:string or FILTER(STR(?v) = "x").
"""
import os
from pathlib import Path

from rdflib import Graph, Namespace

PREFIXES = {
    "rdf": Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
    "rdfs": Namespace("http://www.w3.org/2000/01/rdf-schema#"),
    "xsd": Namespace("http://www.w3.org/2001/XMLSchema#"),
    "ies_top": Namespace("http://purl.org/ies/top/v0/ont/"),
    "ies_core": Namespace("http://purl.org/ies/core/v0/ont/"),
    "ical": Namespace("http://www.w3.org/2002/12/cal/ical#"),
}


def ask(store, where: str) -> bool:
    """True if the WHERE graph pattern matches in the store's graph. `where` is a
    brace-free pattern (the ASK {} wrapper is added here), so callers can use a
    multi-line f-string and interpolate {var} without doubling braces."""
    return bool(store.graph.query(f"ASK {{ {where} }}", initNs=PREFIXES))


def count(store, where: str) -> int:
    """Number of solutions for the (brace-free) WHERE graph pattern."""
    return len(list(store.graph.query(f"SELECT * WHERE {{ {where} }}", initNs=PREFIXES)))


def assert_matches_golden(store, path) -> None:
    """Assert the store's whole graph equals the golden Turtle file at `path`.
    The golden is Turtle (readable for review); comparison parses it back to a graph
    and checks graph equality, so it is order-independent (exact given pinned URIs and
    no blank nodes). Run with UPDATE_GOLDENS=1 to (re)write the golden instead."""
    path = Path(path)
    if os.environ.get("UPDATE_GOLDENS"):
        for prefix, ns in PREFIXES.items():
            store.graph.namespace_manager.bind(prefix, ns, replace=True)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(store.graph.serialize(format="turtle"), encoding="utf-8")
        return
    expected = set(Graph().parse(source=str(path), format="turtle"))
    actual = set(store.graph)
    if actual == expected:
        return
    lines = [f"graph differs from golden {path.name} (run UPDATE_GOLDENS=1 to refresh):"]
    lines += [f"  + {s} {p} {o}" for s, p, o in sorted(actual - expected, key=str)]
    lines += [f"  - {s} {p} {o}" for s, p, o in sorted(expected - actual, key=str)]
    raise AssertionError("\n".join(lines))
