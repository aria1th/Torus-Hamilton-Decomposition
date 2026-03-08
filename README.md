# Hamilton decompositions of the directed 3-torus

This bundle contains the editorial-revision manuscript and supporting
information for:

*Hamilton decompositions of the directed 3-torus `D(m)`: explicit constructions
for all `m >= 3`* by Sanghyun Park.

## Context

The problem studied here is the same directed `3`-torus decomposition problem
highlighted in Donald Knuth's note *Claude's Cycles* (dated February 28, 2026;
revised March 6, 2026):

https://www-cs-faculty.stanford.edu/~knuth/papers/claude-cycles.pdf

Knuth's note frames the question of decomposing the arcs of the digraph on
`(Z/mZ)^3` into three directed Hamilton cycles, discusses an odd-`m`
construction found in AI-assisted exploration, and records the state of the
even case during that period. The manuscript in this bundle gives a full
mathematical treatment for all `m >= 3`, including:

- explicit odd constructions;
- a parity obstruction for Kempe-from-canonical approaches in the even case;
- the Route E construction for even `m >= 6`;
- a separate finite witness for `m = 4`.

## Main files

- `d3torus_complete_m_ge_3_editorial_revision.pdf` - main manuscript.
- `d3torus_complete_m_ge_3_editorial_revision_appendices_upload.pdf` - appendix
  / supplementary PDF.
- `anc/` - verification scripts and the `m = 4` witness bundle referenced by
  the manuscript.
- `SuppInfo_d3torus_complete_m_ge_3.zip` - packaged supporting-information
  archive.

## Supporting information

The files in `anc/` are verification aids only. They are not part of the
formal proofs in the manuscript.

Typical use:

```bash
cd anc
python run_even_artifact_suite.py
```

## Citation and license

Citation metadata is provided in `CITATION.cff`. The repository is released
under the MIT License; see `LICENSE`.
