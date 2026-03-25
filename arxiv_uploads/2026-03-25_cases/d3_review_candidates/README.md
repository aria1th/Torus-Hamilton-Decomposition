# D3 Review Candidates

This folder records the late D3-facing arXiv candidates.
The current chosen D3 arXiv source is the `v8_d3_only` main TeX document.

Each subdirectory is intended to be upload-ready on its own:

- `v8_d3_only/`
- `v9_with_d4/`
- `v9_with_d4_patched/`
- `v10_with_d5_supplement/`

Every candidate includes the same ancillary `anc/` bundle used by the D3 paper:

- `route_e_even.py`
- `routee_return_formula_tables_check.py`
- `routee_first_return_check.py`
- `routee_large_m_certificate.py`
- `m4_witness.json`
- `verify_m4_witness.py`
- `m4_cycle_lists.txt`
- `run_even_artifact_suite.py`
- `requirements-artifacts.txt`
- the supporting-information READMEs

## Candidate notes

### `v8_d3_only`

- Source:
  `arxiv_uploads/2026-03-25_cases/d3_review_candidates/v8_d3_only/d3torus_complete_m_ge_3_odometer_revision_v8_rewrite.tex`
- Scope: D3 only
- Strength: cleanest standalone D3 manuscript
- Best use: current dedicated D3 arXiv submission

### `v9_with_d4`

- Source: `tex/d3torus_complete_m_ge_3_odometer_revision_v9_with_d4.tex`
- Scope: joint D3 + D4 manuscript
- Status: superseded by the patched variant below

### `v9_with_d4_patched`

- Source: `tex/d3torus_complete_m_ge_3_odometer_revision_v9_with_d4_patched.tex`
- Scope: joint D3 + D4 manuscript
- Difference from `v9_with_d4`: only a small textual cleanup and reordered lane
  description in one Case-II discussion; mathematically the same paper
- Best use: joint D3 + D4 arXiv submission

### `v10_with_d5_supplement`

- Source: `RoundY/tex/d3torus_complete_m_ge_3_odometer_revision_v10_with_d5_supplement.tex`
- Scope: D3 + D4 manuscript plus an odd-D5 supplementary section
- Strength: most up-to-date superset
- Weakness: less focused if the submission target is strictly D3 or D3+D4

## Recommendation

- Current chosen D3 arXiv source:
  `v8_d3_only/d3torus_complete_m_ge_3_odometer_revision_v8_rewrite.tex`

Use:

- `v8_d3_only/` if the target paper is really about `d=3`;
- `v9_with_d4_patched/` if the target paper is the combined `d=3,d=4` story;
- `v10_with_d5_supplement/` only if the odd-D5 supplement is intentionally part
  of the submission.
