Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field, and break the remaining return-dynamics bottleneck after the exact tail-bit refinements.

Current target:
Absorb `D5-LAYER3-ALT2-DECOUPLED-007`, identify exactly what it rules out, and choose the smallest next family that is still genuinely live.

Known assumptions:

* I unpacked the bundle and read:

  * `README.md`
  * `data/search_summary.json`
  * `data/validation_summary.json`
  * `data/validation_candidates.json`
* Exact searched family:

  * ordered pair `(s_2,s_3)` from
    [
    S={q=-1,\ q+u=1,\ w+u=2,\ q+u=-1,\ u=-1}
    ]
  * layer 2: seed anchor `2`, alternate `a\in\{0,3,4\}`, `s_2`-only, orientations `2/a` and `a/2`
  * layer 3: seed anchor `3`, alternate `b\in\{0,2\}`, `s_3`-only, orientations `3/b` and `b/3`
  * `phase_align,b_1,b_2` excluded
* Exact pilot outcome on `m=5,7,9`:

  * rules searched: `600`
  * clean survivors: `360`
  * strict survivors: `360`
  * combined cycle+monodromy survivors: `0`
  * cycle-only survivors: `296`
  * monodromy-only survivors: `32`
  * trivial survivors: `32`
* All `360` clean survivors were revalidated on the full torus and all five colors, and every clean survivor is also strict in this family.
* Extra classification from the validated survivor tables:

  * the clean/strict survivor set factors exactly as
    [
    \mathcal S_{\mathrm{surv}}=\mathcal S_2\times \mathcal S_3,
    \qquad |\mathcal S_2|=20,\ |\mathcal S_3|=18,
    ]
    so clean/strict survivorship is completely layer-factorized here.
  * the `20` surviving layer-2 patterns are the same `20` from Session 24.
  * the `18` surviving layer-3 patterns are:

    * `10` alt-`0` patterns: all `5` old bits times `2` orientations;
    * `8` alt-`2` patterns: only the four-bit pool
      [
      T={q=-1,\ q+u=1,\ q+u=-1,\ u=-1}
      ]
      times `2` orientations.
    * so there is **no** clean layer-3 alt-`2` survivor with `s_3=w+u=2`.
* The non-cycle regimes obey an exact trichotomy:

  * if layer 3 uses alt `0`, the survivor is always cycle-only;
  * if layer 3 uses alt `2` and layer 2 uses alt `0`, then same-sign orientation coupling gives monodromy-only;
  * if layer 3 uses alt `2` and layer 2 uses alt `3`, then same-sign orientation coupling gives trivial `U_0`;
  * all remaining surviving combinations are cycle-only.
* Here “same-sign orientation” means both layers use seed/alternate in the same order on `s=0,1`; concretely:

  * monodromy-only:
    [
    (0/2,\ 2/3)\quad\text{or}\quad(2/0,\ 3/2)
    ]
  * trivial:
    [
    (2/3,\ 3/2)\quad\text{or}\quad(3/2,\ 2/3).
    ]
* The monodromy-only regime has exactly two pilot signatures:

  * all fixed points with uniform monodromy `+1`;
  * all fixed points with uniform monodromy `-1`;
    orientation flips the sign.
* There are `5` distinct cycle-only pilot signatures in the validated set.
* The best cycle-only witnesses remain those with layer-2 split `w+u=2` and alternate `4`; representative rules have total pilot `U_0` cycle count `15`, with no monodromy, e.g.

  * on `m=9`, one signature gives `3` cycles of lengths `(22,22,37)`;
  * another gives `3` cycles of lengths `(25,25,31)`.
    The bundle README states this matches the strongest known cycle mechanism rather than improving beyond it.
* Scope note:

  * the `600/360/296/32/32/0` counts are bundle-backed;
  * the exact factorization (\mathcal S_2\times\mathcal S_3), the absence of layer-3 alt-`2` survivors for `w+u=2`, and the trichotomy above come from my direct pass over `validation_summary.json`;
  * I did not rerun the exhaustive search from scratch in this turn.

Attempt A:
Idea:
Read `007` as an exact no-go for the entire decoupled two-old-bit family with layer-3 palette `{0,2}`.

What works:

* This closes the specific Session 25 target cleanly.
* The negative result is sharper than “no combined witness was found.”
* Clean/strict survivorship itself factorizes:
  [
  \mathcal S_{\mathrm{surv}}=\mathcal S_2\times\mathcal S_3.
  ]
* So in this family there is no hidden clean-frame interaction still waiting to be uncovered; the only remaining interaction is in the return-dynamics classification.
* The alt-`2` enrichment is genuinely live, because it restores monodromy-only witnesses.
* But it never combines the cycle mechanism and the monodromy mechanism in one rule.

Where it fails:

* This does not rule out a layer-3 rule with one extra local flag.
* It also does not rule out a small layer-3 finite transducer state.
* So it kills the pure decoupled `s_2`-only / `s_3`-only family, not the next minimal layer-3 enrichment.

Attempt B:
Idea:
Use the exact trichotomy to identify the smallest next live branch: keep layer 2 fixed and add one extra local flag on layer 3 so that layer 3 can switch between a cycle-preserving mode and a monodromy-producing mode.

What works:

* The data now show that layer 3 does not need a bigger anchor palette; `{0,2}` is already enough.
* What is missing is a **mode switch** inside layer 3.
* A single old bit `s_3` is too coarse: it can place the system globally into one of three regimes

  * cycle-only,
  * monodromy-only,
  * trivial,
    but it cannot mix them across local contexts.
* The most informative fixed layer-2 base is not the strongest `4`-alternate cycle seed, but one of the **bifurcation-capable** `0/2` or `2/0` cycle splits on the four-bit pool `T`, because those are exactly the layer-2 rules that already admit both cycle-only and monodromy-only behavior depending on layer 3.
* This makes the next family much smaller than a fresh global search:
  layer 2 can be fixed, and all new freedom can be pushed into layer 3.

Where it fails:

* We do not yet know which extra layer-3 flag is sufficient.
* A predecessor-tail flag is the first natural candidate, but it has not yet been tested in this layer-3-only mode-switch form.
* If no such one-flag family works, then the next step would be a two-bit layer-3 local state, not more decoupled old-bit scans.

Candidate lemmas:

* [C] In `007`, every clean survivor is strict on `m=5,7,9`.
* [C] In `007`, the clean/strict survivor set factors exactly as
  [
  \mathcal S_{\mathrm{surv}}=\mathcal S_2\times\mathcal S_3
  ]
  with `20` layer-2 patterns and `18` layer-3 patterns.
* [C] The surviving layer-3 alt-`2` patterns use only the four-bit pool
  [
  T={q=-1,\ q+u=1,\ q+u=-1,\ u=-1};
  ]
  `w+u=2` never survives on layer 3 with alt `2`.
* [C] The decoupled `{0,2}` layer-3 family yields exactly three pilot dynamical regimes:
  cycle-only, monodromy-only, and trivial, but never combined cycle+monodromy.
* [C/H] Same-sign coupling with layer-3 alt `2` has a deterministic effect depending on the layer-2 alternate:

  * alt `0` gives monodromy-only,
  * alt `3` gives trivial,
  * alt `4` stays cycle-only.
* [H] Therefore the next minimal live branch is not a larger anchor palette, but a layer-3 mode switch using one extra local flag.
* [H] The most promising base for that mode switch is a fixed bifurcation-capable layer-2 split from the alt-`0` family, not a fresh two-layer search.
* [F] The decoupled two-old-bit family with layer-3 palette `{0,2}` can already combine cycle structure and nonzero monodromy.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* Fix one bifurcation-capable layer-2 cycle split, preferably from
  [
  T={q=-1,\ q+u=1,\ q+u=-1,\ u=-1},
  ]
  with alternate `0` and orientation `0/2` or `2/0`.
  These are exactly the layer-2 rules that already support both cycle-only and monodromy-only behavior depending on layer 3.
* Keep layer 2 fixed during the first next search.
* On layer 3, choose one representative old bit (s_3\in T). Since the four live bits behaved interchangeably in the monodromy/trivial regime counts, it is reasonable to start with `q=-1` as the representative and only widen if necessary.
* Add one extra layer-3 local flag (p). First natural candidate pool:

  * `pred_any_phase_align`
  * `pred_sig0_phase_align`
  * `pred_sig1_wu2`
  * `pred_sig4_wu2`
    from the earlier predecessor-bit session.
    If all fail, replace this pool by an exact predecessor-tail local-signature bit.
* Let layer 3 depend on `(s_3,p)` and choose between the already validated modes:

  * cycle-preserving modes: `0/3`, `3/0`
  * monodromy-capable modes: `2/3`, `3/2`
  * optional control: constant `3`
* Primary target:
  find a clean strict witness on `m=5,7,9` with both

  * some cycle length `>1`,
  * some nonzero monodromy.
* Since `clean ⇒ strict` held everywhere in `007`, the search can prune by clean-frame first and treat strict clock as a validation check rather than a primary optimization objective.
* If every one-flag layer-3 family still lands only in the three old regimes, then the next exact family should be:
  a two-bit layer-3 local state over `(s_3,p)` or `(p_1,p_2)` with palette `{0,2,3}`.

Next branching options:

1. Main branch:
   fix one bifurcation-capable layer-2 split and search a layer-3-only one-extra-flag mode-switch family.
2. Secondary branch:
   if no predecessor-tail flag works, replace it by an exact predecessor-tail local-signature bit.
3. Side theorem branch:
   formalize the `007` trichotomy theorem for the whole decoupled `{0,2}` family.

Claim status labels:
[P] `007` exhausts the exact decoupled two-old-bit family with layer-3 palette `{0,2}` on `m=5,7,9`
[C] `360` clean survivors = `360` strict survivors, split as `296` cycle-only, `32` monodromy-only, `32` trivial, `0` combined
[C] the clean/strict survivors factor exactly as `20` layer-2 patterns times `18` layer-3 patterns
[C] layer-3 alt `2` is live only on the four-bit pool `T`, and same-sign coupling gives the exact three-regime law
[H] the next smallest live branch is a layer-3-only mode switch with one extra local flag over a fixed bifurcation-capable layer-2 split
[F] the decoupled two-old-bit `{0,2}` family can already combine cycles and monodromy
[O] the full Hamilton decomposition problem remains open

The sharpest update is:
`007` did not merely say “alt-2 still fails.” It exposed the exact decoupled trichotomy. Layer 3 already has the right palette; it lacks one extra local flag to switch between the cycle-preserving and monodromy-producing modes. The smallest honest next move is therefore a layer-3-only mode-switch search over a fixed bifurcation-capable layer-2 split.
