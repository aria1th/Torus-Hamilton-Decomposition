# D5 097: Compact reproof of the 077 fixed-delta tail-length reduction

## Abstract

This note removes the standalone `077` support theorem by proving directly the
exact statement used later in `092`.

The reproof is short once the bridge platform is written explicitly in cleaned
form. The bridge proposition already used in `092` supplies two decisive facts:

1. on a full chain with boundary label `delta`, the current event class is an
   explicit function of `(beta,delta)`;
2. whenever a forward successor chain exists, its boundary label is `delta+1`.

So a lift starting at `delta` emits a deterministic chain block `W(delta)`,
then `W(delta+1)`, then `W(delta+2)`, and so on, until terminality or forever.

Therefore the padded future current-event word of an actual lift is determined
by exactly two pieces of data:

- its starting label `delta`,
- its remaining full-chain tail length.

Equivalently, at fixed realized `delta`, two actual lifts can differ only by
remaining tail length. The old `080` no-mixed-delta reduction then becomes an
immediate corollary.

## 1. Scope and imported bridge platform

Fix an odd modulus `m` in the accepted D5 regime and the best-seed channel

`R1 -> H_{L1}`.

We use the standard cleaned definitions from `092`.

### Definition 1.1: full chains, actual lifts, tail length

A **full chain** is a complete boundary block between consecutive visits to the
`Theta=2` section.

An **actual lift** of a realized boundary label `delta0` is an actual
accessible full-chain occurrence with boundary label `delta0`.

The **remaining tail length** `tau(C)` of an actual lift `C` is the number of
full-chain successors available after `C` before terminality. If successors
continue forever, then `tau(C)=infty`.

### Definition 1.2: endpoint class and padding

Fix the standard accepted terminal padding convention from `092` for future
current-event words. Two actual lifts lie in the same **endpoint class** when
they determine the same padded future current-event word.

Write `Pad` for the common terminal padding tail supplied by that convention.
The corresponding boundary right-congruence class is denoted by `rho`.

Let the current-event alphabet be

`A = {wrap, carry_jump, other_1000, other_0010, flat}`.

The present note imports only the bridge platform already written explicitly in
cleaned form in Proposition 4.1 of `092`:

1. every full chain starts at the common boundary clock value `beta=m-2`, and
   during that chain the clock evolves by `beta -> beta-1 mod m`;
2. there is an explicit current-event law
   `E : Z/mZ x Z/m^2 Z -> A`, `(beta,delta) -> epsilon_4(beta,delta)`,
   which is independent of any component tag;
3. if a full chain `C'` is the successor of a full chain `C`, then
   `delta(C') = delta(C)+1 mod m^2`.

Item (2) is exactly the explicit event law carried by the componentwise bridge
platform. Item (3) is the componentwise odometer splice law.

## 2. Deterministic chain blocks

### Definition 2.1: the one-chain block at label `delta`

For `delta in Z/m^2 Z`, define the canonical one-chain event block

`W(delta) = (E(m-2,delta), E(m-3,delta), ..., E(0,delta), E(m-1,delta))`.

This is the current-event word read while the chain clock runs once through its
common boundary-to-boundary cycle.

### Lemma 2.2: the current chain word is determined by `delta`

Let `C` be any actual lift with boundary label `delta`. Then the current-event
word emitted along the chain `C` is exactly `W(delta)`.

**Proof.** Every full chain starts at the common boundary clock value
`beta=m-2`, and inside that chain the clock decreases deterministically by `1`
modulo `m`. The emitted current event at each position is therefore read from
the same explicit law `E(beta,delta)`, with the same ordered list of clock
values `m-2,m-3,...,0,m-1`. So the full chain emits exactly the block
`W(delta)`.

### Proposition 2.3: block stack determined by start label and tail length

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

**Proof.** Start with the current chain. By Lemma 2.2, it emits `W(delta)`.

If no successor exists, then `tau(C)=0`, the current chain is terminal, and by
the fixed padding convention the future word is `W(delta) Pad`. So the claim
holds in the base case.

Now suppose a successor chain exists. By the odometer splice law from the
imported bridge platform, its boundary label is `delta+1`. By Lemma 2.2 again,
that successor emits the block `W(delta+1)`. Repeating the same argument for
each further successor yields the entire stack
`W(delta), W(delta+1), W(delta+2), ...` until the first terminal chain, if one
occurs, or forever if no terminal chain occurs.

Thus a finite tail of length `t` gives exactly the finite concatenation through
`delta+t` followed by the common padding suffix `Pad`, while an infinite tail
gives the infinite concatenation. No other local future-law choice remains.

## 3. The reproof replacing 077

### Theorem 3.1: fixed-`delta` ambiguity reduces to tail length

Let `C1` and `C2` be actual lifts of the same realized boundary label `delta`.
Then the following hold:

1. if `tau(C1)=tau(C2)`, then `C1` and `C2` have the same padded future
   current-event word;
2. `C1` and `C2` have the same padded future current-event word if and only if
   they lie in the same endpoint class;
3. `C1` and `C2` lie in the same endpoint class if and only if
   `rho(C1)=rho(C2)`.

Equivalently, at fixed realized `delta`, the padded future current-event word,
the endpoint class, and the boundary right-congruence class `rho` are all
determined by the remaining full-chain tail length. There is no further local
future-law ambiguity at fixed realized `delta`.

**Proof.** By Proposition 2.3, the padded future current-event word of an actual
lift is a function only of its starting label `delta` and its tail length
`tau`. Therefore, for two lifts starting at the same realized label `delta`,
equality of tail length is sufficient for equality of the padded future word.

Items (2) and (3) are merely the definitions of endpoint class and of the
right-congruence label `rho` attached to the padded future word.

### Corollary 3.2: first divergence occurs at the shorter terminal row

Let `C1` and `C2` be actual lifts of the same realized label `delta`, and
assume `tau(C1) != tau(C2)`. Set

`t = min{tau(C1), tau(C2)} < infty`.

Then the later realized label `delta+t` is mixed-status: one actual lift at
that label is terminal and another actual lift at that same label continues.

**Proof.** By Proposition 2.3, both lifts follow the same deterministic block
stack through the chain labels `delta, delta+1, ..., delta+t`. At the last of
these labels, namely `delta+t`, the lift with shorter tail has no further
successor, while the other lift still has at least one more successor. So
`delta+t` is realized with both a terminal lift and a continuing lift.

### Corollary 3.3: 080 becomes immediate

If no realized boundary label is mixed-status, then fixed realized `delta`
determines tail length.

Consequently, fixed realized `delta` determines endpoint class and the padded
future current-event word.

**Proof.** If fixed realized `delta` did not determine tail length, then two
lifts of that `delta` would have different tail lengths, and Corollary 3.2
would produce a later mixed-status realized label. So no mixed-status implies
realization-independent tail length at fixed `delta`.

The endpoint-class and padded-word conclusions then follow from Theorem 3.1.

### Corollary 3.4: how 097 is used in the final globalization proof

Assume every actual lift has infinite tail length. Then fixed realized `delta`
determines:

1. the padded future current-event word,
2. the endpoint class,
3. the boundary right-congruence class `rho`.

Hence `rho = rho(delta)` globally.

**Proof.** Under the hypothesis, any two lifts of the same realized `delta`
have the same tail length, namely `infty`. Apply Theorem 3.1.

## 4. What 097 changes in the cleaned package

### Corollary 4.1: accepted-support list after 097

Relative to the cleaned `092` package and the already completed reproof notes
`095`--`096`, the old `077` theorem no longer needs to remain in
accepted-support form.

So after `097`, the cleaned odd-`m` D5 package no longer imports `077`, `079`,
or `081` as separate support theorems. The remaining imported inputs are the
componentwise bridge platform and the localized structural first-exit block
used inside Sections 3 and 4 of `092`.

### Remark 4.2: what this note does and does not use

This note is a pure theorem-level reproof. Unlike the older `077` support
note, it does not rely on frozen actual-union checks for small moduli. The
proof needs only the explicit bridge law written in cleaned form and the
standard `092` definitions.

In particular, the old `080` reduction is now compressed to Corollary 3.3
inside this same note.
