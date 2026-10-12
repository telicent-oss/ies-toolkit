"""The IES-terms layer over the generated terms file (*_terms_generated.py), two
behaviours:
  * the typed namespace (IesCore / IesTop) - symbolic, typo-safe term access;
  * the non-IES warning (ies_terms.IesTermsMixin) - warns when a class/predicate not
    in IES is used, scoped to the IES Top/Core wrappers (RDFS base never warns)."""
import logging

import pytest
from rdflib import URIRef

from ies_toolkit.constants import IES_CORE
from ies_toolkit.ies_core import IesCore, Person
from ies_toolkit.ies_top import IesTop
from ies_toolkit.rdflib_plugin import RdfLibPlugIn
from ies_toolkit.rdfs import Rdfs_Resource
from tests.rdf_assert import ask


def _non_ies_warnings(caplog):
    return [r for r in caplog.records if "non-IES" in r.message]


# --- typed namespace: symbolic, typo-safe term access --------------------------

def test_namespace_terms_resolve_to_uris():
    assert IesCore.Person == URIRef("http://purl.org/ies/core/v0/ont/Person")
    assert IesTop.isPartOf == URIRef("http://purl.org/ies/top/v0/ont/isPartOf")


def test_namespace_unknown_term_raises():
    with pytest.raises(AttributeError):
        _ = IesCore.Persn          # typo'd class
    with pytest.raises(AttributeError):
        _ = IesTop.isPartof        # typo'd predicate


def test_namespace_terms_usable_in_add_triple():
    store = RdfLibPlugIn()
    store.add_triple("http://d/a", IesTop.isPartOf, IesCore.Person, is_literal=False)
    assert ask(store, "<http://d/a> ies_top:isPartOf ies_core:Person")


# --- non-IES warning -----------------------------------------------------------


def test_uriref_input_is_matched_not_just_str(caplog):
    """A URIRef term (not only a str) must be matched against the registry - a valid
    IES class passed as URIRef must not falsely warn; a foreign one must."""
    store = RdfLibPlugIn()
    person = Person(store=store, uri="http://d/fred")
    with caplog.at_level(logging.WARNING):
        person.add_type(URIRef(f"{IES_CORE}Organization"))  # valid IES class, as URIRef
    assert _non_ies_warnings(caplog) == []
    with caplog.at_level(logging.WARNING):
        person.add_type(URIRef("http://foreign/Thing"))
    assert len(_non_ies_warnings(caplog)) == 1


def test_ies_wrapper_warns_on_non_ies_class(caplog):
    store = RdfLibPlugIn()
    with caplog.at_level(logging.WARNING):
        Person(store=store, uri="http://d/fred", classes=["http://foreign/Thing"])
    warnings = _non_ies_warnings(caplog)
    assert len(warnings) == 1
    assert "non-IES class" in warnings[0].message and "http://foreign/Thing" in warnings[0].message


def test_ies_wrapper_add_type_warns_on_non_ies_class(caplog):
    store = RdfLibPlugIn()
    person = Person(store=store, uri="http://d/fred")
    with caplog.at_level(logging.WARNING):
        person.add_type("http://foreign/Thing")
    assert len(_non_ies_warnings(caplog)) == 1


def test_ies_wrapper_no_warning_for_ies_class(caplog):
    store = RdfLibPlugIn()
    with caplog.at_level(logging.WARNING):
        Person(store=store, uri="http://d/fred")  # rdf:type ies:Person
    assert _non_ies_warnings(caplog) == []


def test_rdfs_level_does_not_warn_on_non_ies_class(caplog):
    """The RDFS base wrappers hold no IES knowledge: a non-IES class must NOT warn
    at the RDFS level - the check is scoped to the IES Top/Core wrappers."""
    store = RdfLibPlugIn()
    with caplog.at_level(logging.WARNING):
        Rdfs_Resource(store=store, uri="http://d/x", classes=["http://foreign/Thing"])
        Rdfs_Resource(store=store, uri="http://d/y").add_type("http://foreign/Thing")
    assert _non_ies_warnings(caplog) == []


def test_non_ies_category_does_not_warn(caplog):
    """Categories are fine: ies_core:category is a declared IES property and the
    concept is the object, not a type."""
    store = RdfLibPlugIn()
    with caplog.at_level(logging.WARNING):
        Person(store=store, uri="http://d/fred",
                       categories=["http://foreign/RoyalNavyRank"])
    assert _non_ies_warnings(caplog) == []


def test_ies_wrapper_warns_on_non_ies_predicate(caplog):
    store = RdfLibPlugIn()
    person = Person(store=store, uri="http://d/fred")
    with caplog.at_level(logging.WARNING):
        person.add_literal("http://foreign/note", "hi")
    assert len(_non_ies_warnings(caplog)) == 1
    assert "non-IES property" in _non_ies_warnings(caplog)[0].message


def test_label_comment_predicates_do_not_warn(caplog):
    store = RdfLibPlugIn()
    person = Person(store=store, uri="http://d/fred")
    with caplog.at_level(logging.WARNING):
        person.add_label("Fred")      # rdfs:label - structural, exempt
        person.add_comment("a note")  # rdfs:comment - structural, exempt
    assert _non_ies_warnings(caplog) == []
