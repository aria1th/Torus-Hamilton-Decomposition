# D5 293 Resonant Support Refinement Search

This note records the first autonomous search run carried out directly from the
`291/292` campaign split.

The purpose was not to search the whole residual family space again.
The purpose was to test a narrower question:

> if we freeze the current exact control family and only allow changes on
> promoted-collar-support classes, does the reduced resonant color-`1` object
> actually move?

The answer is yes, but not yet in a promotion-ready way.

The main artifacts are:

- [d5_293_resonant_support_refinement_search_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_293_resonant_support_refinement_search_summary.json)
- [search.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_293_resonant_support_refinement_search/search.json)
- [changed_support_classes.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_293_resonant_support_refinement_search/changed_support_classes.json)
- [alternate_m9_first_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_293_resonant_support_refinement_search/alternate_m9_first_summary.json)
- [torus_nd_d5_resonant_support_refinement_search_293.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_resonant_support_refinement_search_293.py)

## 1. Search setup

The search starts from the best exact family found in the older
line-bit search `281`.

It then freezes the bulk rule and only allows changes on a promoted-collar
support surrogate:

- top interior
- double-top interior
- top hinge
- double hinge

In practice this means:

- exactness is still enforced by the finite local CSP on small moduli;
- only the promoted-support classes are allowed to change;
- and the score is no longer “how many Hamilton colors?” but rather the
  cycle structure of the color-`1` `P0` return on resonant moduli.

So this is already a case-reduced search in the precise sense suggested by
[d5_291_residual_compute_campaign_conclusion.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_291_residual_compute_campaign_conclusion.md).

The stable `15`-first run used:

- search moduli `7,9,11`
- evaluation moduli `15,9`
- promotion check modulus `13`

The resulting class space has:

- `112` support-refined free keys,
- coming from `80` coarse support base keys.

## 2. First main result: support-only refinements are not vacuous

The search does produce candidates that genuinely improve the reduced resonant
color-`1` object.

Relative to the frozen control family, the best `15`-first candidate changes the
color-`1` `P0` return as follows:

- control at `m=15`: `171` cycles, largest cycle `19127`
- best support-refined candidate at `m=15`: `166` cycles, largest cycle `27661`

So the reduced resonant object is not rigid under these support-local
refinements.

This matters because it rules out the pessimistic reading:

- “once the promoted-collar package is fixed, nothing short of a much broader
  search can change the resonant base behavior.”

That pessimistic reading is false.

## 3. Second main result: the improvement is not yet stable

The same best `15`-first candidate does **not** yet promote.

Two reasons are already visible.

### A. The gain is not uniform across resonant controls

For the same candidate:

- at `m=15`, the cycle count improves from `171` to `166`;
- at `m=9`, the cycle count stays at `51`, and the largest cycle drops from
  `5548` to `2559`.

So this candidate is not a clean all-resonant improvement.

### B. Exactness already fails at the next promotion modulus

The promotion check at `m=13` fails with the explicit witness:

- target `y = (11,0,11,11,9)`
- incoming colors `[1,1,2,3,4]`

So the candidate is not yet a promoted residual theorem candidate.

## 4. Third result: there is a real Pareto split

The search was also run in an alternate `9`-first scoring order.

That alternate run, saved in
[alternate_m9_first_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_293_resonant_support_refinement_search/alternate_m9_first_summary.json),
found the opposite type of candidate:

- at `m=9`, the cycle count improves from `51` to `43`;
- but at `m=15`, it worsens from `171` to `175`.

So the current support-only search does not point to one universal winner.
It points to a genuine tradeoff:

- one candidate improves the `15`-type resonant object,
- another candidate improves the `9`-type resonant object,
- neither one is exact enough to promote.

This is strong evidence that the next refinement needs one more local bit,
not a broader uncontrolled family.

## 5. Where the changes actually concentrate

Although the support-refined family had `112` free support keys, the best
`15`-first candidate changes only `41` of them relative to control.

The changed classes are saved in
[changed_support_classes.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_293_resonant_support_refinement_search/changed_support_classes.json).

The changes are not spread uniformly.
They cluster mainly on:

- `S3(0)` and `S3(1)` support classes,
- `S4+` support classes,
- and a narrow set of `S2` support classes such as
  `S2({0,2})`, `S2({2})`, `S2({1,2,4})`, `S2({2,3})`,
  together with a few hinge-specific variants.

So the next refinement should not reopen all support classes uniformly.
It should start from this much smaller changed-class cluster.

## 6. Current interpretation

This search does **not** finish the resonant residual theorem.

But it does give three concrete conclusions.

1. The `291` operational split was correct:
   the right current score is a reduced resonant object, not broad Hamiltonicity.
2. Support-only promoted-collar refinements can already move the reduced
   resonant color-`1` return in a substantial way.
3. That movement is not yet stable across resonant controls and not yet exact at
   the next promotion modulus, so one more local distinction is still missing.

## 7. Practical next step

The next search should now be narrowed again.

Instead of:

- freeing all promoted-support classes,

it should:

- freeze the unchanged support classes,
- keep only the changed-class cluster from `293`,
- and add one further local bit aimed specifically at separating the
  `m=13` failure witness and the `9`-vs-`15` tradeoff.

So `293` should be read as:

> the first case-reduced evidence that the current resonant obstruction can be
> moved by a narrow support-local refinement, but that one more local phase
> distinction is still needed before promotion.
