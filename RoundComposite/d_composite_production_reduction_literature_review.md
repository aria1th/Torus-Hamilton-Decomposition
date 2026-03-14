I reviewed the note . Overall, the mathematical backbone looks good: I do not see a fatal logical gap in Proposition 1 or Theorem 2, and the main reduction idea is genuinely clean. The biggest weaknesses are expository rather than structural: scope is stated a bit too loosely, and the note is under-cited.

### Logical flow

* The proof architecture is sensible. The square lemma gives a concrete 2-dimensional base case, and the multiplicative-closure theorem is then the real engine: block the coordinates, align one Hamilton factor from each (D_a(m)) block, observe that the product is a copy of (D_b(m^a)), decompose that, and then partition the full arc set by the index (i). Proposition 1 is especially nice because the odometer conjugation makes Hamiltonicity immediate once the 1-factor check is done. 

* The main scope issue is consistency. The abstract says the class of dimensions admitting decompositions “for every modulus” is multiplicatively closed, but Theorem 2 and Corollary 3 are stated only for moduli (m,n \ge 3), while Proposition 1 covers (n \ge 2). That is not a logical error, but it does create avoidable friction. Either change the headline to “for every modulus (m \ge 3)” or add one sentence explaining why modulus (2) is being set aside in higher dimensions. 

* Theorem 2 is slightly over-stated relative to its proof. What the proof actually uses is: if (D_a(m)) has a Hamilton decomposition and (D_b(m^a)) has one, then (D_{ab}(m)) has one. The present (\forall n) formulation is fine for the later semigroup-style corollary, but the local theorem would read more sharply if it matched the proof. I would also replace “canonically isomorphic” by just “isomorphic,” unless you explicitly choose cyclic labelings of the Hamilton cycles (A_i^{(r)}). Remark 5 is basically right, but I would phrase it more carefully: the reduction is theorem-level rather than local-rule-level, yet it is still constructive once decompositions of (D_a(m)) and (D_b(m^a)) are supplied. 

* Corollary 4 is the least polished part. Item 3 is logically redundant, because (4=2\cdot 2) already follows from the square lemma plus Theorem 2, so “(D_4(n)) is also solved here” adds no new existence statement unless you mean an explicit witness-level construction. More broadly, phrases like “in this repository” and “also solved here” need actual citations or internal theorem labels. I could not assess those companion (d=3) and (d=4) claims because they were not included in the uploaded note. The manuscript also needs an actual references section. 

### Literature

At minimum, I would position the note against these four clusters:

* **Classical Hamiltonicity of directed cycle products.** Trotter and Erdős (1978) gave the criterion for when (C_{n_1}\square C_{n_2}) is Hamiltonian, and Curran–Witte (1985) characterized Hamilton paths in two-cycle products and showed that any Cartesian product of three or more nontrivial directed cycles has a Hamilton cycle. Your square lemma is stronger than the equal-side (2)-factor Hamiltonicity statement because it gives a full decomposition into two Hamilton cycles, not merely one Hamilton cycle. 

* **Nearby decomposition and multi-cycle results for directed cycle products.** Bogdanowicz (2017) proved that if the factor lengths have a common factor (f \ge 2), then the Cartesian product can be decomposed into equal-length directed cycles; Bogdanowicz (2020) then identified explicit Hamilton cycles and, under extra arithmetic conditions, two arc-disjoint Hamilton cycles in these products. These are the closest published items I found to the territory of your Proposition 1 and to the broader “more than one Hamilton object” theme. ([ScienceDirect][1])

* **Current status on multiple Hamilton objects.** Darijani, Miraftab, and Morris (2025) proved that the Cartesian product of two directed cycles has two arc-disjoint Hamiltonian paths, and that the same is true for any product of four or more directed cycles, while some cases with three factors remain open. That makes it important for your note to say explicitly that it is about full Hamilton decompositions in the special one-way torus family (D_d(m)), not about arbitrary Cartesian products of directed cycles. ([opus.uleth.ca][2])

* **General context and analogies.** For background, the standard survey references are Curran–Gallian (1996) and Lanel et al. (2019). If you want one undirected analogue for the product-reduction flavor, Stong (1991) is the natural reference on Hamilton decompositions of Cartesian products of graphs under mild hypotheses; that helps readers see the analogy while also seeing that your orientation model is different. ([ScienceDirect][3])

### Bottom line

My recommendation would be: keep the core proofs, tighten the scope statements, and add a short bibliography plus one paragraph that explains exactly where this result sits relative to Hamiltonicity/path results for products of directed cycles. Based on the sources I checked, I did **not** find this exact multiplicative-closure theorem for full Hamilton decompositions of the one-way torus stated in this form, but I did not do an exhaustive MathSciNet/zbMATH search. A one-paragraph literature-positioning paragraph after the abstract would probably be enough.

[1]: https://www.sciencedirect.com/science/article/pii/S0166218X17302755 "https://www.sciencedirect.com/science/article/pii/S0166218X17302755"
[2]: https://opus.uleth.ca/items/f99be3db-5d52-4b3a-839d-3c01b5455637 "https://opus.uleth.ca/items/f99be3db-5d52-4b3a-839d-3c01b5455637"
[3]: https://www.sciencedirect.com/science/article/pii/0012365X95000725 "https://www.sciencedirect.com/science/article/pii/0012365X95000725"
