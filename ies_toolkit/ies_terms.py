"""IES-terms adherence policy — the IES layer's override of the neutral hooks on
rdfs.Rdfs_Resource.

An IES "term" is a class or property declared by the IES ontology. This warns when a
class used as a type, or a predicate, is not an IES term. It is an IES Top/Core
concern, so it lives here (not in rdfs.py, which holds no IES knowledge):
IesTermsMixin is woven onto the IES root (Thing, via ThingMixin), so every IES
wrapper inherits it while the bare RDFS wrappers keep the rdfs.py no-op. Categories
pass silently - ies_core:category is a declared IES property and the concept is the
object, not a type.
"""
import logging

from .constants import RDF_TYPE, RDFS_COMMENT, RDFS_LABEL, RDFS_SUBCLASSOF, RDFS_SUBPROPERTYOF
from .ies_core_terms_generated import IES_CLASS_URIS as _CORE_C
from .ies_core_terms_generated import IES_PROPERTY_URIS as _CORE_P
from .ies_top_terms_generated import IES_CLASS_URIS as _TOP_C
from .ies_top_terms_generated import IES_PROPERTY_URIS as _TOP_P

logger = logging.getLogger(__name__)

_IES_CLASS_URIS = _TOP_C | _CORE_C
_IES_PROPERTY_URIS = _TOP_P | _CORE_P
# RDF/RDFS structural predicates the tool itself emits; not IES terms, but expected.
_STRUCTURAL_PREDICATES = frozenset({RDF_TYPE, RDFS_LABEL, RDFS_COMMENT, RDFS_SUBCLASSOF, RDFS_SUBPROPERTYOF})


class IesTermsMixin:
    """Overrides the neutral rdfs.py hooks to warn on a class/predicate that is not
    an IES term. Inherited by every IES wrapper (via ThingMixin on the root)."""

    def _check_type_term(self, uri):
        if str(uri) not in _IES_CLASS_URIS:  # str(): a URIRef is not set-equal to its str
            logger.warning(f"non-IES class used: {uri}")

    def _check_predicate_term(self, uri):
        uri = str(uri)
        if uri not in _IES_PROPERTY_URIS and uri not in _STRUCTURAL_PREDICATES:
            logger.warning(f"non-IES property used: {uri}")
