# D5 275 Route-E Color-2 Residual Probe

This note records the next honest reduction after the compressed exactness
search of
[d5_274_routee_assembly_pattern_search.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_274_routee_assembly_pattern_search.md).

Primary files:

- [torus_nd_d5_routee_color2_residual_probe_275.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_routee_color2_residual_probe_275.py)
- [d5_275_routee_color2_residual_probe_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_275_routee_color2_residual_probe_summary.json)
- [per_modulus.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_275_routee_color2_residual_probe/per_modulus.json)
- [best_rule.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_275_routee_color2_residual_probe/best_rule.json)

## 1. Setup

Let `H_0,...,H_4` be the five torus maps defined by the combined best exact
rule saved in `274`:

- keep the closed `Sel*` colors `3,4`,
- assign colors `0,1,2` by one fixed permutation on
  `S0`, `S1`, `S4+`, `S2(A2)`, `S3(1 in A3)`.

Let

- `P0 = {x : Sigma(x) = 0}`,
- `R_c = (H_c)^m | P0`.

The purpose of this note is not to prove Hamiltonicity yet. It is to identify
which residual color now looks like a genuine Route-E target.

## 2. Exactness of the combined best rule

The checker verifies that this combined-best `274` rule is exact on the checked
odd moduli

- `m = 5,7,9,11,13`.

So the remaining problem is no longer “find an exact family.” The family is
already exact on the checked range. What remains is Hamiltonicity of the open
colors inside that family.

## 3. Why color `2` is the clean residual target

On `P0`, the checked first-return cycle profiles are:

- color `1`:
  - `m=5`: `{47:1, 128:1, 129:1, 154:1, 167:1}`
  - `m=7`: `{2401:1}`
  - `m=9`: `{753:1, 1540:1, 4268:1}`
  - `m=11`: `{52:1, 1383:1, 1636:1, 5745:1, 5825:1}`
  - `m=13`: `{2305:1, 2772:1, 6943:1, 7124:1, 9417:1}`
- color `2`:
  - `m=5`: `{5:16, 9:1, 268:2}`
  - `m=7`: `{7:36, 181:1, 1968:1}`
  - `m=9`: `{9:112, 5553:1}`
  - `m=11`: `{11:100, 13541:1}`
  - `m=13`: `{13:144, 26689:1}`

So color `1` is not the clean next target. Its checked behavior changes too
much across small moduli.

Color `2` is different:

- it keeps one dominant long cycle;
- the defect part is visibly organized into short `m`-cycles;
- and, most importantly, its `P0` return law collapses to a fixed finite
  displacement support.

That is the classical Route-E signature.

## 4. Stable five-branch affine support

For every checked modulus `m = 5,7,9,11,13`, the color-`2` first return `R_2`
has exactly five displacement vectors on the first four `P0` coordinates:

- `G = (m-2, 1, 0, 1)`,
- `M = (m-3, 2, 0, 1)`,
- `A = (m-3, 1, 0, 2)`,
- `B = (m-3, 1, 0, 1)`,
- `C = (m-3, 1, 1, 1)`.

The checked branch counts are:

- `|A| = |B| = |C| = m(m-1)`,
- `|M| = 145,469,1089,2101,3601` for `m=5,7,9,11,13`,
- `|G| = 420,1806,5256,12210,24492` for `m=5,7,9,11,13`.

In particular, the displacement support is already stable before any symbolic
proof is written.

## 5. Finite-defect geometry already visible

The three smallest defect branches are not spread arbitrarily across `P0`.
They are localized on three simple coordinate surfaces throughout the checked
range:

- every `B`-branch point satisfies `x_3 = m-2`,
- every `A`-branch point satisfies `x_4 = m-1`,
- every `C`-branch point satisfies `x_0 = m-1`.

So even before writing the theorem, the residual color-`2` return already has
the shape of a finite-defect stitching problem, not a broad uncontrolled
selector search.

## 6. No linear-invariant obstruction remains

There is no nontrivial linear invariant of the form

`L(x_0,x_1,x_2,x_3) (mod m)`

that is forced purely by the affine support of `R_2` on the checked moduli
`m = 5,7,9,11,13`.

This matters because the old obstruction notes `269–271` ruled out the previous
families precisely by finding coarse invariants or coarse local collisions.
That type of obstruction has now disappeared for the residual color-`2`
candidate.

## 7. Meaning for the remaining theorem

After `274`, the remaining five-color assembly theorem was reduced to

- a finite exactness family, followed by
- one or two residual Hamilton closures.

After the present probe, the sharper reading is:

- the combined best `274` family is an exact checked family,
- color `2` is the clean Route-E residual target,
- color `1` is no longer the immediate next theorem target.

So the next serious theorem should be a color-`2` Route-E statement for the
combined-best `274` family:

1. identify a natural section inside `P0`,
2. write the first return on that section,
3. prove a finite-defect stitching theorem,
4. lift back to Hamiltonicity of `H_2`.

## 8. Bottom line

The five-color assembly problem is no longer best read as “find a brand-new
five-color package.”

It is now much narrower:

- keep the combined-best exact `274` family,
- treat color `2` as the next Route-E branch,
- and prove one more finite-defect return/stitching theorem.

That is the cleanest current path toward a fully closed odd-`m`, `d=5`
graph-side proof.
