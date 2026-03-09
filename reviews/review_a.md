Below is a referee-style report.

**Referee report on**
*Hamilton decompositions of the directed (3)-torus (D(m)): explicit constructions for all (m\ge 3)*

**Scope of my assessment.** I examined the full manuscript, including the appendices, compiled the LaTeX successfully, ran the supplied ancillary verification scripts, and independently brute-force checked the explicit constructions written in the paper for odd (m=3,5,7) and even (m=6,8,\dots,24) directly from the stated rules. I did **not** independently re-derive every appendix case split symbolically for arbitrary (m), and for the (m=4) case I relied on the supplied witness/checker rather than tracing the 64-cycles by hand from the printed table.

**Recommendation:** **Minor revision** (publishable after revision).

The problem is well positioned relative to the literature: products of three or more directed cycles are known to have a Hamilton cycle, Bogdanowicz studied decompositions of Cartesian products of directed cycles into equal-length directed cycles, and Darijani–Miraftab–Morris still report remaining open three-factor cases for arc-disjoint Hamilton paths. ([ScienceDirect][1])

In my view, the manuscript makes a genuine and interesting contribution for a specialist graph-theory/combinatorics venue. The main theorem is clean, the odd case is elegant, and the sign-product invariant is a nice conceptual addition because it explains why the even case cannot come from Kempe swaps starting at the canonical coloring. The even case is much more technical, but the return-map / first-return framework is coherent, the appendices appear logically connected to the main theorem, and the concrete checks I ran are consistent with the stated formulas and the claimed Hamilton decompositions.

What follows are the points I would ask the authors to address before publication.

**1. The even-case “splice” stage should be made a bit more formal.**
The place where I was least comfortable as a reader is Proposition  (\ref{prop:routeE-splice}) and the surrounding discussion. Phrases such as “after absorbing the isolated bridge vertices into adjacent arithmetic runs” are intuitively clear, but they are not fully formal as written. The proposition is probably correct, and the explicit block lists make the intended meaning recoverable, but I would still ask the authors to tighten this passage.

A small fix would suffice: define precisely what it means to absorb a bridge vertex into a block, or bypass that language and instead state directly that the listed ordered blocks satisfy the successor rule required by the splice-graph lemma. As written, this is more expository than formal, and it sits at an important place in the proof.

**2. The paper needs one clearer proof roadmap for Route E.**
The odd case is easy to audit. The even case is auditable, but only after repeated back-and-forth between the main text and several appendices. I recommend a short roadmap near the start of Section 5 or immediately before Theorem (\ref{thm:routeE-even-main}), explicitly listing:

* where the return-map formulas are derived,
* where the finite-defect normal forms are extracted,
* where the first-return formulas for each color are proved,
* where the single-cycle property of each induced lane map is established,
* and where bijectivity of the full color maps follows.

This is not a request for new mathematics. It is a request for better navigability in a proof that is otherwise quite verification-heavy.

**3. Clarify more explicitly how this differs from earlier equal-length decomposition results.**
A reader is likely to wonder whether the theorem is already a direct corollary of prior work on decompositions into equal-length directed cycles. Since the paper’s contribution is specifically a decomposition into **Hamilton** cycles of the symmetric three-factor torus, I think the introduction should say in one or two explicit sentences why that conclusion is not already immediate from the existing equal-length decomposition results cited by the authors. That would help readers calibrate the novelty more quickly. ([ScienceDirect][2])

**4. The role of the verification artifacts should be stated carefully.**
The artifact bundle is useful and, in my opinion, strengthens confidence in the manuscript. But I would still encourage the authors to say even more explicitly that the proofs are intended to be complete without the scripts, and that the scripts are regression checks / independent validation only. For the (m=4) case in particular, the reliance on a machine-readable witness is acceptable as supplementary material, but some editors and readers may prefer a slightly more human-readable summary of the three 64-cycles in the supplement.

**5. A few presentational improvements would materially help the reader.**

* In the proof of the affine five-swap theorem, the justification of step (4) is correct in spirit, but one more sentence spelling out why the restriction of (\tau_{0,1}) to (P_1) remains canonical after steps (1)–(3) would make this part easier to check.
* I would move a worked Route E example slightly earlier, before the full first-return analysis, not after the framework is already in place.
* A short notation guide for the successive coordinate systems on (P_0) would help: ((i,k)), then the color-adapted bulk coordinates, then the lane/clock interpretation.
* There are some routine typesetting issues (overfull boxes, hyperref warnings from math in PDF strings) that should be cleaned up in revision.

**Overall judgment.**
I am positive on the paper. The odd-case construction is neat and memorable. The even case is undeniably ad hoc and technical, but I did not find a mathematical contradiction, and my concrete checks support the correctness of the stated construction. My reservation is therefore not about the theorem itself, but about exposition: the Route E part should be made easier to verify from the printed text alone.

**Decision:** **Accept after minor revision.**

[1]: https://www.sciencedirect.com/science/chapter/bookseries/abs/pii/S0304020808729967 "Hamilton Paths in Cartesian Products of Directed Cycles"
[2]: https://www.sciencedirect.com/science/article/pii/S0166218X17302755 "On decomposition of the Cartesian product of directed ..."
