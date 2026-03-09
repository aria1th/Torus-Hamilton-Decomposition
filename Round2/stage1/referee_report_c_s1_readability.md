# Referee Report C — Readability, Flow, and Word Usage

**Manuscript:** *Hamilton decompositions of the directed 3-torus D(m): explicit constructions for all m ≥ 3*

**Focus:** prose readability, sentence-level flow, word choice, naturalness, and surface-level editorial polish.

---

## Overall Assessment

The paper is **well-organized and clearly structured**, with a genuine mathematical narrative that progresses logically from the parity obstruction through the odd-case Kempe construction and into the even-case Route E design. The writing is above average for combinatorics papers of this density. That said, a careful line-level pass reveals recurring patterns — heavy nominalizations, overlong sentences, and a few vocabulary habits — that collectively slow the reader. The suggestions below are grouped thematically.

**Verdict:** Minor revision on readability grounds. None of the items below affect mathematical correctness; all are prose-level improvements that would bring the text closer to journal-ready quality.

---

## 1. Sentence Length and Complexity

Several sentences in the introduction and the even-case narrative carry too many subordinate clauses for comfortable reading. These should be split or restructured.

| Location | Current phrasing (paraphrased) | Issue |
|----------|-------------------------------|-------|
| Abstract, lines 47–53 | Six-clause sentence from "For even $m$…" through "…handled separately." | Packs five distinct ideas (sign-product, parity obstruction, Route E, strand failure, affine defect, splice, boundary case) into one paragraph-length sentence. |
| §1 Intro, lines 76–78 | "These results concern… subsequently treated by… As $D(m)$ is a Cayley digraph…" | Three independent ideas in one sentence joined by semicolons. |
| §4 framework, lines 658–659 | "Conceptually, the argument will be read in four steps: a primary geometry…, a precise obstruction…, a short no-go argument…, and the actual repaired Route E construction followed by a finite splice." | The colon-introduced list contains four list items, where the last itself has a subordinate clause. Better as a displayed list. |

**Recommendation:** Break sentences at natural pause points. A good rule of thumb for this density of mathematical writing: no sentence should contain more than three quantifiers or conditional clauses.

---

## 2. Nominalization and Passive Voice

The paper occasionally defaults to heavy nominalizations where a verb-based construction would read more naturally.

| Current | Suggested |
|---------|-----------|
| "the derivation of the piecewise formulas" | "deriving the piecewise formulas" |
| "the resulting maps are permutations, and hence form a coloring, is proved later" | "the resulting maps are proved to be permutations — and hence a valid coloring — in …" |
| "the orbit displays below" | "the orbit traces below" (or "orbit diagrams") |
| "the verification as a coloring is proved later" (line 156) | "that this assignment is a valid coloring is proved in …" |
| "A direction assignment on $D(m)$ is a triple $\delta = (d_0,d_1,d_2)$ with $d_c : V \to \{0,1,2\}$…" | Consider rephrasing as "A direction assignment assigns to each vertex…" for a gentler entry. |

---

## 3. Repeated Vocabulary / Verbal Tics

A few words and phrases recur with notably high frequency, reducing stylistic variety.

| Word/Phrase | Approx. occurrences | Suggestion |
|-------------|---------------------|------------|
| "legitimate" / "valid" | ~20 | Use "valid" consistently for colorings; drop "legitimate" entirely. |
| "displayed" (as in "the displayed formula") | ~25 | Alternate with "the formula above," "these expressions," "the rule in (∗)." |
| "hence" at sentence start | ~18 | Alternate with "so," "therefore," "it follows that," or restructure. |
| "gives" / "giving" | ~30 | Alternate with "yields," "produces," "results in." |
| "exactly" (in non-mathematical usage) | ~15 | Often redundant; remove when the exactness is already clear from context. |
| "so the claim follows" | ~5 endings | Fine once or twice, but monotonous as a proof-ending refrain. Vary with "as required," "which completes the proof," or simply end the calculation. |

---

## 4. Connective Tissue and Transitions

### 4a. Section openings

Several sections open with "We now turn to…" or "We now carry out…" These are functional but bland. Consider:
- §4 (line 517): "We now turn to the even case" → "The even case requires a different strategy."
- §4.2 (line 1280): "We now carry out the color-2 computation in full" → "We work out the color-2 return map in full, as the cleanest representative case."

### 4b. Paragraph-initial variety

Many proof paragraphs begin with "The orbit is…" or "The orbit begins…" (at least 8 instances in §4.2 and the appendices). Where possible, lead with the lane value: "Starting from lane $x = 3$, the orbit…"

### 4c. Forward references

The paper makes frequent forward references ("as we will see in Section X," "proved later in Theorem Y"). These are necessary for a paper of this length, but a few can be shortened:
- Line 155–156: "As we will see in Section 4, Route E will first be specified only as a direction assignment; its verification as a coloring is proved later from the bijectivity of its return maps via Lemma 7." → "Route E is first specified as a direction assignment; Lemma 7 later upgrades it to a coloring."

---

## 5. Technical Jargon and Definitions

### 5a. "Stall" terminology

The term "stall" (line 651) is introduced informally — "We call a step at which the return map departs from the uniform translation a *stall*" — and used extensively thereafter. This is a well-chosen metaphor but deserves a slightly more formal introduction, perhaps as a numbered definition or a clearly set-off sentence, since it becomes load-bearing vocabulary for the entire even-case argument.

### 5b. "Bulk" as an adjective

"Bulk branch," "bulk coordinates," "bulk move," "bulk displacement," "bulk repair" — the word "bulk" does a lot of work. Its meaning shifts subtly: sometimes it means "generic" (as in the generic branch of the return map), sometimes "interior" (as in genuine bulk repair vs. boundary corrections). Consider:
- Use **"generic"** when referring to the dominant branch of the return map.
- Reserve **"bulk"** for the contrast with "boundary" in the obstruction/repair narrative.

### 5c. "Arithmetic family-blocks"

This compound noun (line 746, etc.) is central but cumbersome. On first use, provide a brief gloss: "arithmetic family-blocks — maximal runs of consecutive lanes sharing the same defect itinerary — …" The current parenthetical is close but slightly buried.

---

## 6. Specific Word-Level Suggestions

| Line | Current | Suggested | Reason |
|------|---------|-----------|--------|
| 47 | "five Kempe swaps of the canonical arc-coloring produce the decomposition" | "five Kempe swaps from the canonical arc-coloring produce the decomposition" | preposition mismatch |
| 50 | "A natural primary low-layer geometry already closes colors 0 and 2" | "The natural primary geometry on the low layers already closes colors 0 and 2" | article + word order |
| 51 | "boundary-only corrections cannot repair this obstruction, so an additional affine defect family is forced" | "boundary-only corrections cannot repair this obstruction, so an additional affine defect family must be introduced" | "is forced" is slightly awkward in isolation |
| 82 | "sits at a natural boundary between" | "lies at a natural boundary between" | "sits" is colloquial |
| 95 | "The even argument is organized as a deductive surgery" | "The even argument proceeds as a deductive surgery" | "organized as" is slightly stiff |
| 130 | "is therefore a disjoint union of directed cycles" | "and therefore consists of disjoint directed cycles" | avoids the heavy noun phrase |
| 544 | "this isolates the even design problem" | "this clarifies the even-case design problem" | "isolates" is overloaded (already used technically) |
| 651 | "the number of stalls per orbit is bounded independently of $m$" | "each orbit encounters only boundedly many stalls" | more natural phrasing |
| 1250 | "show how the even proof should be read" | "show how the even proof is organized" | "should be read" is prescriptive |
| 1548 | "Route E is designed for $m \ge 6$" | "Route E applies for $m \ge 6$" | "designed" anthropomorphizes |

---

## 7. Abstract and Introduction Polish

### Abstract
The abstract is dense but effective. Two suggestions:
1. The phrase "explicit return-map formulas on a fixed plane show that each color class is Hamiltonian" could be more specific: "explicit return-map formulas on the plane $P_0 = \{S = 0\}$ show…"
2. "The repaired first-return maps are then closed by a finite splice argument" — the verb "closed" is ambiguous (could mean "proved to be single cycles" or "concluded"). Say "shown to be single cycles by a finite splice argument."

### Introduction
- Lines 86–92: The three-item roadmap is clear and effective. However, item (iii) ("a necessary case split") is at a different level of abstraction from items (i) and (ii), which describe specific mathematical tools. Consider: "a ​*case split forced by the parity invariant*: the odd and even cases require fundamentally different coloring strategies."
- Lines 93–95: These two sentences summarize the entire paper in very compressed form. They work, but the second sentence (line 94–95) is too long and could be split after "ruling out all Kempe-from-canonical approaches."

---

## 8. Proof Endings and Transitions

Many proofs end with a terse "the claim follows" or "this proves the stated formulas" without a brief backward glance. In a paper this long, a one-line summary at the end of major proofs helps the reader re-orient. For example:
- End of Theorem 3 proof (line 474): add "Thus all three return maps are single $m^2$-cycles, completing the Hamilton decomposition for odd $m$."
- End of Proposition 12 proof (line 1492): add "The seven cases exhaust all lanes, and the combined return times sum to $m^2$." (This is almost present but could be more explicit.)

---

## 9. Tables and Displays

- **Table 1** (line 105): compact and useful. No changes needed.
- **Table 2** (line 1043): excellent summary. The caption could be slightly more informative: "…for the three colors, derived from Lemmas 8 and 9" (giving the reader breadcrumbs back).
- **Derivation tables** (Tables 3–6 in the appendix): These are dense but serve their purpose. Consider adding a brief preamble sentence before each: "The following table traces the three-step word computation for each region of $P_0$."

---

## 10. Figure and Remark Quality

- **Figure 1** (line 1060): The three-panel schematic is well-conceived. The only issue is that the center panel uses $(x,y) = (i, i+k)$ while the text sometimes uses $(u,t)$. The caption acknowledges this, but a brief in-figure label like "working frame" would help.
- **Remark 4** (line 737): This is one of the strongest expository passages in the paper. It clearly explains the design logic. The only suggestion is to move the final sentence ("What changes at $m \equiv 4 \pmod{6}$…") to a new paragraph for visual separation, since it introduces a distinct point.

---

## 11. Discussion Section

The discussion (§6) is appropriately brief. Two minor notes:
1. "What remains open is whether this can be packaged as a clean Route E-specific critical-lane theorem…" — "packaged" is informal. Consider "formalized" or "stated."
2. The final question ("does Corollary 3 generalize to higher dimensions…") is a strong closing. No changes needed.

---

## Summary of Recommendations

1. **Split long sentences** — especially in the abstract and §1, §4 introductory paragraphs.
2. **Vary vocabulary** — reduce repetition of "displayed," "hence," "gives," "exactly."
3. **Sharpen transitions** — replace bland openers ("We now turn to…") with content-carrying transitions.
4. **Clarify "bulk" vs. "generic"** usage.
5. **Promote "stall" to a formal definition** or set-off introduction.
6. **Add brief proof summaries** at the end of the longest proofs.
7. **Polish the abstract** — two specific fixes above.

None of these items are structural or mathematical in nature. The paper's conceptual spine is strong (as Reports A and B note), and the mathematical content requires no revision. This report addresses only the surface-level prose polish needed for final journal publication.
