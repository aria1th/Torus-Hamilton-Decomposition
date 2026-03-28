# D5 292 Residual Compute Request Template

This is the stable RoundY version of the `2026-03-25` residual compute request
template.

Use it together with:

- [d5_291_residual_compute_campaign_conclusion.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_291_residual_compute_campaign_conclusion.md)
- [d5_289_promoted_collar_base_section_reduction_and_no_go.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_289_promoted_collar_base_section_reduction_and_no_go.md)
- [d5_290_current_assumption_and_gap_audit.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_290_current_assumption_and_gap_audit.md)

Its purpose is to standardize new residual-branch compute requests so that:

- each candidate is compared against the right control family;
- the saved outputs are enough for later promotion;
- and the acceptance criterion tracks real structural progress.

## 1. Request identity

- Branch target:
  - [ ] Pure color-`1` frontier
  - [ ] `B`-active / gate branch
- Family ID:
- Candidate formula:
- Quotient-simplified class pattern:
- Nearest control family:

## 2. Modulus set

- Controls:
- Discovery range:
- Promotion range:

## 3. What to compute

### Mandatory outputs

1. Color profile `[ℓ0, ℓ1, ℓ2]`
2. Support rows and row-classes after quotient simplification
3. Induced section-map cycle counts on `H_m`
4. Induced base permutation cycle type on `B_m`
5. One witness state for each short cycle
6. Comparison against the nearest control family

### Additional branch diagnostics

#### Pure color-`1` frontier

- `F_m : H_m -> H_m` cycle lengths
- `P_m : B_m -> B_m` cycle lengths
- top / double-top / hinge / side-top episode counts
- donor color-`2` stability surrogate

#### `B`-active / gate branch

- color-`0` wall length and wall width
- gate destination / gate terminus
- whether the gate splices the wall back into the bulk cycle
- whether the same gate gives color `1` a transversal kick
- whether color `2` remains a bystander

## 4. Promotion rules

### Reject immediately if

- quotient-equivalent to the control family
- no change in `P_m` or in wall/gate geometry
- one collateral color collapses badly across the checked range

### Promote if

- `P_m` cycle count decreases consistently across the checked range, or
- wall/gate geometry shows a genuine splice mechanism, and
- the candidate stays distinct from all controls after quotient simplification

## 5. Storage requirements

### Manifest row for every candidate

- modulus
- family ID
- simplified class pattern
- `[ℓ0, ℓ1, ℓ2]`
- `H_m` cycle summary
- `B_m` cycle summary
- short-cycle witness states
- one-line diagnostic note

### Full bundle only for promoted candidates

- exact section-return dump
- exact induced maps on `H_m` and `B_m`
- representative witness trajectories
- short prose note describing what changed relative to control

## 6. Recommended campaign order

1. Regression on controls and current seed families
2. Atlas extension to the next resonant range
3. Pure color-`1` base-splicer sweep at `k = 3`
4. Base-visible one-line `k = 4` sweep
5. `B`-active scaffold + gate sweep
6. Promotion dump for a small number of strong candidates

## 7. Interpretation rule

Do not treat “local repair looks nicer” as success by itself.

At the current frontier, the first real signs of progress are:

- a genuine change in the reduced base permutation `P_m`, or
- a genuine change in wall/gate splice geometry.

If neither happens, the candidate should be recorded as a control-near miss,
not as a promoted residual theorem candidate.
