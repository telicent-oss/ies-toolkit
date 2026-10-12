# IES-Tool architecture — maintainer guide

This document explains how the Python wrapper classes are produced, and what to
do **when the ontology / SHACL changes** or **when you need to add custom code**.

## The big picture

The classes and builders in `ies_toolkit/` are **partly generated from the ontology
+ SHACL shapes** and **partly hand-written**. The generator reads `ies-top.ttl`,
`ies-core.ttl` and `ies-core-shacl.ttl` and emits (a) one wrapper class per
ontology class and (b) a relationship/reified-builder mixin per host class;
everything that cannot be derived is hand-written and *woven in*.

```
ies-top.ttl  ies-core.ttl  ies-core-shacl.ttl     ← sources of truth
        │
        │  python tools/generate_ies.py --target core   (top likewise)
        ▼
ies_core_generated.py            ← 100% GENERATED classes, never hand-edit
ies_core_relations_generated.py  ← 100% GENERATED relationship/reified builders
ies_core_terms_generated.py      ← 100% GENERATED terms: typed namespace (IesCore.Person) + URI registry
        │  builders import mixins from ↓
ies_core_custom.py   ies_top_custom.py    ← hand-written MIXINS (per-class + engines)
        │  re-exported by ↓
ies_core.py          ies_top.py           ← hand-written PUBLIC overlay (re-export only)
        └──────────────── public API ─────────────┘

(each target emits the same set: ies_top_generated.py / _relations_generated.py* / _terms_generated.py)
* top relations pending the top-shacl fix
```

Supporting hand-written modules that are **not** generated: `rdfs.py`,
`constants.py`, `rdf_plugin.py`, `rdflib_plugin.py`, `ies_terms.py`.

`ies-top-shacl.ttl` exists but is not yet consumed for `top` relations (its
exporter emits parenthesised, non-existent class IRIs — see "fail-fast" below).

### Why it is built this way

- **File-based separation.** Generated and hand-written code live in *separate
  files*. The generated files are overwritten wholesale, so there are no
  "protected regions" and nothing hand-written is ever clobbered.
- **Generation-time injection.** Per-class custom code is supplied as *mixins*
  the generator prepends to a class's bases (driven by small `TARGETS` registries).
  Keeps the inheritance graph intact and the custom code type-checkable.

## What is generated vs. hand-written

| File | Generated? | Contents |
|------|-----------|----------|
| `*_generated.py` | **Yes — do not edit** | One wrapper class per ontology class. |
| `*_relations_generated.py` | **Yes — do not edit** | One `{Host}_Relations` mixin per host class: the SHACL-derived relationship/reified builders (participation, lifecycle boundary, typed identifiers), woven into the host classes. |
| `*_terms_generated.py` | **Yes — do not edit** | This module's declared IES terms (classes + properties) in two forms: (a) a typed `DefinedNamespace` (`IesCore` / `IesTop`) — attribute access → `URIRef` (`IesCore.Person`), unknown term raises; (b) `IES_CLASS_URIS` / `IES_PROPERTY_URIS` frozensets (the URI registry) consumed by `ies_terms.py` for the non-IES warning. Base URI is the single-source constant. |
| `*_custom.py` | No (hand-written) | **Mixins**: custom behaviour for *specific* classes + the hand-written *engines* the generated builders call. |
| `ies_terms.py` | No (hand-written) | **IES-terms policy** (`IesTermsMixin`): unions the per-module registries and overrides the neutral `rdfs.py` hooks to warn on a non-IES class/predicate. Woven onto the IES root via `ThingMixin`. |
| `ies_core.py` / `ies_top.py` | No (hand-written) | **Public overlay**: re-exports the generated classes and the typed namespace (`IesCore` / `IesTop`). No behaviour, no monkey-patching. |
| `constants.py`, `rdfs.py`, `rdf_plugin.py`, `rdflib_plugin.py` | No | Base infrastructure — **no IES knowledge**, with one deliberate cosmetic exception: `RdfLibPlugIn` binds the `ies_top:`/`ies_core:`/`iso8601:` (and `data:`) prefixes by default so serialised output is readable — namespace strings only, no class/validation logic. `rdfs.py` exposes neutral `_check_type_term` / `_check_predicate_term` hooks (no-ops) that the IES layer overrides. |

### `ies_*.py` (overlay) vs. `ies_*_custom.py` (mixins)

Both are hand-written; the split is about the *shape* of the code. A **mixin**
attaches to one class the generator knows about; the **overlay** just re-exports
(`from .<target>_generated import *`, plus the licence header in `ies_top.py`).
There is no monkey-patching. Hierarchy-wide behaviour (e.g. SKOS `categories`) is
a mixin method (`ThingMixin._apply_categories`) plus a generated
`self._apply_categories(...)` call in each `__init__`.

### No hand-written type stubs

Every public method lives in real, type-hinted code — generated classes, generated
relations mixins, and hand-written mixins — so type checkers/IDEs get accurate
signatures from source. There is deliberately **no hand-written `.pyi`**.

## What the generator derives

### From the ontology (`ies-top.ttl` / `ies-core.ttl`)
- **Class list** — every `rdfs:Class` / `owl:Class`.
- **Class names** — the public wrapper name is the ontology local name, bare:
  `ies_core:Person` → `Person`, `ies_top:State` → `State`. The two RDFS roots keep
  an `Rdfs_` prefix (`Rdfs_Resource`, `Rdfs_Class`). Internally the generator keys
  every class on the module-qualified name (`IesCore_Person`, `IesTop_State`), so a
  name stays unique across modules and reconstructs its URI; `emit_name()` drops the
  `IesCore_`/`IesTop_` prefix only at emission (class defs, `__all__`, imports,
  `{Host}_Relations`). `TARGETS` config keys therefore use the qualified name.
  `validate_emit_names` (run from `load_graph`) fails generation fast if two classes
  would collapse to the same bare name, or a bare name is a Python keyword/builtin.
- **Inheritance** — from `rdfs:subClassOf`, full multiple inheritance, ordered
  most-derived-first so the MRO is valid.
- **Constructor style** — a class transitively descending from `ies_top:State`
  gets `_state_init` (with `start`/`finish`); everything else gets `_cls_init`.
- **`instance_type`** (what `.instantiate()` mints) — from `<member> ies_top:powertype <SetClass>`.
- **Dropped foreign parents** — foreign-namespace parents with no wrapper (e.g. `geosparql:Feature`).
- **Terms** (`*_terms_generated.py`) — this module's declared classes
  (`rdfs:Class`/`owl:Class`) and properties (`rdf:Property`), namespace-filtered,
  emitted two ways from one term list: a `DefinedNamespace` (`IesCore` / `IesTop`)
  for symbolic, typo-safe access (`IesTop.isPartOf` → `URIRef`; re-exported via the
  overlay), and `IES_CLASS_URIS` / `IES_PROPERTY_URIS` frozensets for the non-IES
  warning (which needs the class/property split the flat namespace can't give). Note
  the two forms: `IesCore.Person` is the class's *URI*; `Person` is the *wrapper
  class* you instantiate.

**Non-IES warning (layering).** `rdfs.py` and the store hold **no IES knowledge**:
`rdfs.py` calls two neutral no-op hooks (`_check_type_term` on each `rdf:type` in
`__init__`/`add_type`, `_check_predicate_term` in `add_literal`). The IES policy is
`IesTermsMixin` in `ies_terms.py`, which unions the per-module registries and
overrides those hooks to warn on a non-IES class/predicate. It is woven onto the IES
root by having `ThingMixin` inherit it — so **every IES wrapper** (all descend from
`Thing`) warns, while the bare RDFS wrappers keep the no-op. Structural
predicates (`rdf:type`/`rdfs:label`/`comment`/`subClassOf`/`subPropertyOf`) are
exempt; categories are exempt (`ies_core:category` is a declared property and the
concept is the object, not a type).

### From the SHACL shapes (`ies-core-shacl.ttl`)
The relationship/reified builders in `*_relations_generated.py`:
- **`sh:targetClass` property shapes** → per-host typed builders. Two families:
  - **Reified nodes** (participation, lifecycle boundary): mint the reified node
    and wire its shaped edges to the typed endpoints. Participation host = the
    `isPartOf` target that descends from `ies_core:Activity` (always wired). The
    remaining (non-host) edges are the participant/entity: **exactly one → a
    required arg; several → all optional** (a choice of participant type, e.g.
    `add_participation_in_governance(person=None, organization=None)` vs the single
    `add_person_in_communication(person)`). e.g. `Account.add_account_holder(person=None, …)`,
    `LivingOrganism.add_birth_state()`.
  - **Representation/identifier** (`hasName`/`isIdentifiedBy`/`isRepresentedAs`,
    detected by the predicate's range descending from `Representation`):
    `host.add_<target>(value)` delegating to `ThingMixin._add_representation`.
    Two sub-cases: a real `Representation` subclass → `rdf:type` it
    (`Country.add_iso3166_1_alpha_3`); a **SKOS concept** → `rdf:type` the range
    root (`Identifier`/`Name`) + `ies_core:category <concept>`
    (`HumanMadeSystem.add_part_number`).
- **`sh:targetSubjectsOf`/`sh:targetObjectsOf`** → property domain/range, incl.
  the literal-vs-object split (a property with a domain but no object-range is
  literal-valued).
- **Specialisation projection**: one shared engine per reified root
  (`ActivityMixin.add_participant`, `ThingMixin.add_*`) + a generated
  `add_<snake(subclass)>` per descendant of that root.

The dry-run report `tools/shacl_report.py` prints the full builder inventory
without touching any generated file.

## What is hand-configured in the generator (`TARGETS`)

One entry per target in `tools/generate_ies.py`:

| Config key | Purpose |
|-----------|---------|
| `full_mi` | Emit all parents vs. only the first. Both targets use `True`. |
| `custom_module` | Which `*_custom.py` to import mixins from. |
| `shacl_files` | SHACL files to read for the relations layer (core: `ies-core-shacl.ttl`). |
| `reified_engine` | The hand-written base mixin the generated `{Host}_Relations` mixins inherit (`ReifiedBuilderMixin`). |
| `relations_out` | Output path for `*_relations_generated.py`. |
| `terms_out` | Output path for `*_terms_generated.py` (this module's terms: typed `DefinedNamespace` + IES class/property URI registry). |
| `mixins` | `{ClassName: (MixinName, "extend" \| "replace")}` — per-class custom-code registry. |
| `construction_mixins` | `{Ancestor: {params, call, replaces_temporal}}` — inject constructor params + a call into the generated `__init__` of an ancestor **and all its descendants** (see Kind 2). |
| `instance_type_extra` | `instance_type` values the ontology omits from `powertype`. |
| `no_temporal` | State-descended classes that suppress `start`/`finish`. |

Module-level `FOREIGN_DROP_PREFIXES` lists foreign namespaces to drop.

## Fail-fast on ontology / SHACL problems

Generation **raises** rather than papering over an inconsistency; the maintainer
fixes it **at source** (the ontology or the SHACL exporter), never in the tool:

- **Undeclared predicate** a builder would emit → `validate_relation_predicates`
  raises (e.g. a SHACL path in the wrong namespace), with a same-local-name hint.
- **Undeclared host/minted class** → `validate_relation_classes` raises (e.g. a
  `sh:targetClass` that is a SKOS concept, not a class).
- **A constrained shape targeting an undeclared class** → `validate_shacl_targets`
  raises (an orphan shape, or a class missing from the ontology — it could never
  yield a valid builder, so it fails here rather than falling through silently).
- **Unparsable SHACL** → `load_shacl` raises (no silent empty output).
- **Namespace drift** → `_validate_namespaces` (in `load_graph`) raises if the
  ontology's declared `ies_top` / `ies_core` `@prefix` disagrees with the namespace
  constants. `ies_toolkit/constants.py` holds the single definition (`IES_TOP` /
  `IES_CORE`); the generator imports them, so a version bump is one edit there,
  confirmed against the ontology on the next generation.

---

## Maintainer workflow: when the ontology / SHACL changes

1. **Regenerate** (each target's default run emits the classes, the relations file
   and the terms file — typed namespace + URI registry):
   ```bash
   python tools/generate_ies.py --target core
   python tools/generate_ies.py --target top
   ```
   `--relations` regenerates only the relations file plus the terms file
   (both are quick; useful while iterating).
2. **If generation raises**, it found an inconsistency — fix the `.ttl` / SHACL at
   source (undeclared predicate, non-class `targetClass`, parse error). Do **not**
   code around it in the generator.
3. **Run the tests:** `pytest tests/ -q` (the drift guards fail if a committed
   generated file — classes, relations or terms — doesn't match a fresh generation).
4. **Commit** the edited `.ttl` / SHACL *and* the regenerated files together.

Most ontology edits need nothing more. Touch `TARGETS` only for: a new class
needing custom code (a mixin), a `SetOf…` without `powertype` (`instance_type_extra`),
a foreign parent to keep (`py_name()` + a wrapper), or a new construction-param
subtree (`construction_mixins`).

---

## Maintainer workflow: adding custom code

All hand-written behaviour is a **mixin** in a `*_custom.py` module. There are two
kinds, distinguished by whether the generator's `render` (which writes each
`__init__`) has to know about it.

### Kind 1 — API mixins (the common case; `TARGETS["mixins"]` only)

A mixin that **adds methods**. `render` just prepends it to the bases.
Examples: `RecurringTimespanMixin`, the Tuple mixins, `ThingMixin`'s
`add_name`/`add_identifier`/`add_representation`, `StateMixin`'s relationship +
period methods (`is_part_of`, `starts_in`, `put_in_period`, …), `ActivityMixin`'s
generic `add_participant`, `LivingOrganismMixin`'s `add_birth`/`add_death`/`add_lifespan`.

To add one: write the mixin, register it under `TARGETS[target]["mixins"]` as
`("MixinName", "extend"|"replace")`, regenerate, test.
- **`extend`** — class keeps its generated `__init__`; mixin only adds methods.
- **`replace`** — mixin owns the whole class body incl. `__init__` (only
  `StateMixin` → `IesTop_State` today; the generated class emits `pass`).

**No load-time circular imports.** A `*_custom.py` module must not `import` from
its `*_generated.py` at module top level. Import a generated class *inside* the
method if needed at runtime (see `ies_top_custom._new_state`). The same lazy trick
lets an `ies_top` mixin mint `ies_core` classes (`ThingMixin.add_name`).

### The generated relations layer (also Kind 1, but generated)

`ReifiedBuilderMixin` (hand-written in `ies_core_custom.py`) provides the
primitives (`_mint_node`, `_wire`); the generated `{Host}_Relations` mixins
inherit it and hold the typed builders. `ActivityMixin` provides the generic
`add_participant` engine that the generated specialisations parallel. You don't
hand-write the `{Host}_Relations` mixins — the SHACL emits them.

### Kind 2 — construction params (`render`-coupled)

Behaviour that must run *at construction* and be exposed as a **constructor
keyword argument**. Two mechanisms:

1. **Load-bearing primitives baked into `render`** — `_state_init` (backs
   `start`/`finish`) and `_apply_categories` (backs `categories`). `render`'s
   `__init__` template emits hardcoded calls to these, so they must exist.
2. **`construction_mixins` config** — the general, config-driven way to add
   construction params to a class **and all its descendants** without editing
   `render`. An entry is `{Ancestor: {params, call, replaces_temporal}}`:
   `render` appends `params` to the generated `__init__` signature and emits
   `call` in the body. `replaces_temporal: True` drops `start`/`finish` from the
   signature (the params supersede them) and calls `_state_init` with no bounds.
   Today: `IesCore_LivingOrganism` → `date_of_birth`/`place_of_birth`/
   `date_of_death`/`place_of_death` + `self.add_lifespan(...)`, replacing
   `start`/`finish` for the LivingOrganism subtree.

So a new construction-param subtree is normally a `construction_mixins` entry
(config), not a `render` edit — the earlier "you must edit `render`" applies only
to the two baked-in primitives.

---

## Bounding a State in time — two patterns

There are deliberately **two** ways a start/finish is attached to a period, and a
maintainer will see both:

1. **Non-timespan State** (person, rank, activity, …) → **mint a bounding State**.
   `StateMixin.starts_in` / `finishes_in` create a separate boundary `ies_top:State`
   that `isAStartOf`/`isAFinishOf` the state and `isPartOf` the `ParticularPeriod`.
   The duration state itself is *not* linked to the period.
2. **Timespan** (e.g. `RecurringTimespan`) → **link the period directly**.
   `RecurringTimespanMixin.add_bounding_start` / `add_bounding_finish` make the
   `ParticularPeriod` itself `isAStartOf`/`isAFinishOf` the timespan, with no
   intermediate State.

The divergence is intentional, not an inconsistency: a `Timespan` *is* a period, so
a `ParticularPeriod` can be a temporal part of it at any position (including its
start/finish); a non-timespan State cannot be a temporal part of an instant period,
so it needs a bounding State to carry the `isPartOf period` link. Rule of thumb:
**bounding a Timespan → period linked directly; bounding anything else → mint a
_bounding_ State.**

---

## Testing

Layout under `tests/` (run everything with `pytest tests/ -q`; `run_tests.sh` and
CI do this):

- `tests/unit/` — behaviour of the classes + mixins through the public API
  (`test_ies_core`, `test_ies_top`, `test_rdfs`, `test_recurring_timespan`,
  `test_canonical_patterns`, `test_store` (store conveniences),
  `test_ies_terms` (the non-IES class/predicate warnings),
  `test_custom_plugin` (the `RDFPlugin` contract end-to-end)).
- `tests/generator/` — meta-tests of the generator: **drift guards** (committed
  `*_generated.py`, the relations file and the terms file must each equal a
  fresh generation),
  class faithfulness (bases are real ontology parents; constructor style matches
  State-descent), `instance_type`/`powertype`, and **SHACL faithfulness** — every
  constrained SHACL shape is either realized as a builder or listed in a
  `KNOWN_UNREALIZED` ledger (each entry a recorded reason), so a new/changed shape
  that is neither trips the test for triage rather than being silently dropped.
- `tests/examples/falklands/` — real-world acceptance examples; each is a self-
  contained module + colocated `data/` (CSV) + `golden/` (expected N-Triples-as-
  TTL).

**Assertions on produced RDF use SPARQL**, via `tests/rdf_assert.py`:
- `ask(store, where)` / `count(store, where)` — the `where` is a brace-free
  pattern (the `ASK`/`SELECT {}` wrapper is added), so use multi-line `f"""` and
  interpolate `{var}` without doubling braces.
- `assert_matches_golden(store, path)` — whole-graph acceptance; the golden is
  readable Turtle, compared as a triple *set* (order-independent; exact given
  pinned URIs and no blank nodes). Regenerate goldens with `UPDATE_GOLDENS=1 pytest …`.
- Gotcha: string literals are stored `^^xsd:string`; rdflib SPARQL does not equate
  a bare `"x"` with `"x"^^xsd:string` — match with `"x"^^xsd:string` or
  `FILTER(STR(?v)="x")`.

Example tests **pin all URIs** so graphs are deterministic. `test_generated`
(generator meta-tests) stays plain Python asserts — it checks source/structure,
not a graph.

## Quick reference

```bash
# Regenerate after an ontology / SHACL / generator change (emits classes + relations + terms)
python tools/generate_ies.py --target core
python tools/generate_ies.py --target top

# Relations file + terms only (fast iteration); dry-run builder inventory
python tools/generate_ies.py --relations --target core
python tools/shacl_report.py

# Refresh example golden files after an intended output change
UPDATE_GOLDENS=1 python -m pytest tests/examples

# Test everything (includes the drift guards)
pytest tests/ -q
```

| I want to… | Edit |
|-----------|------|
| Change what classes exist / their hierarchy | the `.ttl` ontology, then regenerate |
| Change a class's relationships/builders | the SHACL shapes, then regenerate (`--relations` while iterating) |
| Add a method/builder to one class (Kind 1) | a mixin in `*_custom.py` + register in `TARGETS[…]["mixins"]` |
| Add a method to every Thing (Kind 1) | a method on `ThingMixin` |
| Replace one class's constructor | a `"replace"`-mode mixin |
| Add constructor params to a class + its descendants | a `construction_mixins` entry (no `render` edit) |
| Fix a missing `instance_type` | `TARGETS[…]["instance_type_extra"]` |
| Resolve a generation error | fix the ontology / SHACL at source (never code around) |
| Never | edit any `*_generated.py` by hand |

## Design note: generating a `.pyi` (a future direction)

There is a known alternative to the "typed real `.py`, no stub" design — generate
a `.pyi` and simplify the runtime so construction customisation no longer touches
`render` at all. `construction_mixins` already moves most construction params to
config (only `_state_init`/`_apply_categories` remain baked in), so the pressure
is lower than before. The full analysis and the **trigger** for revisiting are in
[generated-pyi-future-direction.md](generated-pyi-future-direction.md).
