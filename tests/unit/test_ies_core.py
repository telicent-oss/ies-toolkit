from ies_toolkit.constants import IES_CORE
from ies_toolkit.ies_core import (
    Account,
    Activity,
    Actor,
    Country,
    GeoIdentity,
    HumanMadeSystem,
    Identifier,
    ISO3166_1Alpha_3,
    LivingOrganism,
    Name,
    Organization,
    Person,
    PersonName,
    Representation,
    Vehicle,
)
from ies_toolkit.ies_top import Set, SpatiotemporalExtent, Stuff, Thing, Tuple
from ies_toolkit.rdflib_plugin import RdfLibPlugIn
from tests.rdf_assert import ask, count


def test_monkey_patching():
    """Create an IES Actor with a Name."""
    store = RdfLibPlugIn()
    my_actor = Actor(store=store, uri="http://test.org/ies_actor_test_1")
    name = my_actor.add_name("Fred")

    assert my_actor.uri == "http://test.org/ies_actor_test_1"
    assert type(name) is Name
    assert ask(store, f"""
        <{name.uri}> a ies_core:Name ;
                     ies_core:representationValue "Fred"^^xsd:string .
    """)

def test_monkey_patching_advanced():
    """Create an IES Person with a Person Name."""
    store = RdfLibPlugIn()
    my_actor = Person(store=store, uri="http://test.org/ies_person_test_1")
    name = my_actor.add_name("Fred", representation_classes=[f"{IES_CORE}PersonName"])

    assert my_actor.uri == "http://test.org/ies_person_test_1"
    assert type(name) is PersonName
    assert type(name) is not Name
    assert ask(store, f"""
        <{name.uri}> a ies_core:PersonName ;
                     ies_core:representationValue "Fred"^^xsd:string .
    """)

def test_category_on_state_subclass():
    "ies_core:category triples are added for a State-based class."
    store = RdfLibPlugIn()
    spy_concept = "http://example.org/skos/Spy"
    my_person = Person(store=store, uri="http://test.org/ies_person_cat_1", categories=[spy_concept])

    assert ask(store, f'<{my_person.uri}> ies_core:category <{spy_concept}>')

def test_category_on_ies_top_thing():
    "ies_core:category works on Thing - the rdfs:domain of category."
    store = RdfLibPlugIn()
    concept = "http://example.org/skos/MyCategory"
    my_thing = Thing(store=store, uri="http://test.org/thing_cat_1", categories=[concept])

    assert ask(store, f'<{my_thing.uri}> ies_core:category <{concept}>')

def test_category_on_ies_spatiotemporal_extent():
    "ies_core:category triples are added for SpatiotemporalExtent."
    store = RdfLibPlugIn()
    concept = "http://example.org/skos/SomeConcept"
    my_extent = SpatiotemporalExtent(store=store, uri="http://test.org/ste_cat_1", categories=[concept])

    assert ask(store, f'<{my_extent.uri}> ies_core:category <{concept}>')

def test_category_on_ies_top_set():
    "ies_core:category works on Set (rdfs:domain of category is Thing)."
    store = RdfLibPlugIn()
    concept = "http://example.org/skos/MyCategory"
    my_set = Set(store=store, uri="http://test.org/set_cat_1", categories=[concept])

    assert ask(store, f'<{my_set.uri}> ies_core:category <{concept}>')

def test_category_on_ies_top_tuple():
    "ies_core:category works on Tuple (rdfs:domain of category is Thing)."
    store = RdfLibPlugIn()
    concept = "http://example.org/skos/MyCategory"
    my_tuple = Tuple(store=store, uri="http://test.org/tuple_cat_1", categories=[concept])

    assert ask(store, f'<{my_tuple.uri}> ies_core:category <{concept}>')

def test_category_on_ies_top_stuff():
    "ies_core:category works on Stuff (rdfs:domain of category is Thing)."
    store = RdfLibPlugIn()
    concept = "http://example.org/skos/MyCategory"
    my_stuff = Stuff(store=store, uri="http://test.org/stuff_cat_1", categories=[concept])

    assert ask(store, f'<{my_stuff.uri}> ies_core:category <{concept}>')

def test_multiple_categories():
    "Multiple ies_core:category triples are added."
    store = RdfLibPlugIn()
    cat1 = "http://example.org/skos/DoubleDeckerBus"
    cat2 = "http://example.org/skos/PublicTransport"
    my_vehicle = Vehicle(store=store, uri="http://test.org/ies_vehicle_cat_multi", categories=[cat1, cat2])

    assert ask(store, f'<{my_vehicle.uri}> ies_core:category <{cat1}>')
    assert ask(store, f'<{my_vehicle.uri}> ies_core:category <{cat2}>')

def test_no_categories_by_default():
    "No ies_core:category triples when categories are not provided."
    store = RdfLibPlugIn()
    Person(store=store, uri="http://test.org/ies_person_no_cat")

    assert not ask(store, '?s ies_core:category ?o')


# Tests for the add_representation factory: verify all three add_X methods
# (add_representation / add_name / add_identifier) work with the correct
# default Python class, predicate, and minted-URI suffix.

def test_add_representation_default_class_and_predicate():
    "add_representation uses isRepresentedAs, Representation default, _rep_ URI suffix."
    store = RdfLibPlugIn()
    person = Person(store=store, uri="http://test.org/p_rep")
    rep = person.add_representation("some-value")

    assert type(rep) is Representation
    assert "_rep_" in rep.uri  # URI suffix from the factory
    assert ask(store, f"""
        <{person.uri}> ies_core:isRepresentedAs <{rep.uri}> .
        <{rep.uri}> a ies_core:Representation ;
                    ies_core:representationValue "some-value"^^xsd:string .
    """)

def test_add_name_default_class_and_predicate():
    "add_name uses hasName, Name default, _name_ URI suffix."
    store = RdfLibPlugIn()
    person = Person(store=store, uri="http://test.org/p_name")
    name = person.add_name("Alice")

    assert type(name) is Name
    assert "_name_" in name.uri
    assert ask(store, f"""
        <{person.uri}> ies_core:hasName <{name.uri}> .
        <{name.uri}> a ies_core:Name ;
                     ies_core:representationValue "Alice"^^xsd:string .
    """)

def test_add_identifier_default_class_and_predicate():
    "add_identifier uses isIdentifiedBy, Identifier default, _id_ URI suffix."
    store = RdfLibPlugIn()
    person = Person(store=store, uri="http://test.org/p_id")
    ident = person.add_identifier("ABC123")

    assert type(ident) is Identifier
    assert "_id_" in ident.uri
    assert ask(store, f"""
        <{person.uri}> ies_core:isIdentifiedBy <{ident.uri}> .
        <{ident.uri}> a ies_core:Identifier ;
                      ies_core:representationValue "ABC123"^^xsd:string .
    """)

def test_add_identifier_with_specific_subclass():
    "add_identifier with explicit representation_classes resolves to the requested subclass (e.g. GeoIdentity)."
    store = RdfLibPlugIn()
    person = Person(store=store, uri="http://test.org/p_geo")
    geo = person.add_identifier("51.5074,-0.1278", representation_classes=[f"{IES_CORE}GeoIdentity"])

    assert type(geo) is GeoIdentity
    assert type(geo) is not Identifier
    assert ask(store, f'<{geo.uri}> a ies_core:GeoIdentity')

def test_returned_representation_object_is_usable():
    "Regression: the returned object is fully constructed (has a store), so add_label works."
    store = RdfLibPlugIn()
    person = Person(store=store, uri="http://test.org/p_usable")
    name = person.add_name("Alice")

    name.add_label("Alice the name")  # would raise AttributeError on the old __new__-only handle
    assert ask(store, f'<{name.uri}> rdfs:label "Alice the name"^^xsd:string')

def test_constructor_writes_rdf_type():
    "Sanity check: regular constructors emit rdf:type for the IES class."
    store = RdfLibPlugIn()
    person = Person(store=store, uri="http://test.org/person_type_check")

    assert ask(store, f'<{person.uri}> a ies_core:Person')

def test_generic_add_participant():
    "Every ies_core:Activity carries the generic add_participant (ActivityMixin)."
    store = RdfLibPlugIn()
    activity = Activity(store=store, uri="http://test.org/act_p")
    person = Person(store=store, uri="http://test.org/p_p")
    node = activity.add_participant(person, participation_uri="http://test.org/participation_p")

    assert ask(store, f"""
        <{node}> a ies_core:Participation ;
                 ies_top:isPartOf <{activity.uri}> ;
                 ies_top:isTemporalPartOf <{person.uri}> .
    """)

def test_add_participant_subclass_inherits():
    "Activity subclasses inherit add_participant; role_class overrides the node type."
    store = RdfLibPlugIn()
    activity = Activity(store=store, uri="http://test.org/act_role")
    person = Person(store=store, uri="http://test.org/p_role")
    node = activity.add_participant(person, role_class=f"{IES_CORE}Creator",
                                   participation_uri="http://test.org/creator_role")

    assert ask(store, f'<{node}> a ies_core:Creator ; ies_top:isPartOf <{activity.uri}>')

def test_generated_specialised_participation_builder():
    "Generated add_account_holder mints an AccountHolder wired to host + participant."
    store = RdfLibPlugIn()
    account = Account(store=store, uri="http://test.org/acc")
    person = Person(store=store, uri="http://test.org/holder")
    org = Organization(store=store, uri="http://test.org/org")
    node = account.add_account_holder(person, organization=org, participation_uri="http://test.org/ah")

    # host (Activity) + participant + optional secondary, all on the one node
    assert ask(store, f"""
        <{node}> a ies_core:AccountHolder ;
                 ies_top:isPartOf <{account.uri}> ;
                 ies_top:isTemporalPartOf <{person.uri}> ;
                 ies_top:isPartOf <{org.uri}> .
    """)

def test_generated_optional_arg_omitted():
    "Optional secondary endpoints are skipped when not supplied."
    store = RdfLibPlugIn()
    account = Account(store=store, uri="http://test.org/acc2")
    person = Person(store=store, uri="http://test.org/holder2")
    node = account.add_account_holder(person, participation_uri="http://test.org/ah2")

    assert ask(store, f"""
        <{node}> ies_top:isTemporalPartOf <{person.uri}> ;
                 ies_top:isPartOf <{account.uri}> .
    """)
    # the only isPartOf object is the host; no stray organization edge
    assert count(store, f'<{node}> ies_top:isPartOf ?o') == 1

def test_generated_boundary_state_builder():
    "Generated add_birth_state mints a BirthState that isAStartOf the organism."
    store = RdfLibPlugIn()
    org = LivingOrganism(store=store, uri="http://test.org/lo")
    node = org.add_birth_state(state_uri="http://test.org/birth")

    assert ask(store, f'<{node}> a ies_core:BirthState ; ies_top:isAStartOf <{org.uri}>')

def test_generated_typed_identifier_real_subclass():
    "Typed identifier on a real Representation subclass: rdf:type is the subclass, no category."
    store = RdfLibPlugIn()
    country = Country(store=store, uri="http://test.org/gb")
    rep = country.add_iso3166_1_alpha_3("GBR", representation_uri="http://test.org/iso")

    assert type(rep) is ISO3166_1Alpha_3
    assert ask(store, f"""
        <{country.uri}> ies_core:isIdentifiedBy <{rep.uri}> .
        <{rep.uri}> a ies_core:ISO3166_1Alpha_3 ;
                    ies_core:representationValue "GBR"^^xsd:string .
    """)
    assert not ask(store, '?s ies_core:category ?o')  # real subclass -> no category

def test_generated_typed_identifier_skos_category():
    "Typed identifier on a SKOS concept: rdf:type is the range root (Identifier) + category."
    store = RdfLibPlugIn()
    sys = HumanMadeSystem(store=store, uri="http://test.org/sys")
    rep = sys.add_part_number("PN-99", representation_uri="http://test.org/pn")

    assert type(rep) is Identifier  # minted as the range root, not a PartNumber class
    assert ask(store, f"""
        <{sys.uri}> ies_core:isIdentifiedBy <{rep.uri}> .
        <{rep.uri}> a ies_core:Identifier ;
                    ies_core:category ies_core:PartNumber ;
                    ies_core:representationValue "PN-99"^^xsd:string .
    """)
