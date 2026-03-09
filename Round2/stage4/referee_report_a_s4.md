**Recommendation:** **Accept after minor revision**
**Equivalent accept-only label:** **Weak accept**
**Overall score:** **8/10**
**Referee confidence:** **medium-high**

**Score criterion used:** 9–10 = strong accept, 7–8 = weak accept / minor revision territory, 5–6 = major revision, 3–4 = weak reject, 1–2 = strong reject.

### Referee report

I reviewed the current PDF version directly, including a visual pass on representative pages to assess layout and readability. I also ran the accompanying artifact suite as supplied; all six stages passed, including the (m=4) witness, the low-layer table checks, the first-return checks, theorem-mode checks through even (m=500), exact (P_0) checks through (m=60), and exact full-graph checks through (m=30). Separately, I brute-force checked the odd closed-form construction for odd (m \le 101), and in those tests each color class was a single Hamilton cycle. I did **not** rederive every appendix branch line by line by hand, so my correctness assessment is based on the proof architecture together with substantial computational verification.

The manuscript proves that the directed 3-torus
[
D(m)=\mathrm{Cay}((\mathbb Z_m)^3,{e_1,e_2,e_3})
]
admits a decomposition into three arc-disjoint directed Hamilton cycles for every (m\ge 3). The argument is split into the odd affine five-swap construction, the even Route E construction driven by the sign-product obstruction and return-map analysis, and the separate finite witness for (m=4). The current version also gives the reader genuine navigational aids: Table 1, Table 2, Figure 1, the “primary geometry / obstruction / repair” section, Example 2, and Appendix E on verification artifacts. 

My overall judgment is positive. This is a natural and nontrivial theorem, and the current paper presents a convincing strategy for the hardest part, namely the even case. The manuscript does not just list case distinctions; it explains why the odd and even cases must diverge, why the primary geometry almost works, where the real obstruction first appears, and why the added Case II family is doing genuine interior repair rather than cosmetic endpoint patching. That conceptual arc is the paper’s strongest feature. 

On readability and flow, the main text now works reasonably well for a specialist reader. The introduction states the three governing ideas clearly. Section 4 is organized as a story instead of as raw casework, and that improves the paper substantially. Table 2 and Figure 1 are especially helpful because they give the reader a standing reference for the three coordinate systems and their defect supports. Example 2 at (m=10) is also a good choice: it shows the genuinely delicate Case II repair, not just the easier universal color-2 mechanism. In the main body, I found the narrative coherent and followable. 

My main remaining reservation is about the appendices. The paper’s **main text** flows well enough, but Appendices B and C still read more like an audit log than like a guided proof. Definition 4 remains the hardest entry point because the layer-0 rule is presented across a dense two-page formula block. Appendix B is logically sound, but compressed. Appendix C contains many orbit traces and endpoint cases in succession; by the time one reaches Proposition 13 and the sequence of corollaries, the argument is still correct, but the reading pace has become laborious. In other words: the paper is now readable, but not yet maximally reader-friendly. 

For that reason I stop short of strong accept. I do think the manuscript is publishable, but I would still request minor revisions aimed specifically at readability and overall flow:

1. Add a short “how to read Appendices B–C” paragraph near the start of the appendix section, telling the reader exactly what each appendix contributes and in what order it should be read.
2. Reformat Proposition 13 into a more visual summary, ideally with clearer case separation or a compact table, since it is the compression point for the splice argument.
3. Trim repeated roadmap prose that currently appears in the introduction, Section 4.1, Section 4.2, Theorem 5, and the Discussion.
4. Add one brief orienting remark before the hardest Case II color-0 material, since that is the point where many readers are most likely to lose the thread.

### Scores

* Originality: **8/10**
* Significance: **7/10**
* Correctness confidence: **8/10**
* Readability: **7/10**
* Overall flow / organization: **7/10**
* Reproducibility / auditability: **9/10**
* Overall: **8/10**

### Recommendation to the editor

I recommend **accept after minor revision**. The theorem is strong enough, the proof strategy is convincing, and the present version is already close to final. The remaining work is mostly editorial: improving navigability through the dense appendix material, not repairing a substantive mathematical defect.
