# Supporting-information files (editorial revision)

These files accompany the manuscript `d3torus_complete_m_ge_3_odometer_revision_v8_rewrite.tex` as supporting information. They keep the executable checks focused on the places where a referee or editor would most naturally want to verify the construction.

For submission, upload the `anc/` bundle as a LaTeX supplementary file. The companion manifest `SuppInfo_manifest.md` gives the short journal-facing description of the bundle.

## Included files

- `route_e_even.py` - main direct verifier for the Route E construction.
- `routee_return_formula_tables_check.py` - checks the partition sets, low-layer words, and displayed return-map formulas.
- `routee_first_return_check.py` - checks the appendix first-return maps and return-time formulas.
- `routee_large_m_certificate.py` - proof-backed O(1) certificate path for very large even `m`.
- `m4_witness.json` - machine-readable finite witness for the `m=4` decomposition.
- `verify_m4_witness.py` - checks the `m=4` witness against the direction table and extracted cycles.
- `run_even_artifact_suite.py` - convenience runner for the full suite.
- `requirements-artifacts.txt` - minimal dependency note.

## Recommended commands

### Full suite (default)

```bash
python run_even_artifact_suite.py
```

### Quick sweep

```bash
python run_even_artifact_suite.py --theorem-max 500 --tables-max 24 --first-return-max 40 --p0-max 0 --full-max 0
```

### Main direct verifier only

```bash
python route_e_even.py 500 --mode theorem
python route_e_even.py 60 --mode p0-check
python route_e_even.py 30 --mode full-check
```

### Large-`m` proof-backed certificates

```bash
python routee_large_m_certificate.py --m-list 1000,1000000,1000000000
```

### Boundary case `m=4`

```bash
python verify_m4_witness.py
```

## Scope

These artifacts are verification aids only. They are not part of the proofs.

The bundle separates two roles:

- Route E scripts audit the technically delicate even case `m >= 6`.
- `routee_large_m_certificate.py` is the post-proof large-`m` path: it evaluates the splice normal forms and return-time identities directly, so the cost per tested `m` is constant.
- The `m=4` files provide a compact machine-readable finite witness, so the paper no longer needs to print three full 64-cycles inline.
