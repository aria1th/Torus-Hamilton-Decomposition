# D5 262 SelStar Color-3 `B0` Return Formula

This note records the first short symbolic proof on the live `Sel*`
color-`3` section-model route.

Primary artifacts:

- [d5_260_selstar_color3_row_model_all_m.md](./d5_260_selstar_color3_row_model_all_m.md)
- [d5_261_selstar_color3_section_model_all_m.md](./d5_261_selstar_color3_section_model_all_m.md)

## 1. Setup

Fix `m >= 9`.

Let `T_m^sharp` be the explicit section model from `261` on coordinates
`(a,b,e)`, with

- `c = 2 - a - b - e (mod m)`,

and branches `A,B,C,D,G` exactly as listed in `261`.

Let

- `B0 = {(a,b,e) : b = 0}`.

Write

- `R_m^sharp : B0 -> B0`

for the first return of `T_m^sharp` to `B0`.

We identify `B0` with `(Z/mZ)^2` by `(a,0,e) <-> (a,e)`.

## 2. Theorem

For every `m >= 9`, the first return `R_m^sharp` is exactly the row model
`W_m` from `260`:

- if `a <= m-3`, then `R_m^sharp(a,e) = (a+1,e)`;
- if `a = m-2` and `e = 5`, then `R_m^sharp(a,e) = (m-1,5)`;
- if `a = m-2` and `e = m-3`, then `R_m^sharp(a,e) = (0,m-1)`;
- if `a = m-2` and `e = m-2`, then `R_m^sharp(a,e) = (0,6)`;
- if `a = m-2` and `e` is different from `5,m-3,m-2`, then
  `R_m^sharp(a,e) = (0,e+1)`;
- if `a = m-1` and `e = 4`, then `R_m^sharp(a,e) = (0,m-2)`;
- if `a = m-1` and `e != 4`, then `R_m^sharp(a,e) = (m-1,e+1)`.

## 3. Proof

Let the initial state be `(a,0,e)`.

### Case 1. `a <= m-3` and `e != m-2`

Branches `A` and `D` are impossible because `a != m-1`, and branch `C` is
impossible because `e != m-2`.

So the orbit follows `G` until it reaches `(a,m-2,e)`. There branch `B`
applies, giving `(a+1,m-1,e)`. Since `a+1 <= m-2` and still `e != m-2`,
the next step is `G`, which returns to `(a+1,0,e)`.

Hence `R_m^sharp(a,e) = (a+1,e)`.

### Case 2. `a <= m-3` and `e = m-2`

Now branch `C` occurs exactly when

- `c = m-1`,

which is equivalent to

- `a + b = 5 (mod m)`.

So there is exactly one `C` step before the first return to `B0`, namely at

- `b0 = 5 - a (mod m)`.

At that step the state moves from `(a,b0,m-2)` to `(a+1,b0,m-2)`.
Afterwards the `C` condition cannot recur before `b` wraps, because the left
side has been shifted from `a + b = 5` to `a + b = 6`.

Also `A` and `D` remain impossible because `a+1 <= m-2`.
So after that one `C` step, the orbit proceeds by `G` until it returns to
`(a+1,0,m-2)`.

Hence `R_m^sharp(a,m-2) = (a+1,m-2)`.

### Case 3. `a = m-2`

#### Subcase 3a. `e = 5`

No `C` occurs because `e != m-2`. The orbit follows `G` to `(m-2,m-2,5)`,
then `B` to `(m-1,m-1,5)`, and then one `G` to `(m-1,0,5)`.

Hence `R_m^sharp(m-2,5) = (m-1,5)`.

#### Subcase 3b. `e notin {5,m-3,m-2}`

Again the orbit follows `G` to `(m-2,m-2,e)`, then `B` to `(m-1,m-1,e)`.
At that point `D` applies, producing `(0,m-1,e+1)`, and one `G` returns to
`(0,0,e+1)`.

Hence `R_m^sharp(m-2,e) = (0,e+1)`.

#### Subcase 3c. `e = m-3`

As above, `G` leads to `(m-2,m-2,m-3)` and `B` to `(m-1,m-1,m-3)`.
There branch `A` applies once, producing `(m-1,m-1,m-2)`.
Then `D` applies, producing `(0,m-1,m-1)`, and one `G` returns to
`(0,0,m-1)`.

Hence `R_m^sharp(m-2,m-3) = (0,m-1)`.

#### Subcase 3d. `e = m-2`

Now branch `C` occurs when `a + b = 5 (mod m)`.
Since `a = m-2`, this is exactly

- `b = 7`.

So the orbit first follows `G` to `(m-2,7,m-2)` and then `C` to
`(m-1,7,m-2)`.

For a fixed `b` with `7 <= b <= m-2`, branch `A` keeps `b` fixed and increases
`e` until the unique value

- `e = 4 - b (mod m)`,

at which point `A` fails and the orbit advances one `G` step to the next `b`.

This staircase continues until `b = m-2`, where the stopping value is `e = 6`.
At `(m-1,m-2,6)`, branch `B` applies by the exceptional top-row allowance
`e = 6`, sending the orbit to `(0,m-1,6)`. One final `G` returns to
`(0,0,6)`.

Hence `R_m^sharp(m-2,m-2) = (0,6)`.

### Case 4. `a = m-1`

#### Subcase 4a. `e != 4`

At `(m-1,0,e)` we have

- `c = 3 - e (mod m) != m-1`,

so branch `A` applies immediately and sends the orbit to `(m-1,0,e+1)`.
This is already back in `B0`.

Hence `R_m^sharp(m-1,e) = (m-1,e+1)`.

#### Subcase 4b. `e = 4`

At `(m-1,0,4)` we have `c = m-1`, so the first step is `G` to `(m-1,1,4)`.

For each fixed `b = 1,2,...,6`, branch `A` again keeps `b` fixed and increases
`e` until the unique stopping value `e = 4 - b (mod m)`, after which one `G`
advances to the next `b`.

At `b = 6` this stopping value is `e = m-2`, so the orbit reaches
`(m-1,6,m-2)`. There branch `C` applies, sending the orbit to `(0,6,m-2)`.
From there successive `G` steps return to `(0,0,m-2)`.

Hence `R_m^sharp(m-1,4) = (0,m-2)`.

All cases are complete.

## 4. Consequence

This closes the first short symbolic gap on the model side:

- the explicit `B0` first-return really is the row model `W_m` for all
  `m >= 9`.

Together with `260`, this gives a genuine all-`m` theorem for the reduced
two-dimensional row model. The remaining model-internal work is then the
global stitching from `B0` back to the full three-dimensional section model.
