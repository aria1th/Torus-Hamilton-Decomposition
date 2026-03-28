# D5 281 Route-E Line-Bit Search

This note records the first follow-up search after
[d5_280_one_point_repair_color1_line_obstruction.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_280_one_point_repair_color1_line_obstruction.md).

Primary files:

- [torus_nd_d5_routee_line_bit_search_281.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_routee_line_bit_search_281.py)
- [d5_281_routee_line_bit_search_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_281_routee_line_bit_search_summary.json)
- [search.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_281_routee_line_bit_search/search.json)

## 1. Question

`280` isolates the residual color-`1` obstruction in the `279` repaired family:
for checked odd `m` with `3 \nmid m`, the `P0` first return preserves the
explicit affine line family

- `x_0 + 3x_1 + x_3 + 3x_4 = 7`.

The natural next question is therefore:

> if the finite exactness CSP is allowed to see this line relation as a local
> bit, does that already repair the remaining five-color assembly problem?

## 2. Search family

`281` refines the `277/279` class family by adjoining two extra bits:

- the `279` one-point source bit
  `U = 1_{x = (m-1,6,m-1,m-1,m-1)}`,
- the `280` line bit
  `L = 1_{x_3 != m-1, x_4 != m-1, x_0 + 3x_1 + x_3 + 3x_4 = 7 mod m}`.

The search then asks for exactness on

- `m = 7,9,11`

and evaluates cycle structure on

- `m = 7,9,11,13`.

## 3. Result

The answer is: not yet.

The family is not empty; exact solutions exist on the checked exactness moduli.

But the best time-limited search found so far only reaches Hamilton-color
counts

- `m=7 -> 3`,
- `m=9 -> 2`,
- `m=11 -> 2`,
- `m=13 -> 2`.

So the line bit is real and useful, but by itself it does **not** finish the
remaining five-color assembly theorem.

## 4. Meaning

`280` was still the right obstruction to isolate.

`281` shows that the next missing local distinction is now even sharper:

- not “we forgot the color-`1` line family,”
- but “the line family alone is not enough information to choose the final
  local repair.”

The most plausible next target is therefore a transported or phase-marked
version of that line relation, rather than the raw `P0` line bit alone.

## 5. Bottom line

After `279–281`, the five-color assembly frontier can be read as:

- color `2` is closed on the checked range in the repaired family,
- color `1` has an explicit affine line obstruction in that same family,
- and even when that line obstruction is exposed directly to the exactness CSP,
  the resulting family is still not enough.

So the next refinement should not be broad. It should be the smallest local
bit that distinguishes how the `280` line family is transported through the
residual branch.
