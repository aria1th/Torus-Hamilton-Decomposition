# D5 084 Compute Evidence Index

This note organizes the most useful compute evidence files in `RoundY/checks/`,
especially the ones whose filenames are terse, historical, or not
self-explanatory.

Its job is to answer:

> which check file supports which theorem layer?

## 1. Current canonical evidence chain

For the active `076–083` theorem chain, the most important stable evidence files
are:

- `checks/d5_077_compact_interval_summary.json`
- `checks/d5_081_regular_union_endpoint_table.csv`

These are the two check files most directly cited by the current frontier notes.

## 2. Bridge and exact-reduction evidence

### `d5_065_beta_section_stress_test_066.json`

Meaning:

- early direct support that `(B,beta)` is exact for
  `q, c, epsilon4, tau, next_tau, next_B`
- also supports the section/chain reduction viewpoint

Best paired theorem note:

- `theorem/d5_065_beta_section_stress_test_066.md`

### `d5_compute_support_validation_068.json`

Meaning:

- exact-reduction validation on the marked-chain object
- supports the chain-first reduction and the rigidity reading

Best paired theorem notes:

- `theorem/d5_compute_support_validation_068.md`
- `theorem/d5_070_exact_reduction_chain_first.md`

### `d5_exact_reduction_compute_support_070.json`

Meaning:

- marked-chain exact reduction diagnostics
- supports the statement that the first exact object is a marked length-`m`
  chain, not yet a full cycle

Best paired theorem note:

- `theorem/d5_exact_reduction_compute_support_070.md`

### `d5_marked_chain_rule_and_local_quotient_071.json`

Meaning:

- exact per-chain rule and local quotient evidence
- supports the statement that the intended class already sees full affine chain
  coordinate on each fixed chain

Best paired theorem notes:

- `theorem/d5_marked_chain_rule_and_local_quotient_071.md`
- `theorem/d5_marked_chain_rule_and_quotient_20260314_071.md`

## 3. Decorated-bridge and symmetry evidence

### `d5_073_r1_support.json`

Meaning:

- support for the static decorated-bridge obstruction
- shows why chain-static `(beta,a,b)` is not enough globally

Best paired theorem note:

- `theorem/d5_073_r1.md`

### `d5_researcher2_decorated_symmetry_support_073.json`

Meaning:

- support for the symmetry/asymmetry update
- shows that the clock normalizes globally while finite decoration remains

Best paired theorem notes:

- `theorem/d5_072_r2.md`
- `theorem/d5_073.md`

### `d5_074_r1_support.json`

Meaning:

- support for the dynamic boundary odometer candidate
- early evidence for `(beta,q,sigma)` / `(beta,delta)`

Best paired theorem note:

- `theorem/d5_074_r1.md`

### `d5_074_r2_support.json`

Meaning:

- support for the “symmetric clock, asymmetric splice memory” interpretation

Best paired theorem note:

- `theorem/d5_074_r2.md`

## 4. Realization and bridge support

### `d5_075_bridge_support.json`

Meaning:

- evidence for the dynamic boundary odometer bridge in the `075` packaging

Best paired theorem note:

- `theorem/d5_075_bridge.md`

### `d5_075_realization_support.json`

Meaning:

- evidence for the `075` realization packaging
- supports the corner-time descent reading once the right quotient is exact

Best paired theorem note:

- `theorem/d5_075_realization.md`

## 5. Current globalization evidence

### `d5_077_compact_interval_summary.json`

Meaning:

- compact summary of the realized `delta` interval structure
- includes the key interval-start formula and compact per-source data

Best paired theorem notes:

- `theorem/d5_077_tail_length_and_actual_union.md`
- `theorem/d5_079_exceptional_interface_support.md`

### `d5_081_regular_union_endpoint_table.csv`

Meaning:

- regular cutoff endpoint/continuation witness table
- the main check object supporting closure of the regular raw gluing sector

Best paired theorem notes:

- `theorem/d5_081_regular_union_and_gluing_support.md`
- `theorem/d5_082_frontier_and_theorem_map.md`

## 6. Historical but still useful support

These are older support files that are still occasionally useful, but are no
longer the main active evidence:

- `d5_CJ_flat_corner_support_057.json`
- `d5_CJ_theta_event_law_058.json`
- `d5_small_compute_support_069.json`
- `d5_chain_catalog_search_069.json`
- `d5_full_branch_catalog_search_069.json`
- `d5_spliced_chain_catalog_search_069.json`

They support the earlier compression story, but the current active frontier no
longer depends on them directly.

## 7. Recommended citation policy

When citing compute evidence:

- cite the theorem note first;
- use the JSON/CSV file as the explicit machine-check support object;
- prefer the files in sections 2–5 above over the older historical support
  files unless you are discussing the earlier route compression itself.

## 8. Bottom line

The most important poorly named but still useful evidence files are:

- `d5_073_r1_support.json`
- `d5_researcher2_decorated_symmetry_support_073.json`
- `d5_074_r1_support.json`
- `d5_074_r2_support.json`
- `d5_075_bridge_support.json`
- `d5_075_realization_support.json`

The most important current canonical evidence files are:

- `d5_077_compact_interval_summary.json`
- `d5_081_regular_union_endpoint_table.csv`
