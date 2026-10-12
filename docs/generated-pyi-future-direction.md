# Design note: generating a `.pyi` stub (a future direction)

**Status:** Deferred — not adopted. Revisit when the trigger below is hit.

This records an architecture option we deliberately did *not* take yet, plus the
signal that should make us reconsider, so the decision isn't re-litigated from
scratch and the trigger is recognised when it arrives.

## Context — where we are now

The public API lives in **real, type-hinted code**: the generated
`*_generated.py` classes plus the hand-written mixins in `*_custom.py`. There is
**no `.pyi` stub.** Both static tools (IDE, mypy) *and* runtime introspection
(`inspect.signature`, `help()`) read accurate signatures directly from the `.py`,
and nothing can drift (a hand-written stub previously drifted and produced a real
bug — `add_name(name=…)` raised `TypeError` because the stub lied).

The cost of this design is that mixins come in **two kinds** (see
[architecture.md](architecture.md) → "when adding custom code"):

- **Kind 1 — API mixins** (the common case): add methods users call. Registered
  in `TARGETS["mixins"]` only; the generator's `render` never changes.
- **Kind 2 — construction customisation** (load-bearing): back a constructor
  **keyword argument**. Two mechanisms:
  - **Baked-in primitives** — `_state_init` → `start`/`finish`,
    `_apply_categories` → `categories`. `render` hardcodes the call and the kwarg
    in the signature templates, so adding one of *these* still needs a `render`
    edit.
  - **`construction_mixins` config** — adds params + a construction call to a
    class and its descendants from `TARGETS` (incl. `replaces_temporal`, which
    drops `start`/`finish`), **without a `render` edit**. Today:
    `IesCore_LivingOrganism` → `date_of_birth`/`place_of_birth`/`date_of_death`/
    `place_of_death` + `add_lifespan(...)`.

  So most new construction kwargs are now config, not a template edit; only the
  two baked-in primitives still couple to `render`.

## The alternative

Have `generate_ies.py` emit a **generated** `.pyi`, make the runtime `__init__`
uniform (`**kwargs` + cooperative `super().__init__()` so mixins apply
themselves), and have the generator **derive each class's signature by
introspecting the registered mixins** instead of hardcoding `state_sig`/
`cls_sig`. The typed contract then lives in the generated stub; the runtime is
simple and pluggable.

The payoff: **Kind 2 collapses into Kind 1.** Adding a construction mixin updates
the stub automatically — no `render` template edit.

## Why deferred (it is a worse trade *today*)

- A generated `.pyi` over the *current* typed `.py` is **redundant** — it only
  earns its keep once the runtime `.py` is simplified to `**kwargs`.
- Going `**kwargs` **re-hides the real arguments from runtime introspection** —
  `inspect.signature` / `help()` would show `(**kwargs)`. A `.pyi` only helps
  *static* tools. That is exactly the regression we removed when we deleted the
  categories monkey-patch wrapper.
- It requires a cooperative-`super()` rewrite of the whole construction
  mechanism (ordering, leaf-only `rdf:type`, kwarg forwarding) **plus**
  signature-introspection in the generator — a lot of moving parts to avoid an
  occasional one-line edit.
- Construction kwargs still couple to `render` only for the two baked-in
  primitives (`start`/`finish`, `categories`); `construction_mixins` already
  absorbs the rest as config, so the recurring-friction pressure is lower.

## Trigger — switch when any of these is true

- **`render`'s signature templates need repeated editing** for new construction
  kwargs — i.e. the two baked-in primitives grow into a family that
  `construction_mixins` config can't cover. This recurring friction is the
  primary signal; `construction_mixins` has pushed it further off, so it now
  fires only if the *baked-in* set itself needs to grow.
- **`ies-top` / `ies-core` are split into separate distributable packages** — a
  generated stub is the clean way to declare the cross-package API surface.
- **A minimal/uniform runtime is wanted** for its own sake, and losing runtime
  `inspect`/`help()` fidelity is acceptable (types come from the stub).

When that happens, the generator already has the model needed to emit the `.pyi`;
the remaining work is the cooperative-`super()` runtime plus deriving signatures
from the mixins. Until then, the typed `.py` with no stub is simpler and strictly
better for runtime introspection.
