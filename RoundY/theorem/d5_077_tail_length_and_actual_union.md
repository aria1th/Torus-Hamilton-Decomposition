# D5 077 Tail Length And Actual Union

This note promotes the stable `077` globalization reduction from `tmp/`.

It collects the two decisive `077` outcomes:

1. fixed-`delta` ambiguity reduces to tail length;
2. the actual frozen regular union already glues to the odometer with no local
   future-word conflict.

## 1. Tail-length reduction

### Theorem 1.1

Once the concrete bridge package `(beta,delta)` is accepted, two realizations
of the same boundary label `delta` can differ only by remaining full-chain tail
length.

Equivalently:

- there is no further local future-law ambiguity at fixed `delta`;
- any fixed-`delta` ambiguity is purely endpoint / terminal-distance geometry.

So:

`rho = rho(delta)` globally

holds if and only if fixed realized `delta` has realization-independent tail
length.

## 2. Actual frozen-union check

### Main checked result

On the actual saved regular full-chain union for `m = 7,9,11`:

- every defined `(beta,delta)` transition matches the odometer successor;
- repeated realized `(beta,delta)` states have no observed future-prefix
  conflicts;
- repeated realized boundary `delta` values have no conflicting observed future
  prefixes;
- the all-source regular union glues to one deterministic cycle of size `m^3`.

So on the actual frozen range, the remaining obstruction is not local event-law
ambiguity. It is only possible trace-end / component geometry.

### Small-modulus caveat

`m=5` remains the tiny degenerate exception, with incomplete boundary coverage
on the saved regular full-chain union.

## 3. Practical consequence

After `077`, the globalization question is no longer:

> does the concrete bridge have the right local readout?

It is:

> does fixed realized `delta` have realization-independent tail length on the
> true accessible union?

That is the reduction later sharpened further by the `080` no-mixed-delta
lemma.

## 4. Stable support

The compact interval summary is promoted at:

- `checks/d5_077_compact_interval_summary.json`

## 5. Promoted references

This note promotes the substance of:

- `tmp/077_d5_trackB_tail_length_reduction.md`
- `tmp/d5_077_trackC_actual_union_check_20260314.md`
