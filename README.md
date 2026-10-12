# IES Toolkit

[![Tests](https://github.com/telicent-oss/ies-toolkit/actions/workflows/python-test-build.yaml/badge.svg)](https://github.com/telicent-oss/ies-toolkit/actions/workflows/python-test-build.yaml)
[![Security](https://github.com/telicent-oss/ies-toolkit/actions/workflows/security.yml/badge.svg)](https://github.com/telicent-oss/ies-toolkit/actions/workflows/security.yml)

> **Alpha release.** This toolkit is built against IES Next RC1. Updates will be made as the ontology moves towards its final official release.

A Python library for building IES data.

Information Exchange Standard (IES) is a UK Government data-exchange standard: a 4D ontology specified in RDF.
It exists to enable compliant, interoperable data exchange — and the goal of this toolkit
is to make producing that data straightforward.

Formal ontologies can be hard to approach, because they are **constructional** rather than
like a traditional data model. Instead of defining entities with a fixed set of fields to
fill in, an ontology like IES gives you a small set of common objects that you assemble by
following well-defined patterns. That flexibility suits domains where requirements change
faster than a traditional schema can be re-engineered. But it also means that, without an
in-depth understanding of the underlying principles (4D, extensional, constructional), it is
easy to end up with structures that don't follow the patterns.

To counter this, we have collected together a number of conventions and helpers used across projects into
a single Python library, to help data engineers get started and encourage appropriate use of
the ontology. The IES patterns are encoded for you: the wrapper classes and their `add_*`
builders are generated directly from the [`ies-top`](https://github.com/IES-Org/ies-top) /
[`ies-core`](https://github.com/IES-Org/ies-core) ontologies, so the IES-correct structure is
the path of least resistance.

This is work in progress, and we want to hear from users about what is missing or not working,
and of course requests for new features. We will keep adding functionality as we identify the
need in real projects.

## Installation

```bash
pip install telicent-ies-toolkit

# From a source checkout, for development
pip install -e ".[dev]"
```

## Getting Started

> The RDF shown in these examples uses conventional prefixes (`data:` for the example data
> namespace; `ies_core:`/`ies_top:`/`iso8601:` for the IES associated namespaces) for readability.

### Basic Usage

Create an RDF data store and start building IES data.

```python
from ies_toolkit.rdflib_plugin import RdfLibPlugIn
from ies_toolkit.ies_core import Person

store = RdfLibPlugIn()

# Create a person, name them, and their birth
sandy = Person(store=store, uri="http://example.org/rdf/SandyWoodward")
sandy.add_name("Sandy Woodward")
sandy.add_birth(date_of_birth="1932-05-01")

print(store.get_rdf("ttl"))
```

This produces:

```turtle
data:SandyWoodward a ies_core:Person ;
    ies_core:hasName data:SandyWoodward_name_1 .

data:SandyWoodward_name_1 a ies_core:Name ;
    ies_core:representationValue "Sandy Woodward"^^xsd:string .

data:SandyWoodward_birth_2 a ies_core:BirthState ;
    ies_top:isAStartOf data:SandyWoodward ;
    ies_top:isPartOf iso8601:19320501 .

iso8601:19320501 a ies_core:ParticularPeriod ;
    ies_core:iso8601PeriodRepresentation "1932-05-01"^^xsd:string .
```

Here the toolkit mints the underlying IES structure:
- The class instantiation creates a `Person` with the supplied URI;
- `add_name` mints a `Name` node linked by `hasName`;
- `add_birth` mints a `BirthState` that `isAStartOf` the person and which `isPartOf` 
the `ParticularPeriod` of "1932-05-01".

You describe the domain in plain method calls; the toolkit builds the IES.

### Using a Default Store

To avoid passing the `store` parameter to every object, set a default store once:

```python
from ies_toolkit.rdflib_plugin import RdfLibPlugIn
from ies_toolkit.ies_core import Person, Organization
from ies_toolkit import rdfs

# Create an RDF store and set it as the default
store = RdfLibPlugIn()
rdfs.set_default_store(store)

# Now create objects without passing store=
sandy = Person(uri="http://example.org/rdf/SandyWoodward")
sandy.add_name("Sandy Woodward")

navy = Organization(uri="http://example.org/rdf/RoyalNavy")
navy.add_name("Royal Navy")

print(store.get_rdf("ttl"))
```

This produces:

```turtle
data:SandyWoodward a ies_core:Person ;
    ies_core:hasName data:SandyWoodward_name_1 .

data:SandyWoodward_name_1 a ies_core:Name ;
    ies_core:representationValue "Sandy Woodward"^^xsd:string .

data:RoyalNavy a ies_core:Organization ;
    ies_core:hasName data:RoyalNavy_name_1 .

data:RoyalNavy_name_1 a ies_core:Name ;
    ies_core:representationValue "Royal Navy"^^xsd:string .
```

You can still pass an explicit `store` to override the default — useful whenever more than
one graph is required, e.g. building multiple independent datasets in one program (e.g. for access control purposes), 
or giving each thread/worker its own store.

### Working with States and time

To time-bound a State, give a date/datetime and the tool builds the canonical structure for
you — it mints the `ParticularPeriod`, mints a **bounding state**, and adds
`bounding isAStartOf/​isAFinishOf self` + `bounding isPartOf period`:

```python
from ies_toolkit.rdflib_plugin import RdfLibPlugIn
from ies_toolkit.ies_top import State

store = RdfLibPlugIn()
employment = State(store=store, uri="http://example.org/rdf/emp1")

employment.starts_in("2024-03-02")      # mints emp1_start + the ParticularPeriod, adds isAStartOf
employment.finishes_in("2025-06-30")    # mints emp1_finish + the ParticularPeriod, adds isAFinishOf

print(store.get_rdf("ttl"))
```

This produces:

```turtle
data:emp1 a ies_top:State .

data:emp1_start a ies_top:State ;
    ies_top:isAStartOf data:emp1 ;
    ies_top:isPartOf iso8601:20240302 .

data:emp1_finish a ies_top:State ;
    ies_top:isAFinishOf data:emp1 ;
    ies_top:isPartOf iso8601:20250630 .

iso8601:20240302 a ies_core:ParticularPeriod ;
    ies_core:iso8601PeriodRepresentation "2024-03-02"^^xsd:string .

iso8601:20250630 a ies_core:ParticularPeriod ;
    ies_core:iso8601PeriodRepresentation "2025-06-30"^^xsd:string .
```

Use `put_in_period("2024-03-02")` when a state's lifetime falls **entirely within** a
single ParticularPeriod: it links *self* directly (`self isPartOf period`), rather than
minting separate start/finish bounding States. This is useful when there is vague knowledge about the precise start and finish of a state.

### Participations

A **participation** is a state of an entity taking part in an activity. Every activity
carries typed `add_<role>(…)` methods for its shaped roles, plus a generic
`add_participant` for any role that has no typed builder. How you supply the participating
entity depends on how it is involved in the activity — whether it is *wholly* involved
(`isTemporalPartOf`) or *partially* involved (`isPartOf`):

```python
from ies_toolkit.rdflib_plugin import RdfLibPlugIn
from ies_toolkit.ies_core import (
    Meeting, Create, Person, Organization,
)

store = RdfLibPlugIn()
fred = Person(store=store, uri="http://example.org/rdf/fred")
acme = Organization(store=store, uri="http://example.org/rdf/acme")

# 1. Wholly involved: the whole entity takes part.
#    e.g. a person attends a party.
party = Meeting(store=store, uri="http://example.org/rdf/party1")
party.add_attendance(fred)

# 2. Partially involved: only part of the entity is involved.
#    e.g. an organisation manufactures something — only part of its workforce did the work.
create = Create(store=store, uri="http://example.org/rdf/create1")
create.add_creator(organization=acme)

# 3. On behalf of: an entity is involved on behalf of a greater whole.
#    e.g. a person attends a meeting as a representative of a company.
meeting = Meeting(store=store, uri="http://example.org/rdf/meeting1")
meeting.add_attendance(person=fred, organization=acme)

# 4. A plain participant: for a role which is unknown: use the foundational method of
#    add_participant
party.add_participant(fred)

print(store.get_rdf("ttl"))
```

This produces one participation state per call — each typed by its role (`Attendance`,
`Creator`) or `Participation` for the generic method:

```turtle
data:fred a ies_core:Person .
data:acme a ies_core:Organization .

# 1. Wholly involved:
data:party1 a ies_core:Meeting .

data:party1_attendance_1 a ies_core:Attendance ;
    ies_top:isPartOf data:party1 ;
    ies_top:isTemporalPartOf data:fred .

# 2. Partially involved:
data:create1 a ies_core:Create .

data:create1_creator_2 a ies_core:Creator ;
    ies_top:isPartOf data:acme ;
    ies_top:isPartOf data:create1 .

# 3. On behalf of:
data:meeting1 a ies_core:Meeting .

data:meeting1_attendance_3 a ies_core:Attendance ;
    ies_top:isPartOf data:acme ;
    ies_top:isPartOf data:meeting1 ;
    ies_top:isTemporalPartOf data:fred .

# 4. A plain participant:
data:party1_participation_4 a ies_core:Participation ;
    ies_top:isPartOf data:party1 ;
    ies_top:isTemporalPartOf data:fred .

```

### Categories: taxonomic extension with SKOS

Most extensions to IES are **taxonomic** — narrower kinds of an existing concept (a more
specific type of `Vehicle`, say). IES
models these with [SKOS categories](https://www.w3.org/TR/skos-reference/) rather than RDF
subclassing, which it reserves for extensions that introduce genuinely *new semantics*. The
SKOS regime is:

- the extension is a `skos:Concept`, linked by `skos:broader` up to the IES class (or
  concept) it refines;
- every instance still carries a real IES `rdf:type` — its type is always an IES class;
- `ies_core:category` ties the instance to the concept.

So however much custom taxonomy you layer on, an instance's `rdf:type` always resolves to an
IES class every consumer understands. Every wrapper takes a `categories=` argument that adds
`ies_core:category`:

```python
from ies_toolkit.rdflib_plugin import RdfLibPlugIn
from ies_toolkit.ies_core import Vehicle

store = RdfLibPlugIn()
AMBULANCE = "http://example.org/vehicles#Ambulance"

# An instance keeps its IES rdf:type (Vehicle); ies_core:category ties it to the concept
ambulance_07 = Vehicle(store=store, uri="http://example.org/rdf/ambulance-07", categories=[AMBULANCE])

print(store.get_rdf("ttl"))
```

This produces (the instance keeps its IES `rdf:type`, with the extension attached as a category):

```turtle
data:ambulance-07 a ies_core:Vehicle ;
    ies_core:category <http://example.org/vehicles#Ambulance> .
```

### Plain RDF: labels and comments

Alongside the IES builders, every entity supports ubiquitous ordinary RDF/RDFS operations such as
`rdfs:label` and `rdfs:comment`.

```python
from ies_toolkit.rdflib_plugin import RdfLibPlugIn
from ies_toolkit.ies_core import Person

store = RdfLibPlugIn()
sandy = Person(store=store, uri="http://example.org/rdf/SandyWoodward")

sandy.add_label("Sandy Woodward")            # rdfs:label
sandy.add_comment("Royal Navy admiral")      # rdfs:comment

print(store.get_rdf("ttl"))
```

This produces:

```turtle
data:SandyWoodward a ies_core:Person ;
    rdfs:label "Sandy Woodward"^^xsd:string ;
    rdfs:comment "Royal Navy admiral"^^xsd:string .
```

### Referencing IES terms directly

Most data generation goes through the wrapper classes and their `add_*` builders. When you
need a raw term — building a triple by hand, or a SPARQL query — use the typed
namespaces `IesTop` / `IesCore`. Attribute access returns a `URIRef`, and a misspelt
term raises `AttributeError` rather than silently producing a wrong URI:

```python
from ies_toolkit.ies_top import IesTop
from ies_toolkit.ies_core import IesCore

store.add_triple(person.uri, IesTop.isPartOf, org.uri, is_literal=False)
IesCore.Person   # -> URIRef("http://purl.org/ies/core/v0/ont/Person")
IesCore.Persn    # -> AttributeError (typo caught)
```

(`IesCore.Person` is the class's *URI*; `Person` is the *wrapper class* you
instantiate to build one.)

### Large datasets

The whole graph is held in memory. For loads consuming a large amount of RAM, consider using
`clear=True`: it serialises the current triples and then empties the graph, so each
call returns only what was built since the last clear. N-Triples is line-based, so
you can stream batches to one file:

```python
store = RdfLibPlugIn()
with open("out.nt", "w") as f:
    for batch in batches:
        for record in batch:
            ...  # build IES objects against `store`
        f.write(store.get_rdf("nt", clear=True))
```

`save_rdf(path, clear=True)` writes to a file directly, but overwrites `path` each
call — give each batch its own filename if you use it that way.

The store is **not thread-safe** — `generate_data_uri` bumps a shared counter and the
in-memory graph assumes a single writer, so build on one thread. To use more cores,
give each thread/process its own `RdfLibPlugIn` and concatenate the output (each
instance mints URIs under its own unique prefix, so they won't collide).

## Architecture (for maintainers)

The wrapper classes are **partly generated** from `ies-top.ttl` / `ies-core.ttl`
and partly hand-written. If you are changing the ontology or adding custom
behaviour, read [docs/architecture.md](docs/architecture.md) first — it explains
the generation pipeline, the generated-vs-hand-written split, and the exact
steps to follow when the ontology changes or new custom code is needed.

```bash
# Regenerate the wrapper classes after an ontology change
python tools/generate_ies.py --target core
python tools/generate_ies.py --target top
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run a specific group (unit / generator / examples)
pytest tests/unit -v

# Or use the test script
./run_tests.sh
```
