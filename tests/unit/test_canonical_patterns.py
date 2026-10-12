"""Unit tests for canonical IES-NEXT modelling forms (worked examples from Andreas).

These pin the shapes the tool must produce: birth/death bounding of a Person, and an
Activity with participants. Pinned URIs; SPARQL ASKs document each shape.
"""
import pytest

from ies_toolkit.ies_core import (
    BirthState,
    DeathState,
    GovernanceActivity,
    Location,
    Meeting,
    Organization,
    PartyInCommunication,
    Person,
)
from ies_toolkit.rdflib_plugin import RdfLibPlugIn
from tests.rdf_assert import ask

D = "http://d/"
ISO = "http://iso8601.iso.org/"


def test_person_bounded_by_birth_and_death():
    """A Person's life bounded by BirthState/DeathState: each isAStartOf/isAFinishOf the
    person and isPartOf both a Location and a ParticularPeriod."""
    store = RdfLibPlugIn()
    fred = Person(store=store, uri=f"{D}fred")
    london = Location(store=store, uri=f"{D}London")
    birmingham = Location(store=store, uri=f"{D}Birmingham")

    birth = BirthState(store=store, uri=f"{D}fred_birth")
    birth.is_start_of(fred)
    birth.is_part_of(london)
    birth.put_in_period("1968")

    death = DeathState(store=store, uri=f"{D}fred_death")
    death.is_finish_of(fred)          # ies_top:isAFinishOf (the declared property)
    death.is_part_of(birmingham)
    death.put_in_period("2034")

    assert ask(store, f"""
        <{D}fred> a ies_core:Person .
        <{D}fred_birth> a ies_core:BirthState ;
            ies_top:isAStartOf <{D}fred> ;
            ies_top:isPartOf <{D}London> ;
            ies_top:isPartOf <{ISO}1968> .
        <{D}London> a ies_core:Location .
        <{ISO}1968> a ies_core:ParticularPeriod .
        <{D}fred_death> a ies_core:DeathState ;
            ies_top:isAFinishOf <{D}fred> ;
            ies_top:isPartOf <{D}Birmingham> ;
            ies_top:isPartOf <{ISO}2034> .
        <{D}Birmingham> a ies_core:Location .
        <{ISO}2034> a ies_core:ParticularPeriod .
    """)


def test_person_lifecycle_helpers():
    """add_lifespan bundles birth+death (date + place each) in one call — the dob/pob/dod/pod
    ergonomics — producing the same shape as the manual boundary pattern."""
    store = RdfLibPlugIn()
    fred = Person(store=store, uri=f"{D}fred")
    london = Location(store=store, uri=f"{D}London")
    birmingham = Location(store=store, uri=f"{D}Birmingham")
    fred.add_lifespan(date_of_birth="1968", place_of_birth=london,
                      date_of_death="2034", place_of_death=birmingham,
                      birth_uri=f"{D}fred_birth", death_uri=f"{D}fred_death")

    assert ask(store, f"""
        <{D}fred_birth> a ies_core:BirthState ;
            ies_top:isAStartOf <{D}fred> ;
            ies_top:isPartOf <{D}London> ;
            ies_top:isPartOf <{ISO}1968> .
        <{D}fred_death> a ies_core:DeathState ;
            ies_top:isAFinishOf <{D}fred> ;
            ies_top:isPartOf <{D}Birmingham> ;
            ies_top:isPartOf <{ISO}2034> .
        <{ISO}1968> a ies_core:ParticularPeriod .
        <{ISO}2034> a ies_core:ParticularPeriod .
    """)


def test_person_constructor_lifecycle():
    """The LivingOrganism-subtree constructor params: Person(date_of_birth=,
    place_of_birth=, date_of_death=, place_of_death=) mint the birth/death boundary states
    at construction (node URIs are auto-minted, hence the ?birth/?death variables)."""
    store = RdfLibPlugIn()
    london = Location(store=store, uri=f"{D}London")
    birmingham = Location(store=store, uri=f"{D}Birmingham")
    Person(store=store, uri=f"{D}fred",
                   date_of_birth="1968", place_of_birth=london,
                   date_of_death="2034", place_of_death=birmingham)

    assert ask(store, f"""
        <{D}fred> a ies_core:Person .
        ?birth a ies_core:BirthState ;
            ies_top:isAStartOf <{D}fred> ;
            ies_top:isPartOf <{D}London> ;
            ies_top:isPartOf <{ISO}1968> .
        ?death a ies_core:DeathState ;
            ies_top:isAFinishOf <{D}fred> ;
            ies_top:isPartOf <{D}Birmingham> ;
            ies_top:isPartOf <{ISO}2034> .
    """)


def test_activity_with_participants():
    """An Activity (Meeting) isPartOf a Location and a ParticularPeriod, with participants
    attending via Attendance participations (isTemporalPartOf the person, isPartOf the meeting)."""
    store = RdfLibPlugIn()
    fred = Person(store=store, uri=f"{D}fred")
    alice = Person(store=store, uri=f"{D}alice")
    office = Location(store=store, uri=f"{D}office_101")

    meeting = Meeting(store=store, uri=f"{D}meeting_001")
    meeting.is_part_of(office)
    meeting.put_in_period("2024-03-02T10:00")
    meeting.add_attendance(fred, participation_uri=f"{D}fred_attendance_of_meeting_001")
    meeting.add_attendance(alice, participation_uri=f"{D}alice_attendance_of_meeting_001")

    assert ask(store, f"""
        <{D}meeting_001> a ies_core:Meeting ;
            ies_top:isPartOf <{D}office_101> ;
            ies_top:isPartOf <{ISO}20240302T1000> .
        <{D}office_101> a ies_core:Location .
        <{ISO}20240302T1000> a ies_core:ParticularPeriod .
        <{D}fred_attendance_of_meeting_001> a ies_core:Attendance ;
            ies_top:isTemporalPartOf <{D}fred> ;
            ies_top:isPartOf <{D}meeting_001> .
        <{D}alice_attendance_of_meeting_001> a ies_core:Attendance ;
            ies_top:isTemporalPartOf <{D}alice> ;
            ies_top:isPartOf <{D}meeting_001> .
    """)


def test_participation_optional_when_participant_is_a_choice():
    """When a participation allows a choice of participant type (Person OR Organization),
    each is independently optional - an Organization's ParticipationInGovernance needs no
    person, and a Person's needs no organization."""
    # organization only
    store = RdfLibPlugIn()
    org = Organization(store=store, uri=f"{D}acme")
    gov = GovernanceActivity(store=store, uri=f"{D}gov_001")
    gov.add_participation_in_governance(organization=org, participation_uri=f"{D}acme_pig")
    assert ask(store, f"""
        <{D}acme_pig> a ies_core:ParticipationInGovernance ;
            ies_top:isPartOf <{D}gov_001> ;
            ies_top:isPartOf <{D}acme> .
    """)
    assert not ask(store, f'<{D}acme_pig> ies_top:isTemporalPartOf ?p')  # no person wired

    # person only
    store = RdfLibPlugIn()
    fred = Person(store=store, uri=f"{D}fred")
    gov = GovernanceActivity(store=store, uri=f"{D}gov_001")
    gov.add_participation_in_governance(person=fred, participation_uri=f"{D}fred_pig")
    assert ask(store, f"""
        <{D}fred_pig> a ies_core:ParticipationInGovernance ;
            ies_top:isPartOf <{D}gov_001> ;
            ies_top:isTemporalPartOf <{D}fred> .
    """)
    # only the host isPartOf is present (no second, organization, isPartOf)
    from tests.rdf_assert import count
    assert count(store, f'<{D}fred_pig> ies_top:isPartOf ?o') == 1


def test_participation_mandatory_when_single_participant():
    """A participation with a single participant type requires it."""
    store = RdfLibPlugIn()
    pic = PartyInCommunication(store=store, uri=f"{D}pic_001")
    with pytest.raises(TypeError):
        pic.add_person_in_communication()  # person is mandatory


def test_participation_on_behalf_of_organisation():
    """The choice edges may BOTH be provided when one entity participates on behalf of
    another: a person attends a Meeting on behalf of an organisation, so the Attendance
    isTemporalPartOf the person and isPartOf the organisation (as well as the meeting)."""
    store = RdfLibPlugIn()
    fred = Person(store=store, uri=f"{D}fred")
    acme = Organization(store=store, uri=f"{D}acme")
    meeting = Meeting(store=store, uri=f"{D}meeting_001")
    meeting.add_attendance(person=fred, organization=acme, participation_uri=f"{D}fred_attendance")

    assert ask(store, f"""
        <{D}fred_attendance> a ies_core:Attendance ;
            ies_top:isPartOf <{D}meeting_001> ;
            ies_top:isTemporalPartOf <{D}fred> ;
            ies_top:isPartOf <{D}acme> .
    """)
