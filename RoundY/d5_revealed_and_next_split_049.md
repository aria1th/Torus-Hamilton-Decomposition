# D5 Revealed Facts And Next Split 049

This note freezes what is currently revealed on the D5 branch and separates
the next proof direction from the next compute direction.

The point is to avoid conflating two different but compatible pictures:

- the **minimal theorem-side object**:
  `(B, tau, epsilon4)`
- the **stronger checked constructive refinement**:
  `(B, rho)` with `rho = source_u + 1 mod m`

All checked statements below refer to the active best-seed branch on
`m = 5,7,9,11` unless a larger tested range is explicitly stated.

## 1. What is currently revealed

### 1.1 Structural theorem chain

The checked chain through `044–048` is now:

1. `044`
   finite-cover normal form
   `B <- B+c <- B+c+d`
   with
   `B = (s,u,v,layer,family)`,
   `c = 1_{q=m-1}`,
   `d = 1_{next carry u >= m-3}`.

2. `045`
   first carry-only admissibility no-go:
   the first current-edge / short-transition / low-cardinality gauge catalogs
   do not realize `c`.

3. `046`
   conceptual carry theorem:
   `c` is already an exact one-sided future grouped-transition datum.
   The exact future signature is of the form
   `B + tau + eta`,
   where `tau` is the initial flat-run length for `dn = (0,0,0,1)` and `eta`
   is the first nonflat grouped-delta event.

4. `047`
   boundary sharpening:
   all ambiguity in `B + tau` lies at `tau = 0`,
   and the boundary event class is genuinely
   `{wrap, carry_jump, other}`.
   The cleaner checked per-modulus form is
   `B + min(tau, m-3) + epsilon4`.

5. `048`
   internal carrier law:
   `tau` is already an exact countdown carrier.
   - if `tau > 0`, then `tau' = tau - 1`
   - all nontrivial behavior is at `tau = 0`
   - boundary reset:
     - `wrap -> 0`
     - `carry_jump` exact on `(s,v,layer)`
     - `other` exact on `(s,u,layer)`

So the hidden datum is no longer a vague future window. It is a countdown
carrier with a tiny reset law.

### 1.2 Stronger checked source-memory refinement

The checked data also support a stronger refinement, and this now persists by
direct replay through `m = 13,15,17,19` as well:

- define `rho = source_u + 1 mod m`
- then `tau` is exact on `(s,u,v,layer,rho)`
- `next_tau` is exact on `(s,u,layer,rho,epsilon4)`
- `c` is exact on `(u,rho,epsilon4)`
- and on checked data:
  `q ≡ u - rho + 1_{epsilon4 = carry_jump} (mod m)`

This is the cleanest current bridge from the older transport story to the
new countdown story.

But this refinement must be stated carefully:

- `rho` is **not** equivalent to the minimal future-side object
  `(B, tau, epsilon4)`
- for `m >= 7`, `rho` is not recoverable from `(B, tau, epsilon4)`
- on the tested extended range, the ambiguous bucket count matches `2m-11`
- so `rho` should be treated as a **checked refinement**, not as an equivalent
  reparametrization

The supporting check is
`RoundY/checks/d5_tau_rule_validation_048a.json`.

## 2. Next proof direction

The proof branch should stay centered on the minimal theorem-side object.

### 2.1 Recommended proof hierarchy

1. finite-cover normal form (`044`)
2. first carry no-go (`045`)
3. carry as anticipation datum (`046`)
4. boundary sharpening (`047`)
5. countdown carrier law (`048`)

This keeps the conceptual theorem language clean:

- `046` is the main conceptual theorem
- `047` is a sharpening at the boundary
- `048` turns the hidden anticipation datum into a concrete countdown/reset
  carrier

### 2.2 What to add next on the proof side

The next proof notes should add two things:

1. the explicit lower-bound witness family from `s63`
   as the first serious no-go direction for bounded future horizons
2. a clear statement that `rho` is a checked refinement of the future-side
   carrier, not an equivalent coordinate

### 2.3 Exact proof fork

The proof fork is now sharp:

- positive route:
  prove an admissible/local coding theorem for the countdown carrier `tau`
  or for its reset law at `tau = 0`
- negative route:
  prove a reduction lemma showing that the intended admissible/local mechanism
  class collapses to a bounded transition/reset catalog, then apply the
  explicit witness families

## 3. Next compute direction

The compute branch should no longer be framed as “code tau somehow.”
It should split into two separate jobs.

### 3.1 Compute branch A: reset-law coding

Target the `tau = 0` boundary reset law directly.

This was the original `049` work-template direction:

- freeze the reset dataset at `tau = 0`
- search smallest exact observables for:
  - `carry_jump -> next_tau`
  - `other -> next_tau`
  - global reset law `(epsilon4, ...) -> next_tau`
- then integrate with the already-known internal rule
  `tau' = tau - 1` for `tau > 0`

This remains the smallest honest local target on the theorem-side coordinates.
But as a pure validation branch, it is now materially stronger than before:
artifact `050` shows the same reset-law structure persists through
`m = 13,15,17,19`.

### 3.2 Compute branch B: source-residue transport

This branch is now no longer hypothetical. Artifact `049` shows the stronger
checked refinement persists exactly through `m = 19`:

- initialize enough of `rho = source_u + 1`
- transport it through the active branch
- read out:
  - `tau` from `(s,u,v,layer,rho)`
  - `next_tau` from `(s,u,layer,rho,epsilon4)`
  - `c` from `(u,rho,epsilon4)`

This is not the same as the theorem-side minimal object.
It is a stronger constructive route that may be easier to realize locally.

### 3.3 What not to do

Do not reopen:

- broad one-bit scans
- generic tiny-transducer widening
- vague future-window search
- direct search for the full residual sheet `d`

## 4. Practical guidance

The clean split is now:

- **proof branch**:
  stay minimal, use `(B, tau, epsilon4)`, and treat `rho` only as a checked
  refinement / remark
- **compute branch**:
  exploit `rho` aggressively if it helps, because it turns the hidden object
  into transported current memory rather than pure anticipation
- **proof-support compute**:
  use `050` to validate that the `048` reset law and the `047/048` witness
  family persist on larger odd moduli without changing the theorem object

That is the most stable way to push both sides forward without mixing their
goals.
