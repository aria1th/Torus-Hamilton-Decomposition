# D5 257 SelStar Color-3 Route-E Probe

This note records the first focused exploration after the `256` no-go result for
the explicit `G1` two-swap package.

Primary files:

- [d5_256_G1_transport_incompatibility_no_go_note.tex](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/tmp/d5_256_G1_transport_incompatibility_no_go_note.tex)
- [torus_nd_d5_selstar_color3_routee_probe_257.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_selstar_color3_routee_probe_257.py)
- [d5_257_selstar_color3_routee_probe_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_257_selstar_color3_routee_probe_summary.json)
- [per_modulus.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_257_selstar_color3_routee_probe/per_modulus.json)

## 1. Why this probe

`256` shows that the explicit two-swap package from `247` is not merely missing
a proof of cyclic transport:

- it is not one color-relative family;
- and its non-color-`4` maps are structurally non-Hamilton.

So a D3 Route-E-style fallback becomes the natural question:

- instead of transporting one closed Hamilton branch by cyclic conjugacy,
- can one isolate a low-complexity near-factor for the live `Sel*` color-`3`
  branch,
- and then prove a finite-defect affine-itinerary / splice theorem on top of
  it?

This note probes exactly that.

## 2. Candidate factor

Work on the first return

- `R_3^* = (F_3^*)^m | P0`

for the explicit selector surgery `Sel*` from the `119` chain, with

- `P0 = {Sigma = 0}`.

Take the best `m^3`-scale near-factor already visible in `119`:

- `Phi_3(x) = (p0(x), p1(x), p2(x), M0(x))`

where

- `p_i(x) = x_{i-1} + x_{i+2} (mod m)`,
- `M0(x) = 1[x_0 = m-1]`.

The probe checks this factor on odd moduli

- `m = 9,11,13,15,17`.

## 3. Main result

The nondeterminism of `Phi_3` is not diffuse.
It collapses exactly to two affine defect lines in the `b = 0` slice.

Write a factor state as `(u,v,w,b)`.
Then the bad states are exactly

- `L_A(m) = { (m-4, t, 2-t, 0) : t in Z_m, t != m-2 }`,
- `L_B(m) = { (s, 1-s, m-3, 0) : s in Z_m, s != m-4 }`.

So the total number of bad factor states is exactly

- `|L_A| + |L_B| = 2m - 2`.

The script verifies this equality exactly on all checked moduli.

## 4. Route-E-style defect fibers

Each bad factor state has raw fiber size `m-1`.
More importantly, each such fiber has a single explicit exceptional raw point.

For `L_A(m)`:

- the raw fiber is
  `A_t(a) = (a, 4-t, m-2, t-a, m-2)` with `a != m-1`;
- the unique exceptional raw point is
  `A_t^exc = A_t(t+1) = (t+1, 4-t, m-2, m-1, m-2)`.

For `L_B(m)`:

- the raw fiber is
  `B_s(a) = (a, m-1, s+2, 1-s-a, m-2)` with `a != m-1`;
- the unique exceptional raw point is
  `B_s^exc = B_s(m-2) = (m-2, m-1, s+2, 3-s, m-2)`.

So each bad factor state is not an uncontrolled branching locus.
It is an `m-1`-point affine family with one explicit exceptional point and a
default branch on the remaining `m-2` points.

## 5. Explicit branch formulas

The probe also identifies the exact successor sets.

For `L_A(m)`:

- default branch:
  `(m-2, t-3, 4-t, 0)`,
- exceptional branch:
  `(m-2, t-2, 3-t, eps_A(t))`,

where

- `eps_A(t) = 1` if `t = m-3`,
- `eps_A(t) = 0` otherwise.

For `L_B(m)`:

- default branch:
  `(s+2, -s-1, m-2, 0)`,
- exceptional branch:
  `(s+2, -s-1, m-2, 1)`.

These formulas are checked exactly on all probed moduli.

## 6. Generic affine law

Away from the defect lines, the exact transition has a dominant affine increment

- `(u,v,w,b) -> (u+2, v-2, w+1, b)`.

On the checked moduli this is the overwhelmingly dominant exact update on the
`Phi_3` factor, with counts:

- `1280` at `m=9`,
- `2400` at `m=11`,
- `4032` at `m=13`,
- `6272` at `m=15`,
- `9216` at `m=17`.

So the checked picture is not “no small structure.”
It is:

- one dominant affine law,
- plus two affine defect lines,
- plus one explicit exceptional raw point per bad factor state.

## 7. Consequence

This is strong evidence that the live color-`3` graph-side route should be read
in the same style as D3 Route E:

- not as a cyclic transport theorem from another color,
- but as a finite-defect affine-itinerary / splice theorem for `R_3^*`.

That is, after `256`, the plausible next graph-side theorem is no longer

- `G1 -> G2` transport compatibility for the old explicit package,

but rather something closer to:

- a first-return factor theorem for `Phi_3`,
- a defect-line itinerary theorem on `L_A union L_B`,
- and a resulting Hamiltonicity theorem for the `Sel*` color-`3` branch.

## 8. Bottom line

`256` ruled out the old transport route.
`257` shows that the replacement route is not blind search:

- the `Sel*` color-`3` branch already exhibits a clean finite-defect skeleton,
- and that skeleton is exactly the kind of object for which a D3 Route-E-style
  proof package would make sense.
