# D5 096: Compact reproof of the 081 regular closure theorem

## Abstract

This note replaces the standalone `081` support note by isolating the exact
regular-closure statement used later in `092` and proving it in a shorter
manuscript form.

The proof has two ingredients:

1. the already frozen regular-window formulas from `095`, which control the
   source windows and their endpoint labels;
2. the promoted endpoint witness table
   `checks/d5_081_regular_union_endpoint_table.csv`, used in the exact sense
   advertised by the original `081` note: as an actual-lift end-gluing
   certificate on the true larger regular accessible union.

The interval arithmetic is uniform in odd `m`. The raw endpoint certificate in
the bundle is checked on the same range as the old `081` support file,
namely `m = 13,15,17,19,21`. This note keeps exactly that support range. It
does **not** re-prove the `077` tail-length reduction.

## 1. Scope and imported endpoint certificate

Fix an odd modulus `m` in the accepted D5 regime and the best-seed channel

`R1 -> H_L1`.

Let

`R_reg = {1,2,4,5,...,m-1}`

be the regular source labels.

We use the regular window formulas already frozen in `095`:

- source-`u` start label  
  `s_u = m((u+2) mod m) - 1`;
- source-`u` terminal label  
  `e_u = m(u-1) - 2`;
- source-`u` window  
  `I_u = [s_u, e_u]`, a contiguous interval of length `m(m-3)` in
  `Z/m^2 Z`;
- endpoint shift  
  `e_u + 1 = s_{u-3}`;
- grouped successor is exact inside each source window.

We also use the promoted regular endpoint witness table

`checks/d5_081_regular_union_endpoint_table.csv`.

In the present note that table is used in the same theorem-level sense stated
by the old `081` support note: each row is an actual-lift endpoint certificate
on the true larger regular accessible union, not merely a quotient-holder
summary.

## 2. Endpoint arithmetic on regular source windows

### Definition 2.1 (regular holders)

For a regular source label `v in R_reg`, say that a boundary label `delta`
has a **source-`v` regular holder** if `delta in I_v`.

A source-`v` holder is **terminal** when `delta = e_v`; otherwise it is
**interior**.

### Proposition 2.2 (which regular windows contain `e_u`)

Let `u,v in R_reg`. Then:

1. `e_u in I_v` if and only if `v` is not one of the three predecessors
   `u-3, u-2, u-1` (mod `m`, intersected with `R_reg`);
2. among the regular holders of `e_u`, the only terminal one is the
   source-`u` holder.

#### Proof

Compute in `Z/m^2 Z`:

`e_u - s_v = (m(u-1)-2) - (m((v+2) mod m)-1) = m((u-v-3) mod m) - 1`.

Write

`t = (u-v-3) mod m in {0,1,...,m-1}`.

Because the source-`v` window has length `m(m-3)`, the label `e_u` belongs to
`I_v` exactly when the difference above is one of the values

`m-1, 2m-1, ..., m(m-3)-1`.

Equivalently, `t` must satisfy

`1 <= t <= m-3`.

The excluded cases are therefore `t = 0, m-2, m-1`, which are exactly the three
predecessors `v = u-3, u-2, u-1` modulo `m`.

Now `e_u` is terminal in source `v` exactly when the difference is the last
point of the interval, namely

`e_u - s_v = m(m-3) - 1`.

That means `t = m-3`, equivalently `v = u`. So the only terminal regular
holder of `e_u` is the source-`u` holder. `qed`

### Corollary 2.3 (containing and continuing regular holders at `e_u`)

For each regular endpoint label `e_u`:

- the excluded regular sources are  
  `R_reg intersect {u-3, u-2, u-1}`;
- the containing regular holders are  
  `R_reg \ (R_reg intersect {u-3, u-2, u-1})`;
- the continuing regular holders are exactly the containing regular holders
  other than `u`.

So every containing regular holder of `e_u` except the source-`u` holder is
interior and therefore continues to `e_u + 1`.

#### Proof

This is immediate from Proposition 2.2. `qed`

### Proposition 2.4 (preferred witness pattern in the promoted endpoint table)

A direct row-by-row read of the promoted endpoint table shows the uniform
preferred-witness pattern

- `p(1) = 2`,
- `p(2) = 4`,
- `p(u) = u+1` for `4 <= u <= m-2`,
- `p(m-1) = 1`.

For each row, the recorded successor target is

`e_u + 1 = s_{u-3}`.

This target is a regular start unless `u = 6`, in which case it is the
exceptional start.

#### Proof

The successor formula is already `e_u + 1 = s_{u-3}` from the regular-window
algebra imported from `095`. The promoted CSV records exactly the preferred
witness pattern above on every checked row `m = 13,15,17,19,21`, and each such
`p(u)` belongs to the continuing-holder set described in Corollary 2.3. So the
recorded preferred witnesses are always genuine continuing witnesses at the
same endpoint label. `qed`

## 3. The reproof replacing 081

### Theorem 3.1 (regular endpoint continuation)

For each checked regular endpoint row `e_u`, every actual regular lift at label
`e_u` glues on the true larger regular accessible union to the continuing class
certified by the preferred witness `p(u)` from Proposition 2.4.

Consequently, every regular endpoint lift continues to the successor label

`e_u + 1 = s_{u-3}`,

with `u = 6` giving the exceptional start and all other `u` giving a regular
start.

#### Proof

By the theorem-level meaning assigned to the promoted endpoint table in the old
`081` package, each row of that table is already an actual-lift endpoint
certificate on the true larger regular accessible union. Proposition 2.4
identifies, on each checked row, a preferred same-label continuing witness and
its exact successor target. Therefore every actual regular endpoint lift at
`e_u` is certified to glue to a continuing witness and hence has a forward
successor to `e_u + 1`. `qed`

### Theorem 3.2 (regular closure theorem; replacement for 081)

On the true larger regular accessible union, every regular realization of every
realized `delta` continues.

This is proved on the same checked raw range carried by the promoted endpoint
table:

`m = 13,15,17,19,21`.

#### Proof

Take any regular realization and choose one regular holder for its label.

If the realization is interior in that holder, grouped successor exactness
inside the source window gives a forward successor immediately.

If the realization sits at the terminal label of that holder, then its label is
some `e_u`, and Theorem 3.1 gives a forward successor on the true larger
regular accessible union.

So every regular realization continues. `qed`

### Corollary 3.3 (no regular mixed-status label)

No realized regular `delta` has both continuing and terminal regular lifts.

#### Proof

By Theorem 3.2, every regular lift continues. `qed`

### Remark 3.4 (what this note does and does not replace)

Theorem 3.2 is exactly the `081` content used in `092`:

- regular realizations never create a new endpoint sheet;
- the full odd-`m` package can no longer fail for a regular reason.

This note does **not** separately re-prove the stronger wording
“no regular tail-length ambiguity.” That belongs to the later `077`
fixed-`delta` reduction.

## 4. Two representative checked rows

The promoted CSV contains `75` endpoint rows across the checked moduli
`13,15,17,19,21`. Two representative rows already show the two structural
shapes that matter.

### Example 4.1 (`m=13`, ordinary regular handoff)

For `u=4` one has

- `e_4 = 37`,
- containing regular holders  
  `{4,5,6,7,8,9,10,11,12}`,
- continuing regular holders  
  `{5,6,7,8,9,10,11,12}`,
- preferred witness `p(4)=5`,
- next label `38 = s_1`, a regular start.

So the unique terminal source-`4` holder at `37` is glued to a same-label
continuing witness and therefore does not launch a new regular endpoint sheet.

### Example 4.2 (`m=13`, regular-to-exceptional handoff)

For `u=6` one has

- `e_6 = 63`,
- containing regular holders  
  `{1,2,6,7,8,9,10,11,12}`,
- continuing regular holders  
  `{1,2,7,8,9,10,11,12}`,
- preferred witness `p(6)=7`,
- next label `64 = s_3`, the exceptional start.

So even the regular endpoint whose successor lands in the exceptional source
still has a certified continuing witness on the true larger accessible union.

## 5. Package consequence after 096

After inserting Theorem 3.2 into the cleaned `092` suite, Proposition 4.4 no
longer needs to remain an accepted-support theorem.

Combined with the earlier `094` and `095` reproof notes, the remaining serious
imported support in the cleaned odd-`m` package is now:

1. `077`, the fixed-`delta` tail-length reduction;
2. the localized structural `033/062` input already sitting inside the
   first-exit theorem.

So `096` removes `081` from the manuscript-order accepted-support list while
keeping the same honest raw support range as the promoted endpoint table.

## Bottom line

The point of `096` is not to reopen the D5 regular sector. It is to state the
regular closure theorem in the exact form later used by `092`, and to make the
proof object explicit:

- uniform regular-window arithmetic isolates the endpoint rows;
- the promoted endpoint table certifies actual endpoint gluing there;
- therefore every regular realization continues;
- so regular rows can no longer support a new endpoint sheet.
