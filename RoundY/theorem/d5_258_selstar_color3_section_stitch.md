# D5 258 SelStar Color-3 Section-Stitch Probe

This note records the next step after the `256` no-go and the `257`
factor-level Route-E probe.

Primary files:

- [d5_257_selstar_color3_routee_probe.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_257_selstar_color3_routee_probe.md)
- [torus_nd_d5_selstar_color3_section_stitch_probe_258.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_selstar_color3_section_stitch_probe_258.py)
- [d5_258_selstar_color3_section_stitch_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_258_selstar_color3_section_stitch_summary.json)
- [per_modulus.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_258_selstar_color3_section_stitch/per_modulus.json)

## 1. Purpose

`257` showed that the `Sel*` color-`3` first return

- `R_3^* = (F_3^*)^m | P0`

admits a clean `m^3`-scale near-factor with only two affine defect lines.

The next natural question is sharper:

- is there an exact nested-return section for `R_3^*`,
- on which the live color-`3` route becomes a finite-defect affine-itinerary
  map in the direct D3 Route-E style?

This note gives a positive checked answer.

## 2. Exact section

Inside

- `P0 = {Sigma = 0}`,

write

- `S_m = {x in P0 : x_2 = m - 2}`.

The probe checks odd moduli

- `m = 9,11,13,15,17,19,21`.

For every checked modulus, every point of `S_m` returns to `S_m` after
exactly `m` iterates of `R_3^*`.

So the exact section map

- `T_m = (R_3^*)^m | S_m`

is well defined on all checked odd moduli.

## 3. Checked Hamiltonicity on the section

For every checked modulus,

- `|S_m| = m^3`,
- `T_m` is a single `m^3`-cycle.

This is stronger than the old factor-level evidence.
The live color-`3` branch is no longer merely “near a small factor.”
It already has an exact nested-return section with one checked global orbit.

## 4. Section coordinates and exact checked law

On `S_m`, use section coordinates

- `(a,b,e) = (x_0, x_1, x_4)`,

and write

- `c = x_3 = 2 - a - b - e (mod m)`.

Then on every checked modulus the section map `T_m` has exactly five branches.

### Generic branch

Otherwise,

- `(a,b,e) -> (a, b+1, e)`.

### Branch A

If

- `a = m-1`,
- `c != m-1`,
- and `(b != m-1 or e = m-3)`,

then

- `(a,b,e) -> (a, b, e+1)`.

### Branch B

If

- `b = m-2`,
- `e != m-2`,
- and `(a != m-1 or e = 6)`,

then

- `(a,b,e) -> (a+1, b+1, e)`.

### Branch C

If

- `e = m-2`,
- `c = m-1`,

then

- `(a,b,e) -> (a+1, b, e)`.

### Branch D

If

- `a = m-1`,
- `b = m-1`,
- `e notin {5, m-3}`,

then

- `(a,b,e) -> (a+1, b, e+1)`.

The checker verifies that these five clauses match the exact section map
without failure on all checked odd moduli `9..21`.

## 5. Exact checked counts

The branch counts are polynomial and stable on the checked range:

- generic `G`: `m^3 - 2m^2 + 2m - 2`,
- branch `A`: `m^2 - 2m + 2`,
- branch `B`: `m^2 - 2m + 2`,
- branch `C`: `m`,
- branch `D`: `m - 2`.

Equivalently, the only section-step displacements that occur are:

- `(0,1,0)` on the generic branch,
- `(0,0,1)` on branch `A`,
- `(1,1,0)` on branch `B`,
- `(1,0,0)` on branch `C`,
- `(1,0,1)` on branch `D`.

So the section dynamics are not diffuse.
They are a finite-defect affine-itinerary system with four explicit defect
families on top of one dominant translation rule.

## 6. Consequence for the live proof route

This changes the graph-side target substantially.

After `256`, the explicit `G1 -> G2` transport route is no longer the right
active endgame for the current explicit package.

After `257` and now `258`, the plausible graph-side closure route is:

1. prove the section theorem for `S_m = {x_2 = m-2}`,
2. prove that the piecewise section law above is a single cycle for odd `m`,
3. lift that section-cycle theorem back to `R_3^*`,
4. and hence to Hamiltonicity of the `Sel*` color-`3` branch.

So the remaining theorem is no longer “prove cyclic transport.”
It is now much closer to:

- a direct Route-E-style finite-defect section-stitch theorem.

## 7. Current claim level

This note is still a checked theorem target, not yet a full symbolic proof.

What is now established is:

- an exact nested-return section exists in checked odd moduli,
- the section map has a stable five-branch piecewise law in checked odd moduli,
- and that section map is already one cycle in checked odd moduli.

That is enough to treat the live color-`3` route as a sharply defined theorem
problem rather than a loose search problem.
