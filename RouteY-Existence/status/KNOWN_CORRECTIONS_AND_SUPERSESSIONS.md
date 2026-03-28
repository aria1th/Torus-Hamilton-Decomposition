# KNOWN CORRECTIONS AND SUPERSESSIONS (2026-03-28)

이 문서는 현재 bundle에서 **무엇이 기준 note인지**,
그리고 **어떤 기대나 옛 문구를 그대로 믿으면 안 되는지**를 모아 둔 ledger입니다.

## 1. Local dependency-clean replacements

다음 옛 note들은 보존되어 있지만, current baseline은 오른쪽 replacement입니다.

- `d5_hinge_corner_proof_upgrade_2026-03-26.md`
  -> `d5_hinge_corner_dependency_free_proof_2026-03-27.md`

- `d5_bulk_side_top_proof_upgrade_2026-03-26.md`
  -> `d5_bulk_side_top_dependency_free_closure_2026-03-27.md`

- `d5_c0_compact_return_proof_upgrade_2026-03-26.md`
  -> `d5_c0_compact_return_dependency_free_reproof_2026-03-27.md`

- March 26 actual-entry / corrected-visibility exact-supported wording
  -> `d5_actual_entry_visibility_dependency_free_upgrade_2026-03-27.md`

- old promoted-collar support / corner packet
  -> `d5_promoted_control_dependency_free_reproof_2026-03-27.md`

## 2. Arithmetic status notes: what they mean now

- `d5_active_arithmetic_status_after_t1_and_genmod5eq2_2026-03-27.md`
  는 더 이상 current full status가 아닙니다.

- `d5_active_arithmetic_status_after_generic_full_theorem_2026-03-27.md`
  는 **active arithmetic status**로는 여전히 유효합니다.

다만 current arithmetic main flow 전체는 이제 아래 chain으로 읽는 것이 맞습니다.

- `d5_generic_late_base_splice_7split_theorem_2026-03-27.md`
- `d5_generic_late_base_splice_odometer_reduction_2026-03-27.md`
- `d5_generic_late_defect_three_block_theorem_2026-03-27.md`
- `d5_generic_late_reduced_base_machine_15r3_15r9_theorem_2026-03-27.md`
- `d5_generic_late_split_componentwise_conjugacy_and_global_nogo_2026-03-28.md`
- `d5_generic_late_hidden_plus5_clock_and_seam_surgery_draft_2026-03-28.md`

## 3. Superseded exploratory notes

다음 note들은 theorem note 또는 synthesis note로 대체된 exploratory records입니다.

- `01_notes/90_exploratory_superseded/d5_generic_late_full_cycle_candidate_2026-03-27.md`
  -> theorem note:
     `01_notes/d5_generic_late_reduced_arithmetic_machine_and_full_cycle_theorem_2026-03-27.md`

- `01_notes/90_exploratory_superseded/d5_generic_late_defect_three_block_formula_candidate_2026-03-27.md`
  -> theorem note:
     `01_notes/d5_generic_late_defect_three_block_theorem_2026-03-27.md`

- `02_scripts_and_reports/90_exploratory_superseded/d5_generic_late_defect_three_block_scan_*`
  -> theorem check:
     `02_scripts_and_reports/d5_generic_late_defect_three_block_theorem_check_*`

## 4. Base splice reduction: what stayed valid

- `d5_base_splice_mod3_reduction_note_2026-03-27.md`
  는 **abstract reduction theorem**으로서 여전히 유효합니다.

- 다만 그 note에서 sampled generic-late data가 암시하던 universal drift reading은
  now replaced by
  `d5_generic_late_base_splice_7split_theorem_2026-03-27.md`.

즉 generic-late base splice는

- `7∤M`에서는 reduced machine으로 내려가고,
- `7|M`에서는 structural obstruction이 있습니다.

## 5. Scope correction for the lower-strip claim

다음 문구는 현재 기준으로 잘못입니다.

```text
R_t = R_* = R_wd1 on all of A_m^c.
```

current packet이 정확히 보이는 것은 lower strip

```text
0 <= d <= m-3
```

입니다.

반례와 corrected scope:

- `02_scripts_and_reports/d5_lower_strip_localization_scope_counterexample_2026-03-27.txt`
- `01_notes/d5_bulk_side_top_dependency_free_closure_2026-03-27.md`

## 6. The global-odometer expectation is no longer the current conjecture

다음 기대는 현재 bundle 기준으로는 유지하지 않는 것이 맞습니다.

```text
The full reduced base map g_t should be globally conjugate to x -> x+c on Z_M.
```

split good branch의 prime counterexamples 때문에, 이것은 universal theorem candidate가 아닙니다.

대표 예:

- `m=69`, `M=23`, cycle type `[17,3,3]`
- `m=123`, `M=41`, cycle type `[31,5,5]`

따라서 current viewpoint는

- one global odometer
가 아니라
- explicit odometer pieces + finite seam surgery

입니다.

## 7. Reference input versus theorem note

`resonant_common_plus5_odometer_carrier_coordinate_and_explicit_splice_placement_note_2026-03-27.md`
는 현재 bundle에서 **reference input / structural hint**로 두는 것이 맞습니다.

이 note는 `+5` clock와 carrier/splice localization insight를 제공했지만,
current theorem-order chain은 그것을 직접 인용하지 않고도

- odometer reduction note
- defect three-block theorem
- explicit reduced base-machine theorem

으로 다시 서 있습니다.

## 8. Documentation caveat

split first-special-hit result는 현재 bundle 안에 standalone precursor note로 따로 분리되어 있지 않습니다.
현재 보존된 형태는

- `01_notes/d5_generic_late_split_componentwise_conjugacy_and_global_nogo_2026-03-28.md`
- `02_scripts_and_reports/d5_generic_late_split_componentwise_conjugacy_and_global_nogo_check_report_2026-03-28.txt`

입니다.

즉 current bundle은 이 result를 “componentwise packaging + evidence” 형태로 보존합니다.
