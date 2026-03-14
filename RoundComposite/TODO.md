# RoundComposite TODO

- Package the composite-dimension reduction as a manuscript-quality note with a
  short introduction and references to the solved `d=3` and `d=4` cases.
- Do a focused literature review on Hamilton decompositions / Hamiltonicity of
  Cartesian products, especially the Stong line, Foregger-type product
  decompositions, and directed-cycle product results such as Trotter--Erdos and
  Curran--Witte.
- Record which parts of the current argument are classical, which are merely
  adjacent in the literature, and which formulation appears genuinely new for
  directed tori.
- Decide whether the square lemma should be cited as folklore/product-graph
  background or kept fully self-contained as it is now.
- Add a short markdown companion note mirroring the TeX theorem statements.
- Update the TeX note after the literature review:
  add citations,
  clarify novelty claims,
  and decide whether to keep only the torus-specialized multiplicative closure
  or also incorporate the abstract square-lift theorem for arbitrary digraphs.
- Connect the top-level README and research-summary docs to the new composite
  reduction more explicitly.
- Design the Lean abstraction layer:
  deterministic digraph product,
  Hamilton decomposition interface,
  and the `D_{ab}(m) ≃ D_b(D_a)` block-product identification.
- Formalize the square lemma in Lean once the abstract graph-product interface
  is settled.
- Formalize the multiplicative-closure theorem after the square lemma and the
  torus block-product equivalence are in place.
- Decide whether to expose unconditional families such as `d=6,8,9,12,...` in
  the main manuscript or keep them in auxiliary notes for now.
