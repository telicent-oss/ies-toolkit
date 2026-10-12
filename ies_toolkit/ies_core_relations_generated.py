"""Relationship / reified builders generated from the SHACL shapes.

DO NOT EDIT BY HAND. Regenerate with:  python tools/generate_ies.py --relations
The reified-node engine lives in the hand-written overlay (ies_core_custom.ReifiedBuilderMixin).
"""
from .ies_core_custom import ReifiedBuilderMixin
from .constants import IES_CORE, IES_TOP


class Access_Relations(ReifiedBuilderMixin):
    def add_accessed(self, state, participation_uri=None):
        """Mint an Accessed (isPartOf this Access)."""
        node = self._mint_node(f"{IES_CORE}Accessed", "accessed", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        self._wire(node, f"{IES_TOP}isTemporalPartOf", state)
        return node

    def add_accessor(self, person=None, organization=None, participation_uri=None):
        """Mint an Accessor (isPartOf this Access)."""
        node = self._mint_node(f"{IES_CORE}Accessor", "accessor", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        if person is not None:
            self._wire(node, f"{IES_TOP}isTemporalPartOf", person)
        if organization is not None:
            self._wire(node, f"{IES_TOP}isPartOf", organization)
        return node


class Account_Relations(ReifiedBuilderMixin):
    def add_account_details(self, value, representation_uri=None):
        """Add an AccountDetails to this Account (isRepresentedAs + representationValue)."""
        rep = self._add_representation(value, f"{IES_CORE}AccountDetails", f"{IES_CORE}isRepresentedAs", "account_details", "IesCore_Representation", None, representation_uri)
        return rep

    def add_account_holder(self, person=None, organization=None, participation_uri=None):
        """Mint an AccountHolder (isPartOf this Account)."""
        node = self._mint_node(f"{IES_CORE}AccountHolder", "account_holder", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        if person is not None:
            self._wire(node, f"{IES_TOP}isTemporalPartOf", person)
        if organization is not None:
            self._wire(node, f"{IES_TOP}isPartOf", organization)
        return node

    def add_account_in_communication(self, party_in_communication, participation_uri=None):
        """Mint an AccountInCommunication (isPartOf this Account)."""
        node = self._mint_node(f"{IES_CORE}AccountInCommunication", "account_in_communication", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        self._wire(node, f"{IES_TOP}isPartOf", party_in_communication)
        return node

    def add_account_provider(self, person=None, organization=None, participation_uri=None):
        """Mint an AccountProvider (isPartOf this Account)."""
        node = self._mint_node(f"{IES_CORE}AccountProvider", "account_provider", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        if person is not None:
            self._wire(node, f"{IES_TOP}isTemporalPartOf", person)
        if organization is not None:
            self._wire(node, f"{IES_TOP}isPartOf", organization)
        return node

    def add_provision(self, artefact, participation_uri=None):
        """Mint a Provision (isPartOf this Account)."""
        node = self._mint_node(f"{IES_CORE}Provision", "provision", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        self._wire(node, f"{IES_TOP}isTemporalPartOf", artefact)
        return node


class Assessment_Relations(ReifiedBuilderMixin):
    def add_assessor(self, person=None, information_processing_system=None, organization=None, participation_uri=None):
        """Mint an Assessor (isPartOf this Assessment)."""
        node = self._mint_node(f"{IES_CORE}Assessor", "assessor", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        if person is not None:
            self._wire(node, f"{IES_TOP}isTemporalPartOf", person)
        if information_processing_system is not None:
            self._wire(node, f"{IES_TOP}isPartOf", information_processing_system)
        if organization is not None:
            self._wire(node, f"{IES_TOP}isPartOf", organization)
        return node


class Country_Relations(ReifiedBuilderMixin):
    def add_iso3166_1_alpha_3(self, value, representation_uri=None):
        """Add an ISO3166_1Alpha_3 to this Country (isIdentifiedBy + representationValue)."""
        rep = self._add_representation(value, f"{IES_CORE}ISO3166_1Alpha_3", f"{IES_CORE}isIdentifiedBy", "iso3166_1_alpha_3", "IesCore_Representation", None, representation_uri)
        return rep


class Create_Relations(ReifiedBuilderMixin):
    def add_created(self, artefact=None, right_granting_artefact=None, participation_uri=None):
        """Mint a Created (isPartOf this Create)."""
        node = self._mint_node(f"{IES_CORE}Created", "created", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        if artefact is not None:
            self._wire(node, f"{IES_TOP}isAStartOf", artefact)
        if right_granting_artefact is not None:
            self._wire(node, f"{IES_TOP}isPartOf", right_granting_artefact)
        return node

    def add_creator(self, person=None, organization=None, participation_uri=None):
        """Mint a Creator (isPartOf this Create)."""
        node = self._mint_node(f"{IES_CORE}Creator", "creator", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        if person is not None:
            self._wire(node, f"{IES_TOP}isTemporalPartOf", person)
        if organization is not None:
            self._wire(node, f"{IES_TOP}isPartOf", organization)
        return node


class Destroy_Relations(ReifiedBuilderMixin):
    def add_destroyed(self, artefact, participation_uri=None):
        """Mint a Destroyed (isPartOf this Destroy)."""
        node = self._mint_node(f"{IES_CORE}Destroyed", "destroyed", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        self._wire(node, f"{IES_TOP}isAFinishOf", artefact)
        return node

    def add_destroyer(self, person=None, organization=None, participation_uri=None):
        """Mint a Destroyer (isPartOf this Destroy)."""
        node = self._mint_node(f"{IES_CORE}Destroyer", "destroyer", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        if person is not None:
            self._wire(node, f"{IES_TOP}isTemporalPartOf", person)
        if organization is not None:
            self._wire(node, f"{IES_TOP}isPartOf", organization)
        return node


class Entitlement_Relations(ReifiedBuilderMixin):
    def add_exchange_movement(self, exchange=None, entitlement=None, state_uri=None):
        """Mint an ExchangeMovement (isAStartOf this Entitlement)."""
        node = self._mint_node(f"{IES_CORE}ExchangeMovement", "exchange_movement", state_uri)
        self._wire(node, f"{IES_TOP}isAStartOf", self.uri)
        if exchange is not None:
            self._wire(node, f"{IES_TOP}isPartOf", exchange)
        if entitlement is not None:
            self._wire(node, f"{IES_TOP}isAFinishOf", entitlement)
        return node

    def add_exchange_movement_is_a_finish_of(self, exchange=None, entitlement=None, state_uri=None):
        """Mint an ExchangeMovement (isAFinishOf this Entitlement)."""
        node = self._mint_node(f"{IES_CORE}ExchangeMovement", "exchange_movement", state_uri)
        self._wire(node, f"{IES_TOP}isAFinishOf", self.uri)
        if exchange is not None:
            self._wire(node, f"{IES_TOP}isPartOf", exchange)
        if entitlement is not None:
            self._wire(node, f"{IES_TOP}isAStartOf", entitlement)
        return node

    def add_recognizer(self, person=None, organization=None, participation_uri=None):
        """Mint a Recognizer (isPartOf this Entitlement)."""
        node = self._mint_node(f"{IES_CORE}Recognizer", "recognizer", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        if person is not None:
            self._wire(node, f"{IES_TOP}isTemporalPartOf", person)
        if organization is not None:
            self._wire(node, f"{IES_TOP}isPartOf", organization)
        return node

    def add_right_granting_artefact(self, artefact, participation_uri=None):
        """Mint a RightGrantingArtefact (isPartOf this Entitlement)."""
        node = self._mint_node(f"{IES_CORE}RightGrantingArtefact", "right_granting_artefact", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        self._wire(node, f"{IES_TOP}isTemporalPartOf", artefact)
        return node

    def add_right_holder(self, person_or_organization, participation_uri=None):
        """Mint a RightHolder (isPartOf this Entitlement)."""
        node = self._mint_node(f"{IES_CORE}RightHolder", "right_holder", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        self._wire(node, f"{IES_TOP}isTemporalPartOf", person_or_organization)
        return node

    def add_right_to(self, state, participation_uri=None):
        """Mint a RightTo (isPartOf this Entitlement)."""
        node = self._mint_node(f"{IES_CORE}RightTo", "right_to", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        self._wire(node, f"{IES_TOP}isTemporalPartOf", state)
        return node


class GeoPoint_Relations(ReifiedBuilderMixin):
    def add_easting(self, value, representation_uri=None):
        """Add an Easting to this GeoPoint (isIdentifiedBy + representationValue)."""
        rep = self._add_representation(value, f"{IES_CORE}Easting", f"{IES_CORE}isIdentifiedBy", "easting", "IesCore_Representation", None, representation_uri)
        return rep

    def add_latitude(self, value, representation_uri=None):
        """Add a Latitude to this GeoPoint (isIdentifiedBy + representationValue)."""
        rep = self._add_representation(value, f"{IES_CORE}Latitude", f"{IES_CORE}isIdentifiedBy", "latitude", "IesCore_Representation", None, representation_uri)
        return rep

    def add_longitude(self, value, representation_uri=None):
        """Add a Longitude to this GeoPoint (isIdentifiedBy + representationValue)."""
        rep = self._add_representation(value, f"{IES_CORE}Longitude", f"{IES_CORE}isIdentifiedBy", "longitude", "IesCore_Representation", None, representation_uri)
        return rep

    def add_northing(self, value, representation_uri=None):
        """Add a Northing to this GeoPoint (isIdentifiedBy + representationValue)."""
        rep = self._add_representation(value, f"{IES_CORE}Northing", f"{IES_CORE}isIdentifiedBy", "northing", "IesCore_Representation", None, representation_uri)
        return rep


class GovernanceActivity_Relations(ReifiedBuilderMixin):
    def add_participation_in_governance(self, person=None, organization=None, participation_uri=None):
        """Mint a ParticipationInGovernance (isPartOf this GovernanceActivity)."""
        node = self._mint_node(f"{IES_CORE}ParticipationInGovernance", "participation_in_governance", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        if person is not None:
            self._wire(node, f"{IES_TOP}isTemporalPartOf", person)
        if organization is not None:
            self._wire(node, f"{IES_TOP}isPartOf", organization)
        return node


class HumanMadeSystem_Relations(ReifiedBuilderMixin):
    def add_part_number(self, value, representation_uri=None):
        """Add a PartNumber to this HumanMadeSystem (isIdentifiedBy + representationValue)."""
        rep = self._add_representation(value, f"{IES_CORE}Identifier", f"{IES_CORE}isIdentifiedBy", "part_number", "IesCore_Representation", None, representation_uri)
        rep._apply_categories([f"{IES_CORE}PartNumber"])
        return rep

    def add_serial_number(self, value, representation_uri=None):
        """Add a SerialNumber to this HumanMadeSystem (isIdentifiedBy + representationValue)."""
        rep = self._add_representation(value, f"{IES_CORE}Identifier", f"{IES_CORE}isIdentifiedBy", "serial_number", "IesCore_Representation", None, representation_uri)
        rep._apply_categories([f"{IES_CORE}SerialNumber"])
        return rep


class IndividualDocument_Relations(ReifiedBuilderMixin):
    def add_individual_document_id(self, value, representation_uri=None):
        """Add an IndividualDocumentID to this IndividualDocument (isIdentifiedBy + representationValue)."""
        rep = self._add_representation(value, f"{IES_CORE}Identifier", f"{IES_CORE}isIdentifiedBy", "individual_document_id", "IesCore_Representation", None, representation_uri)
        rep._apply_categories([f"{IES_CORE}IndividualDocumentID"])
        return rep


class IndividualTicket_Relations(ReifiedBuilderMixin):
    def add_ticket(self, value, representation_uri=None):
        """Add a Ticket to this IndividualTicket (aCopyOf + representationValue)."""
        rep = self._add_representation(value, f"{IES_CORE}Ticket", f"{IES_CORE}aCopyOf", "ticket", "IesCore_Representation", None, representation_uri)
        return rep


class LegalOwnership_Relations(ReifiedBuilderMixin):
    def add_legal_owner(self, participation_uri=None):
        """Mint a LegalOwner (isPartOf this LegalOwnership)."""
        node = self._mint_node(f"{IES_CORE}LegalOwner", "legal_owner", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        return node

    def add_owned_legally(self, participation_uri=None):
        """Mint an OwnedLegally (isPartOf this LegalOwnership)."""
        node = self._mint_node(f"{IES_CORE}OwnedLegally", "owned_legally", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        return node


class LivingOrganism_Relations(ReifiedBuilderMixin):
    def add_birth_state(self, state_uri=None):
        """Mint a BirthState (isAStartOf this LivingOrganism)."""
        node = self._mint_node(f"{IES_CORE}BirthState", "birth_state", state_uri)
        self._wire(node, f"{IES_TOP}isAStartOf", self.uri)
        return node

    def add_death_state(self, state_uri=None):
        """Mint a DeathState (isAFinishOf this LivingOrganism)."""
        node = self._mint_node(f"{IES_CORE}DeathState", "death_state", state_uri)
        self._wire(node, f"{IES_TOP}isAFinishOf", self.uri)
        return node


class Meeting_Relations(ReifiedBuilderMixin):
    def add_attendance(self, person=None, organization=None, participation_uri=None):
        """Mint an Attendance (isPartOf this Meeting)."""
        node = self._mint_node(f"{IES_CORE}Attendance", "attendance", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        if person is not None:
            self._wire(node, f"{IES_TOP}isTemporalPartOf", person)
        if organization is not None:
            self._wire(node, f"{IES_TOP}isPartOf", organization)
        return node


class Modify_Relations(ReifiedBuilderMixin):
    def add_modifier(self, person=None, organization=None, participation_uri=None):
        """Mint a Modifier (isPartOf this Modify)."""
        node = self._mint_node(f"{IES_CORE}Modifier", "modifier", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        if person is not None:
            self._wire(node, f"{IES_TOP}isTemporalPartOf", person)
        if organization is not None:
            self._wire(node, f"{IES_TOP}isPartOf", organization)
        return node


class Movement_Relations(ReifiedBuilderMixin):
    def add_arrival(self, location, state_uri=None):
        """Mint an Arrival (isAFinishOf this Movement)."""
        node = self._mint_node(f"{IES_CORE}Arrival", "arrival", state_uri)
        self._wire(node, f"{IES_TOP}isAFinishOf", self.uri)
        self._wire(node, f"{IES_TOP}isPartOf", location)
        return node

    def add_departure(self, location, state_uri=None):
        """Mint a Departure (isAStartOf this Movement)."""
        node = self._mint_node(f"{IES_CORE}Departure", "departure", state_uri)
        self._wire(node, f"{IES_TOP}isAStartOf", self.uri)
        self._wire(node, f"{IES_TOP}isPartOf", location)
        return node


class Nation_Relations(ReifiedBuilderMixin):
    def add_iso3166_1_alpha_3(self, value, representation_uri=None):
        """Add an ISO3166_1Alpha_3 to this Nation (isIdentifiedBy + representationValue)."""
        rep = self._add_representation(value, f"{IES_CORE}ISO3166_1Alpha_3", f"{IES_CORE}isIdentifiedBy", "iso3166_1_alpha_3", "IesCore_Representation", None, representation_uri)
        return rep


class Observation_Relations(ReifiedBuilderMixin):
    def add_observed(self, state=None, state_2=None, participation_uri=None):
        """Mint an Observed (isPartOf this Observation)."""
        node = self._mint_node(f"{IES_CORE}Observed", "observed", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        if state is not None:
            self._wire(node, f"{IES_TOP}isTemporalPartOf", state)
        if state_2 is not None:
            self._wire(node, f"{IES_TOP}isPartOf", state_2)
        return node

    def add_observer(self, person=None, information_processing_system=None, organization=None, participation_uri=None):
        """Mint an Observer (isPartOf this Observation)."""
        node = self._mint_node(f"{IES_CORE}Observer", "observer", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        if person is not None:
            self._wire(node, f"{IES_TOP}isTemporalPartOf", person)
        if information_processing_system is not None:
            self._wire(node, f"{IES_TOP}isPartOf", information_processing_system)
        if organization is not None:
            self._wire(node, f"{IES_TOP}isPartOf", organization)
        return node


class PartyInCommunication_Relations(ReifiedBuilderMixin):
    def add_account_in_communication(self, account, participation_uri=None):
        """Mint an AccountInCommunication (isPartOf this PartyInCommunication)."""
        node = self._mint_node(f"{IES_CORE}AccountInCommunication", "account_in_communication", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        self._wire(node, f"{IES_TOP}isPartOf", account)
        return node

    def add_information_processing_system_in_communication(self, information_processing_system, participation_uri=None):
        """Mint an InformationProcessingSystemInCommunication (isPartOf this PartyInCommunication)."""
        node = self._mint_node(f"{IES_CORE}InformationProcessingSystemInCommunication", "information_processing_system_in_communication", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        self._wire(node, f"{IES_TOP}isPartOf", information_processing_system)
        return node

    def add_person_in_communication(self, person, participation_uri=None):
        """Mint a PersonInCommunication (isPartOf this PartyInCommunication)."""
        node = self._mint_node(f"{IES_CORE}PersonInCommunication", "person_in_communication", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        self._wire(node, f"{IES_TOP}isTemporalPartOf", person)
        return node


class PersonName_Relations(ReifiedBuilderMixin):
    def add_person_name(self, value, representation_uri=None):
        """Add a PersonName to this PersonName (inRepresentation + representationValue)."""
        rep = self._add_representation(value, f"{IES_CORE}PersonName", f"{IES_CORE}inRepresentation", "person_name", "IesCore_Representation", None, representation_uri)
        return rep


class TransactionActivity_Relations(ReifiedBuilderMixin):
    def add_transaction_participant(self, participation_uri=None):
        """Mint a TransactionParticipant (isPartOf this TransactionActivity)."""
        node = self._mint_node(f"{IES_CORE}TransactionParticipant", "transaction_participant", participation_uri)
        self._wire(node, f"{IES_TOP}isPartOf", self.uri)
        return node


class VersionOfDocument_Relations(ReifiedBuilderMixin):
    def add_version_number(self, value, representation_uri=None):
        """Add a VersionNumber to this VersionOfDocument (isIdentifiedBy + representationValue)."""
        rep = self._add_representation(value, f"{IES_CORE}VersionNumber", f"{IES_CORE}isIdentifiedBy", "version_number", "IesCore_Representation", None, representation_uri)
        return rep


class WorkOfDocumentation_Relations(ReifiedBuilderMixin):
    def add_title(self, value, representation_uri=None):
        """Add a Title to this WorkOfDocumentation (hasName + representationValue)."""
        rep = self._add_representation(value, f"{IES_CORE}Title", f"{IES_CORE}hasName", "title", "IesCore_Representation", None, representation_uri)
        return rep


__all__ = [
    "Access_Relations",
    "Account_Relations",
    "Assessment_Relations",
    "Country_Relations",
    "Create_Relations",
    "Destroy_Relations",
    "Entitlement_Relations",
    "GeoPoint_Relations",
    "GovernanceActivity_Relations",
    "HumanMadeSystem_Relations",
    "IndividualDocument_Relations",
    "IndividualTicket_Relations",
    "LegalOwnership_Relations",
    "LivingOrganism_Relations",
    "Meeting_Relations",
    "Modify_Relations",
    "Movement_Relations",
    "Nation_Relations",
    "Observation_Relations",
    "PartyInCommunication_Relations",
    "PersonName_Relations",
    "TransactionActivity_Relations",
    "VersionOfDocument_Relations",
    "WorkOfDocumentation_Relations",
]
