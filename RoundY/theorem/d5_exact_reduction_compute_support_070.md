# D5 Exact Reduction Compute Support 070

This note pushes the compute-support side of the `069` exact-reduction program on the frozen checked-range data only. It does **not** reopen broad controller search.

## Inputs
- `045` frozen active carry dataset
- `047` frozen `(B,c,tau,epsilon4)` dataset
- `045` admissible family catalog (`69,994` families total across the three catalogs)

## 1. Marked length-`m` slice chains
I extracted the regular carry-jump slice chains exactly as in the `068/069` support picture: for each checked modulus and each fixed `(source_u, w)` with regular family, the carry-jump rows form a chain
\[
q=0,1,\dots,m-1
\]
with carry mark `c=1` only at `q=m-1`.

I then ran an **exhaustive** search over all `69,994` catalog families on these slice chains, asking for:
- exact carry readout on every slice chain, and
- deterministic successor on every slice chain.

Result:
- the smallest exact deterministic quotient size is exactly `m` on each checked modulus;
- the best families already appear among the 025-style gauge features, for example:
  - `cur:antidiag_omit.tau_lo`
  - `cur:diag_omit.tau_lo`
  - `nxt:antidiag_omit.tau_lo`
  - `nxt:diag_omit.tau_lo`
- by contrast, the 2-state families built from `next_dn` (and `dn + next_dn`) still read carry exactly but remain nondeterministic.

So on the first exact marked object, the intended class already sees an **exact deterministic length-`m` chain**, and `m` is the first exact deterministic quotient scale in the checked catalog.

## 2. Longer spliced source chains do not compress
I then spliced all regular carry-jump slices for a fixed regular source into the longer source-chain of length
\[
m(m-3)
\]
(on the checked moduli: `10, 28, 54, 88`).

Again I ran the full `69,994`-family catalog search, now asking for exact carry readout and deterministic successor on these longer spliced chains.

Result:
- the smallest exact deterministic quotient size jumps to the **full source-chain length** `m(m-3)`;
- no catalog family compresses the spliced chain below that scale while preserving exactness and determinism;
- the same 2-state `next_dn`-type families still read carry exactly but remain nondeterministic.

So the compute evidence now strongly supports the exact-reduction slogan:

> **the right first exact object is a marked length-`m` chain before any stronger cycle / spliced-chain identification.**

## 3. Full active-branch event quotients
On the full checked active branch, I also searched the smaller catalogs exhaustively for an **exact deterministic current-event quotient** using the refined event label
\[
\mathrm{event}_5 \in \{\mathrm{flat},\mathrm{wrap},\mathrm{carry\_jump},\mathrm{other\_1000},\mathrm{other\_0010}\}.
\]

Exhaustive checked-range results:
- `core_transition`: **0** exact deterministic event quotients
- `point_defect_basis`: **0** exact deterministic event quotients

I also checked the **full catalog vectors** themselves:
- full `core_transition` vector: exact for current event, but not deterministic on successor
- full `gauge_transition_basis` vector: exact for current event, but not deterministic on successor
- full `point_defect_basis` vector: exact for current event, but not deterministic on successor

So the first small admissible catalogs do **not** yet produce the full exact deterministic event quotient on the whole active branch, even though they already see the marked slice chain exactly.

## 4. Compute conclusion
The checked compute picture is now:

1. the marked carry-jump slice chain of length `m` is the safer first exact reduction object;
2. the admissible catalog already induces exact deterministic quotients of size exactly `m` on that object;
3. the longer spliced source-chain does **not** compress inside the same catalog;
4. the first small catalogs still do **not** give an exact deterministic current-event quotient on the full active branch.

So the most honest next reduction/realization question is now:

> can one pass from the exact marked length-`m` chain to the exact event quotient needed for realization, without trying to force the longer spliced chain/cycle too early?

## 5. Compute cost
- slice-chain exhaustive catalog search: `73.48` s
- spliced-chain exhaustive catalog search: `41.58` s
- full-branch small-catalog event search: lightweight (core + point catalogs only)
