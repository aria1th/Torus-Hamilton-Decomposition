# D5 127: local/countdown-carrier provenance check on the exact marked object

This note records the compute follow-up requested after `124`--`126`.

## Scope

The theorem-side M3 quotient burden is already closed by `126` with the intended
quotient fixed to `(B,beta)`. The separate historical question is whether an
older local/countdown-carrier object can be identified with the theorem-side
quotient through its realized clock object.

The tested candidate families are:

- `Q_tau = (B, min(tau,8), epsilon4)`
- `Q_fw = (B, epsilon4, f1,...,f7)`

The run is performed on the regenerated carry-jump-to-wrap exact marked object,
not on the full raw active-row dump.

## Outputs

- summary JSON:
  [d5_127_local_provenance_compare_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_127_local_provenance_compare_summary.json)
- per-modulus table:
  [per_modulus.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_127_local_provenance_compare/per_modulus.json)
- extracted first-witness packet:
  [d5_127_local_provenance_first_witness.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_127_local_provenance_first_witness.json)
- full detail dump:
  [details.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_127_local_provenance_compare/details.json)
- compute script:
  [torus_nd_d5_local_provenance_compare_127.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_local_provenance_compare_127.py)

## Main verdict

The checked range is

`m in {11,13,15,17,19,21,23,25}`.

Results:

- at `m=11`, both `Q_tau` and `Q_fw` satisfy Success A on the regenerated exact
  marked object;
- from `m=13` onward, both candidates fail;
- the first failure modulus is `m=13`;
- from `m=13` onward, both candidates have phase-fiber size `3` over the
  theorem-side key and fail deterministic successor on the accessible quotient.

So the historical local provenance statement is false for both tested candidate
families on the checked range.

## First exact obstruction witness

At `m=13`, both candidate families collapse the following two regular states:

- same grouped base `B = (4,1,4,10,regular)`
- same current event `epsilon4 = flat`
- same tested local candidate state

but different theorem-side clocks:

- one state has `beta = 9`, `q0 = 12`, `sigma = 3`, `source_u = 1`
- the other has `beta = 10`, `q0 = 11`, `sigma = 5`, `source_u = 2`

This is already enough to break exact identification with `(B,beta)`.

The same bucket also breaks deterministic successor:

- one successor lands in candidate state over `B = (4,1,4,12,regular)` with
  the next flat countdown value decreased;
- the other lands in the same next `B` but with a different next local state.

So the no-go is not just a missing clock reconstruction at the current state;
the quotient dynamics themselves are already nondeterministic from `m=13`
onward.

## Interpretation

This supports the current theorem-side choice made in `126`:

- use `(B,beta)` as the intended exact deterministic quotient for M3;
- do not identify the older countdown-carrier packages `Q_tau` or `Q_fw`
  canonically with `(B,beta)` on the full exact marked object.

The failure pattern is source-residue shaped in the sense that two states with
the same visible grouped base and the same local countdown/future-window data
still differ by hidden chain bookkeeping, and that hidden bookkeeping changes
both the theorem-side clock and the next local state.
