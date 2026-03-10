# D5-DYNAMIC-COLLAPSE-CORE-001

Artifact bundle for the postmortem analysis of the stable joined-quotient d=5 field.

Contents:
- `summary.md`: executor-facing report and branch recommendation.
- `data/analysis_summary.json`: full deterministic analysis output.
- `data/return_law_summary.json`: exact verification of the stable-field first-return law.
- `data/return_automaton.json`: the extracted `kick-kick-freeze` automaton.
- `data/minimal_collapse_core.json`: compact core-motif summary.
- `data/phase_collision_table.json`: state-level hidden-phase collision data on the representative-color return.
- `data/candidate_refinement.json`: one-bit refinement proposal for the next search.
- `data/canonical_background_path.json`: canonical `m=7` background-path motif chain.
- `data/input_best_stable_field.json`: copied input field analyzed here.
- `logs/analysis.log`: stdout/stderr from the analysis run.
- `scripts/`: exact code used for the analysis.

Reproduce:

```bash
python scripts/torus_nd_d5_dynamic_collapse_core_analysis.py \
  --field-json artifacts/d5_join_quotient_001/data/best_stable_field.json \
  --m-list 5,7,9,11,13 \
  --out-dir artifacts/d5_dynamic_collapse_core_001/data \
  --no-rich
```
