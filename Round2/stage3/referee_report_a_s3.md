**Recommendation:** **Accept after minor revision**
**Overall score:** **7.5/10**
**Referee confidence:** **medium-high**

**Score guide used here:**
9–10 = strong accept, 7–8 = accept/minor revision or weak accept, 5–6 = major revision, 3–4 = weak reject, 1–2 = strong reject.

### Referee report

I reviewed the current LaTeX source, compiled it successfully, and checked the supplied ancillary bundle. I also ran the full artifact suite in the archive; all six stages passed, including the (m=4) witness, Route E table/formula checks, first-return checks, theorem-mode checks through even (m=500), exact (P_0) checks through (m=60), and exact full-graph checks through (m=30). Separately, I brute-force checked the odd closed-form construction for odd (m\le 51), and in those tests each color class was a single Hamilton cycle. I did **not** manually rederive every appendix branch line by line, so my correctness score reflects strong computational support plus a coherent proof architecture, not a complete hand audit of every case distinction.

The paper proves a clean and natural theorem: the directed 3-torus
[
D(m)=\mathrm{Cay}((\mathbb Z_m)^3,{e_1,e_2,e_3})
]
admits a decomposition into three arc-disjoint directed Hamilton cycles for every (m\ge 3). The odd case is handled by a five-swap Kempe construction, the even case by the explicit Route E direction assignment together with return-map analysis, and (m=4) by a separate finite witness. This is a worthwhile result, and the paper now presents the proof in a much more intelligible way than a raw case split.

My overall judgment is that the manuscript is publishable, and the current version is close to final. The remaining issues are mostly about presentation, especially readability in the technically dense even case and the appendices.

### Strengths

The main mathematical strengths are clear. The result is nontrivial, explicit, and complete. The odd/even split is not artificial: the sign-product invariant gives a persuasive conceptual reason that the even case cannot come from Kempe swaps off the canonical coloring. That is the paper’s most memorable structural idea.

On the expository side, the paper is now organized around a genuine story rather than just a sequence of formulas. The introduction explains what the proof is trying to do. The early notation table reduces the cognitive load. In the even case, the route
design principle, framework, primary geometry, obstruction, boundary-only no-go, and forced repair are separated into recognizable stages. The worked (m=10) repair example is especially useful because it finally shows why the Case II affine family changes the interior dynamics rather than merely patching endpoints.

The verification appendix and ancillary bundle also improve auditability. The paper now states the role of the scripts clearly enough: they support the construction but are not part of the proof. That is the right balance.

### Readability and overall flow

This is the main place where I focused, and my view is positive but not unqualified.

The **main text now flows reasonably well** for a specialist reader. Sections 1–4 have a clear progression:

* problem and literature context,
* preliminaries and return-map mechanism,
* odd affine construction,
* even Route E strategy and its conceptual justification.

That is a good high-level structure. The paper is much easier to read once one sees that the even proof is meant to be a “deductive surgery” argument rather than a mysterious piecewise construction.

That said, the **appendix burden remains heavy**. A reader still has to shuttle between:

* Appendix A for the final return-map formulas,
* Appendix B for their derivation from the low-layer rule,
* Appendix C for first-return formulas and splice closure.

This is logically sound, but the reading experience is still somewhat fragmented. The main text explains *why* the construction should work; the appendices explain *exactly how* it works; but the transition between those two modes still takes effort.

The densest obstacle to readability is Appendix B. The large compressed tables do contain the needed information, but in their current form they are more auditable than readable. On paper, they are visually tight and hard to scan. I could follow them, but only slowly.

There is also a mild repetition issue. The conceptual narrative of “primary geometry / obstruction / no-go / repair / splice” appears in the introduction, Section 4, the main even-case theorem proof, the later remark, and the discussion. Repetition is useful in a difficult paper, but here it slightly over-occupies the exposition. A little trimming would improve flow.

Finally, the color-0 Case II structure still arrives late and feels more abrupt than the color-1 discussion. This is not a correctness issue, but it does leave the last difficult part less motivated than it could be.

### Requested revisions

These are minor.

1. **Improve appendix legibility**, especially the large derivation tables. Splitting some tables, rotating them, or formatting them less tightly would help a lot.

2. **Trim repeated roadmap prose** in Section 4, the proof of the main even theorem, and the discussion. The conceptual line is good; it does not need to be restated quite so many times.

3. **Add one brief roadmap paragraph before the hardest appendix material**, especially before the color-0 Case II analysis, indicating where the (m \bmod 12) split enters and what role it plays in the splice step.

4. **Ensure the ancillary bundle is archived with the final version**, since the manuscript now relies on it as a reproducibility aid.

### Scores

* **Originality:** 8/10
* **Significance:** 7/10
* **Correctness confidence:** 8/10
* **Readability:** 7/10
* **Overall flow / organization:** 7/10
* **Reproducibility / auditability:** 9/10
* **Overall:** 7.5/10

### Recommendation to the editor

I recommend **accept after minor revision**.

The theorem is strong enough, the proof architecture is convincing, and the current version is readable enough for a specialist combinatorics audience. My remaining concerns are about presentation and navigability, not the substance of the result. If the venue prefers accept-language rather than revision-language, my evaluation would be closest to **weak accept**.
