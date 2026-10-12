"""IES wrapper classes generated from ies-top.ttl and ies-core.ttl.

DO NOT EDIT BY HAND. Regenerate with:  python tools/generate_ies.py
Custom methods belong in the hand-written overlay (ies_core.py), not here.
"""
import datetime

from .constants import IES_CORE
from .rdf_plugin import RDFPlugin

from .ies_top import IntermittentTimespan, Period, SetOfSetOfStates, SetOfSpatiotemporalExtents, SetOfStates, State, TemporallyContinuousState, TemporallyIntermittentState
from .ies_core_custom import ActivityMixin, LivingOrganismMixin, RecurringTimespanMixin
from .ies_core_relations_generated import Access_Relations, Account_Relations, Assessment_Relations, Country_Relations, Create_Relations, Destroy_Relations, Entitlement_Relations, GeoPoint_Relations, GovernanceActivity_Relations, HumanMadeSystem_Relations, IndividualDocument_Relations, IndividualTicket_Relations, LegalOwnership_Relations, LivingOrganism_Relations, Meeting_Relations, Modify_Relations, Movement_Relations, Nation_Relations, Observation_Relations, PartyInCommunication_Relations, PersonName_Relations, TransactionActivity_Relations, VersionOfDocument_Relations, WorkOfDocumentation_Relations

__all__ = [
    "FusionOfIntegralParts",
    "Activity",
    "Access",
    "Participation",
    "Accessed",
    "Accessor",
    "EndToEndActivity",
    "Account",
    "AccountAdminActivity",
    "AccountClosure",
    "SetOfSigns",
    "Representation",
    "AccountDetails",
    "AccountHolder",
    "AccountInCommunication",
    "AccountOpening",
    "AccountProvider",
    "AccountUpdate",
    "ActiveParticipation",
    "Actor",
    "ArbitraryPeriod",
    "Arrival",
    "Artefact",
    "Assessment",
    "Assessor",
    "Attendance",
    "LivingOrganism",
    "BirthState",
    "Disposition",
    "Capability",
    "Sign",
    "CharacterString",
    "Characteristic",
    "CoLocation",
    "Color",
    "Communication",
    "ContinuousAccess",
    "Contract",
    "Location",
    "Country",
    "LifecycleActivity",
    "Create",
    "Created",
    "Creator",
    "DeathState",
    "Departure",
    "Destroy",
    "Destroyed",
    "Destroyer",
    "SetOfIndividualDocuments",
    "DocumentFormat",
    "SetOfCharacterStrings",
    "Name",
    "Identifier",
    "GeoIdentity",
    "Easting",
    "EndToEndTransaction",
    "Entitlement",
    "SetOfLivingOrganisms",
    "SetOfPersons",
    "Ethnicity",
    "TransactionActivity",
    "Exchange",
    "ExchangeMovement",
    "FiniteSetOfSpatiotemporalExtents",
    "Gender",
    "GeoPoint",
    "GovernanceActivity",
    "System",
    "HumanMadeSystem",
    "ICalRepresentation",
    "ISO3166_1Alpha_3",
    "IndividualDocument",
    "IndividualTicket",
    "InformationProcessingSystem",
    "InformationProcessingSystemInCommunication",
    "Installed",
    "IntermittentAccess",
    "Movement",
    "Journey",
    "SetOfSetOfSigns",
    "SetOfRepresentations",
    "Language",
    "Skill",
    "LanguageProficiency",
    "Latitude",
    "RightHolder",
    "LegalOwner",
    "LegalOwnership",
    "LivingSystem",
    "Longitude",
    "Measure",
    "Meeting",
    "Modifier",
    "Modify",
    "RepresentationScheme",
    "SetOfNames",
    "NamingScheme",
    "PersonOrOrganization",
    "Organization",
    "RegionalConstituency",
    "Nation",
    "Northing",
    "Observation",
    "Observed",
    "Observer",
    "RightTo",
    "OwnedLegally",
    "ParticipationInGovernance",
    "ParticularPeriod",
    "PartyInCommunication",
    "Person",
    "PersonInCommunication",
    "PersonName",
    "Provision",
    "Recognizer",
    "RecurringTimespan",
    "ReplaceableLifespan",
    "RightGrantingArtefact",
    "SetOfInformationProcessingSystems",
    "SetOfStatesWithParticularDuration",
    "SetOfTimeBoundedStates",
    "SetOfUniverseMates",
    "Sex",
    "SimilarUniverseMates",
    "Tendency",
    "WorkOfDocumentation",
    "Ticket",
    "Title",
    "TransactionParticipant",
    "Vehicle",
    "VersionNumber",
    "VersionOfDocument",
]


class FusionOfIntegralParts(State):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}FusionOfIntegralParts",store,uri,start,finish)
        self._apply_categories(categories)

class Activity(ActivityMixin, FusionOfIntegralParts):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Activity",store,uri,start,finish)
        self._apply_categories(categories)

class Access(Access_Relations, Activity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Access",store,uri,start,finish)
        self._apply_categories(categories)

class Participation(State):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Participation",store,uri,start,finish)
        self._apply_categories(categories)

class Accessed(Participation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Accessed",store,uri,start,finish)
        self._apply_categories(categories)

class Accessor(Participation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Accessor",store,uri,start,finish)
        self._apply_categories(categories)

class EndToEndActivity(Activity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}EndToEndActivity",store,uri,start,finish)
        self._apply_categories(categories)

class Account(Account_Relations, EndToEndActivity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Account",store,uri,start,finish)
        self._apply_categories(categories)

class AccountAdminActivity(Activity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}AccountAdminActivity",store,uri,start,finish)
        self._apply_categories(categories)

class AccountClosure(AccountAdminActivity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}AccountClosure",store,uri,start,finish)
        self._apply_categories(categories)

class SetOfSigns(SetOfStates):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}SetOfSigns",store,uri)
        self._apply_categories(categories)
        self.instance_type = Sign

class Representation(SetOfSigns):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Representation",store,uri)
        self._apply_categories(categories)

class AccountDetails(Representation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}AccountDetails",store,uri)
        self._apply_categories(categories)

class AccountHolder(Participation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}AccountHolder",store,uri,start,finish)
        self._apply_categories(categories)

class AccountInCommunication(Participation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}AccountInCommunication",store,uri,start,finish)
        self._apply_categories(categories)

class AccountOpening(AccountAdminActivity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}AccountOpening",store,uri,start,finish)
        self._apply_categories(categories)

class AccountProvider(Participation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}AccountProvider",store,uri,start,finish)
        self._apply_categories(categories)

class AccountUpdate(AccountAdminActivity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}AccountUpdate",store,uri,start,finish)
        self._apply_categories(categories)

class ActiveParticipation(Participation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}ActiveParticipation",store,uri,start,finish)
        self._apply_categories(categories)

class Actor(State):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Actor",store,uri,start,finish)
        self._apply_categories(categories)

class ArbitraryPeriod(Period):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}ArbitraryPeriod",store,uri,start,finish)
        self._apply_categories(categories)

class Arrival(State):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Arrival",store,uri,start,finish)
        self._apply_categories(categories)

class Artefact(State):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Artefact",store,uri,start,finish)
        self._apply_categories(categories)

class Assessment(Assessment_Relations, Activity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Assessment",store,uri,start,finish)
        self._apply_categories(categories)

class Assessor(ActiveParticipation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Assessor",store,uri,start,finish)
        self._apply_categories(categories)

class Attendance(Participation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Attendance",store,uri,start,finish)
        self._apply_categories(categories)

class LivingOrganism(LivingOrganismMixin, LivingOrganism_Relations, State):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None, date_of_birth: str | None = None, place_of_birth=None, date_of_death: str | None = None, place_of_death=None):
        self._state_init(classes,f"{IES_CORE}LivingOrganism",store,uri,None,None)
        self._apply_categories(categories)
        self.add_lifespan(date_of_birth, place_of_birth, date_of_death, place_of_death)

class BirthState(LivingOrganism):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None, date_of_birth: str | None = None, place_of_birth=None, date_of_death: str | None = None, place_of_death=None):
        self._state_init(classes,f"{IES_CORE}BirthState",store,uri,None,None)
        self._apply_categories(categories)
        self.add_lifespan(date_of_birth, place_of_birth, date_of_death, place_of_death)

class Disposition(SetOfStates):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Disposition",store,uri)
        self._apply_categories(categories)

class Capability(Disposition):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Capability",store,uri)
        self._apply_categories(categories)

class Sign(State):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Sign",store,uri,start,finish)
        self._apply_categories(categories)

class CharacterString(Sign):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}CharacterString",store,uri,start,finish)
        self._apply_categories(categories)

class Characteristic(SetOfSpatiotemporalExtents):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Characteristic",store,uri)
        self._apply_categories(categories)

class CoLocation(FusionOfIntegralParts):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}CoLocation",store,uri,start,finish)
        self._apply_categories(categories)

class Color(Characteristic):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Color",store,uri)
        self._apply_categories(categories)

class Communication(Activity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Communication",store,uri,start,finish)
        self._apply_categories(categories)

class ContinuousAccess(Access, TemporallyContinuousState):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}ContinuousAccess",store,uri,start,finish)
        self._apply_categories(categories)

class Contract(Artefact):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Contract",store,uri,start,finish)
        self._apply_categories(categories)

class Location(State):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Location",store,uri,start,finish)
        self._apply_categories(categories)

class Country(Country_Relations, Location):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Country",store,uri,start,finish)
        self._apply_categories(categories)

class LifecycleActivity(Activity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}LifecycleActivity",store,uri,start,finish)
        self._apply_categories(categories)

class Create(Create_Relations, LifecycleActivity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Create",store,uri,start,finish)
        self._apply_categories(categories)

class Created(ActiveParticipation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Created",store,uri,start,finish)
        self._apply_categories(categories)

class Creator(ActiveParticipation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Creator",store,uri,start,finish)
        self._apply_categories(categories)

class DeathState(LivingOrganism):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None, date_of_birth: str | None = None, place_of_birth=None, date_of_death: str | None = None, place_of_death=None):
        self._state_init(classes,f"{IES_CORE}DeathState",store,uri,None,None)
        self._apply_categories(categories)
        self.add_lifespan(date_of_birth, place_of_birth, date_of_death, place_of_death)

class Departure(State):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Departure",store,uri,start,finish)
        self._apply_categories(categories)

class Destroy(Destroy_Relations, LifecycleActivity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Destroy",store,uri,start,finish)
        self._apply_categories(categories)

class Destroyed(ActiveParticipation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Destroyed",store,uri,start,finish)
        self._apply_categories(categories)

class Destroyer(ActiveParticipation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Destroyer",store,uri,start,finish)
        self._apply_categories(categories)

class SetOfIndividualDocuments(Representation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}SetOfIndividualDocuments",store,uri)
        self._apply_categories(categories)
        self.instance_type = IndividualDocument

class DocumentFormat(SetOfIndividualDocuments):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}DocumentFormat",store,uri)
        self._apply_categories(categories)

class SetOfCharacterStrings(SetOfSigns):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}SetOfCharacterStrings",store,uri)
        self._apply_categories(categories)
        self.instance_type = CharacterString

class Name(Representation, SetOfCharacterStrings):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Name",store,uri)
        self._apply_categories(categories)

class Identifier(Name):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Identifier",store,uri)
        self._apply_categories(categories)

class GeoIdentity(Identifier):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}GeoIdentity",store,uri)
        self._apply_categories(categories)

class Easting(GeoIdentity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Easting",store,uri)
        self._apply_categories(categories)

class EndToEndTransaction(EndToEndActivity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}EndToEndTransaction",store,uri,start,finish)
        self._apply_categories(categories)

class Entitlement(Entitlement_Relations, Activity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Entitlement",store,uri,start,finish)
        self._apply_categories(categories)

class SetOfLivingOrganisms(SetOfStates):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}SetOfLivingOrganisms",store,uri)
        self._apply_categories(categories)
        self.instance_type = LivingOrganism

class SetOfPersons(SetOfLivingOrganisms):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}SetOfPersons",store,uri)
        self._apply_categories(categories)
        self.instance_type = Person

class Ethnicity(SetOfPersons):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Ethnicity",store,uri)
        self._apply_categories(categories)

class TransactionActivity(TransactionActivity_Relations, Activity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}TransactionActivity",store,uri,start,finish)
        self._apply_categories(categories)

class Exchange(TransactionActivity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Exchange",store,uri,start,finish)
        self._apply_categories(categories)

class ExchangeMovement(TransactionActivity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}ExchangeMovement",store,uri,start,finish)
        self._apply_categories(categories)

class FiniteSetOfSpatiotemporalExtents(SetOfSpatiotemporalExtents):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}FiniteSetOfSpatiotemporalExtents",store,uri)
        self._apply_categories(categories)

class Gender(SetOfPersons):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Gender",store,uri)
        self._apply_categories(categories)

class GeoPoint(GeoPoint_Relations, Location):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}GeoPoint",store,uri,start,finish)
        self._apply_categories(categories)

class GovernanceActivity(GovernanceActivity_Relations, Activity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}GovernanceActivity",store,uri,start,finish)
        self._apply_categories(categories)

class System(FusionOfIntegralParts):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}System",store,uri,start,finish)
        self._apply_categories(categories)

class HumanMadeSystem(HumanMadeSystem_Relations, System, Artefact):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}HumanMadeSystem",store,uri,start,finish)
        self._apply_categories(categories)

class ICalRepresentation(Representation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}ICalRepresentation",store,uri)
        self._apply_categories(categories)

class ISO3166_1Alpha_3(GeoIdentity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}ISO3166_1Alpha_3",store,uri)
        self._apply_categories(categories)

class IndividualDocument(IndividualDocument_Relations, Artefact):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}IndividualDocument",store,uri,start,finish)
        self._apply_categories(categories)

class IndividualTicket(IndividualTicket_Relations, IndividualDocument):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}IndividualTicket",store,uri,start,finish)
        self._apply_categories(categories)

class InformationProcessingSystem(HumanMadeSystem, Actor):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}InformationProcessingSystem",store,uri,start,finish)
        self._apply_categories(categories)

class InformationProcessingSystemInCommunication(ActiveParticipation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}InformationProcessingSystemInCommunication",store,uri,start,finish)
        self._apply_categories(categories)

class Installed(State):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Installed",store,uri,start,finish)
        self._apply_categories(categories)

class IntermittentAccess(Access, TemporallyIntermittentState):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}IntermittentAccess",store,uri,start,finish)
        self._apply_categories(categories)

class Movement(Movement_Relations, Activity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Movement",store,uri,start,finish)
        self._apply_categories(categories)

class Journey(EndToEndActivity, Movement):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Journey",store,uri,start,finish)
        self._apply_categories(categories)

class SetOfSetOfSigns(SetOfSetOfStates):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}SetOfSetOfSigns",store,uri)
        self._apply_categories(categories)
        self.instance_type = SetOfSigns

class SetOfRepresentations(SetOfSetOfSigns):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}SetOfRepresentations",store,uri)
        self._apply_categories(categories)
        self.instance_type = Representation

class Language(SetOfRepresentations):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Language",store,uri)
        self._apply_categories(categories)

class Skill(Capability, SetOfPersons):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Skill",store,uri)
        self._apply_categories(categories)

class LanguageProficiency(Skill):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}LanguageProficiency",store,uri)
        self._apply_categories(categories)

class Latitude(GeoIdentity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Latitude",store,uri)
        self._apply_categories(categories)

class RightHolder(Participation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}RightHolder",store,uri,start,finish)
        self._apply_categories(categories)

class LegalOwner(RightHolder):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}LegalOwner",store,uri,start,finish)
        self._apply_categories(categories)

class LegalOwnership(LegalOwnership_Relations, Entitlement):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}LegalOwnership",store,uri,start,finish)
        self._apply_categories(categories)

class LivingSystem(System, LivingOrganism):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None, date_of_birth: str | None = None, place_of_birth=None, date_of_death: str | None = None, place_of_death=None):
        self._state_init(classes,f"{IES_CORE}LivingSystem",store,uri,None,None)
        self._apply_categories(categories)
        self.add_lifespan(date_of_birth, place_of_birth, date_of_death, place_of_death)

class Longitude(GeoIdentity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Longitude",store,uri)
        self._apply_categories(categories)

class Measure(Characteristic):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Measure",store,uri)
        self._apply_categories(categories)

class Meeting(Meeting_Relations, Communication):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Meeting",store,uri,start,finish)
        self._apply_categories(categories)

class Modifier(ActiveParticipation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Modifier",store,uri,start,finish)
        self._apply_categories(categories)

class Modify(Modify_Relations, LifecycleActivity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Modify",store,uri,start,finish)
        self._apply_categories(categories)

class RepresentationScheme(SetOfRepresentations):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}RepresentationScheme",store,uri)
        self._apply_categories(categories)

class SetOfNames(SetOfRepresentations):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}SetOfNames",store,uri)
        self._apply_categories(categories)
        self.instance_type = Name

class NamingScheme(RepresentationScheme, SetOfNames):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}NamingScheme",store,uri)
        self._apply_categories(categories)

class PersonOrOrganization(Actor):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}PersonOrOrganization",store,uri,start,finish)
        self._apply_categories(categories)

class Organization(HumanMadeSystem, PersonOrOrganization):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Organization",store,uri,start,finish)
        self._apply_categories(categories)

class RegionalConstituency(Organization):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}RegionalConstituency",store,uri,start,finish)
        self._apply_categories(categories)

class Nation(Nation_Relations, RegionalConstituency):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Nation",store,uri,start,finish)
        self._apply_categories(categories)

class Northing(GeoIdentity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Northing",store,uri)
        self._apply_categories(categories)

class Observation(Observation_Relations, Activity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Observation",store,uri,start,finish)
        self._apply_categories(categories)

class Observed(Participation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Observed",store,uri,start,finish)
        self._apply_categories(categories)

class Observer(ActiveParticipation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Observer",store,uri,start,finish)
        self._apply_categories(categories)

class RightTo(Participation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}RightTo",store,uri,start,finish)
        self._apply_categories(categories)

class OwnedLegally(RightTo):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}OwnedLegally",store,uri,start,finish)
        self._apply_categories(categories)

class ParticipationInGovernance(Participation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}ParticipationInGovernance",store,uri,start,finish)
        self._apply_categories(categories)

class ParticularPeriod(Period):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}ParticularPeriod",store,uri,start,finish)
        self._apply_categories(categories)

class PartyInCommunication(PartyInCommunication_Relations, Activity):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}PartyInCommunication",store,uri,start,finish)
        self._apply_categories(categories)

class Person(LivingSystem, PersonOrOrganization):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None, date_of_birth: str | None = None, place_of_birth=None, date_of_death: str | None = None, place_of_death=None):
        self._state_init(classes,f"{IES_CORE}Person",store,uri,None,None)
        self._apply_categories(categories)
        self.add_lifespan(date_of_birth, place_of_birth, date_of_death, place_of_death)

class PersonInCommunication(ActiveParticipation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}PersonInCommunication",store,uri,start,finish)
        self._apply_categories(categories)

class PersonName(PersonName_Relations, Name):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}PersonName",store,uri)
        self._apply_categories(categories)

class Provision(Participation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Provision",store,uri,start,finish)
        self._apply_categories(categories)

class Recognizer(Participation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Recognizer",store,uri,start,finish)
        self._apply_categories(categories)

class RecurringTimespan(RecurringTimespanMixin, IntermittentTimespan):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}RecurringTimespan",store,uri,start,finish)
        self._apply_categories(categories)

class ReplaceableLifespan(FusionOfIntegralParts):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}ReplaceableLifespan",store,uri,start,finish)
        self._apply_categories(categories)

class RightGrantingArtefact(Participation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}RightGrantingArtefact",store,uri,start,finish)
        self._apply_categories(categories)

class SetOfInformationProcessingSystems(SetOfStates):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}SetOfInformationProcessingSystems",store,uri)
        self._apply_categories(categories)
        self.instance_type = InformationProcessingSystem

class SetOfStatesWithParticularDuration(SetOfStates):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}SetOfStatesWithParticularDuration",store,uri)
        self._apply_categories(categories)

class SetOfTimeBoundedStates(SetOfStates):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}SetOfTimeBoundedStates",store,uri)
        self._apply_categories(categories)

class SetOfUniverseMates(SetOfStates):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}SetOfUniverseMates",store,uri)
        self._apply_categories(categories)

class Sex(SetOfLivingOrganisms):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Sex",store,uri)
        self._apply_categories(categories)

class SimilarUniverseMates(SetOfUniverseMates):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}SimilarUniverseMates",store,uri)
        self._apply_categories(categories)

class Tendency(Disposition):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Tendency",store,uri)
        self._apply_categories(categories)

class WorkOfDocumentation(WorkOfDocumentation_Relations, SetOfIndividualDocuments):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}WorkOfDocumentation",store,uri)
        self._apply_categories(categories)

class Ticket(WorkOfDocumentation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Ticket",store,uri)
        self._apply_categories(categories)

class Title(Name):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}Title",store,uri)
        self._apply_categories(categories)

class TransactionParticipant(Participation):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}TransactionParticipant",store,uri,start,finish)
        self._apply_categories(categories)

class Vehicle(HumanMadeSystem):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, start: datetime.datetime | None = None, finish: datetime.datetime | None = None, categories: list[str] | None = None):
        self._state_init(classes,f"{IES_CORE}Vehicle",store,uri,start,finish)
        self._apply_categories(categories)

class VersionNumber(Identifier):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}VersionNumber",store,uri)
        self._apply_categories(categories)

class VersionOfDocument(VersionOfDocument_Relations, WorkOfDocumentation, SetOfTimeBoundedStates):
    def __init__(self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None, categories: list[str] | None = None):
        self._cls_init(classes,f"{IES_CORE}VersionOfDocument",store,uri)
        self._apply_categories(categories)
