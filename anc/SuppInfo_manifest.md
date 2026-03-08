# Supporting Information Manifest

This directory is intended for submission as the supporting-information bundle for
`d3torus_complete_m_ge_3_editorial_revision.tex`.

## Contents

- `route_e_even.py`: main deterministic verifier for the even-case Route E construction.
- `routee_return_formula_tables_check.py`: checks the partition sets, low-layer words, and displayed return-map formulas.
- `routee_first_return_check.py`: checks the appendix first-return formulas against the displayed return maps.
- `m4_witness.json`: machine-readable finite witness for the case `m = 4`.
- `verify_m4_witness.py`: checks the `m = 4` witness against the printed direction table.
- `run_even_artifact_suite.py`: convenience runner for the full verification bundle.
- `requirements-artifacts.txt`: minimal dependency note.
- `ARTIFACTS_README_evenbundle_editorial_revision.md`: fuller technical README for the bundle.

## Submission note

These files are supporting information only. They are verification aids for the
construction described in Appendix E of the manuscript and are not part of the
formal proofs.

## Suggested archive name

`SuppInfo_d3torus_complete_m_ge_3.zip`
