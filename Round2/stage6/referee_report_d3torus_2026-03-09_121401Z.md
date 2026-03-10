# Referee report

**Manuscript:** *Hamilton decompositions of the directed 3-torus \(D(m)\): explicit constructions for all \(m \ge 3\)*  
**Timestamp (UTC):** 2026-03-09 12:14:01Z

## Overall recommendation

**Decision:** **Accept after minor revision**.

## Editorial assessment at a glance

- **Correctness:** likely correct, with moderate-to-high confidence.
- **Originality:** good; the paper appears to settle a natural and previously unresolved special family.
- **Significance:** solid for a specialist combinatorics / graph-decomposition venue.
- **Exposition:** workable, but the even-case presentation would benefit from targeted revision.
- **Need for revision:** minor, but real.

## Summary of the contribution

The paper proves that the directed 3-torus
\[
D(m)=\operatorname{Cay}((\mathbb Z_m)^3,\{e_1,e_2,e_3\})\cong \vec C_m \square \vec C_m \square \vec C_m
\]
admits a decomposition into three arc-disjoint directed Hamilton cycles for every integer \(m\ge 3\).

The proof splits into three parts:

1. **Odd \(m\):** an elegant five-Kempe-swap modification of the canonical coloring, with return maps on \(P_0=\{i+j+k=0\}\) used to prove Hamiltonicity.
2. **Even \(m\ge 6\):** a parity obstruction shows Kempe-from-canonical methods cannot work, so the authors introduce the explicit Route E direction assignment and analyze its return maps via affine defect sets and first-return maps.
3. **\(m=4\):** a finite witness is provided.

The main conceptual points are strong:

- the **sign-product invariant** is a clean obstruction that explains why the odd and even cases must be treated differently;
- the **return-map reduction** is the correct organizing device for the entire paper;
- the odd-case proof is quite neat;
- the even-case construction is intricate, but it is explicit and the paper makes a real effort to isolate the obstruction and the repair mechanism.

## Checks I performed

I read the manuscript, including the appendices, and I also checked the supplied ancillary files.

In addition, I ran the following verification steps:

- the supplied finite check for **\(m=4\)** (`verify_m4_witness.py`), which passed;
- the supplied even-case artifact suite (`run_even_artifact_suite.py`) on nontrivial ranges, which passed;
- the direct Route E verifier in theorem mode up to **even \(m=500\)**, in \(P_0\)-check mode up to **even \(m=100\)**, and in full-check mode on \(V\) up to **even \(m=30\)**, all of which passed;
- an independent small script of my own implementing the closed-form odd-case maps from Proposition 1, which confirmed that for odd \(m=3,5,\dots,19\) each color class is a single \(m^3\)-cycle, and for even \(m=4,6,\dots,18\) the same formulas reproduce Proposition 2 (colors 0 and 1 Hamiltonian, color 2 splitting into exactly \(m+2\) cycles).

These checks do **not** replace the written proof, but they substantially increase my confidence that the long case analyses in the appendices are internally consistent.

## Main strengths

### 1. The theorem is natural and nontrivial
The family \(\vec C_m\square \vec C_m\square \vec C_m\) is one of the most symmetric directed products one could test against the general theory. The result is therefore a meaningful benchmark, not an arbitrary isolated construction.

### 2. The odd/even split is conceptually justified
I particularly liked that the even case is not introduced as a purely ad hoc workaround. The parity barrier in Section 2 gives a genuine reason that Kempe-from-canonical methods fail for even \(m\), which makes Route E feel motivated rather than merely engineered.

### 3. The return-map viewpoint is effective
Reducing Hamiltonicity on \(m^3\) vertices to cycle structure on \(P_0\) of size \(m^2\), and then further to one-dimensional first-return maps on explicit transversals, is the right organizing principle. This keeps the paper from becoming a brute-force enumeration.

### 4. The authors are unusually transparent about verification
The manuscript clearly distinguishes the written proof from the artifact bundle, and the bundle is well organized. That is a real positive in a paper whose even-case proof is long and technical.

## Main concerns requiring revision

None of the points below is, in my view, a fatal flaw. However, I do think they should be addressed before publication.

### 1. The literature framing in the introduction should be corrected
The introduction currently says that the decomposition problem was subsequently treated by Bogdanowicz and by Darijani--Miraftab--Morris. This is misleading. Darijani--Miraftab--Morris study **arc-disjoint Hamiltonian paths**, not Hamilton decompositions into Hamilton cycles. That paper is certainly relevant, but for a different reason: it shows that the three-factor case remains a natural boundary in the current general theory of arc-disjoint Hamilton paths.

Relatedly, the directed-decomposition history should cite **Kevin Keating's** earlier two-factor work on multiple-ply Hamiltonian digraphs, which already gives a characterization for when the Cartesian product of two directed cycles decomposes into directed Hamilton cycles. Bogdanowicz's 2017 note explicitly builds on that earlier two-factor result.

So I recommend revising the introductory history to say something like:

- single-cycle Hamiltonicity: Trotter--Erdos, Curran--Witte;
- two-factor Hamilton decomposition / multi-ply Hamiltonicity: Keating;
- decompositions into equal-length directed cycles and related refinements: Bogdanowicz;
- arc-disjoint Hamilton paths and the remaining three-factor boundary: Darijani--Miraftab--Morris.

This is the one place where I think the current manuscript is not yet fully accurate in its scholarly positioning.

### 2. The paper should do a bit more to guide the reader through the even case
The even case is correct-looking but cognitively heavy. The main text already contains a roadmap, yet I still found it difficult on first read to track exactly where each of the following enters:

- the **primary geometry**;
- the **first obstruction**;
- the failure of the **boundary corrections alone**;
- the role of the **Case II repair family**;
- the final closure via **arithmetic family-blocks** and the **splice permutation**.

I recommend adding one short proof-dependency diagram or paragraph near the start of Section 4 that explicitly lists the chain

> Definition 5 -> Proposition 3 / Appendix B -> Lemma 9 / defect normal form -> first-return formulas -> Proposition 13 / splice permutation -> Lemma 7 -> Hamiltonicity.

At present, this logic is all there, but the reader has to reconstruct it.

### 3. Color 0 in Case II deserves one more worked example or a clearer bridge paragraph
Color 2 is handled fully in the main text; color 1 gets a good conceptual discussion through Proposition 4, Proposition 5, and Example 2. By contrast, **color 0 in Case II** remains the part I would expect most readers (and referees) to trust only after laborious appendix checking.

I do not think a new proof is needed. But I would strongly encourage one of the following:

- add a short worked example for color 0 in Case II (for example \(m=10\) or \(m=16\)); or
- add a paragraph before Proposition 12/Proposition 13 explaining in words what the residue-4 splice picture is and why the later \(m \bmod 12\) split is only a cyclic reordering.

That would materially improve readability.

### 4. The role of the artifact bundle should be reiterated one more time near the end of Theorem 5
The manuscript already says the bundle is not part of the proof. I still think one extra sentence at the end of Theorem 5, or at the start of Appendix E, would help:

> all logically necessary formulas, first-return maps, and return-time sums appear in Appendices A--D; the scripts in Appendix E only independently audit those displayed formulas and the finite witness.

This is already true, but it is worth emphasizing because the even case is so verification-heavy.

## Minor comments and suggested edits

1. The phrase **"color \(c\) is Hamilton"** is defined, but it is slightly nonstandard. I would not insist on changing it, but "Hamiltonian" may read more smoothly.
2. Table 7 is very useful. I suggest pointing to it explicitly at the very start of Appendix C, perhaps in the first sentence.
3. In Lemma 8, readers may benefit from the explicit inverses of \(\Phi_0,\Phi_1,\Phi_2\), or at least a short remark that the determinants are \(\pm 1\), hence units modulo \(m\).
4. Proposition 13 is important enough that I would consider mentioning it already in the overview paragraph of Section 4.1, not only later.
5. The discussion section is sensible, but it may slightly oversell how cleanly the current proof mechanism should generalize. I would soften any wording that could be read as suggesting a straightforward higher-dimensional extension.

## Recommendation in publication terms

I believe the paper is **publishable** after **minor revision**.

My reason is straightforward:

- the main result is interesting and appears new;
- the odd case is elegant;
- the even case is long but, as far as I can tell, mathematically coherent;
- the appendices contain the necessary proof material, and the supplied artifacts provide useful independent confirmation.

My confidence is not the same as in a short five-page paper with a one-line proof. The even-case appendix is too intricate for me to claim that I have hand-verified every case split line by line. But after reading the proof architecture carefully and running substantial consistency checks, I think the manuscript has crossed the threshold for acceptance, subject to the expository and bibliographic corrections above.

## Confidential note to the editor

If your journal is comfortable publishing long, explicit constructive proofs with substantial appendices, then I would accept this paper after minor revision. If the journal strongly prefers short conceptual papers, then the paper may feel somewhat technical for its payoff. But on mathematical content, I am positive.
