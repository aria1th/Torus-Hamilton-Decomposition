# Codex Work Note s66

## Task

Run the optional narrow compute request after `052`:
probe short symbolic laws for the boundary reset maps and package the result if
the signal is clean.

## Result

Artifact `053` is worth keeping as optional proof support.

- No exact single affine output law was found for either reset map in the
  tested small-coefficient family.
- No exact two-stage piecewise law was found in the tested family.
- One exact simple fiber formula does survive:
  on `carry_jump`, reset value `0` is exactly
  `s + v + layer ≡ 2 (mod m)` on the tested range.
- No similarly short formula was found for the `carry_jump` value `1` fiber or
  for any `other`-branch fiber.

## Interpretation

This is symbolic polish for the boundary-reset theorem discussion.

It does not change the theorem object and it does not open a new compute
branch.
