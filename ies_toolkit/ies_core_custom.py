"""Hand-written custom behaviour for ies-core classes, injected into the
generated module (ies_core_generated.py) as mixins via the generator's registry
(TARGETS["core"]["mixins"]).

Like ies_top_custom, this module must NOT import from ies_core_generated at
module load time (the generated module imports these mixins). Mixins use only
self / self._store and string constants, so no such import is needed.
"""
import datetime

from dateutil.rrule import rrulestr

from .constants import ICAL, IES_CORE, IES_TOP, ISO_8601, RDF_TYPE

UTC = datetime.UTC

# RRULE parts the high-level builder understands, in canonical emission order.
# Anything outside this set (BYSETPOS, WKST, BYWEEKNO, ...) uses the raw
# add_ical_representation escape hatch.
_BY_PARTS = ("BYDAY", "BYMONTH", "BYMONTHDAY", "BYHOUR", "BYMINUTE", "BYSECOND")


def _validate_rrule(rrule: str) -> None:
    """Raise ValueError if `rrule` is not a valid RFC 5545 recurrence rule.

    Validation is delegated to dateutil. The date-vs-DATE-TIME nature of UNTIL
    depends on the (here unknown) DTSTART, so a date-form UNTIL flagged only
    because our probe DTSTART is a DATE-TIME is tolerated; every other error
    (bad FREQ, stray properties like DSTART, garbage) is surfaced.
    """
    try:
        rrulestr(rrule, dtstart=datetime.datetime(2000, 1, 1, tzinfo=UTC))
    except ValueError as e:
        msg = str(e)
        if "UNTIL" in msg.upper() and "UTC" in msg.upper():
            return
        raise ValueError(f"invalid RRULE {rrule!r}: {msg}") from e


def _build_rrule(frequency, interval, count, until, by_values) -> str:
    parts = [f"FREQ={frequency.upper()}"]
    if interval is not None and interval != 1:
        parts.append(f"INTERVAL={int(interval)}")
    if count is not None:
        parts.append(f"COUNT={int(count)}")
    if until is not None:
        parts.append("UNTIL=" + until.astimezone(UTC).strftime("%Y%m%dT%H%M%SZ"))
    for name, val in zip(_BY_PARTS, by_values, strict=False):
        if val is not None:
            seq = val if isinstance(val, list | tuple) else [val]
            parts.append(f"{name}=" + ",".join(str(x) for x in seq))
    return ";".join(parts)


class ReifiedBuilderMixin:
    """Primitives shared by the generated relationship/reified builders in
    ies_core_relations_generated.py: mint a reified node (by rdf:type) and wire
    object edges from it."""

    def _mint_node(self, class_uri: str, suffix: str, node_uri: str | None = None) -> str:
        if node_uri is None:
            node_uri = self._store.generate_data_uri(f"{self.uri}_{suffix}_")
        self._store.add_triple(subject=node_uri, predicate=RDF_TYPE, obj=class_uri, is_literal=False)
        return node_uri

    @staticmethod
    def _obj_uri(target) -> str:
        return target.uri if hasattr(target, "uri") else target

    def _wire(self, subject: str, predicate: str, target) -> None:
        self._store.add_triple(subject=subject, predicate=predicate,
                               obj=self._obj_uri(target), is_literal=False)


class ActivityMixin(ReifiedBuilderMixin):
    """Generic participation builder carried by every ies_core:Activity (extend
    mode). A Participation is a State that isPartOf the Activity and
    isTemporalPartOf the participant entity; the typed specialisations
    (add_account_holder, add_creator, ...) are generated per host class."""

    def add_participant(self, participant, role_class: str = f"{IES_CORE}Participation",
                        participant_predicate: str = f"{IES_TOP}isTemporalPartOf",
                        host_predicate: str = f"{IES_TOP}isPartOf", participation_uri: str | None = None) -> str:
        node = self._mint_node(role_class, "participation", participation_uri)
        self._wire(node, host_predicate, self.uri)
        if participant is not None:
            self._wire(node, participant_predicate, participant)
        return node


class LivingOrganismMixin:
    """Lifecycle convenience for ies_core:LivingOrganism (extend mode). add_birth/add_death mint
    the typed BirthState/DeathState - isAStartOf/isAFinishOf the organism, optionally isPartOf a
    place (Location) and the ParticularPeriod for the date. add_lifespan bundles both in one call.
    Dates are ISO-8601 strings; places are Location wrappers or URIs (the IES4 dob/pob/dod/pod)."""

    def add_birth(self, date_of_birth: str | None = None, place_of_birth=None, birth_uri: str | None = None) -> str:
        return self._life_boundary(f"{IES_CORE}BirthState", f"{IES_TOP}isAStartOf", "birth",
                                   date_of_birth, place_of_birth, birth_uri)

    def add_death(self, date_of_death: str | None = None, place_of_death=None, death_uri: str | None = None) -> str:
        return self._life_boundary(f"{IES_CORE}DeathState", f"{IES_TOP}isAFinishOf", "death",
                                   date_of_death, place_of_death, death_uri)

    def add_lifespan(self, date_of_birth: str | None = None, place_of_birth=None,
                     date_of_death: str | None = None, place_of_death=None,
                     birth_uri: str | None = None, death_uri: str | None = None) -> None:
        """One-call birth + death (each with an optional date and place). Only the parts supplied are emitted."""
        if date_of_birth is not None or place_of_birth is not None or birth_uri is not None:
            self.add_birth(date_of_birth=date_of_birth, place_of_birth=place_of_birth, birth_uri=birth_uri)
        if date_of_death is not None or place_of_death is not None or death_uri is not None:
            self.add_death(date_of_death=date_of_death, place_of_death=place_of_death, death_uri=death_uri)

    def _life_boundary(self, cls, predicate, suffix, date, place, uri):
        node = uri or self._store.generate_data_uri(f"{self.uri}_{suffix}_")
        self._store.add_triple(subject=node, predicate=RDF_TYPE, obj=cls, is_literal=False)
        self._store.add_triple(subject=node, predicate=predicate, obj=self.uri, is_literal=False)
        if place is not None:
            self._store.add_triple(subject=node, predicate=f"{IES_TOP}isPartOf",
                                   obj=place.uri if hasattr(place, "uri") else place, is_literal=False)
        if date is not None:
            self._store.add_triple(subject=node, predicate=f"{IES_TOP}isPartOf",
                                   obj=self._particular_period(date), is_literal=False)
        return node


class RecurringTimespanMixin:
    """Builder methods for ies_core:RecurringTimespan, injected in 'extend' mode
    (the generated class keeps its trivial State __init__; these methods are added).

    A RecurringTimespan is an IntermittentTimespan whose recurrence is captured by
    an iCalendar (RFC 5545) representation, and which is bounded by start/end
    ParticularPeriods. See the IES Core "Time (2 of 2)" documentation.

    Two layers:
      * set_recurrence(...)        - high-level; derive a consistent structure from
                                     structured parameters (recommended).
      * add_ical_representation(...) - low-level escape hatch taking a raw RRULE.
    """

    # ----- high-level -------------------------------------------------------

    def set_recurrence(self, frequency, starts, until=None, count=None, interval=1,
                       by_day=None, by_month=None, by_month_day=None,
                       by_hour=None, by_minute=None, by_second=None,
                       instance_ends=None, representation_uri=None):
        """Build a consistent RecurringTimespan from structured parameters.

        The RRULE, ical:dtstart and the bounding ParticularPeriods are all derived
        from `starts`/`until`, so the RRULE UNTIL and the finish ParticularPeriod
        cannot disagree (which the raw API cannot guarantee).

        Args:
            frequency: SECONDLY|MINUTELY|HOURLY|DAILY|WEEKLY|MONTHLY|YEARLY.
            starts: tz-aware datetime - series/first-instance start
                (-> ical:dtstart AND the start ParticularPeriod).
            until: tz-aware datetime - series end
                (-> RRULE UNTIL AND the finish ParticularPeriod). Mutually
                exclusive with count.
            count: int - number of occurrences (alternative to until; yields no
                finish bound).
            interval, by_day, by_month, by_month_day, by_hour, by_minute,
            by_second: RRULE parts (by_* accept a scalar or a list).
            instance_ends: tz-aware datetime - end of the FIRST instance
                (-> ical:dtend). Distinct from until.
            representation_uri: optional explicit URI for the ICalRepresentation.

        Returns the URI of the ICalRepresentation node.
        """
        if until is not None and count is not None:
            raise ValueError("specify only one of until / count")
        if starts.tzinfo is None:
            raise ValueError("starts must be timezone-aware")
        if until is not None and until.tzinfo is None:
            raise ValueError("until must be timezone-aware")

        rrule = _build_rrule(frequency, interval, count, until,
                             (by_day, by_month, by_month_day, by_hour, by_minute, by_second))
        dtstart = starts.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S")
        dtend = (instance_ends.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S")
                 if instance_ends is not None else None)

        rep = self.add_ical_representation(rrule, dtstart=dtstart, dtend=dtend,
                                           representation_uri=representation_uri)
        self.add_bounding_start(starts)
        if until is not None:
            self.add_bounding_finish(until)
        return rep

    # ----- low-level (escape hatch) ----------------------------------------

    def add_ical_representation(self, rrule, dtstart=None, dtend=None, representation_uri=None):
        """Attach a raw RFC 5545 recurrence as an ies_core:ICalRepresentation.

        `rrule` is validated (RFC 5545) then stored verbatim - supply a pure
        recurrence rule (do not embed DTSTART/DTEND; those are the separate
        dtstart/dtend args). The UNTIL value type must match DTSTART per RFC 5545,
        which is the caller's responsibility.

        Args:
            rrule: the RRULE string, e.g.
                "FREQ=WEEKLY;INTERVAL=1;BYDAY=MO;UNTIL=20250930T000000Z".
            dtstart: ISO-8601 string for the start of the first known instance.
            dtend: ISO-8601 string for the end of the first known instance.
            representation_uri: optional explicit URI for the representation node.

        Returns the URI of the ICalRepresentation node.
        """
        _validate_rrule(rrule)
        if not representation_uri:
            representation_uri = self._store.generate_data_uri(f"{self.uri}_ical_")
        # hasICalRepresentation is a sub-property of isRepresentedAs
        self._store.add_triple(subject=self.uri, predicate=f"{IES_CORE}hasICalRepresentation",
                               obj=representation_uri, is_literal=False)
        self._store.add_triple(subject=representation_uri, predicate=RDF_TYPE,
                               obj=f"{IES_CORE}ICalRepresentation", is_literal=False)
        self._store.add_triple(subject=representation_uri, predicate=f"{ICAL}rrule",
                               obj=rrule, is_literal=True)
        if dtstart is not None:
            self._store.add_triple(subject=representation_uri, predicate=f"{ICAL}dtstart",
                                   obj=dtstart, is_literal=True)
        if dtend is not None:
            self._store.add_triple(subject=representation_uri, predicate=f"{ICAL}dtend",
                                   obj=dtend, is_literal=True)
        return representation_uri

    # ----- bounding ParticularPeriods --------------------------------------

    def add_bounding_start(self, start: datetime.datetime):
        """Bound the recurrence with a start ParticularPeriod (period isAStartOf self)."""
        return self._add_particular_period_bound(start, f"{IES_TOP}isAStartOf")

    def add_bounding_finish(self, finish: datetime.datetime):
        """Bound the recurrence with an end ParticularPeriod (period isAFinishOf self).
        Per the IES standard the end ParticularPeriod aligns with the RRULE UNTIL."""
        return self._add_particular_period_bound(finish, f"{IES_TOP}isAFinishOf")

    def _add_particular_period_bound(self, dt: datetime.datetime, predicate: str) -> str:
        if dt.tzinfo is None:
            raise ValueError("bounding datetime must be timezone-aware")
        utc = dt.astimezone(UTC)
        # ParticularPeriod URI: compact ISO-8601 UTC, no punctuation, no trailing Z
        pp_uri = f"{ISO_8601}{utc.strftime('%Y%m%dT%H%M%S')}"
        self._store.add_triple(subject=pp_uri, predicate=RDF_TYPE,
                               obj=f"{IES_CORE}ParticularPeriod", is_literal=False)
        self._store.add_triple(subject=pp_uri, predicate=predicate, obj=self.uri, is_literal=False)
        self._store.add_triple(subject=pp_uri, predicate=f"{IES_CORE}iso8601PeriodRepresentation",
                               obj=utc.strftime("%Y-%m-%dT%H:%M:%S"), is_literal=True)
        return pp_uri
