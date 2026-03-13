# D5 Phase-Machine Summary 058

This note organizes the current `058/058B` proof-side picture for the `d=5`
boundary reset theorem.

It is meant to answer three questions:

1. what `058` actually improves,
2. what is now the cleanest theorem target,
3. what is proved, supported, or still open.

## Attribution note

The specific "phase-machine" viewpoint recorded here was first proposed in the
AI-assisted RoundY analysis by `GPT 5.4 / Codex` as a proof-side compression of
the `CJ` and boundary-reset behavior.

That is:

- the theorem object itself remains human-chosen and repo-standard,
- the adoption of this viewpoint into the project is a human research decision,
- but the explicit reframing from branchwise reset formulas to a small current
  phase scheduler was proposed in the AI-assisted working analysis around
  `057a-058`.

This note is just recording that provenance clearly in the repository.

## 1. The theorem object does not change

The theorem-side object stays

- `B = (s,u,v,layer,family)`
- `tau`
- `epsilon4 in {flat, wrap, carry_jump, other}`

No new theorem coordinate is being introduced.

Auxiliary quantities such as `rho`, `delta`, `Theta`, or `kappa` are proof
devices only.

## 2. What `057` had already achieved

Before `058`, the `CJ` branch had already been reduced to the flat-corner
lemma:

- on the `CJ` boundary, the zero-reset fiber is already explained,
- every noncarry `CJ` state lands in a flat successor with `delta = m-2`,
- so `CJ` follows if one proves the one-step flat-corner law.

This is the content of:

- [d5_CJ_branch_proof_reduction_056.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_CJ_branch_proof_reduction_056.md)
- [d5_CJ_uniform_proof_progress_057.md](./d5_CJ_uniform_proof_progress_057.md)
- [d5_CJ_flat_corner_support_057a/README.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/artifacts/d5_CJ_flat_corner_support_057a/README.md)

So `057` already compressed `CJ` from a future-window theorem to a tiny
auxiliary lemma.

## 3. What `058` improves

`058` says the `057` flat-corner lemma itself is a corollary of a smaller
current-state scheduler.

Define the active phase

- `Theta = q + s + v + layer mod m`

On the frozen checked range, the current event is an exact function of
`(Theta, s, c)` with `c = 1_{q=m-1}`:

- `Theta = 0 -> wrap`
- `Theta = 1 -> carry_jump`
- `Theta = 2 -> other (1,0,0,0)` iff `c=1`, else flat
- `Theta = 3 -> other (0,0,1,0)` on the checked `(c,s)` condition, else flat
- `Theta >= 4 -> flat`

This is the content of:

- [d5_CJ_phase_event_reduction_058.md](./d5_CJ_phase_event_reduction_058.md)
- [d5_CJ_phase_event_reduction_058.tex](./d5_CJ_phase_event_reduction_058.tex)
- [d5_CJ_theta_event_law_058.json](../checks/d5_CJ_theta_event_law_058.json)

So `058` improves the proof burden from:

- prove flat-corner law,

to:

- prove one small phase-event law.

Then:

- phase-event law -> flat-corner law,
- flat-corner law -> `CJ`.

## 4. What `058B` adds

`058B` sharpens the interpretation.

The important point is not merely that `Theta` helps `CJ`; it is that the
checked boundary/reset behavior appears governed by one tiny phase/corner
machine.

The internal checked observations are:

- the phase advances by `+1 mod m` each step,
- `wrap`, `carry_jump`, and the two `other` subtypes sit at the first few
  phases,
- the flat branch fills the remaining phases,
- the unique corner effect is exactly what creates the short reset in `CJ`.

So the proof problem is no longer best described as:

- prove `CJ` and `OTH` separately,

but rather as:

- prove one uniform odd-`m` phase/corner machine,
- then read `CJ` and likely `OTH` off as corollaries.

This is the real conceptual jump.

See:

- [d5_phase_align_058b.md](./d5_phase_align_058b.md)
- [d5_058b_boundary_reset_assessment_rebuilt_20260313.md](./d5_058b_boundary_reset_assessment_rebuilt_20260313.md)

## 4A. Stronger checked-scope formulation from the rebuilt `058B` note

The rebuilt assessment strengthens the wording of the checked evidence.

On the frozen `047` dataset, restricting to rows with a recorded successor in
their `source_u` trace block, the checked scope is:

- `216` transitions for `m=5`
- `1212` transitions for `m=7`
- `3952` transitions for `m=9`
- `9780` transitions for `m=11`

for a total of `15,160` checked one-step transitions.

On that exact scope, the rebuilt note verifies:

- `kappa = q+s+v+layer mod m` advances by `+1` on every step,
- `wrap` occurs only at `kappa=0`,
- `carry_jump` occurs only at `kappa=1`,
- `other(1,0,0,0)` occurs only at `kappa=2`,
- `other(0,0,1,0)` occurs only at `kappa=3`,
- all `kappa>=4` states are flat,
- phases `2,3` are the only flat/nonflat corner phases.

It also records the exact checked one-step machine:

- `wrap -> carry_jump`
- `carry_jump -> other(1,0,0,0)` iff `c=1`, else `flat`
- `other(1,0,0,0) -> flat` iff `s=1`, else `other(0,0,1,0)`
- `other(0,0,1,0) -> flat` always
- `flat -> wrap` exactly at `kappa = m-1`
- `flat -> other(0,0,1,0)` exactly at the unique corner `(kappa,s)=(2,2)`
- every other flat state stays flat

This is stronger than the original `058` wording because it makes the checked
machine explicit and shows that the same machine already yields both branch
lemmas on the frozen scope:

- `CJ` drops out immediately,
- `OTH` also drops out immediately.

So the honest current compression is:

- not just "`CJ` follows from the phase-event law",
- but "both open branch lemmas are already corollaries of one checked
  phase/corner machine."

## 5. Clean current theorem target

The cleanest current target is:

> On the active best-seed branch, the current event class is governed by a
> uniform odd-`m` phase/corner machine in `Theta = q+s+v+layer mod m`.

This should be stated as an auxiliary branch theorem, not as a replacement for
the main theorem object.

Then the proof chain becomes:

1. prove the active phase-event law,
2. deduce the flat-corner law,
3. deduce the `CJ` reset theorem,
4. try to fold `OTH` into the same machine instead of proving it from scratch.

## 6. Honest status

What is already solid:

- the theorem object remains minimal and stable,
- `057` gives a real reduction of `CJ`,
- `058` gives a smaller and more odometer-like candidate scheduler,
- the rebuilt `058B` assessment upgrades that to an explicit checked one-step
  phase/corner machine on the frozen `047` scope,
- `059B` now gives a safer support route for larger odd moduli:
  branch-local validation instead of the memory-heavy full-state `059A`
  reconstruction, with exact support on `m=25,27,29`,
- an independent support check confirms the `Theta` law at least through
  `m=13` after the checker was fixed,
- `060` reduces `B`-region invariance to avoidance of the six patched classes,
- `061` improves that further: the active nonterminal branch can be shown to
  stay in the unmodified `B` region without assuming the full global raw
  active law in advance, using only local mixed-witness dynamics on current
  `B`-states, the explicit patched-class support, and the universal first-exit
  targets.

What is still only supported, not proved:

- the full uniform odd-`m` phase-event law,
- the claim that `OTH` also falls completely out of the same machine uniformly
  in odd `m`.

What I would do next:

- prove the phase-event law first,
- treat the flat-corner lemma as a corollary,
- use `061` as the preferred route for `B`-region invariance rather than
  postulating the raw active law as a separate global premise,
- postpone any full larger-modulus sweep unless a proof step becomes unclear.

## 7. Bottom line

The best current summary is:

> The `d=5` boundary-reset proof is no longer most naturally organized as
> separate `CJ` and `OTH` branch formulas. The cleanest current proof target is
> a single small phase/corner machine on `Theta = q+s+v+layer`, from which the
> checked `CJ` law already falls out formally and `OTH` may also follow. With
> `060/061`, that phase machine is now tied to a bootstrap route for
> `B`-region invariance, so the honest remaining target is the uniform
> odd-`m` phase-event law together with that bootstrap.
