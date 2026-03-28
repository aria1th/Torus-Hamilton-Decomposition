# D5 263 SelStar Color-3 Section-Model Stitching

This note closes the explicit section model from `261` for all `m >= 9`.

Primary artifacts:

- [d5_260_selstar_color3_row_model_all_m.md](./d5_260_selstar_color3_row_model_all_m.md)
- [d5_261_selstar_color3_section_model_all_m.md](./d5_261_selstar_color3_section_model_all_m.md)
- [d5_262_selstar_color3_B0_return_formula.md](./d5_262_selstar_color3_B0_return_formula.md)

## 1. Setup

Fix `m >= 9`.

Let `T_m^sharp` be the explicit five-branch section model from `261` on
coordinates `(a,b,e)`.

Let

- `B0 = {(a,b,e) : b = 0}`.

By `262`, the first return of `T_m^sharp` to `B0` is the explicit row model
`W_m`, and by `260` that row model is one `m^2`-cycle.

So the only remaining task is to pass from the `B0` return cycle to the full
three-dimensional section model.

## 2. Explicit inverse

Define `S_m : (Z/mZ)^3 -> (Z/mZ)^3` by the following five cases:

- if `a = 0`, `b = m-1`, and `e notin {6,m-2}`, then
  `S_m(a,b,e) = (m-1,b,e-1)`;
- else if `b = m-1`, `e != m-2`, and `(a != 0 or e = 6)`, then
  `S_m(a,b,e) = (a-1,b-1,e)`;
- else if `e = m-2` and `a + b = 6 (mod m)`, then
  `S_m(a,b,e) = (a-1,b,e)`;
- else if `a = m-1`, `((b != m-1) or e = m-2)`, and `e != 5-b (mod m)`, then
  `S_m(a,b,e) = (a,b,e-1)`;
- otherwise
  `S_m(a,b,e) = (a,b-1,e)`.

All coordinates are mod `m`.

### Proposition

`S_m` is the inverse of `T_m^sharp`.

### Proof

The five clauses above are exactly the image-side descriptions of the `D`, `B`,
`C`, `A`, `G` branches, in that order.

Indeed:

- the first clause is exactly the image of `D`;
- the second clause is exactly the image of `B`;
- the third clause is exactly the image of `C`;
- the fourth clause is exactly the image of `A`;
- and the remaining states are exactly the image of `G`.

So on each case, substituting the proposed predecessor into the corresponding
forward branch formula recovers the target point. Hence

- `T_m^sharp(S_m(y)) = y`

for every `y`. The same case split applied to `x` shows

- `S_m(T_m^sharp(x)) = x`

for every `x`. Therefore `S_m = (T_m^sharp)^{-1}`.

In particular, `T_m^sharp` is a permutation of `(Z/mZ)^3`.

## 3. Every orbit hits `B0`

### Proposition

Every point of `(Z/mZ)^3` reaches `B0` after finitely many forward iterates of
`T_m^sharp`.

### Proof

Write the state as `(a,b,e)`.

The only branches that do not increase `b` are `A`, `C`, and `D`.

If `a <= m-2`, then:

- either the next step is `G` or `B`, which increases `b`;
- or the next step is `C`, which keeps `b` fixed but changes `a` to `a+1`.

After a `C` step, the relation `a+b = 5 (mod m)` becomes `a+b = 6 (mod m)`,
so another `C` step cannot occur immediately. Hence from `a <= m-2`, the value
of `b` increases after at most two steps.

If `a = m-1` and `1 <= b <= m-2`, branch `A` may repeat for a while, but each
`A` step increases `e` by `1`. So after finitely many `A` steps, one reaches
the unique stopping value at which `A` fails. At that point:

- either `G` applies and increases `b`,
- or `B` applies when `b = m-2` and `e = 6`,
- or one exceptional `C` step occurs at `b = 6`, after which `a = 0` and the
  next step is `G`.

So from `a = m-1` and `1 <= b <= m-2`, the value of `b` again increases after
finitely many steps.

If `b = m-1`, then:

- either `G` applies immediately and sends `b` to `0`,
- or `D` applies and is followed by one `G`,
- or one `A` step occurs at `e = m-3`, after which `D` and then `G` send the
  orbit to `b = 0`.

Thus every forward orbit reaches `B0`.

## 4. Full stitching theorem

### Theorem

For every `m >= 9`, the explicit section model `T_m^sharp` is one `m^3`-cycle.

### Proof

By `262`, the first return of `T_m^sharp` on `B0` is the row model `W_m`.
By `260`, `W_m` is one `m^2`-cycle.

By the inverse proposition above, `T_m^sharp` is a permutation. Hence its
state space splits into disjoint cycles.

By the reachability proposition, every cycle meets `B0`.
On each full cycle, the first return to `B0` is a cycle on that cycle's
intersection with `B0`.

But the global first return on all of `B0` is already one cycle, namely `W_m`.
Therefore all points of `B0` lie on one and the same full `T_m^sharp` cycle.
Since every full cycle meets `B0`, there can be no other cycle.

Hence `T_m^sharp` is one `m^3`-cycle.

## 5. Consequence

The pure model side is now closed for all `m >= 9`:

- `B0` first-return formula,
- `B0` row-model Hamiltonicity,
- and the full three-dimensional section-model Hamiltonicity.

So the remaining live color-`3` gap is no longer model-internal stitching.
It is only the actual D5 identification step:

- prove that the true `Sel*` color-`3` section return equals this explicit
  section model.

For the small moduli `m = 3,4,5,6,7,8`, the same conclusion already appears in
the checked `261` data.
