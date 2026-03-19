# D5 120 Final-Section `U_m` in Corrected Row Coordinates

This note records the first stable corrected-row model for the final section

`U_m = (F_4^*)^(m^3)|P2`

from the tmp-120 package.

Primary artifacts:

- [../../tmp/d5_120_final_section_U_compute_request.md](../../tmp/d5_120_final_section_U_compute_request.md)
- [../../tmp/d5_120_M5_nested_return_color4_note.tex](../../tmp/d5_120_M5_nested_return_color4_note.tex)
- [../../scripts/torus_nd_d5_final_section_U_corrected_model_120.py](../../scripts/torus_nd_d5_final_section_U_corrected_model_120.py)
- [../checks/d5_120_final_section_U_corrected_model_summary.json](../checks/d5_120_final_section_U_corrected_model_summary.json)

## 1. Correction and scope

On

`P2 = {(a,b,-a,0,-b) : a,b in Z/mZ}`,

write corrected row coordinates

`v = b + c_m(a)`.

The stabilized correction extracted from the compute is:

- `c_m(0..4) = (0,3,6,9,10)`;
- `c_m(a) = 2a + 3 mod m` for `5 <= a <= m-2`;
- `c_m(m-1) = 0`.

Equivalently,

`c_m(a+1) - c_m(a) = (3,3,3,1,3,2,2,...,2,1,0)`.

The exact selector check was rerun on

`m = 11,13,15,17,19,21`,

with extra exact spot-checks on `m = 23,25`.

## 2. Exact transformed rule

In the corrected coordinates `(a,v)`, the exact `U_m` agrees on all checked
moduli with the following symbolic rule.

Row `0`:

- if `v in {m-8, m-1}`, then `(0,v) -> (0, v-2)`;
- otherwise `(0,v) -> (1, 2v+6)`.

Rows `1 <= a <= 6`:

- `(1,4) -> (7,2)`;
- if `v in {2a+2, 2a-10}`, then `(a,v) -> (a, v-2)`;
- otherwise `(a,v) -> (a+1, v)`.

Row `7`:

- `(7, 2*7+2) -> (7, 2*7)`;
- otherwise `(7,v) -> (8,v)`.

Row `8`:

- `(8,4) -> (0, m-2)`;
- `(8, 2*8+2) -> (8, 2*8)`;
- otherwise `(8,v) -> (9,v)`.

Rows `9 <= a <= m-2`:

- if `v in {2a+2, 2a-12}`, then `(a,v) -> (a, v-2)`;
- otherwise `(a,v) -> (a+1, v)`.

Row `m-1`:

- if `v in {0, m-14}`, then `(m-1,v) -> (m-1, v-2)`;
- `(m-1,4) -> (1,4)`;
- `(m-1,2) -> (0, m-1)`;
- if `v` is odd and not one of the special values above, then
  `(m-1,v) -> (0, (v+m-6)/2)`;
- if `v` is even and not one of the special values above, then
  `(m-1,v) -> (0, v/2-3)`.

The exact transformed map from the real selector agrees with this rule on all
exactly checked moduli `11..21`, and also on the extra exact spot-checks
`23,25`.

## 3. Exact defect set

Relative to the clean bulk step `(a,v) -> (a+1,v)`, the corrected defect set is

`D_m = {(a,v) : U_m(a,v) != (a+1,v)}`.

The exact symbolic candidate verified on the checked moduli is

`D_m = D_0 union D_{m-1} union L_A union L_B^- union L_B^+`,

where

- `D_0 = {(0,v) : v != m-6}`;
- `D_{m-1} = {(m-1,v) : v != m-6}`;
- `L_A = {(a, 2a+2) : 1 <= a <= m-2}`;
- `L_B^- = {(a, 2a-10) : 1 <= a <= 6}`;
- `L_B^+ = {(a, 2a-12) : 8 <= a <= m-2}`.

The exact defect count is therefore

`|D_m| = (m-1) + (m-1) + (m-2) + 6 + (m-9) = 4m-7`,

and the JSON check confirms `4m-7` on every exact modulus.

So the final section really is a sparse `O(m)` defect deformation of the clean
row shift on the `m^2`-state section.

## 4. Row stitching data

The corrected model has a particularly clean row-0 section.

For the actual selector on every exact modulus `11..21` and `23,25`:

- every state of `(Z/mZ)^2` hits row `a = 0`;
- the maximum checked hitting time to row `0` is `2m-4`;
- the first return to row `0` is exactly
  `v -> v-2`.

The checked row-0 return-time distribution is also stable:

- two row-0 states return in `1` step;
- one state returns in `10` steps;
- `m-4` states return in `m+2` steps;
- one state returns in `2m-4` steps.

Since `-2` is a unit for odd `m`, the row-0 return is a single `m`-cycle.
Combined with row-0 reachability, this is exactly the shape needed for the
final stitching theorem.

## 5. What is now closed and what remains

On the compute side, `120` is now much sharper than the earlier M5 frontier:

- the corrected row coordinates are explicit;
- the transformed defect set is explicit and exact on the checked moduli;
- the defect pattern is sparse and stable;
- the induced row-0 return already collapses to the primitive translation
  `v -> v-2`.

There is also a useful extra check: the standalone corrected-row model itself
is a single `m^2`-cycle for every odd `m` from `11` through `101`.

What is still not fully written as a manuscript proof is the all-odd deduction
from the symbolic defect rule to the row-0 reachability and first-return law.
So the current status is stronger than a raw compute dump but slightly short of
a complete theorem note:

- the corrected-row model is now explicit and exact on the real selector for
  `11..21` with extra exact checks on `23,25`;
- the model alone already behaves as the desired stitching mechanism on odd
  `m <= 101`;
- the remaining task is to turn that model-level behavior into a clean symbolic
  proof that `U_m` is one cycle for every odd `m >= 11`.
