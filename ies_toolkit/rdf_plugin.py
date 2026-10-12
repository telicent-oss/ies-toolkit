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


class RDFPlugin:

    def generate_data_uri(self,uri_root = None):
        raise NotImplementedError

    def set_classes(self, classes: set):
        raise NotImplementedError

    def set_properties(self, properties: set):
        raise NotImplementedError

    def clear_triples(self):
        raise NotImplementedError

    def get_rdf(self, format: str | None = None, clear: bool = False) -> str:
        raise NotImplementedError

    def add_prefix(self, prefix: str, namespace: str):
        raise NotImplementedError

    def save_rdf(self, path, format: str | None = None, clear: bool = False):
        raise NotImplementedError

    def get_reporting(self) -> str:
        raise NotImplementedError

    def query_sp(self, subject: str, predicate: str) -> list:
        raise NotImplementedError

    def in_graph(self, subject: str, predicate: str, obj: str, is_literal: bool,
                 literal_type: str | None = None) -> bool:
        raise NotImplementedError

    def add_triple(self, subject: str, predicate: str, obj: str, is_literal: bool, literal_type: str | None = None):
        raise NotImplementedError

    def delete_triple(self, subject: str, predicate: str, obj: str, is_literal: bool = False,
                      literal_type: str | None = None) -> bool:
        raise NotImplementedError

    @property
    def default_data_namespace(self) -> str:
        raise NotImplementedError

    @default_data_namespace.setter
    def default_data_namespace(self, value: str):
        raise NotImplementedError

    def can_validate(self) -> bool:
        raise NotImplementedError

    def get_warnings(self):
        raise NotImplementedError

    def make_results_list_from_query(self, query: str, sparql_var_name: str):
        """
        Pulls out individual variable from each row returned from sparql query. It's a bit niche, I know.

        Args:
            query (str): The query
            sparql_var_name (str): The SPARQL var name
        """
        raise NotImplementedError


    def __run_sparql_query(self, query: str):
        """
        Runs a SPARQL query on the data - DOES NOT WORK ON plugins (yet)

        Args:
            query (str): The query to run
        """
        raise NotImplementedError


    @property
    def supported_rdf_serialisations(self) -> list:
        raise NotImplementedError

    @property
    def deletion_supported(self) -> bool:
        raise NotImplementedError
