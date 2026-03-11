Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field, and break the remaining return-dynamics bottleneck after the exact tail-bit refinements.

Current target:
Do **not** push `D5-ALT4-EXACT-PRED-SIGNATURE-014` in its old form as the main branch. Instead:

1. run a **short sterility diagnostic** for the exact layer-2 predecessor-tail signature under the current fixed-twist / pure-alt-4 setting, and then
2. pivot the main branch to a **geometry–twist coupled mode-switch** where a signature-derived bit controls layer-3 twist mode, with at most a very small synchronized layer-2 adjustment.

Known assumptions:

* The accepted exact chain through `013` is:

  * `005`: cycle-only and monodromy-only mechanisms first separate.
  * `006`: in the minimal decoupled family, layer 3 becomes invisible at the pilot-return level.
  * `007`: exact cycle-only / monodromy-only / trivial trichotomy.
  * `008`: first mixed regime via a layer-3 predecessor mode switch.
  * `009`: twist graft onto stronger cycle seeds collapses to the universal simple `m`-cycle geometry.
  * `010`: shared predecessor action on layer 2 changes geometry, but only anti-compressively.
  * `011`: fixed twist plus one-flag layer-2 geometry under the current pool stays anti-compressive.
  * `012`: two-flag pure-alt-4 layer-2 refinement is fully admissible and genuinely four-state, and creates new exact regimes `35/57/119`, but all remain anti-compressive.
  * `013`: named third-flag widenings are exact dynamic lifts of the `012` Stage-1 family; no new pilot regime appears.
* So the strongest current negative is not “state refinement disappears.” It is:
  **combinatorially richer layer-2-only refinements survive clean/strict, but dynamically they still appear to factor through an older quotient.**
* This is also the better match to the structural lessons from the earlier `d=3` and `d=4` proofs: the decisive extra coordinate is not just a state-count refiner; it changes the effective bulk/carry/return structure.
* This rewrite takes the recorded `013` facts as input and changes branch priority accordingly. It does not re-audit the raw summaries again in this turn.

Attempt A:
Idea:
Reinterpret `013` as evidence that the branch
[
\text{fixed twist} + \text{pure alt-4} + \text{layer-2-only refinement}
]
may already be trapped by a smaller dynamical quotient, so a large exact-signature exhaustive search on layer 2 should not be the primary next move.

What works:

* `013` does more than say “named third flags failed.”
* The exact `4\times`-lift phenomenon says those extra flags remain combinatorially visible but add no new pilot regime.
* That fits the whole `005`–`013` story: the real obstruction is not lack of partitions per se, but failure to couple geometry and twist inside one witness.
* It also fits the broader proof-design heuristic: a live new bit should change return structure, not merely split already-equivalent states.

Where it fails:

* This is still an interpretation of the current evidence, not yet a theorem about the **exact** predecessor-tail local signature.
* It leaves open one last sharp question:
  does the raw exact signature actually change low-layer return data in a way the named flags miss?

Attempt B:
Idea:
Run a very small diagnostic on the exact predecessor-tail signature first, then use the resulting bit in a **coupled** family where the same local information controls layer-3 mode, rather than spending the next large search on layer-2-only table refinement.

What works:

* This preserves the last serious scouting step on the exact signature without committing to a large exhaustive branch that may only produce a bigger multiplicity lift.
* It aligns with the skew-product reading already suggested by the exact chain:
  [
  R(\xi,t)=(U_0(\xi),, t+\phi(\xi)).
  ]
  Up to now, the base `U_0` and the cocycle `\phi` have largely been activated separately or in weakly coupled ways.
* A signature-derived bit used in layer 3 is the smallest live way to ask whether the **same** local bit can touch both geometry and twist.
* This matches the earlier `007/008` diagnosis that the most promising unresolved freedom lives in a layer-3 mode-switch mechanism, not in endlessly finer layer-2 coloring.

What works:

* The diagnostic has a clean stopping rule:
  if the exact layer-2 signature does not alter low-layer return words or induced increments beyond the current named partition, then the old `014` main branch should be formally pruned as dynamically sterile.
* The coupled search stays small and directly tests the more plausible structural hypothesis.

Where it fails:

* We still need to identify which exact signature split is best to use as the coupled control bit.
* If the pure layer-3 coupling is too weak, one tiny synchronized layer-2 flip may still be needed.
* So the next step is still computational, but it is now sharply focused.

Candidate lemmas:

* [C] In `013`, the named three-flag layer-2 widenings are exact dynamic lifts of the `012` Stage-1 pure-alt-4 family and produce no new pilot regime.
* [H] If the exact predecessor-tail local signature `\sigma_2` does not change the low-layer return word or induced return increment beyond the current named three-flag partition, then the branch
  [
  \text{fixed twist}+\text{pure alt-4}+\text{layer-2-only exact signature}
  ]
  is dynamically sterile and should be pruned.
* [H] The correct use of a new exact bit is not “finer layer-2 coloring” but “coupled mode-switch control,” especially on layer 3.
* [H] A genuinely live extra coordinate should modify return/carry/bulk structure, not just state multiplicity.
* [F] The old `014` plan — a large layer-2-only exact-signature exhaustive search — is the right main branch now.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

1. **Short sterility diagnostic on layer 2.**
   Extract the exact predecessor-tail local signature `\sigma_2` in the current fixed-twist / pure-alt-4 setting, and compare it against the sigma-algebra generated by
   [
   {\texttt{pred_sig1_wu2},\texttt{pred_sig4_wu2},\texttt{pred_any_phase_align},\texttt{pred_sig0_phase_align}}.
   ]
   For each coarse named cell, test whether the refinement by `\sigma_2` changes:

   * the 3-step low-layer word,
   * the induced return increment,
   * the pilot `U_0` cycle signature / monodromy signature.
     If none of these change, record the sterility lemma and stop the old layer-2-only exact-signature plan.

2. **Main coupled branch.**
   Pick one exact-signature-derived bit `p`:

   * preferably the coarsest exact bit not generated by the named flags,
   * and if the diagnostic finds a dynamically meaningful splitter, use that one first.
     Then:
   * keep canonical anchors fixed,
   * keep one strong cycle-capable layer-2 base fixed,
   * let layer-3 mode depend on `(s_3,p)`,
   * and only if needed, allow one very small synchronized layer-2 flip on one designated local class.

3. **Search target.**
   Find a clean strict mixed witness on `m=5,7,9` with
   [
   \text{total pilot cycle count} < 21,
   ]
   or at least fewer than `m` cycles on one pilot modulus, while keeping nonzero monodromy.

Next branching options:

1. Immediate branch:
   short exact sterility diagnostic for `\sigma_2` under fixed twist / pure alt-4.
2. Main branch:
   geometry–twist coupled mode-switch using a `\sigma_2`-derived bit as a layer-3 controller.
3. Only if that still fails:
   move to a slightly richer exact local-signature state or a minimally synchronized two-layer family, rather than another broad layer-2-only exhaustive search.

Claim status labels:
[P] first mixed regime exists exactly
[C] `013` named third-flag widenings are exact dynamic lifts with no new regime
[H] the next main branch should be coupled, not layer-2-only exact-signature exhaustive search
[F] the old `014` layer-2-only exact-signature branch is the right primary move
[O] the full decomposition problem remains open

This is the rewritten strategic conclusion:

**Keep the program moving, but do not spend the next main search on layer-2-only exact-signature coloring.
First test whether that exact signature is dynamically sterile in the fixed-twist branch, then immediately pivot to a coupled mode-switch where the same local bit is allowed to control twist over a nontrivial base.**
