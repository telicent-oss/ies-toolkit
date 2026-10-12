import logging
from pathlib import Path

import shortuuid
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.term import Identifier

from .constants import IES_CORE, IES_TOP, ISO_8601, VALID_XSD_DATATYPES, XSD_STRING, is_uri
from .rdf_plugin import RDFPlugin


def _validate_uri(value, role: str, method: str):
    """Raise ValueError unless value is a scheme-prefixed URI with no whitespace."""
    if not is_uri(value):
        raise ValueError(f"Invalid URI {role} {value!r} passed into {method}")

_FORMAT_BY_SUFFIX = {
    ".ttl": "turtle", ".turtle": "turtle", ".n3": "n3", ".nt": "nt",
    ".jsonld": "json-ld", ".json": "json-ld", ".xml": "xml", ".rdf": "xml",
    ".trig": "trig",
}

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

logger = logging.getLogger(__name__)

class RdfLibPlugIn(RDFPlugin):

    def __init__(self,uri_base="http://example.org/rdf/"):
        self.graph = Graph()
        self.uuid = shortuuid.uuid()
        self.uuid_counter = 0
        self.uri_base=uri_base
        # Bind readable prefixes for serialisation
        self.add_prefix("data", uri_base)
        self.add_prefix("ies_top", IES_TOP)
        self.add_prefix("ies_core", IES_CORE)
        self.add_prefix("iso8601", ISO_8601)

    def generate_data_uri(self,uri_root = None):
        """Mint a fresh data URI. Not thread-safe: the counter increment is non-atomic."""
        if uri_root is None or uri_root == "":
            uri_root = f"{self.uri_base}{self.uuid}"
        self.uuid_counter = self.uuid_counter + 1
        return f"{uri_root}{self.uuid_counter}"

    def set_classes(self, classes: set):
        raise NotImplementedError

    def set_properties(self, properties: set):
        raise NotImplementedError

    def clear_triples(self):
        self.graph = Graph()

    def get_rdf(self, format: str | None = None, clear: bool = False) -> str:
        rdf = self.graph.serialize(format=format)
        if clear:
            self.clear_triples()
        return rdf

    def add_prefix(self, prefix: str, namespace: str):
        """Bind a namespace prefix for serialisation, e.g.
        add_prefix("ex", "http://example.org/"). A trailing colon on the prefix
        is accepted."""
        self.graph.namespace_manager.bind(prefix.rstrip(":"), Namespace(namespace),
                                          override=True, replace=True)

    def save_rdf(self, path, format: str | None = None, clear: bool = False):
        """Serialise the graph to a file. The format is inferred from the file
        extension when not given, defaulting to Turtle. With clear=True the graph
        is emptied after writing (to serialise large data in batches). Returns the
        path."""
        if format is None:
            format = _FORMAT_BY_SUFFIX.get(Path(path).suffix.lower(), "turtle")
        self.graph.serialize(destination=str(path), format=format, encoding="utf-8")
        if clear:
            self.clear_triples()
        return path

    def get_reporting(self) -> str:
        raise NotImplementedError

    def query_sp(self, subject: str, predicate: str) -> list:
        """Object values (as strings) of every triple with this subject and
        predicate."""
        return [str(o) for o in self.graph.objects(URIRef(str(subject)), URIRef(str(predicate)))]

    @property
    def default_data_namespace(self) -> str:
        """The namespace new data URIs are minted under (used by
        generate_data_uri). Settable."""
        return self.uri_base

    @default_data_namespace.setter
    def default_data_namespace(self, value: str):
        self.uri_base = value
        self.add_prefix("data", value)


    def in_graph(self, subject: str, predicate: str, obj: str, is_literal: bool,
                 literal_type: str | None = None) -> bool:
        _validate_uri(subject, "subject", "in_graph")
        _validate_uri(predicate, "predicate", "in_graph")
        obj_node: Identifier
        if is_literal:
            if literal_type is None or literal_type not in VALID_XSD_DATATYPES:
                literal_type = XSD_STRING
            obj_node = Literal(obj, datatype=literal_type)
        else:
            _validate_uri(obj, "object", "in_graph")
            obj_node = URIRef(obj)
        return (URIRef(str(subject)), URIRef(str(predicate)), obj_node) in self.graph

    def add_triple(self, subject: str, predicate: str, obj: str, is_literal: bool, literal_type: str | None = None):
        _validate_uri(subject, "subject", "add_triple")
        _validate_uri(predicate, "predicate", "add_triple")
        if is_literal:
            if literal_type is None:
                literal_type = XSD_STRING  # None -> default silently
            elif literal_type not in VALID_XSD_DATATYPES:
                logger.warning(f"Invalid datatype {literal_type} - reverting to XSD:string")
                literal_type = XSD_STRING
            self.graph.add((URIRef(str(subject)), URIRef(str(predicate)), Literal(obj, datatype=literal_type)))
        else:
            _validate_uri(obj, "object", "add_triple")
            self.graph.add((URIRef(str(subject)), URIRef(str(predicate)), URIRef(obj)))

    def delete_triple(self, subject: str, predicate: str, obj: str,
                      is_literal: bool = False, literal_type: str | None = None) -> bool:
        """Remove a triple. For a literal object the datatype must match how it was
        stored (add_triple defaults to xsd:string), so the same resolution is used
        here. Returns True if the triple was present."""
        _validate_uri(subject, "subject", "delete_triple")
        _validate_uri(predicate, "predicate", "delete_triple")
        obj_node: Identifier
        if is_literal:
            if literal_type is None or literal_type not in VALID_XSD_DATATYPES:
                literal_type = XSD_STRING
            obj_node = Literal(obj, datatype=literal_type)
        else:
            _validate_uri(obj, "object", "delete_triple")
            obj_node = URIRef(obj)
        triple = (URIRef(str(subject)), URIRef(str(predicate)), obj_node)
        existed = triple in self.graph
        self.graph.remove(triple)
        return existed

    def can_validate(self) -> bool:
        raise NotImplementedError

    def get_warnings(self):
        raise NotImplementedError

    @property
    def supported_rdf_serialisations(self) -> list:
        raise NotImplementedError

    @property
    def deletion_supported(self) -> bool:
        return True

