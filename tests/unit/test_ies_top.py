import datetime

import pytest

from ies_toolkit.constants import ISO_8601
from ies_toolkit.ies_top import Set, SetOfSetOfStates, SetOfStates, State, Thing, Tuple
from ies_toolkit.rdflib_plugin import RdfLibPlugIn
from tests.rdf_assert import ask, count


def test_ies_thing_creation():
    """Create an IES Thing with a URI."""
    store = RdfLibPlugIn()
    my_class = Thing(store=store, uri="http://test.org/ies_thing_test_1")

    assert my_class.uri == "http://test.org/ies_thing_test_1"
    assert my_class.store is not None


def test_ies_set_instantiation():
    "Create a class and instantiate it."
    store = RdfLibPlugIn()
    my_class = Set(store=store, uri="http://test.org/ies_set_test_1")
    instance1 = my_class.instantiate(uri="http://test.org/ies_set_test_1_INSTANCE_1")

    assert instance1.uri == "http://test.org/ies_set_test_1_INSTANCE_1"
    assert type(instance1) is Thing
    assert ask(store, '<http://test.org/ies_set_test_1_INSTANCE_1> a <http://test.org/ies_set_test_1>')

def test_set_of_states_instance_type():
    "A set of states instantiates a State."
    store = RdfLibPlugIn()
    my_class = SetOfStates(store=store, uri="http://test.org/ies_set_test_1")
    instance1 = my_class.instantiate(uri="http://test.org/ies_set_test_1_INSTANCE_1")

    assert instance1.uri == "http://test.org/ies_set_test_1_INSTANCE_1"
    assert type(instance1) is State

def test_set_of_set_of_states_instance_type():
    "A set of set of states instantiates a SetOfStates."
    store = RdfLibPlugIn()
    my_class = SetOfSetOfStates(store=store, uri="http://test.org/ies_set_test_1")
    instance1 = my_class.instantiate(uri="http://test.org/ies_set_test_1_INSTANCE_1")

    assert instance1.uri == "http://test.org/ies_set_test_1_INSTANCE_1"
    assert type(instance1) is SetOfStates

def test_state_start():
    "start= creates a bounding State that isPartOf a typed ParticularPeriod."
    store = RdfLibPlugIn()
    start_date = datetime.datetime.now(datetime.UTC)
    utc_start = start_date.astimezone(datetime.UTC)
    period = f"{ISO_8601}{utc_start.strftime('%Y%m%dT%H%M%S')}"      # per ParticularPeriod convention: no Z
    iso_rep = utc_start.strftime("%Y-%m-%dT%H:%M:%S")
    my_state = State(store=store, start=start_date)
    assert type(my_state.start_state) is State
    assert ask(store, f"""
        <{my_state.start_state.uri}> ies_top:isAStartOf <{my_state.uri}> ;
                                     ies_top:isPartOf <{period}> .
        <{period}> a ies_core:ParticularPeriod ;
                   ies_core:iso8601PeriodRepresentation "{iso_rep}"^^xsd:string .
    """)


def test_ies_state_relationship_methods():
    """State relationship methods add the correct triples."""
    store = RdfLibPlugIn()
    states = {n: State(store=store, uri=f"http://test.org/state_{n}") for n in range(1, 7)}
    s1, s2, s3, s4, s5, s6 = (states[n] for n in range(1, 7))
    s1.is_part_of(s2)
    s2.has_part(s3)
    s3.is_temporal_part_of(s4)
    s4.has_temporal_part(s5)
    s5.is_start_of(s6)
    s6.has_start_state(s1)
    s1.is_finish_of(s2)
    s2.has_finish_state(s3)

    assert ask(store, """
        <http://test.org/state_1> ies_top:isPartOf         <http://test.org/state_2> .
        <http://test.org/state_3> ies_top:isPartOf         <http://test.org/state_2> .
        <http://test.org/state_3> ies_top:isTemporalPartOf <http://test.org/state_4> .
        <http://test.org/state_5> ies_top:isTemporalPartOf <http://test.org/state_4> .
        <http://test.org/state_5> ies_top:isAStartOf       <http://test.org/state_6> .
        <http://test.org/state_1> ies_top:isAStartOf       <http://test.org/state_6> .
        <http://test.org/state_1> ies_top:isAFinishOf      <http://test.org/state_2> .
        <http://test.org/state_3> ies_top:isAFinishOf      <http://test.org/state_2> .
    """)


def test_ies_tuple_places():
    """Tuple add_place creates correct triples, and subPropertyOf only for indices > 4."""
    store = RdfLibPlugIn()
    my_tuple = Tuple(store=store, uri="http://test.org/tuple_1")
    items = {n: Thing(store=store, uri=f"http://test.org/item_{n}") for n in range(1, 6)}
    for n, item in items.items():
        my_tuple.add_place(n, item)

    assert ask(store, """
        <http://test.org/tuple_1> ies_top:tuplePlace_1 <http://test.org/item_1> ;
                                  ies_top:tuplePlace_2 <http://test.org/item_2> ;
                                  ies_top:tuplePlace_3 <http://test.org/item_3> ;
                                  ies_top:tuplePlace_4 <http://test.org/item_4> ;
                                  ies_top:tuplePlace_5 <http://test.org/item_5> .
    """)
    # tuplePlace_5 (index > 4) declares subPropertyOf tuplePlace; 1-4 do not, so exactly one such triple
    assert ask(store, 'ies_top:tuplePlace_5 rdfs:subPropertyOf ies_top:tuplePlace')
    assert count(store, '?tp rdfs:subPropertyOf ies_top:tuplePlace') == 1


def test_ies_tuple_place_rejects_non_positive_index():
    """A tuple index below 1 is rejected, not minted as tuplePlace_0 OR a negative place."""
    store = RdfLibPlugIn()
    my_tuple = Tuple(store=store, uri="http://test.org/tuple_1")
    item = Thing(store=store, uri="http://test.org/item")
    for bad in (0, -1):
        with pytest.raises(ValueError, match="must be >= 1"):
            my_tuple.add_place(bad, item)


def test_bounding_states():
    """The IES-Next bounding-state pattern: a duration State is a temporal part of an
    entity, time-bounded by start/finish States that each isPartOf a ParticularPeriod
    and isAStartOf/isAFinishOf the state (periods are NOT linked to the state directly)."""
    store = RdfLibPlugIn()
    fred = State(store=store, uri="http://d/fred")
    state = State(store=store, uri="http://d/fred_state_001")
    state.is_temporal_part_of(fred)
    state.starts_in("2024-03-02T10:00")     # -> http://d/fred_state_001_start
    state.finishes_in("2024-03-02T13:30")   # -> http://d/fred_state_001_finish

    assert ask(store, """
        <http://d/fred_state_001> ies_top:isTemporalPartOf <http://d/fred> .
        <http://d/fred_state_001_start> a ies_top:State ;
            ies_top:isAStartOf <http://d/fred_state_001> ;
            ies_top:isPartOf <http://iso8601.iso.org/20240302T1000> .
        <http://d/fred_state_001_finish> a ies_top:State ;
            ies_top:isAFinishOf <http://d/fred_state_001> ;
            ies_top:isPartOf <http://iso8601.iso.org/20240302T1330> .
        <http://iso8601.iso.org/20240302T1000> a ies_core:ParticularPeriod ;
            ies_core:iso8601PeriodRepresentation "2024-03-02T10:00"^^xsd:string .
    """)
    # the duration state is NOT itself isPartOf a period; only its bounding states are
    assert not ask(store, '<http://d/fred_state_001> ies_top:isPartOf ?period')


@pytest.mark.parametrize("value,expect_uri_suffix", [
    ("1972", "1972"),                          # year
    ("1954-05", "195405"),                     # year-month
    ("1932-05-01", "19320501"),                # date
    ("2024-03-02T10:00", "20240302T1000"),     # datetime
    ("2024-03-02T10:00:00", "20240302T100000"),
    ("2024-03-02T10:00Z", "20240302T1000"),    # trailing Z stripped (no-Z convention)
])
def test_put_in_period_accepts_valid_iso8601_granularities(value, expect_uri_suffix):
    store = RdfLibPlugIn()
    s = State(store=store, uri="http://d/s")
    period = s.put_in_period(value)
    assert period == f"{ISO_8601}{expect_uri_suffix}"
    assert ask(store, f'<http://d/s> ies_top:isPartOf <{period}>')


@pytest.mark.parametrize("bad", [
    "not-a-date",
    "2024-13-01",                 # invalid month
    "2024-03-32",                 # invalid day
    "2024-03-02T25:00",           # invalid hour
    "2024-03-02T10:00+05:00",     # explicit offset not allowed
    "",                           # empty
])
def test_put_in_period_rejects_invalid_iso8601(bad):
    store = RdfLibPlugIn()
    s = State(store=store, uri="http://d/s")
    with pytest.raises(ValueError):
        s.put_in_period(bad)
