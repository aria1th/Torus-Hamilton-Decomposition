# D5 033 Explicit Trigger Family

This note promotes the one `033` fact that the later D5 theorem chain imports
directly.

It is not a replacement for the full `033` artifact. It isolates the exact
hole-family formula needed by `062` and the final `083` proof.

## Theorem

For the unresolved best-seed channel

`R1 -> H_L1`

in odd `d=5`, the target hole family is exactly

`H_L1 = {(q,w,u,layer) = (m-1,m-1,u,2) : u != 2}`.

Equivalently:

- the target layer is `2`,
- the target current coordinates satisfy `q = m-1` and `w = m-1`,
- the only excluded fiber is `u = 2`.

## Why this matters

This is the precise trigger set used later in:

- `theorem/d5_first_exit_target_proof_062.md`
- `theorem/d5_083_final_theorem_proof.md`

In the current proof chain, it is the only direct theorem-level import from
the broader `033` defect-splice analysis.

## Provenance

This note extracts the theorem content already used in:

- `artifacts/d5_defect_splice_transducer_033/README.md`
- `theorem/d5_phase_corner_manuscript_draft_065.md`
- `theorem/d5_theorem_manuscript_section_066.md`

It should be cited instead of the raw artifact README when only the trigger
family formula is needed.
