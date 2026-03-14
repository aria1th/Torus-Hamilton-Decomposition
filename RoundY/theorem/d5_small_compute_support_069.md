# D5 Small Compute Support 069

This note runs only modest validations on the already-frozen route datasets. It follows the compute-support split in the organized theorem package and does **not** reopen exhaustive raw search. It is aimed at strengthening the theorem package and the clock route. fileciteturn13file0

## 1. Full small-range validation on the frozen `047` rows

Using the full frozen active dataset for `m=5,7,9,11`:

- the phase-corner event law is exact on **every** row,
- the countdown formula for `tau` is exact on **every** row,
- the branchwise reset/countdown formula for `next_tau` is exact on **every nonterminal** row.

Per modulus:

- `m=5`: event exact on 220 rows; `tau` exact on 220 rows; `next_tau` exact on 216 nonterminal rows.
- `m=7`: event exact on 1218 rows; `tau` exact on 1218 rows; `next_tau` exact on 1212 nonterminal rows.
- `m=9`: event exact on 3960 rows; `tau` exact on 3960 rows; `next_tau` exact on 3952 nonterminal rows.
- `m=11`: event exact on 9790 rows; `tau` exact on 9790 rows; `next_tau` exact on 9780 nonterminal rows.

These are direct theorem-side checks, not imported summaries.

## 2. Exact `B+beta` support on the full small-range nonterminal branch

On the same frozen `047` nonterminal rows, define
```text
beta = -(q+s+v+layer) mod m.
```

Then `(B,beta)` is injective on the entire nonterminal active branch for `m=5,7,9,11`, and it exactly reads out:

- `q`
- `w`
- `c`
- `epsilon4`
- `tau`
- `next_tau`
- `next_B`

Per modulus:
- `m=5`: `216` distinct `(B,beta)` states on `216` nonterminal rows; injective = `True`.
- `m=7`: `1212` distinct `(B,beta)` states on `1212` nonterminal rows; injective = `True`.
- `m=9`: `3952` distinct `(B,beta)` states on `3952` nonterminal rows; injective = `True`.
- `m=11`: `9780` distinct `(B,beta)` states on `9780` nonterminal rows; injective = `True`.

This is stronger than a readout check on isolated coordinates: on the checked full small-range nonterminal branch, `(B,beta)` already identifies the full exact current state and its next grouped state.

## 3. Representative theorem-side extension through `m=19`

Using the `049` representative rows for `m=5,7,9,11,13,15,17,19`, the theorem-side formulas remain exact on the sampled states:

- event law exact on every representative row,
- `tau` formula exact on every representative row,
- `next_tau` formula exact on every representative row where the theorem formula is checkable from the sampled fields alone (`tau>0`, `wrap`, or `carry_jump`).

This is not a substitute for exhaustive full-row regeneration, but it is a clean row-level extension of the theorem formulas through `m=19`.

## 4. Representative large-range support on `m=25,27,29`

Using the branch-local support tables from `059b`:

- the universal target-step law is exact for every recorded source family,
- the universal target phases remain
  - regular: `(m-1,m-2,1)` with exit direction `[2]`,
  - exceptional: `(m-2,m-1,1)` with exit direction `[1]`,
- the displayed scheduler anchor is exactly the phase-corner anchor law on every displayed row,
- and the displayed consecutive rows satisfy the predicted `theta -> theta+1` drift exactly.

Per modulus:
- `m=25`: target formulas exact on `24` source families; displayed anchor law exact = `True`; displayed drift exact = `True`.
- `m=27`: target formulas exact on `26` source families; displayed anchor law exact = `True`; displayed drift exact = `True`.
- `m=29`: target formulas exact on `28` source families; displayed anchor law exact = `True`; displayed drift exact = `True`.

## 5. Honest boundary

I did **not** regenerate exhaustive larger-modulus raw rows, and I did **not** compute a new accessible quotient beyond the frozen/support ranges. That remains the heavier compute task from the earlier request.

But the small computations here do strengthen the current picture in exactly the right place:

- the theorem-side phase-corner and countdown/reset formulas are exact on the full checked small-range rows,
- `(B,beta)` is already an exact nonterminal state identifier on that full checked range,
- and the larger branch-local support at `m=25,27,29` matches the same scheduler and universal target formulas.
