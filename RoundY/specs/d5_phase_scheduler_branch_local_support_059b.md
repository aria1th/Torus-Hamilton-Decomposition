# D5 phase scheduler support 059B: branch-local validation plan

Task ID:
D5-PHASE-SCHEDULER-BRANCH-SUPPORT-059B

Question:
Can we validate the real proof-critical premise behind `059` without using the
memory-heavy full-state `059A` checker?

Motivation for changing the support task:

- `059A` attempts to rebuild the full active branch from the old all-state
  constructor.
- On `m=25`, that route already pushed roughly `10 GB` RSS and remained slow,
  so it is not the right support path for `m=27,29`.
- The theorem claim in `059` does not actually need whole-torus support.  It
  only needs support that the representative active branch stays inside the
  unmodified `B`-region where the raw `mixed_008` scheduler applies.

So the support target is changed from:

- full active-branch rebuild on larger moduli,

to:

- branch-local validation on representative source families, using the already
  extracted raw odometer from `037`.

New support questions:

1. On the checked small range `m=5,7,9,11`, do direct class formulas for
   `B/L1/R1/L2/R2/L3/R3` match the actual extracted best-seed labels along the
   active branch?
2. On the larger support range `m=25,27,29`, if we start from the universal raw
   corridor entry state from `037` and follow the exact raw odometer rule:
   - do we avoid all modified classes until the first-exit target?
   - does the mixed-witness scheduler from `059` agree with the raw odometer
     step at every branch-local state?
   - does the predecessor flag reduce exactly to `pred_sig1_wu2 <-> s=2`?
3. Do the regular and exceptional first-exit targets remain the `037` universal
   raw targets?

Planned validation model:

- Small-range anchor:
  use the existing extracted active rows from the old scripts, where labels are
  already known.
- Large-range branch-only model:
  use the `037` raw odometer on `(q,w,lambda)` with universal entry
  `(m-1,1,2)` and universal first-exit targets
  `(m-1,m-2,1)` and `(m-2,m-1,1)`.
- Reconstruct the current branch state from:
  - source family (`regular` / `exceptional`)
  - `rho = source_u + 1`
  - raw triple `(q,w,lambda)`
  - phase count along the corridor
- Compare:
  - class membership
  - scheduler prediction from `059`
  - raw odometer next step from `037`

Why this is not circular:

- the raw odometer model and first-exit targets come from the earlier `037`
  extraction branch,
- the scheduler comes from the `059` proof reduction,
- the support check is whether those two independently obtained descriptions are
  consistent on larger odd moduli.

Outputs:

- `analysis_summary.json`
- `small_range_label_formula_checks.json`
- `large_range_branch_validation.json`
- `representative_branch_tables.json`

Return format:

- exact / not exact on the small-range class-formula check
- exact / not exact on the large-range branch-local scheduler consistency check
- first failure witness if any
- explicit statement whether the new support path justifies replacing `059A`
  for larger odd moduli
