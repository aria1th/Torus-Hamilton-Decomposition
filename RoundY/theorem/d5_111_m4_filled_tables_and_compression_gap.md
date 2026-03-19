# D5 111: M4 filled tables and the remaining compression / selector gap

This note records the first actual filled M4-style data extraction on the
`mixed_008` full torus, and what it does and does not settle.

Main artifacts:

- [d5_111_m4_candidate_invariant_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_111_m4_candidate_invariant_summary.json)
- [d5_111_m4_candidate_invariant_run_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_111_m4_candidate_invariant_run_summary.json)
- [torus_nd_d5_m4_candidate_invariant_extract_111.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_m4_candidate_invariant_extract_111.py)

The raw packet itself is generated locally at
`RoundY/checks/d5_111_m4_raw_coordinate_packet.json` by the extraction script
and is intentionally left out of git because it is too large for `checks/`.

## What was extracted

The new script fills three kinds of data on the actual `mixed_008` full torus:

1. A raw-coordinate table packet with:
   - generator rows by color,
   - predecessor transports by torus generator,
   - local inverse rows.
2. A candidate-compression audit for smaller state spaces:
   - `feature0`,
   - `feature_profile`,
   - `full24_profile`.
3. Failure witnesses whenever a candidate state space stops being exact.

So the question “can we actually populate M4-style tables from existing code?”
now has a definite answer: yes.

## What the raw packet proves

On the raw vertex-coordinate invariant `I_raw(x)=x`, the tables are fully
populated on checked moduli `m=5,7,9`.

- generator readout is exact;
- predecessor transport is exact;
- the local inverse identity is exact;
- all five witness color rows are Latin permutations.

But this is still **not** an M4 closure, because the outgoing coverage criterion
from `108` fails: the colorwise generator rows are not permutations of
`{0,1,2,3,4}` on every state.

The raw packet records the failure counts:

- `m=5`: `990` non-permutation rows
- `m=7`: `3230` non-permutation rows
- `m=9`: `7590` non-permutation rows

The validator confirms this immediately on the packet:

- [validate_d5_m4_packet_110.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/validate_d5_m4_packet_110.py)
  stops at `generator_rows[7] is not a permutation of 0..4`.

So the filled raw packet is a debugging / evidence packet, not an acceptance
packet.

## What the compact candidates do

The smaller candidates behave in a very structured way.

`feature0`

- only `29` states on every checked modulus;
- already fails generator exactness badly:
  `26` generator-failure classes and `13` predecessor-failure classes.

`feature_profile`

- state counts:
  `659, 2157, 4196, 6121` for `m=5,7,9,11`;
- generator readout is exact on all checked moduli;
- outgoing-permutation coverage still fails;
- deterministic predecessor transport fails on
  `1, 96, 576, 1077` states.

`full24_profile`

- state counts:
  `3124, 15662, 46211, 92242` for `m=5,7,9,11`;
- generator readout is exact on all checked moduli;
- outgoing-permutation coverage still fails;
- deterministic predecessor transport fails on
  `1, 665, 5287, 19041` states.

So adding more local neighborhood data does not automatically move the witness
toward the selector criterion. In fact the richer `full24_profile` is much
larger than `feature_profile` and still fails predecessor exactness at many
more states.

## Interpretation

Two different obstructions are now separated cleanly.

1. The current witness rows do not yet satisfy the outgoing-permutation
   coverage demanded by M4, even on raw coordinates.
2. The currently visible compact local invariants do not make predecessor
   transport deterministic.

That means the next missing step is not “write more extraction code.” It is one
of the following:

- a different graph-level selector package whose color rows already have the
  right outgoing coverage;
- or a nontrivial descent from the current witness family to a new invariant
  where both outgoing coverage and predecessor transport close.

## Practical use

This bundle is now good enough to send out.

- If the request is “can you compute the M4 tables at all?”, the answer is yes,
  and the raw packet is the proof.
- If the request is “does the currently visible compact invariant already
  close?”, the answer is no, and the failure-summary JSON shows where.
- If the request is “what should be proved next?”, the answer is:
  construct or identify a selector-compatible graph lift, not just a slightly
  richer local observable.
