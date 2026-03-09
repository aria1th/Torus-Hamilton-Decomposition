Attached: [Referee report (DOCX)](sandbox:/mnt/data/referee_report_d3torus.docx)

Reviewed manuscript: 

**Decision:** Minor revision / accept after minor revision

**Scores (10-point scale):**
Originality 8, Technical depth 8, Correctness confidence 7, Significance 7, Exposition 6, Reproducibility 9.

The manuscript claims a complete decomposition theorem for all (m \ge 3), split into an odd-(m) construction, an even (m \ge 6) Route E construction, and a separate finite witness for (m=4). The main conceptual engine is the combination of a sign-product parity barrier for Kempe-from-canonical constructions in the even case and a return-map/first-return analysis for the explicit Route E low-layer assignment. The novelty claim looks credible relative to Bogdanowicz’s equal-length cycle decomposition result and the 2025 arc-disjoint Hamilton-path paper, whose abstract still reports open cases for Cartesian products of three directed cycles. ([ScienceDirect][1])

For my review scope, I ran the bundled checks `verify_m4_witness.py`, `routee_return_formula_tables_check.py --m-max 24`, `routee_first_return_check.py --m-max 24`, `route_e_even.py 24 --mode p0-check`, `route_e_even.py 14 --mode full-check`, and `route_e_even.py 120 --mode theorem`; all passed. I also independently brute-forced the odd construction for odd (m=3,\dots,25) and Route E for even (m=6,\dots,32), and in every tested case each color class was a single Hamilton cycle. The paper itself is careful to describe the scripts as verification aids, not part of the proof. I did **not** hand-rederive every appendix branch for colors 0 and 1, so my correctness score is high but not maximal.

The main revisions I would request are to sharpen the literature-positioning paragraph, add a compact roadmap/notation table for the several coordinate systems in Section 4, and make the (m=4) certification more archival/portable in case the journal does not preserve supplements well; that part currently relies on the explicit appendix table together with the external witness/checker setup.

[1]: https://www.sciencedirect.com/science/article/pii/S0166218X17302755 "https://www.sciencedirect.com/science/article/pii/S0166218X17302755"
