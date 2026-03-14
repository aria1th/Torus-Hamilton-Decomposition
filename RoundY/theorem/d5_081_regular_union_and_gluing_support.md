# D5 081 Regular Union And Gluing Support

This note promotes the stable results of the `081` round from `tmp/` into the
RoundY theorem record.

Its job is to collect four points in one place:

1. the regular-union theorem,
2. the exceptional-interface reduction,
3. the correct raw proof object,
4. the targeted compute support that isolates the remaining rows.

## 1. Regular-union theorem

### Theorem 1.1

On the true larger regular accessible union, every regular realization of every
realized `delta` continues.

Equivalently:

- no regular cutoff row launches a new endpoint sheet,
- no regular realization creates mixed-status `delta`,
- the regular sector contributes no tail-length ambiguity.

This is the decisive `4.1` result.

### Meaning

The full globalization theorem can no longer fail for a regular reason.

So after `081`, all regular cutoff rows are already closed at the raw theorem
level.

### Stable support

The regular endpoint witness table is promoted at:

- [d5_081_regular_union_endpoint_table.csv](../checks/d5_081_regular_union_endpoint_table.csv)

That table records, for `m=13,15,17,19,21`, the regular cutoff labels
`e_u = m(u-1)-2`, their regular holders, continuing witnesses, and successor
targets.

## 2. Exceptional-interface reduction

### Reduction 2.1

Once the regular sector is closed, the remaining exceptional issue is
equivalent to ruling out a hidden second endpoint sheet over the regular
source-`1` start label

`delta = 3m-1`.

Equivalently, the only remaining globalization issue is whether the exceptional
actual lift at `3m-3` glues into the regular continuing class through

`3m-2 -> 3m-1`.

This is the promoted content of the `4.2` note.

## 3. Correct raw proof object

### Principle 3.1

The right finite proof object is an **end-gluing table on actual lifts**, not
merely on the reconstructed quotient.

This means:

- it is not enough to know that a cutoff label has a quotient-level continuing
  witness;
- one must certify that every actual lift of that cutoff row glues into the
  continuing endpoint class on the true accessible union.

This is the promoted content of the `5.0` note.

### Consequence

The remaining raw-state theorem should be attacked row by row, not by reopening
the whole bridge/globalization problem.

## 4. Targeted compute support

The `6.0` targeted compute gives the correct backup object on the reconstructed
larger chart model for `m=13,15,17,19,21`.

### What it proves at chart level

- every `delta in Z/m^2 Z` is present;
- every `delta` has at least one continuing chart occurrence;
- grouped successor is exact: when continuation exists, the next label is
  always `delta+1`;
- the only mixed chart-status labels are exactly the cutoff labels:
  the regular endpoints `e_u = m(u-1)-2` and the exceptional end `3m-3`;
- every cutoff label already has many same-`delta` continuing witnesses;
- the exceptional cutoff lands at the common interface `3m-2 -> 3m-1`.

### What it does not yet prove

It does **not** prove the raw larger-state theorem on the true accessible
union, because chart occurrences are not yet the same thing as actual larger
boundary-state lifts.

### What it isolates

It isolates the exact finite set of rows that still need raw-state gluing.

This is why the remaining bottleneck is now one exceptional-row question rather
than a broad globalization problem.

## 5. Main promoted conclusion

After `081`, the accepted D5 state is:

- the regular union is closed at the raw theorem level;
- the only remaining gluing issue is exceptional;
- the correct proof object is an actual-lift end-gluing table;
- the larger chart model already isolates the exact rows that still need raw
  certification.

## 6. Promoted references

This note promotes the substance of:

- `tmp/d5_080_081_4.1_rA_regular_union_lemma.md`
- `tmp/d5_081_4.2.md`
- `tmp/d5_081_5.0.md`
- `tmp/d5_081_6.0_rC_targeted_compute.md`
