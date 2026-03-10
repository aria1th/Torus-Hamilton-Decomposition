# Referee Report

**Manuscript:** *Hamilton decompositions of the directed 3-torus* `D(m)`: explicit constructions for all `m ≥ 3`  
**Author:** Sanghyun Park  
**Timestamp (Asia/Tokyo):** 2026-03-09 21:13 JST

## Editorial recommendation

**Recommendation:** **Accept subject to minor revision.**

### Decision summary

| Criterion | Decision |
| --- | --- |
| Correctness | No fatal gap detected in the written argument. |
| Novelty / interest | Publishable and natural contribution, subject to the literature positioning being stated more sharply. |
| Exposition | The paper is readable overall, but the even-case proof would benefit from several targeted clarifications. |
| Ancillary verification | Helpful and well scoped; supports, but does not replace, the written proof. |

## Scope of my checking

I want to be explicit about what I did and did not verify.

### What I checked

1. I read the full manuscript, including the main text and appendices.
2. I ran the supplied ancillary verification suite successfully with the following ranges:
   - theorem mode for even `m = 6, 8, ..., 60`,
   - table / partition checks for even `m = 6, 8, ..., 24`,
   - first-return checks for even `m = 6, 8, ..., 40`,
   - exact `P0` checks for even `m = 6, 8, ..., 20`,
   - exact full checks on `V` for even `m = 6, 8, ..., 16`,
   - the separate `m = 4` witness check.
3. I performed **independent direct brute-force checks from the stated constructions** (not using the theorem-mode certificate) for:
   - odd `m = 3, 5, 7, 9, 11, 13, 15`,
   - even `m = 6, 8, 10, 12, 14, 16, 18`,
   verifying that each of the three color maps is a permutation and a single Hamilton cycle.
4. I independently checked several displayed return-map / first-return formulas against direct iteration, including:
   - the odd-case formulas in Theorem 4,
   - the even-case first-return formulas for colors 1 and 0 for representative even values `m = 6, 8, 10, 12, 14`.

### What I did not check fully

1. I did **not** carry out a fully formal symbolic audit of every orbit trace and every case split in Appendix C for arbitrary `m`.
2. I did **not** attempt proof-assistant formalization.
3. I did **not** perform an exhaustive independent literature search beyond the references in the manuscript and a brief spot-check of the most relevant prior papers.

Accordingly, my confidence is **moderate to high**, not absolute.

## Summary of the paper

The manuscript proves that the directed 3-dimensional torus

`D(m) = C⃗_m □ C⃗_m □ C⃗_m`

admits a decomposition into three arc-disjoint directed Hamilton cycles for every `m ≥ 3`.

The proof splits naturally into three regimes.

- For **odd `m`**, the author starts from the canonical coloring and performs five explicit Kempe swaps. The resulting color maps admit simple return-map formulas on the section `P0 = {S = 0}`, from which Hamiltonicity follows cleanly.
- For **even `m ≥ 6`**, the author proves a parity obstruction showing that a Kempe-from-canonical approach cannot work, then introduces the explicit low-layer direction assignment **Route E**. The resulting return maps are analyzed by a defect / first-return formalism.
- The exceptional case **`m = 4`** is handled by a finite explicit witness.

The paper is strongest when it isolates conceptual structure rather than merely listing cases: the sign-product invariant, the return-map reduction, and the explanation of why the Case II repair family is genuinely needed are all valuable pieces.

## Overall assessment

My overall view is positive. I did not find a fatal mathematical flaw, and the computational evidence I checked is consistent with the claims. The theorem is natural, the odd case is elegant, and the even case—although technically heavy—does contain a real organizing idea rather than being pure brute-force bookkeeping.

The main reservation is expository: the even-case proof is long and case-driven enough that the reader would benefit from a sharper separation between the conceptual mechanism and the bookkeeping layer. I therefore recommend **minor revision**, with the revisions aimed at clarity and positioning rather than at changing the substance of the proof.

## Main strengths

### 1. A clean conceptual split between odd and even cases

The sign-product invariant is a genuinely useful observation. It does more than obstruct one attempted proof strategy: it explains *why* the odd and even cases should look different. This improves the paper substantially.

### 2. The odd-case argument is concise and attractive

The five-swap construction is easy to state and, once the return maps are written down, easy to verify. This part of the paper is particularly successful.

### 3. The even case is not merely computational

Although the Route E analysis is intricate, the manuscript does make a convincing effort to explain the mechanism:

- the bulk-vs-defect viewpoint,
- the first-return reduction,
- the “primary geometry” obstruction,
- and the role of the Case II repair family.

This is important, because it turns what could have been a black-box construction into something with mathematical content.

### 4. The ancillary files are well chosen

The supplementary scripts focus on the delicate parts of the proof and are described in a restrained way. The manuscript is careful to say that these files are **verification aids**, not proof steps. That is the right stance.

## Requested revisions

I do not view any of the points below as fatal, but I do think they should be addressed before publication.

### 1. Clarify the relation to prior decomposition results

The introduction should more explicitly explain why the existing decomposition literature—especially the results of Bogdanowicz cited as [10] and [11]—does **not** already settle the present theorem.

Right now the manuscript says that [10] treats decomposition into equal-length cycles and that the present problem is the extremal Hamiltonian case. That is plausible, but for a referee and for future readers I would like one sharper paragraph explaining exactly what those earlier results do and do not imply for the symmetric case `C⃗_m □ C⃗_m □ C⃗_m`.

This is not a complaint about priority; it is a request for clearer positioning.

### 2. Promote the Route E layer-0 partition check from a remark to a formal lemma

Definition 5 is the combinatorial heart of the even construction. Since correctness depends on the layer-0 cases being pairwise disjoint and exhaustive, I recommend promoting Remark 3 to a short lemma (or adding a short proof immediately after the remark).

At present this is stated but not really demonstrated. A compact proof or a cardinality check would make the construction feel much more secure on first reading.

### 3. Expand one or two crucial “trust me” transitions in the even case

There are several places where the exposition is mathematically believable but still asks a lot from the reader. The most important examples are:

- the proof of Theorem 3, step (4), where the invariance of the restriction of `τ_{0,1}` on `P1` is argued rather quickly;
- the compression in Proposition 13, where many arithmetic-family closures are summarized at once;
- some of the Appendix C orbit traces where the phrase “no other special branch can occur” is correct-looking but deserves one more sentence of justification.

I do **not** think the paper needs much more length. Rather, it needs a few more explicit signposts at the points where readers are most likely to hesitate.

### 4. Make the proof / computation boundary even more explicit

The paper already says that the artifact bundle is not part of the proof. I suggest making this distinction even more explicit in the introduction and again at the start of Appendix E.

For example, a short sentence such as the following would help:

> “All assertions used in the proof are proved in the written text; the scripts only re-check the displayed formulas and finite witnesses.”

That is already effectively the case, but stating it in exactly this form would be reassuring.

### 5. Streamline the abstract and the opening roadmap

The abstract is informative, but it is very technical for an abstract. I would encourage the author to shorten the Case II discussion there and move some of that detail into the introduction.

Similarly, the introduction could emphasize earlier what the reader should retain:

- odd case = five Kempe swaps + affine return maps;
- even case = parity barrier + Route E + defect / splice analysis.

## Detailed comments and suggestions

1. **Theorem 3 (odd case):** I would add one short displayed statement identifying exactly which outgoing arcs on `P1` remain canonical after steps (1)–(3). This would make step (4) easier to trust on a first pass.

2. **Table 2 / Figure 1 / Proposition 13:** these are helpful, but the paper would benefit from one miniature worked example that explicitly shows how a bulk arithmetic family becomes a splice block. Example 2 already helps for color 1 in Case II; something similar for one color-0 block would improve readability.

3. **Remark 4 and Proposition 4 / 5:** these are conceptually important and should be highlighted as such. In a revision, I would consider telling the reader more explicitly that these propositions are what elevate the even construction above a computer-found rule table.

4. **Appendix C navigation:** Table 7 is useful. I would add one sentence before Proposition 13 saying that *all* remaining single-cycle checks are reduced to finite splice permutations on arithmetic blocks. That is the conceptual endpoint of the appendix.

5. **Case `m = 4`:** the treatment is acceptable. Since the full cycles are no longer printed inline, I would make sure the final published supplement preserves the machine-readable witness and the human-readable cycle list.

6. **Notation:** the notation is generally careful. Still, because both the odd and even cases use return maps on `P0`, I support the author’s choice to distinguish `F_c` from `R_c`; that distinction should be mentioned once more when Appendix A begins.

## Bottom line

I find the main result convincing and worthy of publication. The manuscript combines a neat odd-case construction with a technically demanding but conceptually motivated even-case analysis. My checks did not uncover a substantive error.

The paper should, however, be revised to improve the reader’s ability to verify the Route E construction from the text alone and to sharpen the statement of how this work differs from prior decomposition results.

## Final recommendation

**Accept subject to minor revision.**
