# v7 revision notes

Base used: `d3torus_complete_m_ge_3_editorial_revision_v6.tex`

Decision: **revise again, but only surgically**.

Why:
- The three latest referee reports are all positive on correctness and publishability, but they still converge on a small set of confidence-lowering issues in the written text.
- None of the reports asks for new mathematics; the remaining requests are bibliographic positioning, one formalization of the layer-0 partition, one additional bridge through the hardest Case II color-0 material, and slightly sharper proof-versus-verification language.

## Changes applied in v7

1. **Literature framing corrected and sharpened**
   - Added Keating's two-factor 2-ply Hamiltonicity result to the introduction.
   - Rewrote the paragraph around Bogdanowicz and Darijani--Miraftab--Morris so that:
     - Bogdanowicz is positioned as decomposition into equal-length directed cycles / identification under explicit hypotheses;
     - Darijani--Miraftab--Morris is positioned explicitly as an arc-disjoint Hamilton-path result, not a Hamilton-decomposition result.

2. **Layer-0 partition promoted from remark to lemma**
   - Replaced the previous layer-0 partition remark with a formal lemma and short proof.
   - The proof checks the only possible affine-line intersections and explains why the endpoint conventions and coordinate ranges exclude overlaps.

3. **Even-case roadmap strengthened**
   - Added an explicit proof-dependency chain near the start of the Route E framework section:
     `Definition 5 -> transducer / Appendix B -> bulk/defect normal form -> first-return formulas -> Proposition 13 -> corollaries -> Theorem 5`.
   - This makes the main text / appendix split more visible to a referee on first pass.

4. **Odd-case step (4) clarified**
   - Added an explicit displayed statement in the proof of the five-swap theorem that the outgoing arcs on `P_1` remain canonical after steps (1)--(3).
   - This removes one of the quick “trust me” transitions noted by a referee.

5. **Case II color-0 bridge example added in main text**
   - Added a short `m=10` worked example for color 0 in Case II.
   - The example explains the residue-4 strand picture and shows how the finite splice permutation converts those strands into one cycle.

6. **Proof / computation boundary restated in Appendix E**
   - Added the explicit sentence that all assertions used in the proof are proved in the written text, while the scripts only re-check displayed formulas and the finite witness.

7. **Discussion tone slightly softened**
   - Adjusted the higher-dimensional discussion so it no longer suggests a clean direct extension of the current mechanism beyond the three-factor setting.

## Checks performed after editing

Because no TeX engine is installed in this container, I could not render a fresh PDF from the revised source.
I therefore performed source-level checks instead:

- balanced-brace check passed;
- `\label{}` keys are unique;
- every `\cite{}` key has a matching `ibitem{}`;
- begin/end counts match for the main theorem-like environments used in the edited regions.

## Deliverables

- `d3torus_complete_m_ge_3_editorial_revision_v7.tex`
- `REVISION_NOTES_v7.md`
- `d3torus_v6_to_v7.patch`
