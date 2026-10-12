"""IES wrapper classes generated from ies-top.ttl and ies-core.ttl.

DO NOT EDIT BY HAND. Regenerate with:  python tools/generate_ies.py
Custom methods belong in the hand-written overlay (ies_top.py / ies_top_custom.py), not here.
"""
import datetime

from .constants import IES_TOP
from .rdf_plugin import RDFPlugin

from .rdfs import Rdfs_Class, Rdfs_Resource
from .ies_top_custom import FourPlaceTupleMixin, StateMixin, ThingMixin, ThreePlaceTupleMixin, TupleMixin

__all__ = [
    "Thing",
    "Tuple",
    "FourPlaceTuple",
    "SpatiotemporalExtent",
    "State",
    "TemporallyIntermittentState",
    "Timespan",
    "IntermittentTimespan",
    "TemporallyContinuousState",
    "Period",
    "Set",
    "SetOfSpatiotemporalExtents",
    "SetOfDisjointSpatiotemporalExtents",
    "SetOfOverlappingSpatiotemporalExtents",
    "SetOfSetOfSpatiotemporalExtents",
    "SetOfSetOfStates",
    "SetOfStates",
    "Stuff",
    "ThreePlaceTuple",
    "Universe",
]


class Thing(ThingMixin, Rdfs_Resource):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_TOP}Thing",store,uri)
        self._apply_categories(categories)

class Tuple(TupleMixin, Thing):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_TOP}Tuple",store,uri)
        self._apply_categories(categories)

class FourPlaceTuple(FourPlaceTupleMixin, Tuple):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_TOP}FourPlaceTuple",store,uri)
        self._apply_categories(categories)

class SpatiotemporalExtent(Thing):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_TOP}SpatiotemporalExtent",store,uri)
        self._apply_categories(categories)

class State(StateMixin, SpatiotemporalExtent):
    pass

class TemporallyIntermittentState(State):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_TOP}TemporallyIntermittentState",store,uri,start,finish)
        self._apply_categories(categories)

class Timespan(State):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_TOP}Timespan",store,uri,start,finish)
        self._apply_categories(categories)

class IntermittentTimespan(TemporallyIntermittentState, Timespan):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_TOP}IntermittentTimespan",store,uri,start,finish)
        self._apply_categories(categories)

class TemporallyContinuousState(State):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_TOP}TemporallyContinuousState",store,uri,start,finish)
        self._apply_categories(categories)

class Period(TemporallyContinuousState, Timespan):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_TOP}Period",store,uri,start,finish)
        self._apply_categories(categories)

class Set(Thing, Rdfs_Class):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_TOP}Set",store,uri)
        self._apply_categories(categories)
        self.instance_type = Thing

class SetOfSpatiotemporalExtents(Set):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_TOP}SetOfSpatiotemporalExtents",store,uri)
        self._apply_categories(categories)
        self.instance_type = SpatiotemporalExtent

class SetOfDisjointSpatiotemporalExtents(SetOfSpatiotemporalExtents):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_TOP}SetOfDisjointSpatiotemporalExtents",store,uri)
        self._apply_categories(categories)
        self.instance_type = SpatiotemporalExtent

class SetOfOverlappingSpatiotemporalExtents(SetOfSpatiotemporalExtents):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_TOP}SetOfOverlappingSpatiotemporalExtents",store,uri)
        self._apply_categories(categories)
        self.instance_type = SpatiotemporalExtent

class SetOfSetOfSpatiotemporalExtents(Set):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_TOP}SetOfSetOfSpatiotemporalExtents",store,uri)
        self._apply_categories(categories)
        self.instance_type = SetOfSpatiotemporalExtents

class SetOfSetOfStates(SetOfSetOfSpatiotemporalExtents):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_TOP}SetOfSetOfStates",store,uri)
        self._apply_categories(categories)
        self.instance_type = SetOfStates

class SetOfStates(SetOfSpatiotemporalExtents):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_TOP}SetOfStates",store,uri)
        self._apply_categories(categories)
        self.instance_type = State

class Stuff(SpatiotemporalExtent):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_TOP}Stuff",store,uri)
        self._apply_categories(categories)

class ThreePlaceTuple(ThreePlaceTupleMixin, Tuple):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_TOP}ThreePlaceTuple",store,uri)
        self._apply_categories(categories)

class Universe(Period):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_TOP}Universe",store,uri,None,None)
        self._apply_categories(categories)
