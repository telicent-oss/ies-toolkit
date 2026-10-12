"""Declared IesTop terms: a typed namespace + a URI registry.

DO NOT EDIT BY HAND. Regenerate with:  python tools/generate_ies.py --target top
"""
from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace
from .constants import IES_TOP


class IesTop(DefinedNamespace):
    _NS = Namespace(IES_TOP)
    _fail = True

    FourPlaceTuple: URIRef
    IntermittentTimespan: URIRef
    Period: URIRef
    Set: URIRef
    SetOfDisjointSpatiotemporalExtents: URIRef
    SetOfOverlappingSpatiotemporalExtents: URIRef
    SetOfSetOfSpatiotemporalExtents: URIRef
    SetOfSetOfStates: URIRef
    SetOfSpatiotemporalExtents: URIRef
    SetOfStates: URIRef
    SpatiotemporalExtent: URIRef
    State: URIRef
    Stuff: URIRef
    TemporallyContinuousState: URIRef
    TemporallyIntermittentState: URIRef
    Thing: URIRef
    ThreePlaceTuple: URIRef
    Timespan: URIRef
    Tuple: URIRef
    Universe: URIRef
    couple: URIRef
    entirelyAfter: URIRef
    groundingRelation: URIRef
    intersectionOf: URIRef
    isAFinishOf: URIRef
    isAStartOf: URIRef
    isImproperPartOf: URIRef
    isPartOf: URIRef
    isTemporalPartOf: URIRef
    partWhole: URIRef
    powertype: URIRef
    relationship: URIRef
    relationshipBetweenStates: URIRef
    relationshipBetweenUniverseMates: URIRef
    subSuperRelation: URIRef
    tuplePlace: URIRef
    tuplePlace_1: URIRef
    tuplePlace_2: URIRef
    tuplePlace_3: URIRef
    tuplePlace_4: URIRef


IES_CLASS_URIS = frozenset({
    "http://purl.org/ies/top/v0/ont/FourPlaceTuple",
    "http://purl.org/ies/top/v0/ont/IntermittentTimespan",
    "http://purl.org/ies/top/v0/ont/Period",
    "http://purl.org/ies/top/v0/ont/Set",
    "http://purl.org/ies/top/v0/ont/SetOfDisjointSpatiotemporalExtents",
    "http://purl.org/ies/top/v0/ont/SetOfOverlappingSpatiotemporalExtents",
    "http://purl.org/ies/top/v0/ont/SetOfSetOfSpatiotemporalExtents",
    "http://purl.org/ies/top/v0/ont/SetOfSetOfStates",
    "http://purl.org/ies/top/v0/ont/SetOfSpatiotemporalExtents",
    "http://purl.org/ies/top/v0/ont/SetOfStates",
    "http://purl.org/ies/top/v0/ont/SpatiotemporalExtent",
    "http://purl.org/ies/top/v0/ont/State",
    "http://purl.org/ies/top/v0/ont/Stuff",
    "http://purl.org/ies/top/v0/ont/TemporallyContinuousState",
    "http://purl.org/ies/top/v0/ont/TemporallyIntermittentState",
    "http://purl.org/ies/top/v0/ont/Thing",
    "http://purl.org/ies/top/v0/ont/ThreePlaceTuple",
    "http://purl.org/ies/top/v0/ont/Timespan",
    "http://purl.org/ies/top/v0/ont/Tuple",
    "http://purl.org/ies/top/v0/ont/Universe",
})

IES_PROPERTY_URIS = frozenset({
    "http://purl.org/ies/top/v0/ont/couple",
    "http://purl.org/ies/top/v0/ont/entirelyAfter",
    "http://purl.org/ies/top/v0/ont/groundingRelation",
    "http://purl.org/ies/top/v0/ont/intersectionOf",
    "http://purl.org/ies/top/v0/ont/isAFinishOf",
    "http://purl.org/ies/top/v0/ont/isAStartOf",
    "http://purl.org/ies/top/v0/ont/isImproperPartOf",
    "http://purl.org/ies/top/v0/ont/isPartOf",
    "http://purl.org/ies/top/v0/ont/isTemporalPartOf",
    "http://purl.org/ies/top/v0/ont/partWhole",
    "http://purl.org/ies/top/v0/ont/powertype",
    "http://purl.org/ies/top/v0/ont/relationship",
    "http://purl.org/ies/top/v0/ont/relationshipBetweenStates",
    "http://purl.org/ies/top/v0/ont/relationshipBetweenUniverseMates",
    "http://purl.org/ies/top/v0/ont/subSuperRelation",
    "http://purl.org/ies/top/v0/ont/tuplePlace",
    "http://purl.org/ies/top/v0/ont/tuplePlace_1",
    "http://purl.org/ies/top/v0/ont/tuplePlace_2",
    "http://purl.org/ies/top/v0/ont/tuplePlace_3",
    "http://purl.org/ies/top/v0/ont/tuplePlace_4",
})
