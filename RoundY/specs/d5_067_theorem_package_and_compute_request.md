# D5 theorem package draft and focused compute request

This note works only on the theorem-side package requested in the concentrated
handoff, plus a tightly scoped compute-support request.

It does **not** reopen generic search. It treats the theorem side as the
`033 -> 062 -> 059` spine already isolated in the handoffs, and it treats
compute only as support for the exact reduction object and the canonical clock.

## 1. Scope and status

What is being packaged here:

1. a clean statement of the phase-corner theorem;
2. the countdown/reset corollaries;
3. the structural chain reducing everything to the trigger theorem and the
   mixed-witness scheduler;
4. a compute request restricted to:
   - cycle vs chain,
   - accessible quotient,
   - `(B,beta)` exactness on larger moduli.

What remains conditional:

- the explicit `033` trigger-family theorem is taken as input;
- the exact mixed-witness scheduler on `B` from `059` is taken as input;
- finite-cover compatibility `B <- B+c <- B+c+d` is taken as input.

So this note is a manuscript-facing reduction, not a claim that every cited
upstream lemma was reproved from scratch here.

## 2. Main theorem package

### Theorem A (phase-corner theorem)

Fix odd `m >= 5` and the best seed. On the active nonterminal branch define

- `kappa = q + s + v + layer mod m`,
- `c = 1_{q = m-1}`.

Then:

1. `kappa' = kappa + 1 mod m`.
2. The current event `epsilon4` is determined by `(kappa, c, s)` as follows:
   - `kappa = 0  -> wrap`
   - `kappa = 1  -> carry_jump`
   - `kappa = 2  -> other_1000` iff `c = 1`, else `flat`
   - `kappa = 3  -> other_0010` iff `(c = 0 and s = 2)` or `(c = 1 and s != 2)`,
     else `flat`
   - `kappa = 4,...,m-1 -> flat`
3. Among flat states, the only short reset corner is `(kappa, s) = (2, 2)`.

Interpretation: on the active branch, D5 is an odometer with one corner.

### Corollary B (countdown law)

Define `tau` on the active branch by:

- `tau = 0` on nonflat states;
- on flat states,
  - `tau = 1` at the corner `(kappa, s) = (2, 2)`,
  - `tau = m-kappa` otherwise.

Then:

- `tau' = tau - 1` whenever `tau > 0`.

### Corollary C (reset laws)

Using current-state variables only, the reset values are:

- `wrap -> 0`
- `carry_jump ->`
  - `0` if `c = 1`
  - `1` if `c = 0` and `s = 1`
  - `m-2` if `c = 0` and `s != 1`
- `other_1000 ->`
  - `m-3` if `s = 1`
  - `0` if `s != 1`
- `other_0010 -> m-4`

### Corollary D (finite-cover compatibility)

The phase machine is compatible with the finite-cover chain

- `B <- B+c <- B+c+d`.

So the current-state scheduler and countdown/reset laws are the same machine on
that cover, not separate ad hoc formulas.

## 3. Proof spine for Theorem A

The clean structural chain is:

1. explicit trigger family;
2. universal first-exit targets;
3. pre-exit `B`-region invariance;
4. mixed-witness scheduler on `B`;
5. phase-corner theorem;
6. countdown/reset corollaries.

The best current compressed form is therefore:

- `033 -> 062 -> 059`,

with the exit-target theorem `062` used as the bridge from the explicit trigger
family to the pure `B` scheduler.

### Proposition 1 (explicit trigger family input)

Import from `033` the unresolved trigger family

- `H_{L1} = {(q,w,u,layer) = (m-1,m-1,u,2) : u != 2}`.

This is the sole structural input needed to pin down the first exit.

### Proposition 2 (candidate orbit and phase-1 invariant)

Let the post-entry active state in current coordinates be

- `x_0 = (q,w,u,Theta) = (m-1,1,u_source,2)`.

Set

- `rho = u_source + 1 mod m`.

Define the candidate mixed orbit by

- `F(q,w,u,0) = (q+1, w,   u,   1)`
- `F(q,w,u,1) = (q,   w,   u+1, 2)`
- `F(q,w,u,2) = (q,   w+1_{q=m-1}, u, 3)`
- `F(q,w,u,Theta) = (q,w,u,Theta+1)` for `3 <= Theta <= m-1`,

with all residues read mod `m`.

Then every phase-1 candidate state satisfies

- `q = u - rho + 1 mod m`.

Reason: it holds at the first phase-1 state and is preserved because one full
phase cycle increments `u` once and `q` once.

### Proposition 3 (universal first-exit targets)

Only two phase-1 states can hit `H_{L1}` in one alternate step:

- `A = (m-1, m-2, 1)`,
- `B = (m-2, m-1, 1)`.

Using the phase-1 invariant,

- `u(A) = rho - 2 mod m`,
- `u(B) = rho - 3 mod m`.

Since `H_{L1}` requires `u != 2`, the first exit is:

- `A` unless `rho = 4`,
- `B` when `rho = 4`.

So the first-exit targets are universal:

- regular family: `T_reg = (m-1, m-2, 1)`,
- exceptional family: `T_exc = (m-2, m-1, 1)`.

### Proposition 4 (pre-exit B-region invariance)

Before that first exit, the candidate orbit never enters any patched current
class.

Sketch:

- `w` starts at `1` and never decreases;
- patched classes with `w = 0` are therefore impossible;
- the `w = 1, Theta = 3` patch never occurs because the branch enters at
  `Theta = 2`;
- the `L1`-type patch `(m-1,m-1,1)` lies strictly after the universal exit
  target on both the regular and exceptional families.

Hence every candidate state before first exit is `B`-labelled.

By induction, actual branch = candidate branch up to first exit, because on a
`B`-labelled state the mixed witness rule is unmodified and therefore agrees
with the candidate step.

### Proposition 5 (mixed-witness scheduler on B)

On `B`-labelled active states, the mixed witness rule yields an exact phase
scheduler. In theorem gauge this is read by

- `kappa = q+s+v+layer mod m`.

The scheduler is:

- `kappa = 0 -> wrap`
- `kappa = 1 -> carry_jump`
- `kappa = 2 -> other_1000` iff `c = 1`, else `flat`
- `kappa = 3 -> other_0010` iff `(c = 0 and s = 2)` or `(c = 1 and s != 2)`,
  else `flat`
- `kappa >= 4 -> flat`

and the next phase is always

- `kappa' = kappa + 1 mod m`.

This proposition is the exact theorem-side content extracted from `059`.

### Proposition 6 (promotion to Theorem A)

Combining Propositions 1-5 gives the phase-corner theorem on the pre-exit
active branch.

Using finite-cover compatibility

- `B <- B+c <- B+c+d`,

the same current-state machine extends across the whole active nonterminal
branch. Therefore Theorem A follows.

## 4. Derivation of the countdown/reset corollaries

The handoffs already isolate two proof coordinates that may be used without
changing the theorem object:

- `alpha = rho - u`,
- `beta = alpha - (s+v+layer) - J`, where `J = 1_{epsilon4 = carry_jump}`.

On the active branch,

- `beta = -kappa mod m`.

This lets the countdown/reset formulas be derived from Theorem A almost
mechanically.

### 4.1 Countdown

On nonflat states, `tau = 0` by definition.

On flat states:

- if `(kappa,s) = (2,2)`, the branch is at the unique short corner, so `tau=1`;
- otherwise `beta = -kappa = m-kappa`, and on flat states away from the short
  corner the checked exact formula is `tau = beta`, hence `tau = m-kappa`.

Since `kappa' = kappa + 1`, every flat positive countdown step satisfies

- `tau' = tau - 1`.

At `kappa = m-1` this gives `tau = 1` and the next state is wrap, so `tau'=0`
still matches `tau-1`.

### 4.2 Reset laws

Now translate the nonflat event classes into `beta`/`alpha` fibers.

#### Wrap

`wrap` is `kappa = 0`, hence `beta = 0`, so the next countdown is `0`.

#### Carry jump

`carry_jump` is `kappa = 1`, hence `beta = m-1` and `J = 1`.
Then

- `c = 1_{alpha = 2}`.

So the exact `alpha`-side reset law becomes the theorem-side current law:

- `0` if `c = 1`,
- `1` if `c = 0` and `s = 1`,
- `m-2` if `c = 0` and `s != 1`.

#### other_1000

`other_1000` is `kappa = 2`, hence `beta = m-2`, which is equivalent to

- `delta = alpha - (s+v+layer) = m-2`.

So the exact reset law is

- `m-3` if `s = 1`,
- `0` otherwise.

#### other_0010

`other_0010` is `kappa = 3`, hence `beta = m-3`, equivalently

- `delta = m-3`.

So the exact reset law is

- `m-4`.

This proves Corollary C.

## 5. What is actually left on the theorem side

The theorem package now has a clean logical shape.

What still needs to be written sharply in manuscript form is not a new search,
but the exact dependence bookkeeping:

1. quote the `033` trigger theorem precisely;
2. state `062` in the universal-target form;
3. isolate the exact `059` scheduler lemma on `B`;
4. present Theorem A as the conceptual center;
5. demote countdown/reset laws to corollaries.

So the theorem side now looks close to closure in shape.

## 6. Focused compute-support request

This is the compute request that matches the concentrated handoff. It is
strictly limited to reduction validation and clock stress tests.

### Request A: validate the exact reduction object

Goal:

- determine whether the correct exact reduction object is
  - a literal cyclic `m`-section, or
  - a marked length-`m` chain extracted from the regular corridor.

Required procedure:

1. For each tested odd modulus `m`, extract the regular-corridor section using
   the exact return slice already suggested by the current evidence
   (for example the `theta = 2` slice, equivalently the `beta = m-2`
   first-return slice if that gauge is available).
2. Build the induced return/advance object directly from the raw branch data.
3. Record:
   - the ordered state list,
   - the induced map,
   - the marked carry residue(s),
   - entrance/exit behavior.
4. Decide which exact object is correct:
   - **cycle**: one closed `m`-cycle with one carry mark,
   - **chain**: one length-`m` marked chain with the observed entrance/exit.

Pass/fail criteria:

- zero unexpected states in the extracted object;
- zero unexpected induced transitions;
- explicit witness table for the carry mark;
- if cycle fails but chain passes, report chain as the exact first theorem and
  do not force a cycle statement.

### Request B: validate `(B,beta)` exactness on larger moduli

Goal:

- stress-test the canonical clock on larger odd moduli without reopening any
  controller search.

Required datasets:

- frozen active-row datasets with current row and next row information for at
  least `m = 13,15,17,19`;
- preferably extend to `21,23,25,27,29` if those rows are already available;
- include enough columns to recover
  `B`, `q`, `c`, `epsilon4`, `tau`, `next_tau`, and `next_B`.

Required checks for every modulus:

1. define `beta = -q-s-v-layer mod m` from actual current rows;
2. check universal birth on the post-entry row;
3. check unit drift `beta' = beta - 1 mod m` on every recorded transition;
4. check zero-collision exactness of current `(B,beta)` for:
   - `q`,
   - `c`,
   - `epsilon4`,
   - `tau`,
   - `next_tau`,
   - `next_B` where recorded;
5. check the explicit formulas:
   - `q = -beta - s - v - layer mod m`,
   - `c = 1_{beta+s+v+layer = 1}`;
6. check the phase-corner scheduler for `epsilon4` in `kappa` gauge and in
   `beta` gauge.

Pass/fail criteria:

- zero failures on drift;
- zero collisions for all requested current and next readouts;
- zero unexpected rows under the explicit formulas;
- any failure must be reported with the exact row, modulus, and observable.

### Request C: accessible quotient for the intended local/admissible class

Goal:

- validate the induced accessible quotient on the extracted exact reduction
  object, not the whole raw rule space.

Required procedure:

1. Fix the intended local/admissible observable class exactly.
2. Restrict that class to the extracted exact object from Request A.
3. Compute the accessible quotient induced by that observable:
   - quotient states,
   - induced transitions,
   - marked carry behavior.
4. Determine whether that quotient remains bounded as `m` grows.
5. Record whether the quotient still recovers the carry mark exactly.

Pass/fail criteria:

- the quotient computation must be done on the extracted exact reduction
  object, not by broad search over rule families;
- report the quotient size as a function of `m`;
- report whether exact carry recovery survives in the quotient;
- if exact carry recovery forces quotient size `>= m`, that is positive support
  for the rigidity route.

### What compute must not do

- no generic search;
- no reopening broad controller families;
- no new witness hunting outside the exact reduction object;
- no replacing theorem work with empirical exploration.

Compute is now support for reduction validation only.
