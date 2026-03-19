# D5 100: Draft graph-theoretic Hamilton decomposition proof for odd `m`

## Abstract

This note is a working draft of the graph-theoretic proof version for the odd
`m`, `d = 5` torus.

Unlike `099`, which packages the odd-`m` D5 globalization theorem, the present
note aims at the actual graph-level statement:

> the directed torus `D_5(m)` admits a decomposition into five arc-disjoint
> directed Hamilton cycles.

The draft is intentionally incomplete. Every missing graph-level bridge,
reduction, or coverage step is left explicitly as `Sorry.` so the document can
be used as an active proof scaffold rather than as an overclaimed theorem note.

## 1. Graph-theoretic target

Let

`D_5(m) = Cay((Z_m)^5, {e_0, e_1, e_2, e_3, e_4})`

be the directed `5`-torus.

Its vertex set is

`V = (Z_m)^5`,

and its directed arc set is

`A = {(x, x + e_i) : x in V, 0 <= i <= 4}`.

### Definition 1.1 (directed Hamilton cycle)

A **directed Hamilton cycle** in `D_5(m)` is a directed cycle that visits every
vertex of `V` exactly once.

Equivalently, it is a cyclic permutation of the `m^5` vertices whose directed
successor arc lies in `A` at every step.

### Definition 1.2 (Hamilton decomposition)

A **Hamilton decomposition** of `D_5(m)` is a family

`H_0, H_1, H_2, H_3, H_4`

of five directed Hamilton cycles such that:

1. the arc sets of the `H_i` are pairwise disjoint;
2. their union is the full directed arc set `A`.

Since `|V| = m^5` and each Hamilton cycle has exactly `m^5` arcs, such a
decomposition would contain exactly `5m^5` arcs in total, which matches the
full directed arc count of `D_5(m)`.

### Theorem 1.3 (draft graph-theoretic main theorem)

Let `m` be odd in the final intended D5 range.

Then the directed torus

`D_5(m) = Cay((Z_m)^5, {e_0, e_1, e_2, e_3, e_4})`

admits a Hamilton decomposition into five arc-disjoint directed Hamilton
cycles.

#### Proof status

**Sorry.** The rest of this note records the missing theorem layers that still
have to be inserted in order for Theorem 1.3 to become an actual proof rather
than a target statement.

## 2. Imported globalization theorem

### Theorem 2.1 (odd-`m` D5 globalization theorem)

Assume odd `m` lies in the accepted D5 regime and work in the best-seed channel

`R1 -> H_{L1}`.

Then every actual lift of the exceptional cutoff row `delta = 3m-3` continues
through

`3m-2 -> 3m-1`

and lies in the regular continuing endpoint class there.

Consequently:

1. no mixed-status realized `delta` exists;
2. fixed realized `delta` determines tail length;
3. fixed realized `delta` determines endpoint class and padded future word;
4. `rho = rho(delta)` globally;
5. raw global `(beta,delta)` is exact on the true accessible boundary union.

#### Proof status

Imported from the one-pass globalization package
[d5_099_one_pass_odd_m_globalization_package.md](./d5_099_one_pass_odd_m_globalization_package.md).

## 3. Reduction from the full odd-`m` D5 problem

The present draft begins in the specific best-seed channel

`R1 -> H_{L1}`

and therefore cannot yet claim to cover the whole odd-`m`, `d = 5` torus
problem without a separate reduction theorem.

### Theorem 3.1 (channel reduction theorem)

To prove Hamilton decomposition of `D_5(m)` for odd `m`, it is enough to prove
the globalization theorem of Theorem 2.1 on the best-seed channel

`R1 -> H_{L1}`,

together with the statement that all other channels are already closed or
reduce to this one.

#### Proof status

**Sorry.** This theorem needs an explicit channel-classification statement and a
precise proof that the present channel is either the last unresolved case or a
canonical representative of all unresolved cases.

### Remark 3.2 (exact missing content)

The missing reduction package should say one of the following, explicitly:

1. every odd-`m`, `d = 5` configuration reduces to the best-seed channel;
2. all other channels are independently solved, and this channel is the unique
   remaining one;
3. the final Hamilton decomposition theorem is a finite disjunction of channel
   theorems, of which the present channel is the only open branch.

At the moment, none of those is written out in this note.

## 4. From raw global exactness to graph-level successor maps

The globalization theorem is phrased in boundary / chain language. A
graph-theoretic proof still needs a section that turns raw global
`(beta,delta)` exactness into globally defined successor maps on the full torus.

### Definition 4.1 (target color factors)

The intended graph-theoretic completion should produce five maps

`F_0, F_1, F_2, F_3, F_4 : V -> V`

with the following properties:

1. for every `x in V` and every `i`, the arc `(x, F_i(x))` is one of the
   directed torus arcs in `A`;
2. each `F_i` is a permutation of `V`;
3. the arc sets

   `A_i = {(x, F_i(x)) : x in V}`

   are pairwise disjoint and together cover `A`.

When those hold, each `A_i` is a directed spanning `1`-factor.

#### Definition status

**Sorry.** The exact formula or witness rule that defines the `F_i` is not
restated here yet. This is only the target shape of the graph-level objects.

### Theorem 4.2 (global bridge descends to full-torus successor maps)

Assume:

1. the channel reduction theorem;
2. the odd-`m` D5 globalization theorem;
3. the accepted D5 witness package that associates boundary / chain data to
   directed torus arcs.

Then the local D5 witness rule descends to globally well-defined maps

`F_0, ..., F_4`

on the full torus as in Definition 4.1.

#### Proof status

**Sorry.** This is the main missing bridge from the boundary-globalization
package to the graph-theoretic statement. The theorem should explain:

1. how the symbolic/boundary system defines outgoing torus arcs;
2. why raw global exactness removes local ambiguity and makes that choice
   globally well defined;
3. why the resulting maps really live on all vertices of the full torus rather
   than only on the accessible boundary union.

### Proposition 4.3 (each `F_i` uses only torus arcs)

For each `i` and each `x in V`, one has

`F_i(x) - x in {e_0, e_1, e_2, e_3, e_4}`.

#### Proof status

**Sorry.** This should be the direct graph-level translation of the accepted D5
local witness / color rule.

### Proposition 4.4 (each `F_i` is a permutation)

For each `i`, the map `F_i : V -> V` is a bijection.

#### Proof status

**Sorry.** This will likely be proved by showing in-degree `= 1` and out-degree
`= 1` for each factor, or by identifying an explicit inverse rule.

## 5. Hamiltonicity of the graph-level factors

Even after the maps `F_i` are globally defined, one still has to prove that
each factor is a **single** Hamilton cycle rather than a disjoint union of
shorter directed cycles.

### Theorem 5.1 (single-cycle theorem for each factor)

For each `i in {0,1,2,3,4}`, the permutation `F_i` is one directed cycle of
length `m^5`.

Equivalently, the spanning `1`-factor `A_i` is a directed Hamilton cycle.

#### Proof status

**Sorry.** This is another essential missing graph-level layer. The theorem
needs a real bridge from the accepted D5 return-map / boundary package to the
claim that the lifted full-torus permutation has exact period `m^5` and only
one orbit.

### Remark 5.2 (what a proof would likely need)

The missing proof probably has to supply some combination of:

1. a full-torus lift from boundary exactness to a global return object;
2. an exact period computation on the lifted object;
3. a proof that no smaller orbit can survive after lifting back to the torus.

At present none of those is written here.

## 6. Edge-disjointness and coverage

### Proposition 6.1 (edge-disjointness)

The arc sets `A_0, ..., A_4` are pairwise disjoint.

#### Proof status

**Sorry.** This should follow from the exact graph-level color rule, but that
rule is not yet written in this note.

### Proposition 6.2 (full coverage of the torus arc set)

One has

`A = A_0 union A_1 union A_2 union A_3 union A_4`.

#### Proof status

**Sorry.** This should be the graph-level completeness statement saying that the
five factors cover every outgoing arc at every vertex exactly once.

### Corollary 6.3 (counting closure)

If each `A_i` is a directed Hamilton cycle and the five `A_i` are pairwise
disjoint, then they form a Hamilton decomposition of `D_5(m)`.

**Proof.** Each `A_i` has exactly `m^5` arcs. So five pairwise disjoint such
cycles contain exactly `5m^5` arcs. But `D_5(m)` also has exactly `5m^5` arcs,
because it has `m^5` vertices and out-degree `5`. Therefore the five arc sets
must cover the full torus arc set.

## 7. Draft final proof

### Theorem 7.1 (draft graph-theoretic odd-`m` D5 theorem)

Let `m` be odd in the final intended D5 range.

Then `D_5(m)` admits a Hamilton decomposition into five arc-disjoint directed
Hamilton cycles.

#### Proof status

Assuming Theorem 3.1, Theorem 4.2, Theorem 5.1, and Proposition 6.1, the
result follows immediately from Corollary 6.3.

**Sorry.** At present those imported steps are not proved in this file, so this
is still only a proof skeleton.

## 8. Exact remaining work

To turn this draft into a genuine graph-theoretic Hamilton decomposition proof,
the following pieces still have to be written.

1. Replace the phrase “odd in the final intended D5 range” by an exact
   quantified statement in `m`.
2. Prove the channel reduction theorem from the full odd-`m`, `d = 5` torus
   problem to the best-seed channel.
3. Restate the exact graph-level rule that turns the accepted D5 witness
   package into five global successor maps `F_i`.
4. Prove that raw global `(beta,delta)` exactness is exactly what makes those
   `F_i` globally well defined.
5. Prove that each `F_i` is one Hamilton cycle rather than a union of smaller
   cycles.
6. Prove edge-disjointness of the five factors at the graph level.
7. Either close Inputs A--E in the same manuscript, or cite them as formal
   earlier theorems with stable theorem-level statements.

So this file is ready as a working manuscript scaffold, but not yet as a
finished Hamilton-decomposition proof.
