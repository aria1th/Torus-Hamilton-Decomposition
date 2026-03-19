# D5 111: external request for the next M4 step

This request assumes the attached `111` bundle has already been read.
The oversized raw packet is generated locally by
`scripts/torus_nd_d5_m4_candidate_invariant_extract_111.py` at
`RoundY/checks/d5_111_m4_raw_coordinate_packet.json` and is intentionally not
tracked in git.

## What the bundle already settles

- We can populate generator / predecessor / inverse tables on the actual
  `mixed_008` full torus.
- The current small local invariants do **not** close M4:
  they either fail generator exactness (`feature0`) or fail deterministic
  predecessor transport (`feature_profile`, `full24_profile`).
- Even raw coordinates do not satisfy the outgoing-permutation coverage needed
  by the selector criterion.

So the next request is **not** “please compute more raw tables.”

## What is being asked

Please help with one of the following theorem/data targets.

### Target A: a selector-compatible graph lift

Produce a graph-level construction or theorem package in which, for each torus
vertex state `I`,

- the colorwise generator row `g_c(I)` is a permutation of `{0,1,2,3,4}`;
- predecessor transport `P_j(I)` is deterministic;
- the local inverse identity `g_c(P_j(I)) = j` has exactly one solution `j`.

This can be on `(beta,delta)` or on any explicitly equivalent invariant.

### Target B: a no-go / mismatch theorem for the current witness lift

If the current `mixed_008` witness family cannot possibly yield such a
selector-compatible lift, isolate why.

The strongest useful form would be:

- either a direct proof that outgoing-permutation coverage fails for every
  state-space descent compatible with the present witness rows;
- or a proof that any compact local invariant preserving current generator
  readout must fail deterministic predecessor transport.

## Minimal useful deliverables

Any one of the following would be enough to move the project.

1. A compact invariant with explicit formulas for `g_c(I)` and `P_j(I)`,
   checked on pilot moduli and plausibly provable in general.
2. A theorem-level comparison showing that the correct selector package is not
   the current raw witness row but a transformed / descended graph rule.
3. A sharp no-go statement explaining why the present witness row cannot be the
   final M4 selector object.

## Files to look at first

- [d5_108_M4_M5_gate_note.tex](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/tmp/d5_108_M4_M5_gate_note.tex)
- [d5_110_M5_after_M3_fiber_return_note.tex](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/tmp/d5_110_M5_after_M3_fiber_return_note.tex)
- [d5_111_m4_filled_tables_and_compression_gap.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_111_m4_filled_tables_and_compression_gap.md)
- [d5_111_m4_candidate_invariant_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_111_m4_candidate_invariant_summary.json)
- [torus_nd_d5_m4_candidate_invariant_extract_111.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_m4_candidate_invariant_extract_111.py)
