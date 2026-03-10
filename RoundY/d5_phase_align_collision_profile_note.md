# D5 phase_align collision profile

## Result
For the stable joined-quotient field, the proposed one-bit refinement
\[
\text{phase\_align}_c(x)=\mathbf 1_{(v_c-q_c)=0}
\]
is **necessary-looking but not collision-complete**.

It kills every aligned hidden-phase collision, but it leaves a large residual family of multi-\(\delta\) states inside the misaligned branch.

## Deterministic findings
Let
\[
\delta=v-q \pmod m
\]
for representative color 0.
On the visited return states of the stable joined-quotient field:

- original multi-\(\delta\) state counts are
  - \(124, 2338, 4002, 4212, 4212\) for \(m=5,7,9,11,13\);
- after splitting by `phase_align = 1_{\delta=0}` the remaining multi-\(\delta\) counts are
  - \(88, 2040, 3892, 4208, 4212\).

So the split removes the aligned branch but leaves almost all nonzero-\(\delta\) collisions intact for larger odd \(m\).

## Why this still matters
This does **not** show the one-bit refinement is wrong.
If the correct d=5 grammar only needs a zero-trigger carry (as in odometer-style constructions), then separating `delta=0` from `delta\neq0` may still be the right first move.

What it *does* show is:

- `phase_align` is not a full encoding of the hidden phase `delta`;
- if `Theta_AB + phase_align` still collapses, then the next refinement must separate a nonzero-\(\delta\) predecessor/tail class, not just add more anchor freedom.

## Useful pattern
Among the residual misaligned classes, many already contain *all* nonzero delta values.
The counts of states with full nonzero support \((m-1)\) are
- \(1, 61, 331, 469, 501\) for \(m=5,7,9,11,13\).

This is compatible with the idea that the next successful quotient may only need
- a zero-vs-nonzero phase test first,
- and only if that fails, one more predecessor/tail-entry bit.

## Branch decision
- First refinement to try: `Theta_AB + phase_align`.
- If that fails with the same collapse pattern, the next bit should encode a **nonzero phase class / predecessor-tail motif**, not a freer anchor grammar.
