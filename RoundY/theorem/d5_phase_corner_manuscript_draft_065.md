# D5 Phase–Corner Manuscript Draft 065

## Purpose

This note rewrites the current D5 frontier in manuscript form, using the
unified 064 handoff as the organizing document. It keeps the theorem object
minimal:

- `B = (s,u,v,layer,family)`
- `tau`
- `epsilon4`

and treats the auxiliary coordinates

- `rho = u_source + 1`
- `alpha = rho - u`
- `delta = rho - (s+u+v+layer)`
- `kappa = q+s+v+layer`

as proof or constructive coordinates only.

The intended manuscript slogan is:

> **On the active best-seed branch, D5 is an odometer with one corner.**

This draft does **not** claim that all proof obligations are fully closed in a
formal sense. It packages the theorem chain in its cleanest current form,
separates what is already derived from what is still a stated dependency, and
rewrites the argument so that the central theorem is the phase–corner machine
rather than the branchwise reset formulas.

---

## 1. Main theorem target

### Theorem A (Phase–Corner Theorem; manuscript target)
Fix odd `m >= 5` and the best seed

- `left = [2,2,1]`
- `right = [1,4,4]`.

On the active nonterminal branch for the unresolved best-seed channel
`R1 -> H_L1`, define

- `kappa = q + s + v + layer (mod m)`.

Then:

1. `kappa' = kappa + 1 (mod m)`.
2. The current event `epsilon4` is determined by `kappa`, the carry sheet
   `c = 1_{q = m-1}`, and the single corner state `s = 2` as follows:
   - `kappa = 0  -> wrap`
   - `kappa = 1  -> carry_jump`
   - `kappa = 2  -> other_1000` iff `c = 1`, otherwise `flat`
   - `kappa = 3  -> other_0010` iff `(c = 0 and s = 2)` or `(c = 1 and s != 2)`,
     otherwise `flat`
   - `kappa = 4,...,m-1 -> flat`
3. Among flat states, the only short reset occurs at the corner
   `(kappa,s) = (2,2)`.

Equivalently, the active branch is a cyclic phase machine with exactly one
corner correction.

### Corollary B (Countdown carrier)
Define `tau` on the active branch by:

- `tau = 0` on nonflat states;
- on flat states,
  - `tau = 1` at `(kappa,s) = (2,2)`;
  - `tau = m-kappa` otherwise.

Then:

- `tau' = tau-1` whenever `tau > 0`.

### Corollary C (Boundary reset formulas)
At `tau = 0`, the branchwise resets are:

- `wrap -> 0`
- `carry_jump ->`
  - `0` on the zero-reset fiber `s + v + layer ≡ 2 (mod m)`;
  - `1` when `s = 1` off the zero-reset fiber;
  - `m-2` otherwise
- `other_1000 ->`
  - `m-3` if `s = 1`
  - `0` if `s != 1`
- `other_0010 -> m-4`.

### Corollary D (Finite-cover compatibility)
The phase–corner machine is compatible with the checked finite-cover normal
form

- `B <- B+c <- B+c+d`

where

- `B = (s,u,v,layer,family)`
- `c = 1_{q = m-1}`
- `d = 1_{next carry u >= m-3}`.

---

## 2. Best proof spine

The clean proof spine remains the one identified in the unified 064 handoff:

- `033 -> 062 -> 059`,

with `061` used as a bootstrap / consistency picture rather than the primary
narrative.

### Dependency 1: explicit trigger family from 033
Use the exact family formula

- `H_L1 = {(q,w,u,layer) = (m-1,m-1,u,2): u != 2}`.

This gives the precise trigger set for the unresolved channel.

### Dependency 2: universal first-exit targets from 062
Using the phase-1 source-residue invariant

- `q ≡ u - rho + 1 (mod m)` on phase-1 current states,
- `rho = u_source + 1`,

one derives the universal candidate exits

- `T_reg = (m-1,m-2,1)`
- `T_exc = (m-2,m-1,1)`.

The family split is then:

- regular families exit at `T_reg`
- the exceptional family exits at `T_exc`.

### Dependency 3: pre-exit B-region invariance
Once the first-exit targets are fixed, the candidate active orbit agrees with
the actual active branch up to first exit. Therefore every nonterminal active
current state is `B`-labelled.

This is the content of the `061` bootstrap picture, but in the manuscript it
should appear as a corollary of the universal first-exit theorem and the
explicit patched-class formulas.

### Dependency 4: mixed witness scheduler on B
On current `B`-states, the mixed witness rule applies without modification.
The phase coordinate

- `kappa = q+s+v+layer`

is exactly the mixed witness layer bucket, and the event scheduler becomes:

- `kappa = 0 -> wrap`
- `kappa = 1 -> carry_jump`
- `kappa = 2 -> other_1000` iff `c = 1`, else `flat`
- `kappa = 3 -> other_0010` on the stated `(c,s)` condition, else `flat`
- `kappa >= 4 -> flat`.

This is the real conceptual theorem. Once it is written in this form, the
branchwise reset formulas are no longer mysterious; they are corollaries of the
scheduler.

---

## 3. Recommended manuscript structure

### Section X. The active best-seed branch
Define the active branch, the current grouped coordinates, and the theorem
object `(B,tau,epsilon4)`.

State explicitly that the auxiliary coordinates `rho`, `alpha`, `delta`, and
`kappa` are *not* part of the theorem object.

### Section Y. Universal first-exit targets
Prove:

- the exact trigger family for `H_L1`
- the two universal exit targets `T_reg`, `T_exc`
- pre-exit `B`-region invariance.

At the end of this section, the reader should know that the entire active
nonterminal branch stays in the unmodified mixed witness region.

### Section Z. The phase–corner machine
Introduce

- `kappa = q+s+v+layer (mod m)`.

Prove the scheduler theorem (Theorem A).

This section should be the conceptual center of the D5 manuscript.

### Section Z+1. Countdown and reset corollaries
Derive:

- the `tau` countdown law
- the `CJ` reset law
- the `OTH` reset laws
- compatibility with `B <- B+c <- B+c+d`.

This section should make clear that `046` is the conceptual theorem,
`047` the boundary sharpening, and `048+` the countdown/reset packaging.

### Section Z+2. Remarks on constructive and negative routes
Only after the phase–corner theorem is in place should the paper add:

- the stronger constructive `alpha/rho` refinement as a remark or later section
- the bounded-quotient impossibility route as a separate theorem direction.

These should not be mixed into the main theorem statement.

---

## 4. Proof skeleton for Theorem A

We recommend proving Theorem A in the following steps.

### Step 1. First-exit control
Import the explicit `H_L1` family theorem from the branch analysis and prove
that the active branch can only first exit at

- `T_reg = (m-1,m-2,1)`
- `T_exc = (m-2,m-1,1)`.

### Step 2. B-region invariance
Show that before those targets are reached, the active branch cannot hit any of
the six modified current classes. Therefore every pre-exit current state is
`B`-labelled.

### Step 3. Mixed witness scheduler
Since all pre-exit current states are `B`-states, the mixed witness rule
applies exactly. Express the mixed witness current rule in the phase coordinate
`kappa = q+s+v+layer`.

This yields the entire event scheduler.

### Step 4. Corner corollary
Restrict Theorem A to flat states. Then:

- all long stretches are pure odometer drift;
- the only short reset occurs at `(kappa,s)=(2,2)`.

This is the “one corner” statement.

### Step 5. Countdown corollary
Define `tau` by distance to the next nonflat event in the phase machine. The
countdown and reset formulas follow immediately.

---

## 5. How to state the constructive route without polluting the theorem object

The constructive route is now strong enough to deserve a theorem-shaped remark,
but it should remain explicitly separate.

### Remark E (Constructive source-residue refinement)
On the checked range through `m=19`, the stronger current-memory refinement via

- `rho = u_source + 1`
- `alpha = rho - u`

is exact. In the `alpha` gauge one has

- `q ≡ -alpha + J (mod m)`
- `c = 1_{alpha = 1 + J}`

where `J = 1_{epsilon4 = carry_jump}`. Thus `q`, `c`, `tau`, and `next_tau`
are explicit current formulas in the transported source-residue gauge.

This does **not** replace `(B,tau,epsilon4)` as the theorem object. It is a
stronger constructive refinement that may be easier to realize locally.

This remark belongs after the theorem/corollary chain, not before it.

---

## 6. How to state the negative route without disturbing the main theorem

The negative route should also be detached from the phase–corner theorem.

### Proposition F (bounded quotient obstruction; route statement)
If the intended local/admissible mechanism class factors through a bounded
quotient of the active cyclic section dynamics, then it cannot recover the
carry sheet uniformly in odd `m`.

This is a separate route theorem. It should not appear in the main phase–corner
section.

---

## 7. Honest status and next theorem tasks

### Already structurally in place
- universal first-exit theorem shape
- pre-exit `B`-region invariance strategy
- phase scheduler in `kappa`
- countdown/reset corollaries
- compatibility with `B <- B+c <- B+c+d`

### Still to be written as full manuscript proofs
- full proof text for the first-exit theorem using the `033` trigger family
- full proof text that the active branch remains in the `B`-region until first
  exit
- fully polished derivation of the scheduler from the mixed witness rule

### Still open beyond the theorem chain
- local/admissible realization of the constructive `alpha/beta` carrier
- or a bounded-quotient impossibility theorem for the intended class.

---

## 8. Suggested manuscript slogans

Use these sparingly, but consistently.

- **D5 is an odometer with one corner.**
- **Carry is an anticipation datum, but on the active branch it is governed by a current phase machine.**
- **The theorem object is minimal; the source-residue route is a stronger constructive refinement.**

These accurately reflect the current state without overstating what is already
fully proved.
