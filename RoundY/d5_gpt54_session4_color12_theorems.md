# d=5 progress note v7

Problem:
Prove the `d=5` case: for every `m >= 3`, the directed torus
`D_5(m) = Cay((Z_m)^5, {e_0,e_1,e_2,e_3,e_4})`
admits a Hamilton decomposition into five arc-disjoint directed Hamilton cycles.

Current target:
Classify the fixed 26-move witness color-by-color by exact return-map formulas, and separate
- genuinely uniform Hamilton branches,
- from explicit obstruction branches.

New theorem A (positive):
- [P] For every `m >= 5`, the fixed 26-move witness makes **color 2** Hamilton iff `gcd(m,3)=1`.

Setup for color 2:
Use relative coordinates on `P0 = {S=0}`
`(q,w,v,u) = (x_3, x_4, x_0, x_1)`,
so `x_2 = -(q+w+v+u)`.

Exact color-2 prefix:
For every `m >= 5`,
- [P] `d0 = 1` if `w=v=0` and `q+u ≡ m-3`; `d0 = 3` if `w=v=0` and `q+u ≠ m-3`; otherwise `d0 = 2`.
- [P] `d1 = 0` if `w=1`; `d1 = 1` if `w=3` or `(w=4 and v=2)`; otherwise `d1 = 2`.
- [P] `d2 = 1` if `w=1`, or `(w=3 and v=4)`, or `(w=4 and v=0)`; `d2 = 3` if `w != 1` and `v=2`; otherwise `d2 = 2`.
- [P] `d3 = 4` always.

Therefore
`R_2(q,w,v,u) = (q + α, w+1, v + 1_{w=1}, u + γ)`
with
`α = 1_{w=v=0, q+u ≠ m-3} + 1_{w != 1, v=2}`
and
`γ = 1_{w=v=0, q+u = m-3} + 1_{w=3 or (w=4 and v=2)} + 1_{w=1 or (w=3 and v=4) or (w=4 and v=0)}`.

Nested reductions for color 2:
- [P] `w -> w+1` is an absolute clock, so reduce to `T = R_2^m | {w=0}`.
- [P] `v -> v+1` is another absolute clock on `T`, so reduce further to `U = T^m | {v=0}`.

Exact 2D section:
Let `s = q+u`.
Then
- [P] `U(q,u) = (q-1, u+4)` when `s ≡ m-3`,
- [P] `U(q,u) = (q, u+3)` otherwise.

Equivalently:
- [P] `s -> s+3`,
- [P] `q -> q-1` exactly when `s = m-3`.

Consequences:
- [P] If `gcd(m,3)=1`, then after rescaling `t = 3^(-1)s` and replacing `q` by `-q`,
  `U` is the standard 2D odometer, hence one cycle.
- [P] If `3 | m`, then `s mod 3` is invariant, so `U` is not one cycle.
- [P] Therefore color 2 is Hamilton exactly for `3 ∤ m`.

New theorem B (negative):
- [P] For every `m >= 6`, the fixed witness gives **color 1** an explicit fixed-point set on `P0`,
  so color 1 can never be Hamilton for those `m`.

Setup for color 1:
Use relative coordinates
`(q,w,v,u) = (x_2, x_3, x_4, x_0)`,
so `x_1 = -(q+w+v+u)`.

Key observation:
- [P] For color 1, if the first-return map `R_1` fixes a point of `P0`, then the low-layer prefix must be exactly `(1,1,1,1)`.
  Reason: only directions `0,2,3,4` can move the relative coordinates `(q,w,v,u)`, and any such move contributes a nonnegative increment that cannot be cancelled during the same first return.

Exact fixed set:
Define
`F_m = { (q,w,v,u) :
          v not in {0,1,2,3,4},
          u != 4,
          q not in {2,3},
          and not (q=1 and w in {0,2}) }`.

Then:
- [P] For every `m >= 5`,
  `R_1(q,w,v,u) = (q,w,v,u)` iff `(q,w,v,u) in F_m`.

Proof sketch:
- [P] If `(q,w,v,u) in F_m`, then none of the low-layer supports touching color 1 fire, so the prefix is `(1,1,1,1)` and `R_1` is fixed.
- [P] Conversely, if `R_1` is fixed, then all four low-layer directions must be `1`.
  Inspecting the layer-0/1/2/3 supports touching color 1 forces exactly the exclusions
  `v not in {0,1,2,3,4}`, `u != 4`, `q not in {2,3}`, and `not(q=1 and w in {0,2})`.

Counting:
- [P] The number of allowed `(q,w)` pairs is
  `(m-3)m + (m-2) = m^2 - 2m - 2`
  because all allowed `q != 1` admit all `m` values of `w`, while `q=1` forbids `w=0,2`.
- [P] The number of allowed `v` values is `m-5`.
- [P] The number of allowed `u` values is `m-1`.

Hence
- [P] `|Fix(R_1)| = (m^2 - 2m - 2)(m-5)(m-1)`.

So:
- [P] For every `m >= 6`, `Fix(R_1)` is nonempty, hence color 1 is not Hamilton.
- [P] At `m=5`, this count is `0`, which is consistent with the original witness being Hamilton only there.

Computational checks:
- [C] Color-2 formulas and classification were verified for every `m = 5,6,...,16`.
- [C] Color-1 exact fixed-set formula was verified for every `m = 5,6,...,12`.

Color-2 validation summary:
{
  "validated_m": [
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16
  ],
  "results": [
    {
      "m": 5,
      "gcd_m_3": 1,
      "R_cycles": 1,
      "R_max": 625,
      "T_cycles": 1,
      "T_max": 125,
      "U_cycles": 1,
      "U_max": 25,
      "hamilton_color2": true,
      "u_special_count": 5
    },
    {
      "m": 6,
      "gcd_m_3": 3,
      "R_cycles": 13,
      "R_max": 432,
      "T_cycles": 13,
      "T_max": 72,
      "U_cycles": 13,
      "U_max": 12,
      "hamilton_color2": false,
      "u_special_count": 6
    },
    {
      "m": 7,
      "gcd_m_3": 1,
      "R_cycles": 1,
      "R_max": 2401,
      "T_cycles": 1,
      "T_max": 343,
      "U_cycles": 1,
      "U_max": 49,
      "hamilton_color2": true,
      "u_special_count": 7
    },
    {
      "m": 8,
      "gcd_m_3": 1,
      "R_cycles": 1,
      "R_max": 4096,
      "T_cycles": 1,
      "T_max": 512,
      "U_cycles": 1,
      "U_max": 64,
      "hamilton_color2": true,
      "u_special_count": 8
    },
    {
      "m": 9,
      "gcd_m_3": 3,
      "R_cycles": 19,
      "R_max": 2187,
      "T_cycles": 19,
      "T_max": 243,
      "U_cycles": 19,
      "U_max": 27,
      "hamilton_color2": false,
      "u_special_count": 9
    },
    {
      "m": 10,
      "gcd_m_3": 1,
      "R_cycles": 1,
      "R_max": 10000,
      "T_cycles": 1,
      "T_max": 1000,
      "U_cycles": 1,
      "U_max": 100,
      "hamilton_color2": true,
      "u_special_count": 10
    },
    {
      "m": 11,
      "gcd_m_3": 1,
      "R_cycles": 1,
      "R_max": 14641,
      "T_cycles": 1,
      "T_max": 1331,
      "U_cycles": 1,
      "U_max": 121,
      "hamilton_color2": true,
      "u_special_count": 11
    },
    {
      "m": 12,
      "gcd_m_3": 3,
      "R_cycles": 25,
      "R_max": 6912,
      "T_cycles": 25,
      "T_max": 576,
      "U_cycles": 25,
      "U_max": 48,
      "hamilton_color2": false,
      "u_special_count": 12
    },
    {
      "m": 13,
      "gcd_m_3": 1,
      "R_cycles": 1,
      "R_max": 28561,
      "T_cycles": 1,
      "T_max": 2197,
      "U_cycles": 1,
      "U_max": 169,
      "hamilton_color2": true,
      "u_special_count": 13
    },
    {
      "m": 14,
      "gcd_m_3": 1,
      "R_cycles": 1,
      "R_max": 38416,
      "T_cycles": 1,
      "T_max": 2744,
      "U_cycles": 1,
      "U_max": 196,
      "hamilton_color2": true,
      "u_special_count": 14
    },
    {
      "m": 15,
      "gcd_m_3": 3,
      "R_cycles": 31,
      "R_max": 16875,
      "T_cycles": 31,
      "T_max": 1125,
      "U_cycles": 31,
      "U_max": 75,
      "hamilton_color2": false,
      "u_special_count": 15
    },
    {
      "m": 16,
      "gcd_m_3": 1,
      "R_cycles": 1,
      "R_max": 65536,
      "T_cycles": 1,
      "T_max": 4096,
      "U_cycles": 1,
      "U_max": 256,
      "hamilton_color2": true,
      "u_special_count": 16
    }
  ]
}

Color-1 validation summary:
{
  "validated_m": [
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12
  ],
  "results": [
    {
      "m": 5,
      "fixed_points_on_P0": 0,
      "formula_count": 0,
      "matches_formula": true,
      "has_hamilton_obstruction": false
    },
    {
      "m": 6,
      "fixed_points_on_P0": 110,
      "formula_count": 110,
      "matches_formula": true,
      "has_hamilton_obstruction": true
    },
    {
      "m": 7,
      "fixed_points_on_P0": 396,
      "formula_count": 396,
      "matches_formula": true,
      "has_hamilton_obstruction": true
    },
    {
      "m": 8,
      "fixed_points_on_P0": 966,
      "formula_count": 966,
      "matches_formula": true,
      "has_hamilton_obstruction": true
    },
    {
      "m": 9,
      "fixed_points_on_P0": 1952,
      "formula_count": 1952,
      "matches_formula": true,
      "has_hamilton_obstruction": true
    },
    {
      "m": 10,
      "fixed_points_on_P0": 3510,
      "formula_count": 3510,
      "matches_formula": true,
      "has_hamilton_obstruction": true
    },
    {
      "m": 11,
      "fixed_points_on_P0": 5820,
      "formula_count": 5820,
      "matches_formula": true,
      "has_hamilton_obstruction": true
    },
    {
      "m": 12,
      "fixed_points_on_P0": 9086,
      "formula_count": 9086,
      "matches_formula": true,
      "has_hamilton_obstruction": true
    }
  ]
}

Current interpretation:
- [P] The fixed witness is no longer a black box.
  It now splits into:
  - a **uniform positive branch** (color 2) governed by a clean `+3` odometer,
  - a **uniform negative branch** (color 1) with an explicit macroscopic fixed set,
  - and the earlier **odd-m positive branch** (color 3) governed by a clean `+2` odometer.
- [H] This is strong evidence that the right global strategy is to preserve the good arithmetic clocks (colors 2 and 3) while surgically repairing the bad branches (especially colors 1 and then 0/4).

Next branching options:
1. Derive an equally explicit obstruction theorem for color 4 or color 0.
2. Search for a small affine-pinned perturbation that destroys the color-1 fixed set while keeping the proven color-2 and color-3 odometer branches intact.
3. Repackage colors 2 and 3 into a common “unit-step section map” template, to guide a redesigned witness rather than a purely local patch.
