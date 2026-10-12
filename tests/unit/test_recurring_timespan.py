"""Tests for the hand-written RecurringTimespanMixin (custom-code path).

Builds the worked example "every Monday until 30 Sep 2025" and checks the RDF
matches the IES Core standard: a RecurringTimespan with an ICalRepresentation
carrying ical:rrule/dtstart, bounded by start/end ParticularPeriods linked via
ies_top:isAStartOf / isAFinishOf.
"""
import datetime

from ies_toolkit import ies_core as ic
from ies_toolkit import rdfs
from ies_toolkit.constants import ISO_8601
from ies_toolkit.rdflib_plugin import RdfLibPlugIn
from tests.rdf_assert import ask

UTC = datetime.UTC


def _build():
    store = RdfLibPlugIn()
    rdfs.set_default_store(store)
    rt = ic.RecurringTimespan(uri="http://ex/every_monday")
    rep = rt.add_ical_representation(
        rrule="FREQ=WEEKLY;INTERVAL=1;BYDAY=MO;UNTIL=20250930T000000Z",
        dtstart="2025-01-06T09:00:00",
        representation_uri="http://ex/every_monday_ical",
    )
    rt.add_bounding_start(datetime.datetime(2025, 1, 6, 9, 0, tzinfo=UTC))
    rt.add_bounding_finish(datetime.datetime(2025, 9, 30, 0, 0, tzinfo=UTC))
    return store, rep


def test_ical_representation_structure():
    store, rep = _build()
    assert ask(store, f"""
        <http://ex/every_monday> ies_core:hasICalRepresentation <{rep}> .
        <{rep}> a ies_core:ICalRepresentation ;
                ical:rrule "FREQ=WEEKLY;INTERVAL=1;BYDAY=MO;UNTIL=20250930T000000Z"^^xsd:string ;
                ical:dtstart "2025-01-06T09:00:00"^^xsd:string .
    """)
    assert not ask(store, '?s ical:dtend ?o')  # dtend was not supplied


def test_bounding_particular_periods():
    store, _ = _build()
    start_pp = f"{ISO_8601}20250106T090000"
    finish_pp = f"{ISO_8601}20250930T000000"
    assert ask(store, f"""
        <{start_pp}> a ies_core:ParticularPeriod ;
                     ies_top:isAStartOf <http://ex/every_monday> ;
                     ies_core:iso8601PeriodRepresentation "2025-01-06T09:00:00"^^xsd:string .
    """)
    assert ask(store, f"""
        <{finish_pp}> ies_top:isAFinishOf <http://ex/every_monday> ;
                      ies_core:iso8601PeriodRepresentation "2025-09-30T00:00:00"^^xsd:string .
    """)


def test_bound_requires_timezone_aware():
    store = RdfLibPlugIn()
    rdfs.set_default_store(store)
    rt = ic.RecurringTimespan(uri="http://ex/rt")
    naive = datetime.datetime(2025, 1, 6, 9, 0)  # no tzinfo
    try:
        rt.add_bounding_start(naive)
        raise AssertionError("expected ValueError for naive datetime")
    except ValueError:
        pass


def test_set_recurrence_is_consistent():
    """High-level builder derives the RRULE UNTIL and the finish ParticularPeriod
    from the SAME `until` argument, so they cannot disagree."""
    store = RdfLibPlugIn()
    rdfs.set_default_store(store)
    rt = ic.RecurringTimespan(uri="http://ex/weekly")
    rt.set_recurrence(
        frequency="WEEKLY",
        starts=datetime.datetime(2025, 1, 6, 9, 0, tzinfo=UTC),
        until=datetime.datetime(2025, 9, 30, 0, 0, tzinfo=UTC),
        by_day=["MO"],
        instance_ends=datetime.datetime(2025, 1, 6, 10, 0, tzinfo=UTC),
    )
    # RRULE/dtstart/dtend built from the structured params (interval=1 omitted); dtend != UNTIL
    assert ask(store, """
        ?rep ical:rrule "FREQ=WEEKLY;UNTIL=20250930T000000Z;BYDAY=MO"^^xsd:string ;
             ical:dtstart "2025-01-06T09:00:00"^^xsd:string ;
             ical:dtend "2025-01-06T10:00:00"^^xsd:string .
    """)
    # finish ParticularPeriod derived from the same `until` -> aligned with UNTIL
    assert ask(store, f'<{ISO_8601}20250930T000000> ies_top:isAFinishOf <http://ex/weekly>')
    assert ask(store, f'<{ISO_8601}20250106T090000> ies_top:isAStartOf <http://ex/weekly>')


def test_set_recurrence_until_and_count_mutually_exclusive():
    store = RdfLibPlugIn()
    rdfs.set_default_store(store)
    rt = ic.RecurringTimespan(uri="http://ex/x")
    try:
        rt.set_recurrence(frequency="DAILY",
                          starts=datetime.datetime(2025, 1, 1, tzinfo=UTC),
                          until=datetime.datetime(2025, 2, 1, tzinfo=UTC), count=5)
        raise AssertionError("expected ValueError for until+count")
    except ValueError:
        pass


def test_invalid_rrule_rejected():
    store = RdfLibPlugIn()
    rdfs.set_default_store(store)
    rt = ic.RecurringTimespan(uri="http://ex/y")
    for bad in ("totally garbage", "FREQ=BOGUS", "DSTART:20260401T0800;FREQ=DAILY"):
        try:
            rt.add_ical_representation(bad)
            raise AssertionError(f"expected ValueError for {bad!r}")
        except ValueError:
            pass
