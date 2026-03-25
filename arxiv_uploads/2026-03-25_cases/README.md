# arXiv Upload Prep Folders

Prepared on `2026-03-25`.

This directory collects upload-ready source folders for three current cases:

- `d3_review_candidates/`
- `d4_final/`
- `composite_final/`

## Intent

- `d3_review_candidates/` keeps the late D3 revisions side by side, but the
  current chosen D3 arXiv source is now the `v8_d3_only/` bundle.
- `d4_final/` is the current standalone D4 upload candidate.
- `composite_final/` is the current standalone composite-dimension upload
  candidate.

## Current recommendation

- The current main TeX document for the **pure D3 arXiv upload** is
  `d3_review_candidates/v8_d3_only/d3torus_complete_m_ge_3_odometer_revision_v8_rewrite.tex`.
- The enclosing upload-ready folder for that source is
  `d3_review_candidates/v8_d3_only/`.
- If the target is a **joint D3+D4 paper**, start from
  `d3_review_candidates/v9_with_d4_patched/`.
- `d3_review_candidates/v10_with_d5_supplement/` is the broadest archival
  version, but it includes an odd-D5 supplement and is therefore less focused
  for a D3-only or D3+D4 arXiv submission.
- For the D4-only upload, use `d4_final/`.
- For the composite-dimension upload, use `composite_final/`.

## Verification status

The chosen top-level sources were recompiled in draft mode before packaging.
The D3 folders also include the ancillary files referenced in the appendices,
including `m4_cycle_lists.txt`, which had to be restored from the earlier
`Round2/stage5/anc_v3.zip` archive because it is no longer present in the live
`anc/` directory.
