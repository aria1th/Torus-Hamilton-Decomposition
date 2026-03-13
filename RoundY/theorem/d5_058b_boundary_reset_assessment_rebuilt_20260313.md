# D5 boundary-reset assessment (rebuilt)
## Verdict

I do **not** have a uniform proof of the boundary-reset theorem from the bundle as written, and I do **not** have a counterexample either.

What the bundle itself currently establishes is:

1. `RoundY/theorem/d5_boundary_reset_uniform_proof_attempt_055.md` reduces the uniform theorem `BR` to two branch lemmas, `CJ` and `OTH`; see lines 224–250.
2. `RoundY/theorem/d5_CJ_uniform_proof_progress_057.md` reduces `CJ` further to the flat-corner lemma; see lines 166–199.
3. `RoundY/theorem/d5_phase_machine_hypothesis_057a.md` states honestly that the flat-corner lemma, the `OTH` branch, and the phase-machine hypothesis are still unproved uniformly; see lines 279–297.
4. The support artifacts say the checked formulas continue to hold through `m = 23`, but those artifacts are compute evidence, not a uniform proof.

So the theorem is **supported**, but not uniformly proved, by the material in the tarball.

---

## What I verified directly from the frozen `047` data

I worked directly with

- `artifacts/d5_future_transition_carry_coding_047/data/frozen_B_c_tau_epsilon_dataset_047.json`

for `m = 5,7,9,11`.

The file contains 15,188 rows total. For one-step transition analysis, the natural scope is every row with a recorded successor inside its `source_u` trace block. That gives

- `216` transitions for `m=5`
- `1212` transitions for `m=7`
- `3952` transitions for `m=9`
- `9780` transitions for `m=11`

for a total of **15,160 checked transitions**.

On those 15,160 transitions, define

\[
\kappa := q + s + v + \lambda \pmod m.
\]

Then the following statements all hold exactly on the checked scope.

### 1. Phase increment law

Every recorded successor satisfies

\[
\kappa(Fx)=\kappa(x)+1 \pmod m.
\]

So `kappa` behaves like a visible phase.

### 2. Event-class placement by phase

The nonflat event classes occur at the first four phases:

\[
\kappa=0 \Rightarrow \text{wrap},
\qquad
\kappa=1 \Rightarrow \text{carry\_jump},
\qquad
\kappa=2 \Rightarrow \text{other subtype }(1,0,0,0),
\qquad
\kappa=3 \Rightarrow \text{other subtype }(0,0,1,0).
\]

More precisely:

- `wrap` appears only at `kappa = 0`
- `carry_jump` appears only at `kappa = 1`
- `other` with `dn = (1,0,0,0)` appears only at `kappa = 2`
- `other` with `dn = (0,0,1,0)` appears only at `kappa = 3`
- all phases `kappa >= 4` are flat on the checked range
- phases `kappa = 2,3` also contain some flat states, so those are the only flat/nonflat corner phases

### 3. Exact one-step phase machine on the checked scope

The recorded transitions are exactly:

1. `wrap -> carry_jump`
2. `carry_jump -> other(1,0,0,0)` iff `c=1`, otherwise `carry_jump -> flat`
3. `other(1,0,0,0) -> flat` iff `s=1`, otherwise `other(1,0,0,0) -> other(0,0,1,0)`
4. `other(0,0,1,0) -> flat` always
5. `flat -> wrap` exactly when `kappa = m-1`
6. `flat -> other(0,0,1,0)` exactly at the unique corner `(kappa,s)=(2,2)`
7. every other flat state goes to flat

So the checked boundary/reset mechanism is governed by a very small deterministic phase/corner machine.

---

## Consequences for the branch lemmas

This does not prove the theorem uniformly for all odd `m`, because the phase-machine statement above was only verified directly on the frozen `047` rows. But it compresses the proof target beyond what `055` states.

### A. `CJ` follows immediately from the checked phase machine

Since `carry_jump` occurs at `kappa = 1`, one gets

\[
q \equiv 1-s-v-\lambda \pmod m,
\]

which is exactly the checked raw identity `CJ-q` in `055`.

Now take a carry-jump boundary state.

- If `c=1`, the next state is already nonflat, so `tau(Fx)=0`.
- If `c=0`, the next state is flat at `kappa=2`.
  - If current `s=1`, then the successor has `s=2`, so it is the unique flat corner `(kappa,s)=(2,2)`, hence `tau(Fx)=1`.
  - If current `s != 1`, then the successor is an ordinary flat state at `kappa=2`, so the next nonflat event comes after a full `m-2` flat block, hence `tau(Fx)=m-2`.

This recovers exactly the checked `CJ` reset law.

### B. `OTH` also follows immediately from the checked phase machine

For `other` with `dn=(1,0,0,0)`:

- if `s=1`, the next state is flat at `kappa=3`, so `tau(Fx)=m-3`
- if `s!=1`, the next state is immediately the second `other` subtype, so `tau(Fx)=0`

For `other` with `dn=(0,0,1,0)`:

- the next state is flat at `kappa=4`, so `tau(Fx)=m-4`

That is exactly the checked `OTH` law recorded in `055`.

### C. What this changes conceptually

The current proof burden is not best described as

> prove `CJ` and `OTH` separately.

A more compressed description is:

> prove one small phase/corner machine uniformly in odd `m`.

If that machine were proved, then the wrap, `CJ`, and `OTH` reset laws would all be corollaries.

---

## Why this still stops short of a theorem proof

The gap is real.

I verified the phase machine directly only on the frozen `047` data for `m=5,7,9,11`.
The tarball does include broader support through `m=23`, but that broader support is for the formula families, not for a packaged uniform proof of the phase machine itself.

The relevant support summaries say:

- `artifacts/d5_boundary_reset_proof_support_055/data/analysis_summary.json`:
  the carry-jump formula, the raw `q = 1-s-v-layer` identity, the `other` subtype law, and the `r`-discriminator continue to hold exactly on `m=21,23`.
- `artifacts/d5_CJ_flat_corner_support_057a/data/analysis_summary.json`:
  the flat-corner law, flat countdown formula, and CJ delta-reduction continue to hold exactly on `m=13,15,17,19,21,23`.

That is strong positive evidence, but it is still evidence rather than a finished uniform proof.

---

## Final status

So my final mathematical assessment is:

- **Not disproved:** I found no counterexample anywhere in the bundled checks.
- **Not proved uniformly:** the manuscript still leaves `CJ`, `OTH`, and the phase-machine explanation unproved in general odd `m`.
- **Stronger reduction obtained on the checked `047` scope:** the boundary/reset law is exactly controlled by the phase variable
  \[
  \kappa = q+s+v+\lambda \pmod m
  \]
  together with one flat corner `(kappa,s)=(2,2)`.

That is the strongest honest conclusion I can support from the bundle.
