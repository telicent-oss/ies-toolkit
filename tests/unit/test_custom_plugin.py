"""A custom RDFPlugin works with the wrapper classes, mixins and generated
builders. The whole build path reaches the store through exactly two methods -
generate_data_uri and add_triple - so a plugin implementing just those drives
everything: construction, naming (ThingMixin), lifecycle (LivingOrganismMixin),
and the generated reified engine (ReifiedBuilderMixin)."""
import pytest

from ies_toolkit import rdfs
from ies_toolkit.ies_core import Account, Person
from ies_toolkit.rdf_plugin import RDFPlugin


class CapturingPlugin(RDFPlugin):
    """Minimal store: records triples in a list, mints deterministic URIs. It
    implements only the two methods the wrapper layer calls."""

    def __init__(self):
        self.triples = []
        self._counter = 0

    def generate_data_uri(self, uri_root=None):
        self._counter += 1
        return f"{uri_root or 'http://cap/'}{self._counter}"

    def add_triple(self, subject, predicate, obj, is_literal, literal_type=None):
        self.triples.append((str(subject), str(predicate), str(obj), is_literal))


def _local(uri):
    return uri.rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def _has(cap, subj, pred_suffix, obj_local=None, is_literal=None):
    for s, p, o, lit in cap.triples:
        if s == subj and p.endswith(pred_suffix) \
                and (obj_local is None or _local(o) == obj_local) \
                and (is_literal is None or lit == is_literal):
            return True
    return False


def _objs(cap, subj, pred_suffix):
    return [o for s, p, o, lit in cap.triples if s == subj and p.endswith(pred_suffix)]


def test_custom_plugin_drives_construction_and_naming():
    cap = CapturingPlugin()
    fred = Person(store=cap, uri="http://d/fred")
    assert _has(cap, "http://d/fred", "#type", "Person")

    fred.add_name("Fred Bloggs")
    # a Name node is minted (via generate_data_uri) and given the literal value
    assert any(o == "Fred Bloggs" and lit for s, p, o, lit in cap.triples)
    assert cap._counter > 0  # the store minted the Name node's URI


def test_custom_plugin_drives_lifecycle_mixin():
    cap = CapturingPlugin()
    fred = Person(store=cap, uri="http://d/fred")
    fred.add_birth(date_of_birth="1948-05-01", place_of_birth="http://d/london")

    (birth,) = {s for s, p, o, lit in cap.triples if _local(o) == "BirthState"}
    assert _has(cap, birth, "isAStartOf", "fred")
    assert _has(cap, birth, "isPartOf", "london")
    assert _has(cap, birth, "isPartOf")  # + the ParticularPeriod
    # the period carries its iso8601 literal
    assert any("1948-05-01" in o and lit for s, p, o, lit in cap.triples)


def test_custom_plugin_drives_generated_reified_builder():
    cap = CapturingPlugin()
    fred = Person(store=cap, uri="http://d/fred")
    account = Account(store=cap, uri="http://d/acc")
    node = account.add_account_holder(fred)

    assert _has(cap, node, "#type", "AccountHolder")
    assert _has(cap, node, "isPartOf", "acc")           # host edge -> the Account
    assert _has(cap, node, "isTemporalPartOf", "fred")  # participant edge -> the Person


def test_default_store_mechanism_accepts_a_custom_plugin():
    cap = CapturingPlugin()
    rdfs.set_default_store(cap)
    try:
        person = Person(uri="http://d/nostore")  # no store= -> uses the default
        assert person.store is cap
        assert _has(cap, "http://d/nostore", "#type", "Person")
    finally:
        rdfs._default_store = None


def test_missing_default_store_raises_a_clear_error():
    rdfs._default_store = None
    with pytest.raises(RuntimeError, match="No default store"):
        Person(uri="http://d/x")
