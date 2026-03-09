# Discovery and provenance traces

This directory contains selected traces from the exploratory stage of the
directed 3-torus project. It is intentionally separate from `../anc/`, which
holds the referee-facing verification aids for claims stated in the paper.

## Scope

The included files are copied from the parent workspace artifact bundle
`artifacts/torus_20260305/` and preserve:

- deterministic accepted-swap traces from the odd-case alternating-cycle
  search;
- hybrid-solver solution snapshots for representative small instances;
- benchmark summaries for the exploratory hybrid solver;
- the manifest, builder script, and local solver source used to assemble those
  records.

## Interpretation

These files are discovery/provenance records, not proof artifacts. They are
useful for documenting how candidate patterns were explored and stabilized
before the final closed-form arguments were written down.

The mathematical claims in the manuscript remain supported by the written
proofs and by the verification bundle in `../anc/`.

Within `torus_20260305/`, the copied `torus_swap_search.py` keeps the trace
builder closer to self-contained for archival reruns.

## Deliberate exclusions

This paper repository does not include raw chat transcripts, prompt logs, or
mock-referee/editorial AI outputs by default. Those materials are process
history rather than scientific evidence, and keeping them out of the core paper
bundle reduces confusion about what is part of the proof record.

If a later archive needs fuller process provenance, add it under a separate
subdirectory such as `traces/editorial/` with explicit disclaimers.
