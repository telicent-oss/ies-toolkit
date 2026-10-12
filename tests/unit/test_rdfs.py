import logging

import pytest

from ies_toolkit import rdfs
from ies_toolkit.rdflib_plugin import RdfLibPlugIn
from ies_toolkit.rdfs import Rdfs_Class, Rdfs_Resource
from tests.rdf_assert import ask


def test_rdfs_resource_creation():
    """Create an RDFS resource with a URI."""
    store = RdfLibPlugIn()
    my_class = Rdfs_Resource(store=store, uri="http://test.org/rdfs_resource_test_1")

    assert my_class.uri == "http://test.org/rdfs_resource_test_1"
    assert my_class.store is not None


def test_rdfs_resource_output():
    """A resource emits its rdf:type rdfs:Resource triple."""
    store = RdfLibPlugIn()
    Rdfs_Resource(store=store, uri="http://test.org/rdfs_resource_test_1")

    assert ask(store, '<http://test.org/rdfs_resource_test_1> a rdfs:Resource')


def test_rdfs_class_creation():
    """Create an RDFS class with a URI."""
    store = RdfLibPlugIn()
    my_class = Rdfs_Class(store=store, uri="http://test.org/rdfs_class_test_1")

    assert my_class.uri == "http://test.org/rdfs_class_test_1"
    assert my_class.store is not None

def test_rdfs_class_output():
    """A class emits its rdf:type rdfs:Class triple."""
    store = RdfLibPlugIn()
    Rdfs_Class(store=store, uri="http://test.org/rdfs_class_test_1")

    assert ask(store, '<http://test.org/rdfs_class_test_1> a rdfs:Class')

def test_rdf_class_instantiation():
    "Create a class and instantiate it."
    store = RdfLibPlugIn()
    my_class = Rdfs_Class(store=store, uri="http://test.org/rdfs_class_test_1")
    instance1 = my_class.instantiate(uri="http://test.org/rdfs_class_test_1_INSTANCE_1")

    assert instance1.uri == "http://test.org/rdfs_class_test_1_INSTANCE_1"
    assert type(instance1) is Rdfs_Resource
    assert ask(store, '<http://test.org/rdfs_class_test_1_INSTANCE_1> a <http://test.org/rdfs_class_test_1>')


def test_invalid_uri_in_instantiate_raises():
    """An invalid URI passed to instantiate() raises ValueError."""
    store = RdfLibPlugIn()
    my_class = Rdfs_Class(store=store, uri="http://test.org/rdfs_class_test_1")
    with pytest.raises(ValueError, match="Invalid URI"):
        my_class.instantiate(uri="not a valid uri!")


def test_invalid_datatype_in_add_literal_logs_warning(caplog):
    """Passing an invalid XSD datatype triggers a warning log."""
    store = RdfLibPlugIn()
    resource = Rdfs_Resource(store=store, uri="http://test.org/test_resource")

    with caplog.at_level(logging.WARNING):
        resource.add_literal(predicate="http://example.org/prop", obj="test value", literal_type="http://invalid/datatype")

    datatype_warnings = [r for r in caplog.records if "Invalid datatype" in r.message]
    assert len(datatype_warnings) == 1
    assert datatype_warnings[0].levelname == "WARNING"
    assert "http://invalid/datatype" in datatype_warnings[0].message


def test_default_datatype_does_not_warn(caplog):
    """Regression: a literal write with no explicit datatype (literal_type=None
    is the default, not an error) must NOT emit an 'Invalid datatype' warning."""
    store = RdfLibPlugIn()
    with caplog.at_level(logging.WARNING):
        store.add_triple("http://test.org/s", "http://test.org/p", "plain value", is_literal=True)

    datatype_warnings = [r for r in caplog.records if "Invalid datatype" in r.message]
    assert datatype_warnings == [], f"unexpected datatype warning(s): {[r.message for r in datatype_warnings]}"


def test_invalid_uri_in_add_triple_raises():
    """Passing an invalid URI object (is_literal=False) must raise, not silently drop the triple."""
    store = RdfLibPlugIn()
    with pytest.raises(ValueError, match="Invalid URI"):
        store.add_triple(
            subject="http://test.org/subject",
            predicate="http://test.org/predicate",
            obj="this is not a valid uri!!!",
            is_literal=False
        )


def test_invalid_uri_subject_predicate_in_add_triple_raise():
    """A bad subject or predicate must raise."""
    store = RdfLibPlugIn()
    with pytest.raises(ValueError, match="Invalid URI subject"):
        store.add_triple("not a uri!!!", "http://test.org/p", "http://test.org/o", is_literal=False)
    with pytest.raises(ValueError, match="Invalid URI predicate"):
        store.add_triple("http://test.org/s", "not a uri!!!", "http://test.org/o", is_literal=False)


def test_labels_and_comments_read_back():
    """labels/comments read the rdfs:label / rdfs:comment values back off a resource."""
    store = RdfLibPlugIn()
    r = Rdfs_Resource(store=store, uri="http://test.org/r")
    assert r.labels == [] and r.comments == []

    r.add_label("First")
    r.add_label("Second")
    r.add_comment("A note")

    # the raw triples exist (independent of the accessors) ...
    assert ask(store, '<http://test.org/r> rdfs:label "First"^^xsd:string')
    assert ask(store, '<http://test.org/r> rdfs:comment "A note"^^xsd:string')
    # ... and the accessors read them back
    assert sorted(r.labels) == ["First", "Second"]
    assert r.comments == ["A note"]


def test_default_store_functionality():
    """Set a default store and use it without passing the store parameter."""
    store = RdfLibPlugIn()
    rdfs.set_default_store(store)

    resource = Rdfs_Resource(uri="http://test.org/default_store_test")

    assert resource.store is store
    assert resource.uri == "http://test.org/default_store_test"
    assert ask(store, '<http://test.org/default_store_test> a rdfs:Resource')

    rdfs._default_store = None  # reset for other tests


def test_no_default_store_raises_error():
    """Creating a resource without a store and no default raises RuntimeError."""
    rdfs._default_store = None

    with pytest.raises(RuntimeError, match="No default store set"):
        Rdfs_Resource(uri="http://test.org/no_store_test")


def test_explicit_store_overrides_default():
    """Explicitly passing store overrides the default store."""
    default_store = RdfLibPlugIn()
    rdfs.set_default_store(default_store)
    explicit_store = RdfLibPlugIn()

    resource = Rdfs_Resource(store=explicit_store, uri="http://test.org/explicit_store_test")

    assert resource.store is explicit_store
    assert resource.store is not default_store

    rdfs._default_store = None
