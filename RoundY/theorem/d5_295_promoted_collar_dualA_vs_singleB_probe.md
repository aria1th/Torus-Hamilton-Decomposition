# D5 295 Promoted-Collar Dual-A Vs Single-B Probe

This note records the next exact narrowing step for the resonant pure
color-`1` branch after the promoted-collar base-section reduction
[d5_289_promoted_collar_base_section_reduction_and_no_go.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_289_promoted_collar_base_section_reduction_and_no_go.md)
and the package-alignment note
[d5_294_residual_package_alignment_after_tar.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_294_residual_package_alignment_after_tar.md).

The saved check outputs are
[d5_295_resonant_same_row_a_probe_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_295_resonant_same_row_a_probe_summary.json)
and
[per_modulus.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_295_resonant_same_row_a_probe/per_modulus.json).

## 1. Baseline and two first refinements

Fix odd resonant `m` and write `r = (m-1)/2`.

For each sign `u in {r-1, r+1}`, start from the promoted-collar control family

`Nhat_m^(u) = Nhat_m(1) U {A_{u,3}}`.

On the reduced base subset

`B_m = {c = 0, d = 0, e = 0}`,

let `P_m^(u)` denote the next-return permutation induced by the color-`1`
section return.

The present probe compares three objects:

- the promoted-collar control `Nhat_m^(u)`;
- the dual-collar family `Nhat_m^(u) U {A_{u',3}}`, where `u'` is the opposite
  collar row in `{r-1, r+1}`;
- the single-`B` refinements `Nhat_m^(u) U {B_{s,3}}` for all rows `s`.

The operational question is simple:

- does a single extra `B` row already change `P_m^(u)`?
- if not, is the first real positive axis the opposite-collar `A` move?

## 2. Checked exact outcome

For the checked resonant moduli

- `m = 21, 27, 33`,

the promoted-collar control cycle lengths on `B_m` are:

- `m = 21`: `11, 5, 5`
- `m = 27`: `13, 12, 2`
- `m = 33`: `17, 11, 5`

For every tested row `s`, adding a single `B_{s,3}` leaves these cycle types
unchanged.

So on the checked range:

> every one-row `B` refinement is inert at the level of the reduced base
> permutation `P_m`.

By contrast, the opposite-collar `A` move changes `P_m` nontrivially:

- `m = 21`: `21`
- `m = 27`: `11, 10, 2, 2, 2`
- `m = 33`: `16, 13, 4`

In particular, the dual-collar `A` family already makes `P_m` a single cycle
at the first checked resonant modulus `m = 21`.

Additional exact spot checks show that this is not only a smallest-modulus
effect.  The same dual-collar `A` move still changes `P_m` at:

- `m = 39`, from `10, 9, 9, 8, 3` to `22, 4, 3, 3, 3, 2, 2`;
- `m = 51`, from `12, 10, 9, 6, 4, 3, 3, 2, 2` to `22, 10, 7, 6, 6`.

## 3. Interpretation

This is the first exact probe in the current resonant program that separates
two nearby refinement ideas cleanly.

- The promoted-collar baseline is a real reduced no-go packet.
- Adding a single `B` row does not change the reduced base object at all on the
  checked moduli.
- Adding the opposite collar-row `A` does change the reduced base object, and
  in the smallest checked resonant case it already closes it.

So the clean current read is stronger than “dual-collar `A` helps once.”
In every checked resonant modulus currently examined, dual-collar `A` changes
the reduced base permutation while one-row `B` does not.

So the next positive search should not be phrased as

- “try a generic one-row `B` compensator on top of the promoted collar”.

The checked data say that this is the wrong axis.

The right immediate axis is instead:

- dual-collar `A`, and then, if needed, `dual-collar A + further compensation`.

## 4. Consequence for the current frontier

This sharpens the current pure color-`1` read in two ways.

First, it makes the `A+B` heuristic from the tar package more concrete:
before asking whether `B` can compensate collateral damage, one must first see
`B` change the reduced object at all.  On the checked moduli, a lone `B` row
does not.

Second, it gives a more precise next-family target:

1. keep the promoted-collar baseline;
2. turn on the opposite collar-row `A`;
3. only then look for the smallest extra support that changes the remaining
   reduced obstruction.

So the current live pure color-`1` question is best read as a
`dual-collar-A-plus-...` problem, not a `single-B` problem.

## 5. Bottom line

The checked resonant branch now supports the following concrete conclusion:

> after the promoted-collar reduction, the first nontrivial family axis is the
> opposite collar-row `A` move, while every one-row `B` refinement is reducedly
> inert on the tested moduli.

That is a materially sharper statement than the earlier generic “try `A+B`
first” reading.
