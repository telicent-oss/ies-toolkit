"""Falklands acceptance example: persons (Sandy Woodward).

Ports people_csv_to_ttl.py to the IES-Next API: a Person whose career is a series of
named States (temporal parts), each placed in its ParticularPeriod(s), with birth/death
boundary states. Royal Navy ranks have no IES-Next class, so they keep their rn: domain
URIs on an IES-Next State. URIs are pinned (and period URIs are deterministic per the
ParticularPeriod convention), so the whole graph is asserted against a golden; the ASKs
document the birth boundary, a rank state, and the shared ParticularPeriod between ranks.
"""
import csv
from pathlib import Path

from ies_toolkit.constants import IES_CORE, ISO_8601
from ies_toolkit.ies_core import Person
from ies_toolkit.ies_top import State
from ies_toolkit.rdflib_plugin import RdfLibPlugIn
from tests.rdf_assert import ask, assert_matches_golden

HERE = Path(__file__).resolve().parent
DATA = "http://example.com/data#"
RN = "http://royalnavy.mod.uk/ontology#"
IES_NEXT_NS = ("http://purl.org/ies/top/v0/ont/", "http://purl.org/ies/core/v0/ont/")


def _build():
    store = RdfLibPlugIn()
    given, surname = "Sandy", "Woodward"  # from the filename sandy_woodward.csv
    person_uri = DATA + given + surname
    person = Person(store=store, uri=person_uri)
    person.add_name(f"{given} {surname}", representation_classes=[f"{IES_CORE}PersonName"],
                    representation_uri=f"{person_uri}_name")

    rows = list(csv.DictReader((HERE / "data" / "sandy_woodward.csv").open(encoding="utf-8-sig")))
    for i, row in enumerate(rows):
        cls = row["state"]
        uri = f"{person_uri}_state_{i}"
        if cls.startswith(IES_NEXT_NS):
            st = State(store=store, uri=uri, classes=[cls])           # an IES-NEXT class -> rdf:type it
        else:
            st = State(store=store, uri=uri, categories=[cls])        # a foreign class (rn: rank) -> State + category
        if cls.endswith("BirthState"):
            # birth/death are themselves boundary states of the person, at a single instant
            st.is_start_of(person)
            st.put_in_period(row["start"])
        elif cls.endswith("DeathState"):
            st.is_finish_of(person)
            st.put_in_period(row["start"])
        else:
            # a rank is a duration: a temporal part of the person, bounded by start/finish states
            st.is_temporal_part_of(person)
            if row["start"]:
                st.starts_in(row["start"])
            if row["end"]:
                st.finishes_in(row["end"])
    return store, person_uri


def test_persons():
    store, person_uri = _build()
    # the birth state is itself a boundary of the person, within its ParticularPeriod (deterministic URI)
    assert ask(store, f"""
        <{person_uri}_state_0> a ies_core:BirthState ;
                               ies_top:isAStartOf <{person_uri}> ;
                               ies_top:isPartOf <{ISO_8601}19320501> .
        <{ISO_8601}19320501> a ies_core:ParticularPeriod ;
                             ies_core:iso8601PeriodRepresentation "1932-05-01"^^xsd:string .
    """)
    # a rank is a duration: an ies_top:State categorised with the (foreign) rank, a temporal part
    # of the person, bounded by start/finish States that isPartOf ParticularPeriods. No name on it.
    assert ask(store, f"""
        <{person_uri}_state_5> a ies_top:State ;
                               ies_core:category <{RN}Captain> ;
                               ies_top:isTemporalPartOf <{person_uri}> .
        <{person_uri}_state_5_start> a ies_top:State ;
                                     ies_top:isAStartOf <{person_uri}_state_5> ;
                                     ies_top:isPartOf <{ISO_8601}1972> .
        <{person_uri}_state_5_finish> a ies_top:State ;
                                      ies_top:isAFinishOf <{person_uri}_state_5> ;
                                      ies_top:isPartOf <{ISO_8601}198107> .
    """)
    assert not ask(store, f'<{person_uri}_state_5> ies_core:hasName ?n')  # states carry no names
    # consecutive ranks share a ParticularPeriod: Officer's finish and Lieutenant's start are both 1954-05
    assert ask(store, f"""
        <{ISO_8601}195405> a ies_core:ParticularPeriod ;
                           ies_core:iso8601PeriodRepresentation "1954-05"^^xsd:string .
        <{person_uri}_state_1_finish> ies_top:isAFinishOf <{person_uri}_state_1> ;
                                      ies_top:isPartOf <{ISO_8601}195405> .
        <{person_uri}_state_2_start> ies_top:isAStartOf <{person_uri}_state_2> ;
                                     ies_top:isPartOf <{ISO_8601}195405> .
    """)
    assert_matches_golden(store, HERE / "golden" / "persons.ttl")


def test_persons_via_lifecycle_helpers():
    """Same Sandy Woodward graph as test_persons, but birth/death built with the ergonomic
    add_birth/add_death helpers instead of the manual boundary pattern - asserts the SAME golden,
    proving the helpers are equivalent to hand-wiring the boundary states."""
    store = RdfLibPlugIn()
    given, surname = "Sandy", "Woodward"
    person_uri = DATA + given + surname
    person = Person(store=store, uri=person_uri)
    person.add_name(f"{given} {surname}", representation_classes=[f"{IES_CORE}PersonName"],
                    representation_uri=f"{person_uri}_name")

    rows = list(csv.DictReader((HERE / "data" / "sandy_woodward.csv").open(encoding="utf-8-sig")))
    for i, row in enumerate(rows):
        cls = row["state"]
        uri = f"{person_uri}_state_{i}"
        if cls.endswith("BirthState"):
            person.add_birth(date_of_birth=row["start"], birth_uri=uri)
        elif cls.endswith("DeathState"):
            person.add_death(date_of_death=row["start"], death_uri=uri)
        else:
            st = (State(store=store, uri=uri, classes=[cls]) if cls.startswith(IES_NEXT_NS)
                  else State(store=store, uri=uri, categories=[cls]))
            st.is_temporal_part_of(person)
            if row["start"]:
                st.starts_in(row["start"])
            if row["end"]:
                st.finishes_in(row["end"])

    assert_matches_golden(store, HERE / "golden" / "persons.ttl")
