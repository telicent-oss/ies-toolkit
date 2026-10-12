from __future__ import annotations

from .constants import (
    RDF_TYPE,
    RDFS_CLASS,
    RDFS_COMMENT,
    RDFS_LABEL,
    RDFS_RESOURCE,
    RDFS_SUBCLASSOF,
    XSD_STRING,
    is_uri,
)
from .rdf_plugin import RDFPlugin

__license__ = """
Copyright TELICENT LTD

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# Module-level default store
_default_store = None


def set_default_store(store: RDFPlugin):
    """
    Set the default RDF store for all RDFS and IES objects.

    Args:
        store (RDFPlugin): The RDF store to use as default

    Example:
        >>> from ies_toolkit.rdflib_plugin import RdfLibPlugIn
        >>> from ies_toolkit import rdfs
        >>> store = RdfLibPlugIn()
        >>> rdfs.set_default_store(store)
    """
    global _default_store
    _default_store = store


def get_default_store() -> RDFPlugin:
    """
    Get the default RDF store.

    Returns:
        RDFPlugin: The default RDF store

    Raises:
        RuntimeError: If no default store has been set
    """
    if _default_store is None:
        raise RuntimeError("No default store set. Call rdfs.set_default_store() first or pass store parameter.")
    return _default_store


class Rdfs_Resource:
    """
    A Python wrapper class for RDFS Resources
    """
    def __init__(
            self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None
    ):
        """
            Instantiate the RDFS Resource

            Args:
                store (RDFPlugin): the RDF data store plugin (optional if a default store is set)
                uri (str): the URI of the RDFS Resource
                classes (list): the types to instantiate

            Returns:
                Rdfs_Resource:
        """
        if classes is None:
            classes = [RDFS_RESOURCE]
        if store is None:
            store = get_default_store()
        self._store = store
        if not uri:
            self._uri = self._store.generate_data_uri()
        else:
            self._uri = uri

        for cls in classes:
            self._check_type_term(cls)
            self._store.add_triple(subject=self._uri,predicate=RDF_TYPE,obj=cls,is_literal=False)
        self._classes = classes

    def _check_type_term(self, uri):
        """Extension hook, called for each class used as a type. No-op here; a
        subclass may override to validate the URI against a set of known terms."""

    def _check_predicate_term(self, uri):
        """Extension hook, called for each predicate. No-op here; a subclass may
        override to validate the URI against a set of known terms."""

    def _cls_init(self,classes,fallback_class,store,uri):
        if classes is None:
            classes = [fallback_class]
        Rdfs_Resource.__init__(self, store=store, uri=uri, classes=classes)

    @property
    def store(self):
        return self._store

    @property
    def uri(self):
        return self._uri

    @property
    def labels(self):
        """The rdfs:label values on this resource."""
        return self._store.query_sp(self._uri, RDFS_LABEL)

    @property
    def comments(self):
        """The rdfs:comment values on this resource."""
        return self._store.query_sp(self._uri, RDFS_COMMENT)

    def add_type(self, uri):
        self._check_type_term(uri)
        self._store.add_triple(subject=self.uri, predicate=RDF_TYPE, obj=uri,is_literal=False)

    # Adds a triple where the object is a literal
    def add_literal(self, predicate: str, obj: str, literal_type: str = XSD_STRING):
        self._check_predicate_term(predicate)
        return self._store.add_triple(self._uri, predicate, obj, is_literal=True, literal_type=literal_type)

    def add_label(self, label):
        self.add_literal(predicate=RDFS_LABEL, obj=label)

    def add_comment(self, comment):
        self.add_literal(predicate=RDFS_COMMENT, obj=comment)


class Rdfs_Class(Rdfs_Resource):
    """
        A Python wrapper class for RDFS Class
    """
    def __init__(
            self, store: RDFPlugin | None = None, uri: str | None = None, classes: list[str] | None = None
    ):
        """
            Instantiate the RDFS Class

            Args:
                store (RDFPlugin): the RDF data store plugin (optional if a default store is set)
                uri (str): the URI of the RDFS Class
                classes (list): the types to instantiate (default is rdfs:Class)

            Returns:
                Rdfs_Class:
        """
        self._cls_init(classes,RDFS_CLASS,store,uri)
        self.instance_type = Rdfs_Resource

    def instantiate(self, uri: str | None = None):
        if uri is None or uri == "":
            uri = self._store.generate_data_uri()
        if not is_uri(uri):
            raise ValueError(f"Invalid URI {uri!r} passed into instantiate")
        return self.instance_type(self._store, str(uri), [self._uri])

    def add_sub_class(self, sub_class: Rdfs_Class):
        self._store.add_triple(subject=sub_class.uri,predicate=RDFS_SUBCLASSOF,obj=self._uri,is_literal=False)
