# Referee Report — v2 Revision

**Paper:** *Hamilton decompositions of the directed 3-torus D(m): explicit constructions for all m ≥ 3*
**Author:** Sanghyun Park (Yonsei University)
**Manuscript version:** `d3torus_complete_m_ge_3_editorial_revision_reworked_forced_repair_v2.tex` (8 March 2026, 3091 lines, ~132 KB)

---

## Recommendation

| Criterion | Score (1–10) | Comment |
|---|---|---|
| **Correctness** | 8 | The logical chain is complete and carefully modularized. Each return map is derived from an explicit partition table. Minor: occasional forward-referenced notation before the notation table is introduced (e.g. use of *bulk* before Definition 5). |
| **Significance / Novelty** | 7 | Resolves a nontrivial combinatorial question for a natural family of Cayley digraphs. The sign-product parity barrier is attractive. The Route E deductive-surgery paradigm is novel, though the problem is narrow. |
| **Clarity / Exposition** | 6 | The v2 revision is vastly improved over v1 in terms of flow and readability. The notation table (Table 1), the layer-by-layer summary table inside Definition 4, Figure 1, and Example 3.8 are welcome additions. However, the overall length is still a concern (~48 journal pages); the appendix makes up over half the paper and consists mostly of orbit-trace bookkeeping. |
| **Technical depth** | 8 | The three-level reduction strategy (color map → return map on P₀ → first-return map on a 1D transversal → splice permutation) is elegant and well-explained. The primary-geometry/obstruction/no-go/repair narrative is convincing. |
| **Presentation quality** | 7 | LaTeX is clean, references are complete, and the supplementary scripts add confidence. A few minor issues noted below. |
| **Overall** | **7** | |

### Verdict: **Accept after minor revision** (Weak Accept)

---

## Summary

The paper proves that the directed 3-torus D(m) = Cay((ℤ_m)³, {e₁, e₂, e₃}) admits a Hamilton decomposition into three arc-disjoint Hamilton cycles for all m ≥ 3. Three constructions cover the full parameter range:

1. **Odd m:** Five Kempe swaps from the canonical coloring produce an affine skew-product return map; elementary number theory shows each color class is a single m²-cycle.
2. **Even m ≥ 6 (Route E):** A parity barrier rules out all Kempe-from-canonical approaches. An explicit direction assignment on the three lowest layers, with canonical behavior on all higher layers, yields return maps whose Hamiltonicity is proved by a systematic defect-itinerary + splice argument.
3. **m = 4:** A finite witness (explicit direction table + machine-checked orbits).

The deductive-surgery narrative for the even case is the paper's main technical contribution: primary geometry → residue-3 obstruction in color 1 → no-go for boundary-only repair → genuine bulk repair via the Case II affine family → finite splice closure.

---

## Strengths

1. **Complete resolution of a natural problem.** The theorem statement is clean, the scope is exactly delimited, and all three cases are treated explicitly.

2. **The sign-product invariant (Theorem 2.3) and its corollary** provide a conceptually satisfying explanation for *why* the even and odd cases are fundamentally different. This result is self-contained and potentially applicable beyond the present setting.

3. **Modular proof architecture.** The reduction chain `Hamiltonicity on V` → `single cycle of Fc/Rc on P₀` → `single cycle of Tc on a transversal` → `splice permutation on family-blocks` is clean and well-documented. Lemma 3.3 (first-return counting) and Lemma 3.9 (splice graph lemma) are good, reusable tools.

4. **Improved readability in v2.** The notation table (Table 1), layer-by-layer overview in Definition 4, reading guide (Remark 3.14), and the worked Example 3.8 (m = 6, color 2) all substantially improve accessibility. The deductive-surgery narrative (Propositions 3.4, 3.5, Example 3.6) makes the conceptual architecture of the even proof much clearer than in v1.

5. **Supplementary verification scripts** add independent confidence in the return-map formulas and first-return data.

---

## Weaknesses and Suggestions

### Major

1. **Length / balance.** The manuscript is ~3091 lines (≈48 pp. compiled). The main text (§1–§6) is ≈26 pp.; the four appendices (A–D) add ≈22 pp. The appendices consist largely of piecewise case analysis (orbit traces, derivation tables, and itinerary bookkeeping). While the mathematics is correct, the sheer mass of routine case-checking weakens the expository impact.

   **Suggestion:** Consider whether Appendix B (derivation tables, Tables 3–6) could be compressed. Each table repeats the same arithmetic-trace schema; a single representative table plus a statement that "the same method applies to all six tables" would save ≈4 pages without loss of rigor.

2. **The orbit traces in the color-1 and color-0 proofs (Appendix C, §§C.2–C.3)** are thorough but repetitive. The generic-even and generic-odd sub-cases follow identical patterns (B → A → O → return), and the reader can anticipate the arithmetic once the first two are seen.

   **Suggestion:** Group the generic sub-cases into a single parametric statement ("for $x \in \{4, 6, \ldots, m-8\}$ and for $x \in \{3, 5, \ldots, m-7\}$, the orbit follows the same pattern with the same return time"), then work out only the boundary sub-cases in full. This would reduce Appendix C by ≈3–4 pages.

### Minor

3. **Notation: "bulk" vs. "generic."** Definition 5 introduces "stall" but the counterpart — the *non*-stall step — is variously called "bulk" (line 824, the `\bulk` command), "generic" (Lemma 3.6, Lemma 3.7), and later simply "G" in the orbit traces. A sentence early in §3.2 explicitly equating these three terms would remove any ambiguity.

4. **Forward reference in the abstract.** Line 53 mentions "the extra affine defect family performs genuine bulk repair" — this is motivating language, but the notion of "affine defect family" is not defined until Definition 4. Consider softening to "an additional algebraic correction."

5. **Table 2 vs. Figure 1.** Table 2 lists the same affine defect support that Figure 1 illustrates. Apart from the visual angle, the information is redundant. A cross-reference sentence ("see Table 2 for the precise equations; Figure 1 for a schematic visualization") would tie them together.

6. **Return-time-sum verification.** The sums $\sum \rho_c(x) = m^2$ are stated in Corollaries 6.3, 6.5, 6.7, 6.9 with displayed arithmetic but no intermediate steps. These are routine but a brief parenthetical ("expanding and simplifying") would be sufficient.

7. **Bibliographic nit.** Reference [11] (Darijani–Miraftab–Morris) lists the journal issue as "25 (2025), no. 2, P2.10." If the paper is now published, confirm the volume / page numbering; if still forthcoming, mark it as such.

8. **Discussion section.** The discussion raises two natural open problems (Route-E-specific critical-lane theorem; higher-dimensional tori), but could also briefly note:
   - Whether the sign-product invariant generalizes to products of more than three directed cycles.
   - The gap between the present *existence* result and any *counting* result for Hamilton decompositions of D(m).

---

## Detailed Comments / Errata

| Line(s) | Issue |
|---|---|
| 29 | `\bulk` macro defined with comment "see §app:routeE-cycle for definition," but the first *use* is line 824. Consider adding (or moving) a brief remark at first use. |
| 97 | Long sentence (6 clauses). Consider splitting after "…three residue-3 strands;" for readability. |
| 148 | Missing period at end of sentence: "…(Section~\ref{sec:affine})" → add `.` |
| 551 | "This isolates the even design problem:" — semicolon would be clearer after "even $m$". |
| 669 | "The number of stalls per orbit is bounded independently of $m$." — this claim deserves a forward reference to where the bound is verified (the orbit traces in Appendix C). |
| 1064 | "these are the arithmetic family-blocks later spliced in Proposition~\ref{prop:routeE-splice}" — long forward reference; consider a brief parenthetical ("(see Proposition X.Y for the formal statement)"). |
| 3076 | Confirm that [11] is now published and the page/article numbering is final. |

---

## Questions for the Author

1. Can the Route E construction be made "canonical" in some algebraic sense, or does its design genuinely depend on ad-hoc choices? The splice permutations are always single cycles of small length (2, 3, or 4) — is there a structural reason for this?

2. The m ≡ 4 (mod 6) obstruction lives in color 1 only. Is there a conceptual explanation (beyond the mod-6 arithmetic) for why color 1 is the "hardest" color?

3. Do the verification scripts cover any values beyond m = 60? Even a few spot checks at m = 100 or m = 120 would further strengthen confidence.

---

## Conclusion

The paper resolves a complete, well-defined combinatorial problem with a carefully structured proof. The sign-product barrier is elegant, and the four-stage even-case narrative (primary geometry → obstruction → no-go → repair) is the right way to present the material. The v2 revision has addressed most of the readability concerns from the first round. The remaining issues are primarily about **length and compression** of the appendix case-work. I recommend **accept after minor revision**, contingent on tightening the appendices and addressing the minor points above.
