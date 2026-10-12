"""Hand-written custom behaviour for ies-top classes, injected into the
generated module (ies_top_generated.py) as mixins via the generator's registry.

This module must NOT import anything from ies_top_generated at module load time
(the generated module imports these mixins, so a top-level import back would be
circular). Where a generated class is genuinely needed at runtime (minting State
boundary objects) it is imported inside the function body instead.
"""
from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from .constants import IES_CORE, IES_TOP, ISO_8601, RDF_TYPE, RDFS_SUBPROPERTYOF
from .ies_terms import IesTermsMixin

if TYPE_CHECKING:  # for return-type hints only; avoids a runtime top->core import
    from .ies_core import Identifier, Name, Representation


def _py_class_name(rdf_class_name: str) -> str:
    return rdf_class_name.replace(IES_CORE, "").replace(IES_TOP, "")


def _validate_iso8601_period(s: str) -> str:
    """Validate an ISO-8601 period string and return it normalised (space -> T,
    trailing Z stripped). Accepts year (YYYY), year-month (YYYY-MM), date
    (YYYY-MM-DD) or datetime; raises ValueError otherwise. Explicit UTC offsets are
    rejected - use Z (or nothing) for UTC."""
    if not isinstance(s, str) or not s:
        raise ValueError(f"ISO-8601 period must be a non-empty string, got {s!r}")
    norm = s.replace(" ", "T")
    if norm.endswith("Z"):
        norm = norm[:-1]
    parsed = None
    try:
        if "T" in norm:
            parsed = datetime.datetime.fromisoformat(norm)
        elif len(norm) == 4:
            datetime.datetime.strptime(norm, "%Y")
        elif len(norm) == 7:
            datetime.datetime.strptime(norm, "%Y-%m")
        else:
            datetime.date.fromisoformat(norm)
    except ValueError as e:
        raise ValueError(f"invalid ISO-8601 period string: {s!r}") from e
    if parsed is not None and parsed.tzinfo is not None:
        raise ValueError(f"explicit timezone offset not allowed in {s!r} - use Z (or nothing) for UTC")
    return norm


def _new_state(store, uri):
    """Mint a plain State (used for start/finish boundary objects).
    Imported lazily to avoid a module-load circular import."""
    from .ies_top_generated import State
    return State(store=store, uri=uri)


class ThingMixin(IesTermsMixin):
    """Representation / name / identifier builders that every ies_top:Thing
    carries. Injected (extend mode) into the generated Thing, so these are
    real, statically visible methods - no hand-written .pyi stub needed.

    Inherits IesTermsMixin so every IES wrapper (all descend from Thing)
    picks up the non-IES class/predicate warnings, overriding the rdfs.py no-ops.

    These mint ies-core classes, so the core module is imported lazily inside the
    helper (a module-level top->core import would be circular)."""

    def add_name(self, name: str, representation_classes: list[str] | None = None,
                 representation_uri: str | None = None) -> Name:
        return self._add_representation(name, f"{IES_CORE}Name", f"{IES_CORE}hasName",
                                        "name", "Name", representation_classes, representation_uri)

    def add_identifier(self, id: str, representation_classes: list[str] | None = None,
                       representation_uri: str | None = None) -> Identifier:
        return self._add_representation(id, f"{IES_CORE}Identifier", f"{IES_CORE}isIdentifiedBy",
                                        "id", "Identifier", representation_classes, representation_uri)

    def add_representation(self, value: str, representation_classes: list[str] | None = None,
                           representation_uri: str | None = None) -> Representation:
        return self._add_representation(value, f"{IES_CORE}Representation", f"{IES_CORE}isRepresentedAs",
                                        "rep", "Representation", representation_classes, representation_uri)

    def _add_representation(self, value, default_class_uri, predicate, uri_suffix,
                            fallback_name, representation_classes, representation_uri):
        from . import ies_core  # lazy: this mixin loads before ies_core is ready
        if not representation_classes:
            representation_classes = [default_class_uri]
        if not representation_uri:
            representation_uri = self._store.generate_data_uri(f"{self.uri}_{uri_suffix}_")
        cls_name = _py_class_name(representation_classes[0])
        cls = getattr(ies_core, cls_name, None) or getattr(ies_core, fallback_name)
        rep = cls(store=self._store, uri=representation_uri, classes=representation_classes)
        self._store.add_triple(subject=self.uri, predicate=predicate, obj=rep.uri, is_literal=False)
        self._store.add_triple(subject=rep.uri, predicate=f"{IES_CORE}representationValue", obj=value, is_literal=True)
        return rep

    def _apply_categories(self, categories):
        if not categories:
            return
        for cat in categories:
            self._store.add_triple(subject=self._uri, predicate=f"{IES_CORE}category", obj=cat, is_literal=False)


class StateMixin:
    """The ies:State temporal engine: start/finish boundary handling and the
    mereological / temporal relationship methods. Injected in 'replace' mode,
    so this provides State's whole constructor and method set.

    The start/finish logic lives in _state_init (which subclasses call with their
    own class URI); __init__ simply delegates with ies:State as the fallback class.
    """

    def __init__(self, store=None, uri=None, classes: list[str] | None = None,
                 start: datetime.datetime | None = None, finish: datetime.datetime | None = None,
                 categories: list[str] | None = None):
        self._state_init(classes, f"{IES_TOP}State", store, uri, start, finish)
        self._apply_categories(categories)

    def _state_init(self, classes, fallback_class, store, uri, start, finish):
        if classes is None:
            classes = [fallback_class]
        self._cls_init(classes, fallback_class, store, uri)
        self._start_state = None
        self._finish_state = None
        if start is not None:
            self._start_state = self._boundary_from_datetime(start, f"{IES_TOP}isAStartOf", "_start_")
        if finish is not None:
            self._finish_state = self._boundary_from_datetime(finish, f"{IES_TOP}isAFinishOf", "_finish_")

    def _boundary_from_datetime(self, dt, predicate, suffix):
        """Mint a bounding State from a tz-aware datetime: it `predicate`s this state and
        isPartOf the ParticularPeriod for that instant. Returns the bounding State wrapper."""
        if dt.tzinfo is None:
            raise ValueError("datetime must be timezone-aware")
        iso = dt.astimezone(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S")
        period = self._particular_period(iso)
        boundary = _new_state(self._store, self._store.generate_data_uri(uri_root=self.uri + suffix))
        self._store.add_triple(subject=boundary.uri, predicate=predicate, obj=self.uri, is_literal=False)
        self._store.add_triple(subject=boundary.uri, predicate=f"{IES_TOP}isPartOf", obj=period, is_literal=False)
        return boundary

    @property
    def start_state(self):
        return self._start_state

    @property
    def finish_state(self):
        return self._finish_state

    def is_part_of(self, whole):
        self._store.add_triple(subject=self._uri, predicate=f"{IES_TOP}isPartOf", obj=whole.uri, is_literal=False)

    def has_part(self, part):
        self._store.add_triple(subject=part.uri, predicate=f"{IES_TOP}isPartOf", obj=self._uri, is_literal=False)

    def is_temporal_part_of(self, whole):
        self._store.add_triple(subject=self._uri, predicate=f"{IES_TOP}isTemporalPartOf",
                               obj=whole.uri, is_literal=False)

    def has_temporal_part(self, part):
        self._store.add_triple(subject=part.uri, predicate=f"{IES_TOP}isTemporalPartOf",
                               obj=self._uri, is_literal=False)

    def is_start_of(self, whole):
        self._store.add_triple(subject=self._uri, predicate=f"{IES_TOP}isAStartOf", obj=whole.uri, is_literal=False)

    def has_start_state(self, start_state):
        self._store.add_triple(subject=start_state.uri, predicate=f"{IES_TOP}isAStartOf",
                               obj=self._uri, is_literal=False)

    def is_finish_of(self, whole):
        self._store.add_triple(subject=self._uri, predicate=f"{IES_TOP}isAFinishOf", obj=whole.uri, is_literal=False)

    def has_finish_state(self, finish_state):
        self._store.add_triple(subject=finish_state.uri, predicate=f"{IES_TOP}isAFinishOf",
                               obj=self._uri, is_literal=False)

    def _particular_period(self, iso8601: str) -> str:
        """Mint (idempotently) the ies_core:ParticularPeriod for an ISO-8601 string.
        URI per the ParticularPeriod convention: UTC, no punctuation, no trailing Z -
        the string's own granularity is preserved, e.g. "1932-05-01" -> .../19320501
        and "1932-05-01T10:00" -> .../19320501T1000. iso8601PeriodRepresentation is the
        punctuated literal. Deterministic, so periods de-duplicate across their use."""
        iso8601 = _validate_iso8601_period(iso8601)
        period = ISO_8601 + iso8601.replace("-", "").replace(":", "")
        self._store.add_triple(subject=period, predicate=RDF_TYPE, obj=f"{IES_CORE}ParticularPeriod", is_literal=False)
        self._store.add_triple(subject=period, predicate=f"{IES_CORE}iso8601PeriodRepresentation",
                               obj=iso8601, is_literal=True)
        return period

    def put_in_period(self, iso8601: str) -> str:
        """Assert this state's lifetime falls entirely within a ParticularPeriod: self isPartOf period."""
        period = self._particular_period(iso8601)
        self._store.add_triple(subject=self._uri, predicate=f"{IES_TOP}isPartOf", obj=period, is_literal=False)
        return period

    def _bounding_state(self, iso8601: str, predicate: str, boundary_uri: str) -> str:
        """Mint a bounding State that `predicate`s this state and isPartOf the period."""
        period = self._particular_period(iso8601)
        self._store.add_triple(subject=boundary_uri, predicate=RDF_TYPE, obj=f"{IES_TOP}State", is_literal=False)
        self._store.add_triple(subject=boundary_uri, predicate=predicate, obj=self._uri, is_literal=False)
        self._store.add_triple(subject=boundary_uri, predicate=f"{IES_TOP}isPartOf", obj=period, is_literal=False)
        return boundary_uri

    def starts_in(self, iso8601: str, boundary_uri: str | None = None) -> str:
        """Bound the start: a State that isAStartOf this state and isPartOf the period."""
        return self._bounding_state(iso8601, f"{IES_TOP}isAStartOf", boundary_uri or f"{self._uri}_start")

    def finishes_in(self, iso8601: str, boundary_uri: str | None = None) -> str:
        """Bound the finish: a State that isAFinishOf this state and isPartOf the period."""
        return self._bounding_state(iso8601, f"{IES_TOP}isAFinishOf", boundary_uri or f"{self._uri}_finish")


class TupleMixin:
    """ies:Tuple place-assignment. Injected in 'extend' mode (the generated
    class keeps its trivial __init__; this only adds add_place)."""

    def add_place(self, tuple_index: int, related_item):
        if tuple_index < 1:
            raise ValueError(f"tuple index must be >= 1, got {tuple_index}")
        tp_uri = f"{IES_TOP}tuplePlace_{tuple_index}"
        if tuple_index > 4:
            self._store.add_triple(subject=tp_uri, predicate=RDFS_SUBPROPERTYOF,
                                   obj=f"{IES_TOP}tuplePlace", is_literal=False)
        self._store.add_triple(subject=self.uri, predicate=tp_uri, obj=related_item.uri, is_literal=False)


class ThreePlaceTupleMixin:
    """Bounds add_place to 1-3, then defers to TupleMixin via the MRO."""

    def add_place(self, tuple_index: int, related_item):
        if tuple_index > 3:
            raise ValueError(f"ThreePlaceTuple only supports tuple indices 1-3, got {tuple_index}")
        super().add_place(tuple_index=tuple_index, related_item=related_item)


class FourPlaceTupleMixin:
    """Bounds add_place to 1-4, then defers to TupleMixin via the MRO."""

    def add_place(self, tuple_index: int, related_item):
        if tuple_index > 4:
            raise ValueError(f"FourPlaceTuple only supports tuple indices 1-4, got {tuple_index}")
        super().add_place(tuple_index=tuple_index, related_item=related_item)
