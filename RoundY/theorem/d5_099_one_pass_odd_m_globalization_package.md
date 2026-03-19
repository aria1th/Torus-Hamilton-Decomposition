# D5 099: One-pass odd-`m` globalization package

## Abstract

This note rewrites the odd-`m` D5 globalization chain as one read-through
theorem package.

The package is self-contained in the following theorem-level sense:

1. every theorem used later is stated in this document;
2. every downstream proof after the standing package inputs is carried out in
   this document;
3. no cross-note citation is needed while reading the argument.

The standing package inputs are kept explicit and honest:

1. the exact trigger-family formula for `H_{L1}`;
2. the coarse patch facts needed for pre-exit patch avoidance;
3. the componentwise concrete bridge package on full chains;
4. the regular chart / endpoint support package;
5. the exceptional source-`3` interior continuation fact.

From those inputs, the note proves in one place:

1. the structural first-exit theorem;
2. the fixed-`delta` tail-length reduction;
3. the chart/interface landing theorem;
4. the regular closure theorem;
5. the actual exceptional interface landing theorem;
6. the final odd-`m` D5 globalization theorem.

## Scope note

This note is **not yet** a graph-theoretic proof of Hamilton decomposition for
the odd-`m`, `d=5` torus.

What it proves is the odd-`m` D5 globalization theorem inside the accepted D5
regime and the fixed best-seed channel package.

To turn this document into a full Hamilton-decomposition proof, one still needs:

1. a reduction theorem showing why this channel covers the whole odd-`m`,
   `d=5` problem, or why it is the last unresolved channel;
2. a graph-level bridge from raw global `(beta,delta)` exactness to a global
   edge-selection rule, global `2`-factors, Hamiltonicity of each factor, and
   edge-disjoint coverage of the full torus edge set;
3. closure of the standing Inputs A--E and an explicit quantifier for the exact
   allowed values of `m`.

So the right description of this note is: a one-document theorem package for
the odd-`m` D5 globalization theorem, not yet a standalone proof of Hamilton
decomposition for the full torus.

## 1. Scope and basic definitions

Fix an odd modulus `m` in the accepted D5 regime and the best-seed channel

`R1 -> H_{L1}`

with source seed words

`L = [2,2,1]`, `R = [1,4,4]`.

Write

`R_reg = {1,2,4,5,...,m-1}`

for the regular source labels.

### Definition 1.1 (full chains and actual lifts)

A **full chain** is a complete boundary block between consecutive visits to the
`Theta = 2` section.

An **actual lift** of a realized boundary label `delta0` is an actual
accessible full-chain occurrence with boundary label `delta0`.

### Definition 1.2 (tail length)

The **remaining tail length** `tau(C)` of an actual lift `C` is the number of
full-chain successors available after `C` before terminality. If successors
continue forever, then `tau(C) = infty`.

### Definition 1.3 (endpoint class and right-congruence)

Fix the standard accepted terminal padding convention on future current-event
words. Two actual lifts lie in the same **endpoint class** when they determine
the same padded future current-event word.

Write `Pad` for the common terminal padding tail supplied by that convention.
The corresponding boundary right-congruence class is denoted by `rho`.

### Definition 1.4 (distinguished rows)

The **exceptional cutoff row** is

`delta = 3m - 3`.

The corresponding interface rows are

`3m - 2` and `3m - 1`.

### Definition 1.5 (accessible boundary union and splice-connected components)

The **accessible boundary union** is the union of all actual accessible full
chains.

A **splice-connected accessible component** is a connected component of that
union under the successor / predecessor splice relation between consecutive full
chains.

### Definition 1.6 (regular and exceptional realizations)

A full chain or actual lift is **regular** when it lies in one of the regular
source labels `u in R_reg`.

A full chain or actual lift is **exceptional** when it lies in the exceptional
source label `u = 3`.

A **regular realization** of a realized boundary label `delta` is a regular
actual lift at that label.

## 2. Standing theorem-package inputs

Everything after this section is proved in this note from the inputs listed
below.

### Input A (exact trigger family)

The target hole family for the unresolved best-seed channel is exactly

`H_{L1} = {(q,w,u,Theta) = (m-1,m-1,u,2) : u != 2}`.

Equivalently:

1. the target layer is `Theta = 2`;
2. the target current coordinates satisfy `q = w = m - 1`;
3. the only excluded fiber is `u = 2`.

### Input B (coarse patch facts)

For the patched current classes, only the following coarse facts are used:

1. the classes `R1, R2, R3, L2` require `w = 0`;
2. the class `L3` requires `w = 1`;
3. a pre-exit occurrence of `L1` would require the branch to have already
   reached the `w = m - 1` edge of the corridor.

### Input C (componentwise concrete bridge)

On the unique `Theta = 2` boundary state `(q,w,u,2)` of a full chain, define

- `sigma = w + u - q - 1 mod m`,
- `delta = q + m sigma`.

Then on each splice-connected accessible component:

1. consecutive full chains satisfy the odometer splice law

   `delta' = delta + 1 mod m^2`;

2. the current event class `epsilon4` is determined by `(beta,delta)`;

3. the realized boundary image is a forward interval in `Z/m^2 Z` or the full
   odometer cycle.

Let

`A = {wrap, carry_jump, other_1000, other_0010, flat}`

be the current-event alphabet, and write

`E : Z/mZ x Z/m^2Z -> A`, `(beta,delta) -> epsilon4(beta,delta)`

for the corresponding explicit event law.

### Input D (regular chart and endpoint support)

For each regular source label `u in R_reg`:

1. the `Theta = 2` source window starts at

   `s_u = m((u+2) mod m) - 1`;

2. that source window has exactly `m(m-3)` consecutive full-chain labels;

3. its terminal label is

   `e_u = s_u + m(m-3) - 1 = m(u-1) - 2 mod m^2`;

4. grouped successor is exact inside the source window and advances labels by
   `delta -> delta + 1`;

5. every actual regular lift at the endpoint label `e_u` continues on the true
   larger regular accessible union to the successor label

   `e_u + 1 = s_{u-3}`.

### Definition 2.1 (regular source windows and regular holders)

For a regular source label `u in R_reg`, write

`I_u = [s_u, e_u]`

for the corresponding regular source window from Input D.

Say that a boundary label `delta` has a **source-`u` regular holder** when
`delta in I_u`.

A regular holder is **interior** when `delta != e_u`, and **terminal** when
`delta = e_u`.

### Input E (exceptional source-3 interior continuation)

Inside the exceptional source-`3` chart, every exceptional full chain with
label strictly before the cutoff row `3m-3` is an interior chart occurrence and
therefore continues internally by the same grouped successor rule

`delta -> delta + 1`.

## 3. Structural first-exit theorem

Use current coordinates `(q,w,u,Theta)` along the active branch after the
alternate-`2` entry out of `R1`.

### Definition 3.1 (candidate orbit)

Define the source residue

`rho := u_source + 1 (mod m)`

where `u_source` is the source-`u` label of the chosen `R1` family. Start at
the alternate-`2` entry

`E = (m-1,1,u_source,2)`.

Define the candidate orbit `xhat_n = (q_n,w_n,u_n,Theta_n)` by

- `Fhat(q,w,u,0) = (q+1,w,u,1)`
- `Fhat(q,w,u,1) = (q,w,u+1,2)`
- `Fhat(q,w,u,2) = (q, w + 1_{q=m-1}, u, 3)`
- `Fhat(q,w,u,Theta) = (q,w,u,Theta+1)` for `3 <= Theta <= m-1`

On the section `Theta = 2`, this induces the odometer return map

`(q,w) -> (q+1, w + 1_{q=m-1})`.

Equivalently, with

`eta(q,w) := q + m(w-1) - (m-1)`,

one has `eta -> eta + 1`.

The only two phase-`1` states whose direction-`2` or direction-`1` successor can
reach `(q,w) = (m-1,m-1)` are

- `A = (m-1,m-2,1)`
- `B = (m-2,m-1,1)`

with indices

- `eta(A) = m(m-3)`
- `eta(B) = m(m-2)-1`

so `A` is encountered before `B`.

### Lemma 3.2 (phase-1 source-residue invariant)

Along the candidate orbit, every phase-`1` current state satisfies

`q = u - rho + 1 (mod m)`.

Hence

- `u(A) = rho - 2 (mod m)`
- `u(B) = rho - 3 (mod m)`.

**Proof.** The first phase-`1` state after entry is `(0,2,u_source,1)`, so the
relation holds there because `u_source = rho - 1`.

From one phase-`1` state to the next, the phase-`1` witness step increments `u`
by `1`, the later phase-`0` witness step increments `q` by `1`, and no other
step changes either coordinate. So the congruence is preserved.

### Lemma 3.3 (phase-1 trigger criterion)

Let `x` be a phase-`1` current state on the candidate orbit. An alternate step
from `x` lands in `H_{L1}` if and only if one of the following holds:

1. `x = A = (m-1,m-2,1)` and `u(x) != 2`, in which case direction `2` lands in
   `H_{L1}`;
2. `x = B = (m-2,m-1,1)` and `u(x) != 2`, in which case direction `1` lands in
   `H_{L1}`.

**Proof.** By Input A, the successor must satisfy

`(q',w',Theta') = (m-1,m-1,2)` and `u' != 2`.

Only phase-`1` states can step to layer `2`, and only directions `1` and `2`
change `q` or `w`. So the only two ways to reach `(q',w') = (m-1,m-1)` are:

- direction `2` from `(q,w) = (m-1,m-2)`;
- direction `1` from `(q,w) = (m-2,m-1)`.

Those are exactly `A` and `B`. Directions `1` and `2` preserve `u`, so the only
extra condition is `u != 2`.

### Proposition 3.4 (candidate first exits)

On the candidate orbit:

1. if `rho != 4` (regular family), the first exit to `H_{L1}` occurs at
   `A = (m-1,m-2,1)` by direction `2`;
2. if `rho = 4` (exceptional family), the state `A` does not exit and the first
   exit to `H_{L1}` occurs at `B = (m-2,m-1,1)` by direction `1`.

Equivalently,

- `T_reg = (m-1,m-2,1)`
- `T_exc = (m-2,m-1,1)`.

**Proof.** By Lemma 3.3, only `A` and `B` can trigger an exit to `H_{L1}`.
Since `A` is encountered first, it is enough to test whether `u(A) = 2`.

By Lemma 3.2,

`u(A) = rho - 2 (mod m)`.

So `u(A) = 2` if and only if `rho = 4`.

- If `rho != 4`, then `u(A) != 2`, so the first exit is at `A` by direction `2`.
- If `rho = 4`, then `u(A) = 2`, so `A` is blocked.

Still in the exceptional case, Lemma 3.2 gives

`u(B) = rho - 3 = 1 (mod m)`.

So `u(B) != 2`, and the first exit is at `B` by direction `1`.

### Lemma 3.5 (pre-exit patch avoidance)

Let `N_f` be the first-exit time of the candidate orbit in the chosen source
family `f`. For every `0 <= n < N_f`, the candidate state `xhat_n` avoids all
patched current classes.

**Proof.** The value `w` starts at `1` and changes only by the increment
`w -> w+1` at phase `2` with `q = m-1`. So `w` never decreases, and `w = 0`
never occurs before exit. By Input B(1), the classes `R1, R2, R3, L2` are
impossible.

The value `w = 1` occurs only at the entry state `(m-1,1,u_source,2)`, because
the first phase-`2` wrap immediately creates `w = 2` and thereafter `w` never
decreases. So by Input B(2), the class `L3` cannot occur after entry. Since the
entry state itself is the alt-`2` start state rather than a patched class,
`L3` is absent on the whole pre-exit segment.

On a regular family, Proposition 3.4 says the branch exits already at
`A = (m-1,m-2,1)`, before `w` can ever reach `m-1`. So `L1` is impossible.

On the exceptional family, the first creation of `w = m-1` occurs at phase `3`
from `(m-1,m-2,2)`. The next phase-`1` state then has `(q,w) = (0,m-1)`, not
`(m-1,m-1)`. The first later phase-`1` state with `w = m-1` that could also
carry `q = m-1` would occur strictly after `B = (m-2,m-1,1)`, but
Proposition 3.4 says the branch exits already at `B`. So `L1` is impossible
before exceptional exit as well.

Thus no patched current class is encountered before first exit.

### Theorem 3.6 (actual first exits and pre-exit B-region invariance)

For each source family:

1. the actual active branch agrees with the candidate orbit up to first exit;
2. every pre-exit actual current state is `B`-labeled;
3. the first exit to `H_{L1}` occurs at the universal family-dependent target
   `T_reg = (m-1,m-2,1)` or `T_exc = (m-2,m-1,1)`, with regular families
   exiting at `T_reg` by direction `2` and the exceptional family exiting at
   `T_exc` by direction `1`.

**Proof.** Fix a source family and let `N_f` be the candidate first-exit time
from Proposition 3.4. Prove by induction on `n <= N_f` that the actual state
`x_n` agrees with the candidate state `xhat_n` in the full current coordinates
`(q,w,u,Theta)`.

At `n = 0`, both states are the same entry state

`E = (m-1,1,u_source,2)`.

By Lemma 3.5, it is not patched, hence it is `B`-labeled.

Now assume `x_n = xhat_n` for some `n < N_f`. Lemma 3.5 says `xhat_n` is not
patched, so the actual state `x_n` is `B`-labeled. Therefore its witness update
is the unmodified mixed-witness update, which induces exactly the candidate step
on `(q,w,u,Theta)`: direction `1` changes only `q`, direction `4` changes only
`u`, direction `2` changes only `w`, and the other anchors leave `(q,w,u)`
fixed while increasing `Theta` by `1`. So `x_{n+1} = xhat_{n+1}` in full current
coordinates.

Thus the actual and candidate branches agree for all `n <= N_f`, and every
pre-exit actual state is `B`-labeled.

For `n < N_f`, Proposition 3.4 and Lemma 3.3 show that the candidate state does
not exit to `H_{L1}`; because the trigger test depends only on the current
coordinates `(q,w,u,Theta)`, the actual state does not exit either. At time
`N_f`, Proposition 3.4 gives an exit from the candidate orbit at the stated
universal target and direction, so the actual branch exits there as well.

## 4. Fixed-`delta` tail-length reduction

### Definition 4.1 (one-chain event block)

For `delta in Z/m^2 Z`, define the canonical one-chain event block

`W(delta) = (E(m-2,delta), E(m-3,delta), ..., E(0,delta), E(m-1,delta))`.

This is the current-event word read while the chain clock runs once through its
common boundary-to-boundary cycle.

### Lemma 4.2 (the current chain word is determined by `delta`)

Let `C` be any actual lift with boundary label `delta`. Then the current-event
word emitted along the chain `C` is exactly `W(delta)`.

**Proof.** By Input C, every full chain starts at the common boundary clock
value `beta = m - 2`, and inside that chain the clock decreases
deterministically by `1` modulo `m`. The emitted current event at each position
is therefore read from the same explicit law `E(beta,delta)`, with the same
ordered list of clock values `m-2,m-3,...,0,m-1`. So the full chain emits
exactly the block `W(delta)`.

### Proposition 4.3 (block stack determined by start label and tail length)

Let `C` be an actual lift with boundary label `delta`.

1. If `tau(C)=t<infty`, then the forward chain labels are
   `delta, delta+1, ..., delta+t`, where the chain at `delta+t` is terminal,
   and the padded future current-event word of `C` is
   `W(delta) W(delta+1) ... W(delta+t) Pad`.
2. If `tau(C)=infty`, then the padded future current-event word of `C` is the
   infinite concatenation
   `W(delta) W(delta+1) W(delta+2) ...`.

In particular, the padded future current-event word is completely determined by
`delta` together with `tau(C)`.

**Proof.** Start with the current chain. By Lemma 4.2, it emits `W(delta)`.

If no successor exists, then `tau(C)=0`, the current chain is terminal, and by
the fixed padding convention the future word is `W(delta) Pad`. So the claim
holds in the base case.

Now suppose a successor chain exists. By Input C, its boundary label is
`delta+1`. By Lemma 4.2 again, that successor emits the block `W(delta+1)`.
Repeating the same argument for each further successor yields the entire stack
`W(delta), W(delta+1), W(delta+2), ...` until the first terminal chain, if one
occurs, or forever if no terminal chain occurs.

Thus a finite tail of length `t` gives exactly the finite concatenation through
`delta+t` followed by the common padding suffix `Pad`, while an infinite tail
gives the infinite concatenation. No other local future-law choice remains.

### Theorem 4.4 (future data are determined by tail length)

Let `C1` and `C2` be actual lifts of the same realized boundary label `delta`.

Then:

1. if `tau(C1)=tau(C2)`, then `C1` and `C2` have the same padded future
   current-event word;
2. `C1` and `C2` have the same padded future current-event word if and only if
   they lie in the same endpoint class;
3. `C1` and `C2` lie in the same endpoint class if and only if
   `rho(C1)=rho(C2)`.

Equivalently, at fixed realized `delta`, the padded future current-event word,
the endpoint class, and the boundary right-congruence class `rho` are all
determined by the remaining full-chain tail length.

**Proof.** By Proposition 4.3, the padded future current-event word of an actual
lift is a function only of its starting label `delta` and its tail length
`tau`. Therefore, for two lifts starting at the same realized label `delta`,
equality of tail length is sufficient for equality of the padded future word.

Items (2) and (3) are merely the definitions of endpoint class and of the
right-congruence label `rho` attached to the padded future word.

### Corollary 4.5 (different tail lengths create a later mixed-status row)

Let `C1` and `C2` be actual lifts of the same realized label `delta`, and
assume `tau(C1) != tau(C2)`. Set

`t = min{tau(C1), tau(C2)} < infty`.

Then the later realized label `delta+t` is mixed-status: one actual lift at
that label is terminal and another actual lift at that same label continues.

**Proof.** By Proposition 4.3, both lifts follow the same deterministic block
stack through the chain labels `delta, delta+1, ..., delta+t`. At the last of
these labels, namely `delta+t`, the lift with shorter tail has no further
successor, while the other lift still has at least one more successor. So
`delta+t` is realized with both a terminal lift and a continuing lift.

## 5. Regular chart consequences

### Proposition 5.1 (chart/interface landing)

Read the actual exceptional post-exit continuation in the grouped full-chain
chart used for the boundary labels. Then its first two chart labels are forced
to be

`3m-2 -> 3m-1`.

Equivalently, the exceptional chain-label continuation is

`3m-3 -> 3m-2 -> 3m-1`,

where `3m-2` is the unique terminal regular source-`4` occurrence and `3m-1`
is the regular source-`1` start.

**Proof.** The exceptional cutoff row is, by definition,

`delta = 3m-3`.

In the grouped chart quotient, successor is exact and advances the label by
`+1`. Therefore the first chart label after the cutoff row is forced to be

`3m-2`.

By Input D, the source-`4` terminal label is

`e_4 = m(4-1) - 2 = 3m-2`,

and the regular source-`1` start label is

`s_1 = m(1+2) - 1 = 3m-1`.

Again by Input D, the label immediately after `e_4` is `s_{4-3} = s_1`. So the
interface is exactly

`3m-2 -> 3m-1`.

### Theorem 5.2 (regular closure theorem)

On the true larger regular accessible union, every regular realization of every
realized `delta` continues.

**Proof.** Take any regular realization and choose one regular holder for its
label.

If the realization is interior in that holder, grouped successor exactness
inside the source window gives a forward successor immediately.

If the realization sits at the terminal label of that holder, then its label is
some `e_u`, and Input D gives a forward successor to `e_u + 1 = s_{u-3}`.

So every regular realization continues.

### Corollary 5.3 (no regular mixed-status row)

No realized regular `delta` has both continuing and terminal regular lifts.

**Proof.** By Theorem 5.2, every regular lift continues.

## 6. Actual exceptional interface landing

### Theorem 6.1 (actual exceptional interface landing)

Every actual lift of the exceptional cutoff row `delta = 3m-3` reaches the
universal raw exit target

`T_exc = (m-2,m-1,1)`

by direction `1`, and the corresponding full-chain labels continue as

`3m-3 -> 3m-2 -> 3m-1`.

Here `3m-2` is the terminal regular source-`4` occurrence and `3m-1` is the
regular source-`1` start.

**Proof.** By Theorem 3.6, every actual lift of the exceptional family exits
the active branch at the same raw state `T_exc` and with the same exit
direction `1`. Therefore all such lifts share the same immediate raw
post-exit continuation by raw determinism.

Proposition 5.1 then identifies the corresponding chain-label continuation with

`3m-3 -> 3m-2 -> 3m-1`.

So the exceptional actual lift has a forced landing row and a forced interface
continuation.

### Corollary 6.2 (single-row globalization criterion)

Assume the standing inputs of Section 2. Then the full raw globalization
theorem is equivalent to one statement:

> every actual lift of the exceptional cutoff row `delta = 3m-3` glues through
> `3m-2 -> 3m-1` into the regular continuing endpoint class.

**Proof.** By Theorem 5.2, the regular sector is already closed. By Input E,
every exceptional full chain before the cutoff continues internally by
`delta -> delta+1`. So the only row that can still launch a new endpoint sheet
is the exceptional cutoff row.

## 7. Final globalization theorem

### Lemma 7.1 (one-chain pullback of endpoint class)

Let `C1_plus` and `C2_plus` be actual lifts of the same realized boundary label
`delta+1`, and suppose they lie in the same endpoint class.

Assume `C1` and `C2` are predecessor full chains of `C1_plus` and `C2_plus`
respectively, both with boundary label `delta`.

Then `C1` and `C2` also lie in the same endpoint class.

**Proof.** By Lemma 4.2, the current-event word emitted along any full chain of
boundary label `delta` is the same canonical block `W(delta)`. So the padded
future word of each predecessor chain is obtained by prefixing the same block
`W(delta)` to the padded future word of its successor chain.

Since `C1_plus` and `C2_plus` lie in the same endpoint class, they have the
same padded future current-event word. Prefixing the same block `W(delta)` to
both words preserves equality. Therefore `C1` and `C2` have the same padded
future current-event word, hence lie in the same endpoint class.

### Theorem 7.2 (odd-`m` D5 final globalization theorem)

For odd `m` in the accepted D5 regime, every actual lift of the exceptional
cutoff row `delta = 3m-3` continues through

`3m-2 -> 3m-1`

and lies in the regular continuing endpoint class there.

Consequently:

1. no mixed-status realized `delta` exists;
2. fixed realized `delta` determines tail length;
3. fixed realized `delta` determines endpoint class and padded future word;
4. `rho = rho(delta)` globally;
5. raw global `(beta,delta)` is exact on the true accessible boundary union.

**Proof.** Take any accessible full chain.

If it is regular, Theorem 5.2 gives a forward successor.

If it is exceptional but not the cutoff chain, Input E gives a forward
successor by `delta -> delta+1`.

If it is the exceptional cutoff chain, Theorem 6.1 gives a forward successor
and pins its next two labels to `3m-2 -> 3m-1`.

So every accessible full chain has a forward successor.

Now let `C` be a splice-connected accessible component. By Input C, its
realized boundary image is either a forward interval in `Z/m^2 Z` or the full
cycle. A finite forward interval has a right-end chain with no successor, which
we have just ruled out. Hence every splice-connected accessible component is
total, and every actual lift has tail length `infty`.

Theorem 4.4 says that fixed realized `delta` determines the padded future
current-event word, the endpoint class, and the boundary right-congruence class
`rho` once tail length is fixed. Since tail length is now always `infty`, it
follows that

`rho = rho(delta)`

globally, and raw global `(beta,delta)` is exact.

It remains to recover the stated gluing conclusion. Let `E_+` be the
exceptional lift at `delta = 3m-1` reached from the cutoff row, and let `R_+`
be the regular source-`1` start lift at the same label. By Theorem 6.1, `E_+`
exists and is reached through `3m-3 -> 3m-2 -> 3m-1`. Both `E_+` and `R_+`
have infinite tail length, so Theorem 4.4 forces them to have the same
endpoint class. Lemma 7.1 then pulls that equality back one full chain to the
interface row `3m-2`. Thus every actual lift of the exceptional cutoff row
glues through the interface `3m-2 -> 3m-1` into the regular continuing endpoint
class.

## 8. Honest boundary

This note is meant to be read in one pass, but it still has a sharp honesty
boundary.

What is fully carried out here:

1. the structural first-exit theorem from the explicit trigger formula and the
   coarse patch facts;
2. the fixed-`delta` tail-length reduction from the componentwise bridge law;
3. the chart/interface landing theorem;
4. the regular closure theorem;
5. the final globalization proof.

What is stated here as standing theorem-package input rather than redeveloped
from raw artifacts:

1. the exact trigger-family formula itself;
2. the coarse patch-table facts;
3. the componentwise concrete bridge theorem;
4. the regular chart / endpoint support package;
5. the exceptional source-`3` interior continuation fact.

So this is a one-document globalization package for reading and manuscript
flow, not a first-principles rebuild of every older support artifact and not
yet a full graph-theoretic Hamilton-decomposition proof.
