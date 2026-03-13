# Codex Work Note s70

## Task

Replace the dangerous full-state `059A` phase-scheduler support pass with a
branch-local validator that is actually aligned with the theorem claim.

## Why the task changed

The old `059A` route reused the all-state builder and was already too heavy at
`m=25` for optional support work.  That is the wrong asymptotic object for the
current proof, because `059` only needs support that the active representative
branch stays inside the unmodified `B`-region where the mixed witness rule
applies directly.

So the support task was changed from:

- full active-branch rebuild on larger moduli,

to:

- branch-local validation using the `037` raw corridor model plus the `059`
  scheduler.

## Result

The replacement validator succeeded.

- small-range anchor check on `m=5,7,9,11`:
  - modified-class formulas match the actual extracted labels
  - active nonterminal corridor rows are all `B`
- large-range branch-local support on `m=25,27,29`:
  - all representative source-family corridors stay in `B` up to first exit
  - the `059` scheduler agrees exactly with the `037` raw odometer step
  - `pred_sig1_wu2 <-> s=2`
  - the regular and exceptional first-exit targets remain the `037` universal
    raw targets

## Interpretation

This is strong support for `059`, and it is much safer than the original
`059A` route.  If more proof support is needed later, the branch-local model is
the right base to extend, not the old full-state checker.
