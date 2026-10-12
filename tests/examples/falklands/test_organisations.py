"""Falklands acceptance example: organisations.

Ports organisations.py to the IES-Next API. org_type and OrganizationName are SKOS
concepts (not classes), so each org is an Organization instance categorised with its
subtype, named via a Name categorised OrganizationName. URIs are pinned, so the whole
graph is asserted against a golden; the ASKs document the SKOS-category idiom.
"""
import csv
from pathlib import Path

from ies_toolkit.constants import IES_CORE
from ies_toolkit.ies_core import Organization
from ies_toolkit.rdflib_plugin import RdfLibPlugIn
from tests.rdf_assert import ask, assert_matches_golden

HERE = Path(__file__).resolve().parent
DATA = "http://example.com/data#"


def _build():
    store = RdfLibPlugIn()
    rows = list(csv.DictReader((HERE / "data" / "organisations.csv").open(encoding="utf-8-sig")))
    for row in rows:
        # org_type is an ies_core SKOS concept (e.g. ies_core:MilitaryOrganization)
        org = Organization(store=store, uri=DATA + row["id"], categories=[row["org_type"]])
        name = org.add_name(row["name"], representation_uri=f"{DATA}{row['id']}_name")
        name._apply_categories([f"{IES_CORE}OrganizationName"])
    return store


def test_organisations():
    store = _build()
    # an org is the base class categorised with its subtype concept
    assert ask(store, f"""
        <{DATA}RoyalNavy> a ies_core:Organization ;
                          ies_core:category ies_core:MilitaryOrganization .
    """)
    # its name is a Name categorised OrganizationName carrying the literal value
    assert ask(store, f"""
        <{DATA}RoyalNavy> ies_core:hasName ?n .
        ?n a ies_core:Name ;
           ies_core:category ies_core:OrganizationName ;
           ies_core:representationValue "Royal Navy"^^xsd:string .
    """)
    assert_matches_golden(store, HERE / "golden" / "organisations.ttl")
