# v6 revision notes

Base used: `d3torus_complete_m_ge_3_editorial_revision_v5.tex`

Decision: **revise, not stand**.

Why:
- Two independent referee reports identify the same two confidence bottlenecks: the omitted arithmetic in Appendix B and the compressed splice closure in Proposition 13.
- Both reports remain positive on the theorem and overall architecture, so the right move is targeted expansion of the written proof rather than another broad refactor.

## Changes applied in v6

1. **Introduction / proof-vs-verification clarification**
   - Added an explicit paragraph near the main theorem stating that Appendices B--C are part of the written proof, while the artifact bundle is only an independent audit.

2. **Odd case readability**
   - Added a short worked derivation in the proof of the odd-case theorem showing how the displayed formula for `F_0` comes from one low-layer deviation per `m`-step return.

3. **Appendix B completeness**
   - Expanded the previously compressed derivations by adding explicit low-layer trace tables for:
     - color 2, Case I;
     - color 0, Case II;
     - color 2, Case II.
   - These tables now mirror the already-present color-0 / Case-I table and make the omitted cases explicit in the paper itself.

4. **Proposition 13 transparency**
   - Added a representative worked splice derivation for the hardest row: color 0, Case II.
   - The proof now shows how the generic rule and the exceptional terminal images produce the displayed family-blocks and the splice permutation in both congruence subclasses `m ≡ 10 (mod 12)` and `m ≡ 4 (mod 12)`.

5. **Supplement synchronization**
   - Updated ancillary documentation to remove stale wording such as `Definition 3` and `clean proof note`.
   - The scripts now refer generically to the current manuscript / Route E definition, which is more version-stable.

## Verification performed after editing

- Compiled the revised source successfully with `pdflatex` run twice.
- Rendered and visually checked the main changed pages, especially:
  - page 7 (odd-case worked derivation),
  - pages 30--31 (new Appendix B trace tables),
  - pages 42--43 (expanded Proposition 13 proof).
- Reran the ancillary artifact suite after the documentation update; all six stages passed.

## Deliverables

- `d3torus_complete_m_ge_3_editorial_revision_v6.tex`
- `d3torus_complete_m_ge_3_editorial_revision_v6.pdf`
- `anc_v3.zip`
