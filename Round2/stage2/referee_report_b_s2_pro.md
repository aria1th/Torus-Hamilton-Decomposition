**Recommendation:** **Accept after minor revision**
**Overall score:** **8/10**
**Confidence in this review:** **medium-high**

**Score guide used here:** 10 = outstanding / essentially ready; 8 = publishable with small edits; 6 = worthwhile but needs substantial revision; 4 = not ready for publication; 2 = unsuitable.

### Referee report

I reviewed the current manuscript together with the supplied ancillary bundle. The paper proves that the directed 3-torus
[
D(m)=\mathrm{Cay}((\mathbb Z_m)^3,{e_1,e_2,e_3})
]
admits a decomposition into three arc-disjoint directed Hamilton cycles for every (m\ge 3). The proof splits into an odd case handled by five Kempe swaps and affine return maps, an even case handled by the explicit Route E construction plus return/first-return analysis, and a separate finite witness for (m=4). The manuscript also explicitly positions the supplementary scripts as verification aids rather than part of the proof. 

I also ran the supplied artifact suite in the ancillary bundle on my side. It passed all six reported stages, including the (m=4) witness check, low-layer formula/partition checks, first-return checks, theorem-mode checks to even (m=500), exact (P_0) checks to (m=60), and exact full-graph checks to (m=30). In addition, I independently brute-force checked the odd closed-form construction from the manuscript for odd (m\le 101), and in those tests each color class was a single Hamilton cycle. This does not replace a complete hand audit of every appendix branch, but it materially increases confidence in correctness.

In terms of context, the cited adjacent literature covers Hamiltonicity of Cartesian products of directed cycles, equal-length cycle decompositions in such products, identification of Hamilton cycles in some products, and arc-disjoint Hamiltonian paths; the exact three-Hamilton-cycle decomposition theorem proved here is a natural next step beyond those results. ([ScienceDirect][1])

The strongest aspect of the paper is conceptual, not just computational. The sign-product invariant gives a clean explanation of why even (m) cannot be reached by Kempe-from-canonical methods, so the odd/even split is genuinely forced. The current version also makes the even proof much easier to understand than a bare case split: the notation table is helpful, the layer-0 partition is stated explicitly, the “primary geometry / first obstruction / boundary-only no-go / forced repair” narrative is clear, and Appendix E now tells the reader exactly what has been independently checked. 

I therefore view the paper as publishable in principle, and the current version is substantially more auditable than an ordinary long constructive proof. In particular, I no longer regard the absence of executable verification material as a concern, because the bundle is now actually present and runnable.

My remaining reservations are expository rather than mathematical. The even case is still dense and spread across Section 4 and Appendices A–C; a reader must still shuttle between conceptual discussion, piecewise return-map formulas, and first-return splice data. Also, the one detailed worked example is still the universal color-2 case at (m=6), whereas the genuinely delicate regime is the Case II behavior when (m\equiv 4 \pmod 6), especially for colors 1 and 0. 

For that reason I recommend **minor**, not zero, revision. My requested changes are modest:

1. Add one short worked trace in the genuinely difficult Case II regime, preferably for color 1 or color 0 at a small value such as (m=10). That would make the forced-repair mechanism much easier to internalize.

2. Tighten some of the repeated roadmap prose in Section 4 / Appendix C. The conceptual story is good, but parts of it are stated more than once.

3. Make sure the ancillary bundle is archived with the final accepted version in a stable way, since Appendix E now invites the reader to consult those files.

4. Do one final style pass for small presentational polish.

### Scores

* **Originality:** 8/10
* **Significance:** 7/10
* **Correctness confidence:** 8/10
* **Exposition:** 7/10
* **Reproducibility / auditability:** 9/10
* **Overall:** 8/10

### Recommendation to the editor

I recommend **accept after minor revision**. I do not see a substantive mathematical reason to reject the current version. The theorem is natural and nontrivial, the proof strategy has a clear internal logic, and the supplied computational checks meaningfully strengthen confidence. The remaining issues are presentational and archival, not structural.

[1]: https://www.sciencedirect.com/science/chapter/bookseries/abs/pii/S0304020808729967?utm_source=chatgpt.com "Hamilton Paths in Cartesian Products of Directed Cycles"
