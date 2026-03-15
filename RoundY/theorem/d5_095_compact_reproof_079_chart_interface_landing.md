# D5 095: Compact reproof of the 079 chart/interface landing

## Abstract

This note removes the standalone `079` support note by deriving the exact
chart/interface statement used in `092` from the already frozen regular-slice
chart formulas.

The proof stays at the correct scope. It does **not** prove the actual
post-exit continuation exists; that still comes from the structural first-exit
package (`062`, written explicitly in `092` Theorem 3.1). What this note does
prove is that once that post-exit continuation is read in the grouped
full-chain chart, its first two labels are forced to be

`3m-2 -> 3m-1`.

Equivalently, the exceptional chain-label continuation is

`3m-3 -> 3m-2 -> 3m-1`.

So after `095`, the cleaned `092` suite no longer needs `079` as a separate
accepted-support theorem.

## 1. Scope and imported chart package

Fix an odd modulus `m` in the accepted D5 regime and the best-seed channel

`R1 -> H_L1`.

The present note uses only the already frozen regular-slice chart package:

1. for each regular source label `u`, the `Theta = 2` window starts at
   `s_u = m((u+2) mod m) - 1`;
2. each such `Theta = 2` window has exactly `m(m-3)` consecutive full-chain
   labels;
3. grouped successor on the chart quotient is exact: whenever the continuation
   is read in that quotient, labels advance by `delta -> delta + 1`.

These formulas are the stable chart-side data already frozen in

- `checks/d5_077_compact_interval_summary.json`, and
- `checks/d5_081_regular_union_endpoint_table.csv`.

The present note uses the structural first-exit theorem only at the very end,
when connecting the chart labels back to the actual exceptional post-exit
continuation.

## 2. Algebra of the regular source windows

### Definition 2.1 (start and terminal labels)

For a regular source label `u`, write

`s_u = m((u+2) mod m) - 1`

for the `Theta = 2` start label of the source-`u` window.

Because that window has length `m(m-3)`, its terminal label is

`e_u = s_u + m(m-3) - 1`

in `Z/m^2 Z`.

### Proposition 2.2 (closed formula for the terminal label)

For every regular source label `u`,

`e_u = m(u-1) - 2 mod m^2`.

#### Proof

Substitute the start formula into the terminal formula:

`e_u = m((u+2) mod m) - 1 + m(m-3) - 1`.

Modulo `m^2`, this is

`e_u = m(u-1) - 2`.

That is exactly the endpoint formula already recorded in the promoted regular
endpoint table. `qed`

### Corollary 2.3 (the next source window is shifted by `-3`)

The label immediately after the terminal source-`u` label is the start of the
source-`u-3` window:

`e_u + 1 = s_{u-3}`

(modulo `m`, with representatives in `{1,2,4,5,...,m-1}`).

#### Proof

From Proposition 2.2,

`e_u + 1 = m(u-1) - 1`.

But

`s_{u-3} = m(((u-3)+2) mod m) - 1 = m(u-1) - 1`.

So the two labels agree in `Z/m^2 Z`. `qed`

### Corollary 2.4 (the common regular interface)

The terminal regular source-`4` label is

`e_4 = 3m-2`,

and the regular source-`1` start label is

`s_1 = 3m-1`.

Hence the common regular interface is exactly

`3m-2 -> 3m-1`.

#### Proof

From Proposition 2.2,

`e_4 = m(4-1) - 2 = 3m-2`.

From the start formula,

`s_1 = m(1+2) - 1 = 3m-1`.

By Corollary 2.3, the label after `e_4` is `s_1`. So the interface is exactly

`3m-2 -> 3m-1`.

Because each regular source window is one contiguous interval, `e_4` is the
unique terminal source-`4` representative and `s_1` is the source-`1` start
representative. `qed`

## 3. The reproof replacing 079

### Theorem 3.1 (chart/interface landing)

Read the actual exceptional post-exit continuation in the grouped full-chain
chart used for the boundary labels. Then its first two chart labels are forced
to be

`3m-2 -> 3m-1`.

Equivalently, the exceptional chain-label continuation is

`3m-3 -> 3m-2 -> 3m-1`,

where `3m-2` is the unique terminal regular source-`4` occurrence and `3m-1`
is the regular source-`1` start.

#### Proof

The exceptional cutoff row is, by definition,

`delta = 3m-3`.

In the grouped chart quotient, successor is exact and advances the label by
`+1`. Therefore the first chart label after the cutoff row is forced to be

`3m-2`.

By Corollary 2.4, that label is the common regular interface point: the unique
terminal regular source-`4` representative, followed by the regular source-`1`
start at

`3m-1`.

So the chain-label continuation is forced to be

`3m-3 -> 3m-2 -> 3m-1`.

This is exactly the chart/interface statement that `092` uses later. `qed`

### Corollary 3.2 (how this combines with 062)

Combine Theorem 3.1 with the structural first-exit theorem of `062` / `092`:

- `062` supplies existence of the actual exceptional post-exit continuation and
  its universal raw exit target;
- Theorem 3.1 identifies the corresponding full-chain labels as
  `3m-3 -> 3m-2 -> 3m-1`.

So the old `062 + 079` composition step becomes `062 + 095`, with the same
honest scope: raw existence comes from `062`, and chart/interface label
identification comes from the present note.

## 4. Exact finite support table

The frozen chart support files record the source-`4` terminal label and the
source-`1` start label exactly at the interface values below.

| `m` | `3m-3` | source-`4` terminal `= 3m-2` | source-`1` start `= 3m-1` |
|---:|---:|---:|---:|
| 5  | 12 | 13 | 14 |
| 7  | 18 | 19 | 20 |
| 9  | 24 | 25 | 26 |
| 11 | 30 | 31 | 32 |
| 13 | 36 | 37 | 38 |
| 15 | 42 | 43 | 44 |
| 17 | 48 | 49 | 50 |
| 19 | 54 | 55 | 56 |
| 21 | 60 | 61 | 62 |

For the original `079` support range `m = 13,15,17,19,21`, this matches the
promoted chart statement exactly. It also agrees with the frozen smaller-modulus
regular-slice data, including the exact `m=5` interface

`12 -> 13 -> 14`.

## 5. What changes in the cleaned package

### Corollary 5.1 (accepted-support list after 095)

After inserting Theorem 3.1 into the cleaned `092` suite, the standalone `079`
interface note is no longer needed as a separate accepted-support theorem.

The remaining imported support in the cleaned odd-`m` D5 package is:

1. `077` fixed-`delta` tail-length reduction;
2. `081` regular continuation / regular-union theorem;
3. the localized structural `033/062` input already used in the first-exit
   block.

The chart formulas used in the present note are already frozen in the promoted
regular-slice support files, so the remaining stabilization work no longer
needs a separate `079` theorem package.

## Bottom line

`095` does not prove the final raw gluing theorem by itself. What it does prove
is exactly the chain-label statement that `079` was carrying:

- source-`4` terminal regular interface label is `3m-2`;
- source-`1` regular start label is `3m-1`;
- therefore the exceptional chain-label continuation is forced to pass through
  `3m-3 -> 3m-2 -> 3m-1`.

That is the only role `079` needed to play inside the cleaned `092` suite.
