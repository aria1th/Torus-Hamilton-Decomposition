# RoundComposite TODO

- Package the composite-dimension reduction as a manuscript-quality note with a
  short introduction and references to the solved `d=3` and `d=4` cases.
- Decide whether the square lemma should be cited as folklore/product-graph
  background or kept fully self-contained as it is now.
- Add a short markdown companion note mirroring the TeX theorem statements.
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
