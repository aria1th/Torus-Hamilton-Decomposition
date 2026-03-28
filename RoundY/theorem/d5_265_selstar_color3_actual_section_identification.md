# D5 265 SelStar Color-3 Actual Section Identification

This note closes the actual/model identification step for the live `Sel*`
color-`3` Route-E line.

Primary inputs:

- [d5_264_selstar_color3_actual_P0_return_formula.md](./d5_264_selstar_color3_actual_P0_return_formula.md)
- [d5_261_selstar_color3_section_model_all_m.md](./d5_261_selstar_color3_section_model_all_m.md)
- [d5_258_selstar_color3_section_stitch.md](./d5_258_selstar_color3_section_stitch.md)

## 1. Setup

Fix `m >= 9`.

Let

- `R_3^* = (F_3^*)^m | P0`

be the actual `P0` first return from `264`, and let

- `S_m = {x in P0 : x_2 = m-2}`.

By `264`, `x_2` increases by `1` under `R_3^*`, so `S_m` is an exact `m`-step
section. Write

- `T_m = (R_3^*)^m | S_m`.

On `S_m`, use section coordinates

- `(a,b,e) = (x_0,x_1,x_4)`,

and write

- `c = x_3 = 2 - a - b - e (mod m)`.

## 2. Theorem

For every `m >= 9`, the actual section map `T_m` is exactly the explicit
five-branch model `T_m^sharp` from `261`:

- `A`: if `a = m-1`, `c != m-1`, and `(b != m-1 or e = m-3)`,
  then `(a,b,e) -> (a,b,e+1)`;
- `B`: if `b = m-2`, `e != m-2`, and `(a != m-1 or e = 6)`,
  then `(a,b,e) -> (a+1,b+1,e)`;
- `C`: if `e = m-2` and `c = m-1`,
  then `(a,b,e) -> (a+1,b,e)`;
- `D`: if `a = m-1`, `b = m-1`, and `e notin {5,m-3}`,
  then `(a,b,e) -> (a+1,b,e+1)`;
- otherwise `G`: `(a,b+1,e)`.

## 3. Proof

Take `x = (a,b,m-2,c,e) in S_m`.

By `264`, the first `R_3^*` step falls into exactly one of three initial
classes.

### Initial class `C`

If

- `e = m-2` and `c = m-1`,

then the initial `Sigma=2` choice is direction `0`, so after one `R_3^*` step
the state is

- `(a+1,b,m-1,c-3,m-1)`.

Now `x_1 = b` is fixed on the remaining `m-1` steps, while `x_4` starts at
`m-1` and increases by `1` each time. So among the remaining pre-step states,
`x_4 = m-2` never occurs. Hence no later special step can occur.

Therefore the remaining `m-1` steps are all generic later steps, so when the
orbit returns to `S_m` it lands at

- `(a+1,b,e)`.

This is exactly branch `C`.

### Initial class `A`

If

- `a = m-1` and `c != m-1`,

then the initial `Sigma=2` choice is direction `4`, so after one `R_3^*` step
the state is

- `(a,b,m-1,c-3,e+2)`.

For every later `R_3^*` step, `264` says the only possible nongeneric behavior
is the later special step

- `x_1 = m-1` and `x_4 = m-2`.

Here `x_1 = b` is constant on the remaining `m-1` steps, and `x_4` starts at
`e+2` and increases by `1` each time. So there is a later special step iff:

- `b = m-1`, and
- `e+2 != m-1`, equivalently `e != m-3`.

When `b = m-1`, the initial-class condition `c != m-1` becomes

- `4 - e != m-1`,

that is `e != 5`.

So the later special step occurs exactly when

- `a = m-1`, `b = m-1`, and `e notin {5,m-3}`.

If it does not occur, the net effect over the remaining `m-1` generic later
steps is to keep `a,b` fixed and subtract `1` from the post-initial `x_4`,
so the final section image is

- `(a,b,e+1)`,

which is branch `A`.

If the later special step does occur, it contributes one extra `+1` to `x_0`
and nothing to `x_1,x_4` beyond the same net `x_4` decrement by `1`, so the
final section image is

- `(a+1,b,e+1)`,

which is branch `D`.

### Initial class `G`

In every remaining case, the initial `Sigma=2` choice is direction `1`, so
after one `R_3^*` step the state is

- `(a,b+1,m-1,c-3,e+1)`.

Again the only possible later nongeneric event is

- `x_1 = m-1` and `x_4 = m-2`.

Now `x_1 = b+1` is constant on the remaining `m-1` steps, and `x_4` starts at
`e+1`. So there is a later special step iff:

- `b+1 = m-1`, i.e. `b = m-2`, and
- `e+1 != m-1`, i.e. `e != m-2`.

If `b = m-2`, then the failure of initial class `A` is exactly

- not(`a = m-1` and `c != m-1`).

But with `b = m-2`, the relation `c = 2 - a - b - e` becomes

- `c = 5 - a - e`,

so when `a = m-1`, the condition `c = m-1` is equivalent to `e = 6`.

Therefore inside initial class `G`, the later special step occurs exactly when

- `b = m-2`, `e != m-2`, and `(a != m-1 or e = 6)`.

If it does not occur, the final section image is

- `(a,b+1,e)`,

which is branch `G`.

If it does occur, the single later special step contributes one extra `+1` to
`x_0`, so the final section image is

- `(a+1,b+1,e)`,

which is branch `B`.

These three initial classes exhaust `S_m`, so `T_m` is exactly the
five-branch model `T_m^sharp`.

## 4. Consequence

The explicit model extracted in `258` is now the true section return of the
actual `Sel*` color-`3` torus dynamics.

So the live graph-side issue isolated in `256` is no longer “prove actual/model
identification.” That identification is now closed for `m >= 9`.
