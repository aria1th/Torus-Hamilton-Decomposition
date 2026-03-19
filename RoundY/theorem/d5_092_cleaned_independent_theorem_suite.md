# D5 092: Cleaned theorem suite in independent form for odd `m`

## Abstract

This note repackages the current odd-`m` D5 closure into one manuscript-order
suite of theorem statements.

The statements are no longer split across the `033 -> 062 -> 076 -> 077 ->
079 -> 081 -> 082 -> 083` chain. The structural first-exit theorem and the
chart-to-raw composition step are written explicitly, and the final gluing
argument is presented as one continuous proof.

The note stays honest about support. The componentwise concrete bridge remains
in accepted theorem form. The chart/interface, regular-continuation,
tail-length, and compact structural roles are supplied by the cleanup notes
`095`--`098` rather than rederived here from the original compute-backed files.

## 1. Scope and conventions

Fix an odd modulus `m` in the accepted D5 regime, and fix the best-seed channel

`R1 -> H_L1`

with endpoint seed

`L = [2,2,1]`, `R = [1,4,4]`.

The final theorem we want in cleaned form is:

> every actual lift of the exceptional cutoff row `delta = 3m-3` continues
> through `3m-2 -> 3m-1` and lies in the regular continuing endpoint class
> there.

Equivalent corollaries are:

1. no mixed-status realized `delta` exists on the true accessible union;
2. fixed realized `delta` determines tail length;
3. fixed realized `delta` determines endpoint class and padded future word;
4. `rho = rho(delta)` globally;
5. raw global `(beta,delta)` is exact.

The goal of this note is not to enlarge the accepted scope. It is to put the
current odd-`m` D5 result into a theorem package that is independent in
statement and dependency order.

## 2. Definitions

### Definition 2.1 (full chains and actual lifts)

A **full chain** is a complete boundary block between consecutive visits to the
`Theta = 2` section. Its boundary label is the intrinsic digit `delta` defined
below.

An **actual lift** of a row `delta_0` is an actual accessible full-chain
occurrence whose boundary label is `delta_0`.

### Definition 2.2 (accessible boundary union and components)

The **accessible boundary union** is the union of all actual accessible full
chains.

A **splice-connected accessible component** is a connected component of that
union under the successor/predecessor splice relation between consecutive full
chains.

### Definition 2.3 (tail length)

The **remaining tail length** of an actual lift is the number of full-chain
successors still available before terminality. If successors continue forever,
its tail length is `infty`.

### Definition 2.4 (endpoint class and `rho`)

Choose the standard accepted terminal padding convention on future current-event
words, so that finite and infinite tails are compared in one common one-sided
shift space.

Two actual lifts are in the same **endpoint class** when they determine the
same padded future current-event word. The corresponding boundary
right-congruence class is written `rho`.

### Definition 2.5 (distinguished rows)

The **exceptional cutoff row** is

`delta = 3m-3`.

The corresponding interface rows are

`3m-2` and `3m-1`.

## 3. Structural first-exit package

### Theorem 3.1 (structural first-exit theorem)

Let `rho = u_source + 1 mod m` for the chosen source family, and let
`xhat_n = (q_n,w_n,u_n,Theta_n)` be the candidate active orbit starting from the
alt-`2` entry

`E = (m-1,1,u_source,2)`.

Then the following hold.

1. The trigger family is exactly

   `H_L1 = {(q,w,u,lambda) = (m-1,m-1,u,2) : u != 2}`.

2. Every phase-`1` state on the candidate orbit satisfies

   `q = u - rho + 1 mod m`.

3. The only phase-`1` states from which an alternate step can land in `H_L1`
   are

   `T_reg = (m-1,m-2,1)` by direction `2`,

   and

   `T_exc = (m-2,m-1,1)` by direction `1`.

4. If `rho != 4`, the first exit is `T_reg`. If `rho = 4`, the first exit is
   `T_exc`.

5. The actual active branch agrees with the candidate orbit up to first exit.
   Therefore the regular families first exit at `T_reg` by direction `2`, and
   the exceptional family first exits at `T_exc` by direction `1`.

#### Proof

Write the candidate update as

- `Fhat(q,w,u,0) = (q+1,w,u,1)`,
- `Fhat(q,w,u,1) = (q,w,u+1,2)`,
- `Fhat(q,w,u,2) = (q,w+1_{q=m-1},u,3)`,
- `Fhat(q,w,u,Theta) = (q,w,u,Theta+1)` for `3 <= Theta <= m-1`.

The exact trigger family is the compact trigger-family lemma later isolated in
`098`, namely

`H_L1 = {(m-1,m-1,u,2) : u != 2}`.

So only phase-`1` current states can trigger an alternate step into `H_L1`,
and a trigger must arrive at `(q',w') = (m-1,m-1)`.

On the candidate orbit, every phase-`1` state satisfies

`q = u - rho + 1 mod m`.

This is the phase-`1` source-residue invariant later packaged in `098`: it holds at the first
phase-`1` state after entry, and from one phase-`1` state to the next both
sides increment by `1`.

Now there are only two ways to reach `(q',w') = (m-1,m-1)` at layer `2`:

- by direction `2` from `(q,w,Theta) = (m-1,m-2,1)`,
- by direction `1` from `(q,w,Theta) = (m-2,m-1,1)`.

These are exactly `T_reg` and `T_exc`. At `T_reg` the invariant gives

`u = rho - 2 mod m`,

so the trigger condition `u != 2` holds exactly when `rho != 4`. At `T_exc` the
invariant gives

`u = rho - 3 mod m`,

so when `rho = 4` one has `u = 1`, hence `u != 2`, and the exit occurs there.
Thus the candidate first exits are the universal targets stated above.

The last localized structural ingredient is pre-exit patch avoidance, also
written out explicitly in `098`: before the candidate first-exit time, the
candidate orbit avoids the patched current classes. Hence all pre-exit actual
states are `B`-labeled and therefore follow the same full-coordinate updates as
the candidate orbit. So the actual active branch agrees with the candidate
orbit up to first exit, and the same first-exit statement holds on the actual
branch. `qed`

## 4. Support theorems in cleaned form

### Proposition 4.1 (componentwise concrete bridge; accepted support theorem)

On the unique `Theta = 2` boundary state `(q,w,u,2)` of a full chain, define

- `sigma = w + u - q - 1 mod m`,
- `delta = q + m sigma`.

Then on each splice-connected accessible component:

1. consecutive full chains satisfy the odometer splice law

   `delta' = delta + 1 mod m^2`;

2. the current event class `epsilon4` is determined by `(beta,delta)`;

3. the realized boundary image is a forward interval in `Z/m^2 Z` or the full
   odometer cycle.

#### Proof status

This is the promoted theorem content of `076`, rewritten as one compact bridge
statement.

### Proposition 4.2 (tail-length reduction; compactly reproved support theorem)

At fixed realized `delta`, two actual lifts can differ only by remaining
full-chain tail length.

Equivalently, once the concrete bridge package is accepted, there is no further
local future-law ambiguity at fixed realized `delta`; the only possible
ambiguity is endpoint geometry.

#### Proof status

This is the compact reproof content of `097`, replacing the old standalone
`077` role in the cleaned suite.

### Proposition 4.3 (chart/interface theorem; compactly reproved support theorem)

The exceptional continuation is pinned in chart / chain-label coordinates to

`3m-3 -> 3m-2 -> 3m-1`,

where

- `3m-2` is the unique terminal regular source-`4` occurrence,
- `3m-1` is the regular source-`1` start.

#### Proof status

This is the compact reproof content of `095`, replacing the old standalone
`079` role in the cleaned suite.

### Proposition 4.4 (regular continuation theorem; compactly reproved support theorem)

Every regular realization of every realized `delta` continues on the true larger
regular accessible union.

Equivalently, the regular sector contributes no mixed-status `delta` and no
regular tail-length ambiguity.

#### Proof status

This is the compact reproof content of `096`, replacing the old standalone
`081` role in the cleaned suite.

## 5. The cleaned composition theorem

### Theorem 5.1 (actual exceptional interface landing)

Every actual lift of the exceptional cutoff row `delta = 3m-3` reaches the
universal raw exit target

`T_exc = (m-2,m-1,1)`

by direction `1`, and the corresponding full-chain labels continue as

`3m-3 -> 3m-2 -> 3m-1`.

Here `3m-2` is the terminal regular source-`4` occurrence and `3m-1` is the
regular source-`1` start.

#### Proof

By Theorem 3.1, every actual lift of the exceptional family exits the active
branch at the same raw state `T_exc` and with the same exit direction `1`.
Therefore all such lifts share the same immediate raw post-exit continuation by
raw determinism.

Proposition 4.3 then identifies the corresponding chain-label continuation with

`3m-3 -> 3m-2 -> 3m-1`.

So the exceptional actual lift has a forced landing row and a forced interface
continuation. `qed`

### Corollary 5.2 (single-row globalization criterion)

Assume the support theorems of Section 4. Then the full raw
globalization theorem is equivalent to one statement:

> every actual lift of the exceptional cutoff row `delta = 3m-3` glues through
> `3m-2 -> 3m-1` into the regular continuing endpoint class.

#### Proof

By Proposition 4.4, the regular sector is already closed. By Proposition 4.1,
every exceptional full chain before the cutoff continues internally by the
splice law `delta -> delta+1`. So the only row that can still launch a new
endpoint sheet is the exceptional cutoff row. `qed`

## 6. Final globalization theorem

### Theorem 6.1 (odd-`m` D5 final globalization theorem)

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

#### Proof

Take any accessible full chain.

If it is regular, Proposition 4.4 gives a forward successor.

If it is exceptional but not the cutoff chain, Proposition 4.1 gives a forward
successor by the componentwise splice law `delta -> delta+1`.

If it is the exceptional cutoff chain, Theorem 5.1 gives a forward successor
and pins its next two labels to `3m-2 -> 3m-1`.

So every accessible full chain has a forward successor.

Now let `C` be a splice-connected accessible component. By Proposition 4.1, its
realized boundary image is either a forward interval in `Z/m^2 Z` or the full
cycle. A finite forward interval has a right-end chain with no successor, which
we have just ruled out. Hence every splice-connected accessible component is
total, and every actual lift has tail length `infty`.

Proposition 4.2 says that fixed realized `delta` can differ only by tail
length. Since tail length is now always `infty`, fixed realized `delta`
determines the endpoint class and the padded future current-event word.
Therefore the boundary right-congruence state satisfies

`rho = rho(delta)`

globally, and raw global `(beta,delta)` is exact.

It remains to recover the stated gluing conclusion. Let `E_+` be the
exceptional lift at `delta = 3m-1` reached from the cutoff row, and let `R_+`
be the regular source-`1` start lift at the same label. By Theorem 5.1, `E_+`
exists and is reached through `3m-3 -> 3m-2 -> 3m-1`. Both `E_+` and `R_+`
have infinite tail length, so Proposition 4.2 forces them to have the same
endpoint class. Pulling back one full chain gives the same conclusion at
`3m-2`. Thus every actual lift of the exceptional cutoff row glues through the
interface `3m-2 -> 3m-1` into the regular continuing endpoint class. `qed`

## 7. Exact m=5 reference slice

### Proposition 7.1 (m=5 specialization)

At `m=5`, the distinguished rows are

- `3m-3 = 12`,
- `3m-2 = 13`,
- `3m-1 = 14`.

So the exceptional interface row is exactly

`12 -> 13 -> 14`.

The structural objects specialize to

- `H_L1 = {(4,4,u,2) : u != 2}`,
- `T_reg = (4,3,1)`,
- `T_exc = (3,4,1)`.

Using `delta = q + 5 sigma`, the interface slice is

- `12 = 2 + 5*2`,
- `13 = 3 + 5*2`,
- `14 = 4 + 5*2`.

#### Proof

Substitute `m = 5` into the general formulas of Sections 3 and 4. `qed`

### Remark 7.2 (separate concrete witness at m=5)

The bundle also contains `RoundY/d5_m5_kempe_witness_26.json`, a separate
explicit 26-move Kempe-valid witness with cycle counts `[1,1,1,1,1]`.
That file is direct small-modulus existence evidence. It is logically distinct
from the theorem package above, but it is consistent with the same `m=5`
interface picture.
This is only a formula-level and witness-level specialization. It does not by
itself remove the saved-regular-union caveat recorded in `077`.

## 8. Dependency boundary after cleanup

This note makes the following items explicit in one place:

1. the structural first-exit theorem;
2. the chart-to-raw composition theorem for the exceptional interface;
3. the single-row globalization criterion;
4. the final gluing/globalization proof.

The only theorem layer still used in accepted-support form is:

- the componentwise concrete bridge package (`076`).

The chart/interface, regular-continuation, tail-length, and structural roles
are now supplied by the cleanup notes `095`--`098`.

So this note is now very close to independent in theorem statement and proof
order. It is not yet a full replacement for the compact bridge theorem around
`076`, and it does not claim to be one.
