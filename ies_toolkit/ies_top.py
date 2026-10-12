"""IES-Top wrapper classes.

The class hierarchy is generated from ies-top.ttl into ies_top_generated.py
(regenerate with: python tools/generate_ies.py --target top). The custom
behaviour that cannot be derived from the ontology - the ies:State temporal
engine and the Tuple place logic - lives in ies_top_custom.py as mixins that the
generator weaves into the generated classes. This module re-exports the
generated classes as the public ies_top API.
"""
from .ies_top_generated import *  # noqa: F401,F403 - re-export generated wrapper classes
from .ies_top_terms_generated import IesTop  # noqa: F401 - typed namespace (IesTop.isPartOf)

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
