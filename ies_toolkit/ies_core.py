"""IES-Core wrapper classes.

The class hierarchy and all behaviour are generated from ies-core.ttl /
ies-top.ttl into ies_core_generated.py (regenerate with tools/generate_ies.py),
with custom methods supplied as mixins in ies_core_custom.py / ies_top_custom.py.
This module just re-exports the generated classes as the public ies_core API.
"""
from .ies_core_generated import *  # noqa: F401,F403 - re-export generated wrapper classes
from .ies_core_terms_generated import IesCore  # noqa: F401 - typed namespace (IesCore.Person)
