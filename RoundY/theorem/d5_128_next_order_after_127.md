# D5 next order after the 127 local-provenance result

## What is now frozen

The following are no longer live proof targets.

1. **Theorem-side intended quotient** is fixed to
   \[
   Q_{\mathrm{th}}=(B,\beta).
   \]
   This closes the theorem-side M3 burden.

2. **Historical local provenance** via
   \[
   Q_{\tau}=(B,\min(\tau,8),\epsilon_4),
   \qquad
   Q_{\mathrm{fw}}=(B,\epsilon_4,f_1,\dots,f_7)
   \]
   should not be used in the proof spine.
   The checked-range result is:
   - both candidates pass at `m=11`;
   - both fail from `m=13` onward;
   - from `m=13` onward they already fail deterministic successor.

3. The older theorem-side target
   “future words of `epsilon4` separate states on the exact marked object”
   is removed permanently.

## Closed packages

- **M2 theorem-side core**: exact marked carry-jump-to-wrap object with anchor rigidity.
- **M3 theorem-side package**: comparison/factor chain through `(B,beta)`.
- **M4 on SelCorr**: all-odd corrected-selector theorem.
- **M5 color 4 on SelStar**: all-odd Hamiltonicity theorem.
- **M6**: globalization / exceptional continuation package.

## Remaining live packages

### 1. M1

Channel reduction from the full odd-`m`, `d=5` problem to the best-seed channel.

This is now the only theorem-side placeholder.

### 2. Colorwise graph package

Do **not** require one common selector family.
Use the weaker colorwise selector framework:
- one local rule per color,
- outgoing exhaustiveness pointwise,
- incoming uniqueness per color,
- global descent to torus permutations.

This is the right graph-side placeholder because it matches the corrected generic
upgrade theorem.

### 3. Remaining M5 colors

The closed color-4 branch should now be treated as a fixed theorem.
The next serious target should be the branch with the strongest current evidence.
At the moment the best candidate is:
- **color 3 on SelStar**.

Only after one more colorwise Hamiltonicity theorem is closed should we decide
whether to continue branch-by-branch or redesign the graph package.

## Practical order

1. Fold the corrected theorem-side package into the master manuscript.
2. Attack M1 directly.
3. Work graph-side in the colorwise framework.
4. Try to close the color-3 SelStar branch next.
5. Reassess whether a mixed colorwise assembly is realistic.

## What not to do next

- Do not spend new proof effort trying to recover `Q_tau` or `Q_fw` as the intended quotient.
- Do not keep the old future-word-separation phrasing for `epsilon4`.
- Do not force a single common selector family before it is mathematically needed.
