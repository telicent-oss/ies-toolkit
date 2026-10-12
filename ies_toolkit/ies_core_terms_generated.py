"""Declared IesCore terms: a typed namespace + a URI registry.

DO NOT EDIT BY HAND. Regenerate with:  python tools/generate_ies.py --target core
"""
from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace
from .constants import IES_CORE


class IesCore(DefinedNamespace):
    _NS = Namespace(IES_CORE)
    _fail = True

    Access: URIRef
    Accessed: URIRef
    Accessor: URIRef
    Account: URIRef
    AccountAdminActivity: URIRef
    AccountClosure: URIRef
    AccountDetails: URIRef
    AccountHolder: URIRef
    AccountInCommunication: URIRef
    AccountOpening: URIRef
    AccountProvider: URIRef
    AccountUpdate: URIRef
    ActiveParticipation: URIRef
    Activity: URIRef
    Actor: URIRef
    ArbitraryPeriod: URIRef
    Arrival: URIRef
    Artefact: URIRef
    Assessment: URIRef
    Assessor: URIRef
    Attendance: URIRef
    BirthState: URIRef
    Capability: URIRef
    CharacterString: URIRef
    Characteristic: URIRef
    CoLocation: URIRef
    Color: URIRef
    Communication: URIRef
    ContinuousAccess: URIRef
    Contract: URIRef
    Country: URIRef
    Create: URIRef
    Created: URIRef
    Creator: URIRef
    DeathState: URIRef
    Departure: URIRef
    Destroy: URIRef
    Destroyed: URIRef
    Destroyer: URIRef
    Disposition: URIRef
    DocumentFormat: URIRef
    Easting: URIRef
    EndToEndActivity: URIRef
    EndToEndTransaction: URIRef
    Entitlement: URIRef
    Ethnicity: URIRef
    Exchange: URIRef
    ExchangeMovement: URIRef
    FiniteSetOfSpatiotemporalExtents: URIRef
    FusionOfIntegralParts: URIRef
    Gender: URIRef
    GeoIdentity: URIRef
    GeoPoint: URIRef
    GovernanceActivity: URIRef
    HumanMadeSystem: URIRef
    ICalRepresentation: URIRef
    ISO3166_1Alpha_3: URIRef
    Identifier: URIRef
    IndividualDocument: URIRef
    IndividualTicket: URIRef
    InformationProcessingSystem: URIRef
    InformationProcessingSystemInCommunication: URIRef
    Installed: URIRef
    IntermittentAccess: URIRef
    Journey: URIRef
    Language: URIRef
    LanguageProficiency: URIRef
    Latitude: URIRef
    LegalOwner: URIRef
    LegalOwnership: URIRef
    LifecycleActivity: URIRef
    LivingOrganism: URIRef
    LivingSystem: URIRef
    Location: URIRef
    Longitude: URIRef
    Measure: URIRef
    Meeting: URIRef
    Modifier: URIRef
    Modify: URIRef
    Movement: URIRef
    Name: URIRef
    NamingScheme: URIRef
    Nation: URIRef
    Northing: URIRef
    Observation: URIRef
    Observed: URIRef
    Observer: URIRef
    Organization: URIRef
    OwnedLegally: URIRef
    Participation: URIRef
    ParticipationInGovernance: URIRef
    ParticularPeriod: URIRef
    PartyInCommunication: URIRef
    Person: URIRef
    PersonInCommunication: URIRef
    PersonName: URIRef
    PersonOrOrganization: URIRef
    Provision: URIRef
    Recognizer: URIRef
    RecurringTimespan: URIRef
    RegionalConstituency: URIRef
    ReplaceableLifespan: URIRef
    Representation: URIRef
    RepresentationScheme: URIRef
    RightGrantingArtefact: URIRef
    RightHolder: URIRef
    RightTo: URIRef
    SetOfCharacterStrings: URIRef
    SetOfIndividualDocuments: URIRef
    SetOfInformationProcessingSystems: URIRef
    SetOfLivingOrganisms: URIRef
    SetOfNames: URIRef
    SetOfPersons: URIRef
    SetOfRepresentations: URIRef
    SetOfSetOfSigns: URIRef
    SetOfSigns: URIRef
    SetOfStatesWithParticularDuration: URIRef
    SetOfTimeBoundedStates: URIRef
    SetOfUniverseMates: URIRef
    Sex: URIRef
    Sign: URIRef
    SimilarUniverseMates: URIRef
    Skill: URIRef
    System: URIRef
    Tendency: URIRef
    Ticket: URIRef
    Title: URIRef
    TransactionActivity: URIRef
    TransactionParticipant: URIRef
    Vehicle: URIRef
    VersionNumber: URIRef
    VersionOfDocument: URIRef
    WorkOfDocumentation: URIRef
    aCopyOf: URIRef
    allHaveCharacteristic: URIRef
    allHaveDisposition: URIRef
    assessed: URIRef
    attribute: URIRef
    category: URIRef
    documentedBy: URIRef
    duration: URIRef
    endBoundOfSet: URIRef
    finiteMembershipCount: URIRef
    format: URIRef
    formatOfIndividualDocument: URIRef
    hasAssociatedRepresentation: URIRef
    hasCharacteristic: URIRef
    hasEthnicity: URIRef
    hasGeoSparqlRepresentation: URIRef
    hasICalRepresentation: URIRef
    hasIdentifiedGender: URIRef
    hasName: URIRef
    hasQuantity: URIRef
    hasSex: URIRef
    hasSkill: URIRef
    hasTheme: URIRef
    inLanguage: URIRef
    inRepresentation: URIRef
    isDisposedTo: URIRef
    isIdentifiedBy: URIRef
    isRepresentedAs: URIRef
    iso8601DurationRepresentation: URIRef
    iso8601PeriodRepresentation: URIRef
    published: URIRef
    representationValue: URIRef
    schemeMasteredIn: URIRef
    schemeOwner: URIRef
    similarState: URIRef
    spokenLanguage: URIRef
    startBoundOfSet: URIRef
    versionOf: URIRef


IES_CLASS_URIS = frozenset({
    "http://purl.org/ies/core/v0/ont/Access",
    "http://purl.org/ies/core/v0/ont/Accessed",
    "http://purl.org/ies/core/v0/ont/Accessor",
    "http://purl.org/ies/core/v0/ont/Account",
    "http://purl.org/ies/core/v0/ont/AccountAdminActivity",
    "http://purl.org/ies/core/v0/ont/AccountClosure",
    "http://purl.org/ies/core/v0/ont/AccountDetails",
    "http://purl.org/ies/core/v0/ont/AccountHolder",
    "http://purl.org/ies/core/v0/ont/AccountInCommunication",
    "http://purl.org/ies/core/v0/ont/AccountOpening",
    "http://purl.org/ies/core/v0/ont/AccountProvider",
    "http://purl.org/ies/core/v0/ont/AccountUpdate",
    "http://purl.org/ies/core/v0/ont/ActiveParticipation",
    "http://purl.org/ies/core/v0/ont/Activity",
    "http://purl.org/ies/core/v0/ont/Actor",
    "http://purl.org/ies/core/v0/ont/ArbitraryPeriod",
    "http://purl.org/ies/core/v0/ont/Arrival",
    "http://purl.org/ies/core/v0/ont/Artefact",
    "http://purl.org/ies/core/v0/ont/Assessment",
    "http://purl.org/ies/core/v0/ont/Assessor",
    "http://purl.org/ies/core/v0/ont/Attendance",
    "http://purl.org/ies/core/v0/ont/BirthState",
    "http://purl.org/ies/core/v0/ont/Capability",
    "http://purl.org/ies/core/v0/ont/CharacterString",
    "http://purl.org/ies/core/v0/ont/Characteristic",
    "http://purl.org/ies/core/v0/ont/CoLocation",
    "http://purl.org/ies/core/v0/ont/Color",
    "http://purl.org/ies/core/v0/ont/Communication",
    "http://purl.org/ies/core/v0/ont/ContinuousAccess",
    "http://purl.org/ies/core/v0/ont/Contract",
    "http://purl.org/ies/core/v0/ont/Country",
    "http://purl.org/ies/core/v0/ont/Create",
    "http://purl.org/ies/core/v0/ont/Created",
    "http://purl.org/ies/core/v0/ont/Creator",
    "http://purl.org/ies/core/v0/ont/DeathState",
    "http://purl.org/ies/core/v0/ont/Departure",
    "http://purl.org/ies/core/v0/ont/Destroy",
    "http://purl.org/ies/core/v0/ont/Destroyed",
    "http://purl.org/ies/core/v0/ont/Destroyer",
    "http://purl.org/ies/core/v0/ont/Disposition",
    "http://purl.org/ies/core/v0/ont/DocumentFormat",
    "http://purl.org/ies/core/v0/ont/Easting",
    "http://purl.org/ies/core/v0/ont/EndToEndActivity",
    "http://purl.org/ies/core/v0/ont/EndToEndTransaction",
    "http://purl.org/ies/core/v0/ont/Entitlement",
    "http://purl.org/ies/core/v0/ont/Ethnicity",
    "http://purl.org/ies/core/v0/ont/Exchange",
    "http://purl.org/ies/core/v0/ont/ExchangeMovement",
    "http://purl.org/ies/core/v0/ont/FiniteSetOfSpatiotemporalExtents",
    "http://purl.org/ies/core/v0/ont/FusionOfIntegralParts",
    "http://purl.org/ies/core/v0/ont/Gender",
    "http://purl.org/ies/core/v0/ont/GeoIdentity",
    "http://purl.org/ies/core/v0/ont/GeoPoint",
    "http://purl.org/ies/core/v0/ont/GovernanceActivity",
    "http://purl.org/ies/core/v0/ont/HumanMadeSystem",
    "http://purl.org/ies/core/v0/ont/ICalRepresentation",
    "http://purl.org/ies/core/v0/ont/ISO3166_1Alpha_3",
    "http://purl.org/ies/core/v0/ont/Identifier",
    "http://purl.org/ies/core/v0/ont/IndividualDocument",
    "http://purl.org/ies/core/v0/ont/IndividualTicket",
    "http://purl.org/ies/core/v0/ont/InformationProcessingSystem",
    "http://purl.org/ies/core/v0/ont/InformationProcessingSystemInCommunication",
    "http://purl.org/ies/core/v0/ont/Installed",
    "http://purl.org/ies/core/v0/ont/IntermittentAccess",
    "http://purl.org/ies/core/v0/ont/Journey",
    "http://purl.org/ies/core/v0/ont/Language",
    "http://purl.org/ies/core/v0/ont/LanguageProficiency",
    "http://purl.org/ies/core/v0/ont/Latitude",
    "http://purl.org/ies/core/v0/ont/LegalOwner",
    "http://purl.org/ies/core/v0/ont/LegalOwnership",
    "http://purl.org/ies/core/v0/ont/LifecycleActivity",
    "http://purl.org/ies/core/v0/ont/LivingOrganism",
    "http://purl.org/ies/core/v0/ont/LivingSystem",
    "http://purl.org/ies/core/v0/ont/Location",
    "http://purl.org/ies/core/v0/ont/Longitude",
    "http://purl.org/ies/core/v0/ont/Measure",
    "http://purl.org/ies/core/v0/ont/Meeting",
    "http://purl.org/ies/core/v0/ont/Modifier",
    "http://purl.org/ies/core/v0/ont/Modify",
    "http://purl.org/ies/core/v0/ont/Movement",
    "http://purl.org/ies/core/v0/ont/Name",
    "http://purl.org/ies/core/v0/ont/NamingScheme",
    "http://purl.org/ies/core/v0/ont/Nation",
    "http://purl.org/ies/core/v0/ont/Northing",
    "http://purl.org/ies/core/v0/ont/Observation",
    "http://purl.org/ies/core/v0/ont/Observed",
    "http://purl.org/ies/core/v0/ont/Observer",
    "http://purl.org/ies/core/v0/ont/Organization",
    "http://purl.org/ies/core/v0/ont/OwnedLegally",
    "http://purl.org/ies/core/v0/ont/Participation",
    "http://purl.org/ies/core/v0/ont/ParticipationInGovernance",
    "http://purl.org/ies/core/v0/ont/ParticularPeriod",
    "http://purl.org/ies/core/v0/ont/PartyInCommunication",
    "http://purl.org/ies/core/v0/ont/Person",
    "http://purl.org/ies/core/v0/ont/PersonInCommunication",
    "http://purl.org/ies/core/v0/ont/PersonName",
    "http://purl.org/ies/core/v0/ont/PersonOrOrganization",
    "http://purl.org/ies/core/v0/ont/Provision",
    "http://purl.org/ies/core/v0/ont/Recognizer",
    "http://purl.org/ies/core/v0/ont/RecurringTimespan",
    "http://purl.org/ies/core/v0/ont/RegionalConstituency",
    "http://purl.org/ies/core/v0/ont/ReplaceableLifespan",
    "http://purl.org/ies/core/v0/ont/Representation",
    "http://purl.org/ies/core/v0/ont/RepresentationScheme",
    "http://purl.org/ies/core/v0/ont/RightGrantingArtefact",
    "http://purl.org/ies/core/v0/ont/RightHolder",
    "http://purl.org/ies/core/v0/ont/RightTo",
    "http://purl.org/ies/core/v0/ont/SetOfCharacterStrings",
    "http://purl.org/ies/core/v0/ont/SetOfIndividualDocuments",
    "http://purl.org/ies/core/v0/ont/SetOfInformationProcessingSystems",
    "http://purl.org/ies/core/v0/ont/SetOfLivingOrganisms",
    "http://purl.org/ies/core/v0/ont/SetOfNames",
    "http://purl.org/ies/core/v0/ont/SetOfPersons",
    "http://purl.org/ies/core/v0/ont/SetOfRepresentations",
    "http://purl.org/ies/core/v0/ont/SetOfSetOfSigns",
    "http://purl.org/ies/core/v0/ont/SetOfSigns",
    "http://purl.org/ies/core/v0/ont/SetOfStatesWithParticularDuration",
    "http://purl.org/ies/core/v0/ont/SetOfTimeBoundedStates",
    "http://purl.org/ies/core/v0/ont/SetOfUniverseMates",
    "http://purl.org/ies/core/v0/ont/Sex",
    "http://purl.org/ies/core/v0/ont/Sign",
    "http://purl.org/ies/core/v0/ont/SimilarUniverseMates",
    "http://purl.org/ies/core/v0/ont/Skill",
    "http://purl.org/ies/core/v0/ont/System",
    "http://purl.org/ies/core/v0/ont/Tendency",
    "http://purl.org/ies/core/v0/ont/Ticket",
    "http://purl.org/ies/core/v0/ont/Title",
    "http://purl.org/ies/core/v0/ont/TransactionActivity",
    "http://purl.org/ies/core/v0/ont/TransactionParticipant",
    "http://purl.org/ies/core/v0/ont/Vehicle",
    "http://purl.org/ies/core/v0/ont/VersionNumber",
    "http://purl.org/ies/core/v0/ont/VersionOfDocument",
    "http://purl.org/ies/core/v0/ont/WorkOfDocumentation",
})

IES_PROPERTY_URIS = frozenset({
    "http://purl.org/ies/core/v0/ont/aCopyOf",
    "http://purl.org/ies/core/v0/ont/allHaveCharacteristic",
    "http://purl.org/ies/core/v0/ont/allHaveDisposition",
    "http://purl.org/ies/core/v0/ont/assessed",
    "http://purl.org/ies/core/v0/ont/attribute",
    "http://purl.org/ies/core/v0/ont/category",
    "http://purl.org/ies/core/v0/ont/documentedBy",
    "http://purl.org/ies/core/v0/ont/duration",
    "http://purl.org/ies/core/v0/ont/endBoundOfSet",
    "http://purl.org/ies/core/v0/ont/finiteMembershipCount",
    "http://purl.org/ies/core/v0/ont/format",
    "http://purl.org/ies/core/v0/ont/formatOfIndividualDocument",
    "http://purl.org/ies/core/v0/ont/hasAssociatedRepresentation",
    "http://purl.org/ies/core/v0/ont/hasCharacteristic",
    "http://purl.org/ies/core/v0/ont/hasEthnicity",
    "http://purl.org/ies/core/v0/ont/hasGeoSparqlRepresentation",
    "http://purl.org/ies/core/v0/ont/hasICalRepresentation",
    "http://purl.org/ies/core/v0/ont/hasIdentifiedGender",
    "http://purl.org/ies/core/v0/ont/hasName",
    "http://purl.org/ies/core/v0/ont/hasQuantity",
    "http://purl.org/ies/core/v0/ont/hasSex",
    "http://purl.org/ies/core/v0/ont/hasSkill",
    "http://purl.org/ies/core/v0/ont/hasTheme",
    "http://purl.org/ies/core/v0/ont/inLanguage",
    "http://purl.org/ies/core/v0/ont/inRepresentation",
    "http://purl.org/ies/core/v0/ont/isDisposedTo",
    "http://purl.org/ies/core/v0/ont/isIdentifiedBy",
    "http://purl.org/ies/core/v0/ont/isRepresentedAs",
    "http://purl.org/ies/core/v0/ont/iso8601DurationRepresentation",
    "http://purl.org/ies/core/v0/ont/iso8601PeriodRepresentation",
    "http://purl.org/ies/core/v0/ont/published",
    "http://purl.org/ies/core/v0/ont/representationValue",
    "http://purl.org/ies/core/v0/ont/schemeMasteredIn",
    "http://purl.org/ies/core/v0/ont/schemeOwner",
    "http://purl.org/ies/core/v0/ont/similarState",
    "http://purl.org/ies/core/v0/ont/spokenLanguage",
    "http://purl.org/ies/core/v0/ont/startBoundOfSet",
    "http://purl.org/ies/core/v0/ont/versionOf",
})
