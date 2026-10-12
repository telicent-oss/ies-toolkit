"""Store conveniences on RdfLibPlugIn: add_prefix and save_rdf."""
import pytest
from rdflib import Graph

from ies_toolkit.ies_core import Person
from ies_toolkit.rdflib_plugin import RdfLibPlugIn


def _store_with_person():
    store = RdfLibPlugIn()
    Person(store=store, uri="http://ex.org/fred")
    return store


def test_add_prefix_appears_in_serialisation():
    store = _store_with_person()
    store.add_prefix("ex", "http://ex.org/")
    assert "@prefix ex:" in store.get_rdf(format="turtle")


def test_add_prefix_accepts_trailing_colon():
    store = RdfLibPlugIn()
    store.add_prefix("ex:", "http://ex.org/")
    assert "ex" in {prefix for prefix, _ in store.graph.namespaces()}


def test_save_rdf_writes_reparseable_file(tmp_path):
    store = _store_with_person()
    out = store.save_rdf(tmp_path / "graph.ttl")
    assert out.exists()
    assert set(Graph().parse(source=str(out), format="turtle")) == set(store.graph)


def test_save_rdf_infers_format_from_suffix(tmp_path):
    store = _store_with_person()
    out = tmp_path / "graph.nt"
    store.save_rdf(out)
    assert set(Graph().parse(source=str(out), format="nt")) == set(store.graph)


def test_save_rdf_explicit_format_overrides_suffix(tmp_path):
    store = _store_with_person()
    out = tmp_path / "graph.data"
    store.save_rdf(out, format="nt")
    assert set(Graph().parse(source=str(out), format="nt")) == set(store.graph)


def test_save_rdf_clear_empties_graph_after_writing(tmp_path):
    store = _store_with_person()
    out = tmp_path / "graph.ttl"
    store.save_rdf(out, clear=True)
    assert len(store.graph) == 0
    assert set(Graph().parse(source=str(out), format="turtle"))  # file still holds the data


def test_save_rdf_keeps_graph_by_default(tmp_path):
    store = _store_with_person()
    store.save_rdf(tmp_path / "graph.ttl")
    assert len(store.graph) > 0


def test_get_rdf_clear_empties_graph_after_serialising():
    store = _store_with_person()
    rdf = store.get_rdf(format="turtle", clear=True)
    assert "fred" in rdf
    assert len(store.graph) == 0


def test_in_graph_finds_a_string_literal():
    """a literal stored by add_triple (^^xsd:string) must be found by
    in_graph(is_literal=True) - avoids a bare Literal and never matched."""
    store = RdfLibPlugIn()
    s, p = "http://ex.org/a", "http://ex.org/note"
    store.add_triple(subject=s, predicate=p, obj="hi", is_literal=True)  # -> ^^xsd:string
    assert store.in_graph(s, p, "hi", is_literal=True) is True
    assert store.in_graph(s, p, "nope", is_literal=True) is False


def test_in_graph_matches_explicit_literal_datatype():
    store = RdfLibPlugIn()
    s, p, xsd_int = "http://ex.org/a", "http://ex.org/count", "http://www.w3.org/2001/XMLSchema#integer"
    store.add_triple(subject=s, predicate=p, obj="3", is_literal=True, literal_type=xsd_int)
    assert store.in_graph(s, p, "3", is_literal=True, literal_type=xsd_int) is True


def test_in_graph_finds_an_object_triple():
    store = RdfLibPlugIn()
    s, p, o = "http://ex.org/a", "http://ex.org/rel", "http://ex.org/b"
    store.add_triple(subject=s, predicate=p, obj=o, is_literal=False)
    assert store.in_graph(s, p, o, is_literal=False) is True


def test_delete_triple_removes_an_object_triple():
    store = RdfLibPlugIn()
    s, p, o = "http://ex.org/a", "http://ex.org/rel", "http://ex.org/b"
    store.add_triple(subject=s, predicate=p, obj=o, is_literal=False)
    assert store.in_graph(s, p, o, is_literal=False)
    assert store.delete_triple(s, p, o) is True
    assert not store.in_graph(s, p, o, is_literal=False)


def test_delete_triple_matches_literal_datatype():
    store = RdfLibPlugIn()
    s, p = "http://ex.org/a", "http://ex.org/note"
    store.add_triple(subject=s, predicate=p, obj="hi", is_literal=True)  # stored as ^^xsd:string
    assert store.delete_triple(s, p, "hi", is_literal=True) is True
    assert len(store.graph) == 0


def test_delete_triple_returns_false_when_absent():
    store = RdfLibPlugIn()
    assert store.delete_triple("http://ex.org/a", "http://ex.org/rel", "http://ex.org/b") is False


def test_delete_triple_rejects_invalid_uri_object():
    """A malformed non-literal object raises, not a silent no-op."""
    store = RdfLibPlugIn()
    with pytest.raises(ValueError, match="Invalid URI"):
        store.delete_triple("http://ex.org/a", "http://ex.org/rel", "not a uri!!!", is_literal=False)


def test_add_triple_accepts_non_http_iri_schemes():
    store = RdfLibPlugIn()
    for uri in ("urn:uuid:1234", "ex:local", "tag:example,2024:foo"):
        store.add_triple(uri, "http://ex.org/p", "http://ex.org/o", is_literal=False)  # no raise
    assert len(store.graph) == 3


def test_add_triple_rejects_uri_with_whitespace():
    store = RdfLibPlugIn()
    with pytest.raises(ValueError, match="Invalid URI"):
        store.add_triple("http://ex.org/a b", "http://ex.org/p", "http://ex.org/o", is_literal=False)


def test_add_triple_rejects_uri_without_scheme():
    store = RdfLibPlugIn()
    with pytest.raises(ValueError, match="Invalid URI"):
        store.add_triple("noscheme", "http://ex.org/p", "http://ex.org/o", is_literal=False)


def test_add_triple_rejects_iriref_forbidden_chars():
    """URIs with IRIREF-forbidden chars are caught at the boundary, not later at
    serialisation (angle bracket) or silently in invalid output (control char)."""
    store = RdfLibPlugIn()
    for bad in ("http://ex.org/a>b", "http://ex.org/a\x00b", 'http://ex.org/a"b', "http://ex.org/a`b"):
        with pytest.raises(ValueError, match="Invalid URI"):
            store.add_triple(bad, "http://ex.org/p", "http://ex.org/o", is_literal=False)


def test_deletion_supported_is_true():
    assert RdfLibPlugIn().deletion_supported is True


def test_default_data_namespace_get_set():
    store = RdfLibPlugIn()
    store.default_data_namespace = "http://mydata.example/"
    assert store.default_data_namespace == "http://mydata.example/"
    assert store.generate_data_uri().startswith("http://mydata.example/")
