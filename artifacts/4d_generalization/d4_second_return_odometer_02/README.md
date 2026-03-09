# D4 Second Return Odometer 02

## Goal

This bundle addresses Task ID `D4-SECOND-RETURN-ODOMETER-02` from
`RoundX/codex_job_request_2.md`.

The fixed candidate is:

- `candidates/hyperplane_fusion_low_layers_v1.py`

The proof-oriented target is:

1. write the repaired first-return maps `R_c` on `P_0`,
2. write the second-return maps `T_c = R_c^m|_{Q}` on `Q = {q = m-1}`,
3. exhibit affine coordinates in which each `T_c` is the standard 2D
   lexicographic odometer.

## Coordinates

As in the affine-split note, parameterize

`P_0 = {x_0 + x_1 + x_2 + x_3 = 0}`

by

`phi(a,b,q) = (a, b, q-a, -q-b)`.

Then `q = x_0 + x_2`.

## Repaired First-Return Formulas

All arithmetic is modulo `m`.

```text
R_0(a,b,q) =
  (a-1, b,   q-1)   if q = 0
  (a-2, b+1, q-1)   if q = m-1 and b = 1
  (a-1, b+1, q-1)   otherwise

R_1(a,b,q) =
  (a,   b-1, q+1)   if q = 0
  (a+1, b-2, q+1)   if q = m-1 and a != m-1
  (a+1, b-1, q+1)   otherwise

R_2(a,b,q) =
  (a,   b+1, q-1)   if q = 0
  (a+1, b,   q-1)   if q = m-1 and b = 2
  (a,   b,   q-1)   otherwise

R_3(a,b,q) =
  (a+1, b,   q+1)   if q = 0
  (a,   b+1, q+1)   if q = m-1 and a != 0
  (a,   b,   q+1)   otherwise
```

Interpretation:

- the old affine-split correction still sits at `q = 0`,
- the new layer-2 patch appears on `P_0` only as a delayed correction at
  `q = m-1`.

So the repaired witness is no longer "a complicated low-layer table" at the
return-map level. It is "affine-split plus one delayed carry slice."

## Second-Return Formulas On Q

Let `Q = {q = m-1}`. Since each `R_c` changes `q` by `+1` or `-1` every step,
every `R_c`-orbit meets `Q` exactly once every `m` steps. Hence define

`T_c = R_c^m|_Q`.

The resulting maps on `(a,b)` are:

```text
T_0(a,b) = (a - 1_{b=1},         b - 1)
T_1(a,b) = (a - 1,               b - 1 + 1_{a=m-1})
T_2(a,b) = (a + 1_{b=2},         b + 1)
T_3(a,b) = (a + 1,               b + 1 - 1_{a=0})
```

## Odometer Conjugacies

Let

`O(u,v) = (u + 1, v + 1_{u=0})`

on `(Z/mZ)^2`.

Then the following affine coordinate changes conjugate each `T_c` to `O`:

```text
T_0: (u,v) = (1-b,   -a)
T_1: (u,v) = (-a-1,  b-a)
T_2: (u,v) = (b-2,   a)
T_3: (u,v) = (a,     a-b)
```

Verification statement:

`psi_c(T_c(a,b)) = O(psi_c(a,b))`

for every tested `m` and every `(a,b)`.

## Why O Is One Cycle

The low digit `u` increases by `1` at every step.
Whenever `u = 0`, the high digit `v` increases by `1`.

Therefore:

- after exactly `m` steps, `u` returns to its starting value and `v` increases
  by `1`,
- after exactly `m^2` steps, both coordinates return,
- before `m^2` steps, `v` cannot have completed a full turn.

So `O` is a single cycle of length `m^2` on `(Z/mZ)^2`.

Hence each `T_c` is a single `m^2`-cycle on `Q`.

## Lift Back To Hamiltonicity

The proof skeleton is now short.

1. `R_c` changes `q` by `+1` or `-1` every step, so every `R_c`-orbit hits
   `Q` exactly once every `m` steps.
2. Thus the return points on `Q` are exactly the `T_c`-orbit.
3. Since `T_c` is one `m^2`-cycle, `R_c` is one `m^3`-cycle on `P_0`.
4. Since every full color orbit in the torus returns to `P_0` every `m`
   steps, the color map itself is one `m^4`-cycle.

So each color map is Hamiltonian.

## Verification Artifacts

Verifier:
- `../../../torus_nd_second_return_analysis.py`

Summary JSON:
- `verification_summary.json`

Raw log:
- `verification.log`

Representative `Q`-orbit traces:
- `traces/q_traces_m5.json`
- `traces/q_traces_m7.json`

The verifier checked:

- repaired `R_c` formulas,
- repaired `T_c` formulas,
- odometer conjugacies,
- single-cycle behavior of `T_c` on `Q`,

for every `m = 3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20`.

## Unresolved Aesthetic Issues

- The most conceptual explanation of the four layer-2 exceptional rows is still
  missing.
- The proof is now structurally clean, but the layer-2 patch is still being
  read as a delayed carry rather than derived from a minimal routing principle.
- A more symmetric equivalent formulation of the same witness may still exist.

## Reproduction

```bash
python torus_nd_second_return_analysis.py \
  --out artifacts/4d_generalization/d4_second_return_odometer_02/verification_summary.json \
  --trace-dir artifacts/4d_generalization/d4_second_return_odometer_02/traces
```
