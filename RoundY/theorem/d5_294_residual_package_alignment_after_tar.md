# D5 294 Residual Package Alignment After Tar Inspection

This note records what changed after inspecting
[tmp/residual_proof_package_2026-03-25.tar](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/tmp/residual_proof_package_2026-03-25.tar)
alongside the current stable `289–293` frontier.

It is not a new closure theorem.
Its job is to say which parts of the package look genuinely useful for the
current resonant program, which parts only restate what is already known, and
how the package changes the next candidate-family choice.

## 1. Main alignment with the current stable frontier

The package does **not** overturn the current `289/291/293` reading.
It sharpens it.

The stable current facts remain:

- the promoted-collar family is now best read as a control/no-go family;
- the pure color-`1` branch should be scored by whether it changes the reduced
  base object, not by local burst counts alone;
- the `B`-active / gate branch should remain a separate branch.

What the package adds is a more concrete positive candidate geometry inside the
pure color-`1` branch.

## 2. Most useful package contribution

The most useful positive item in the package is the same-row collar refinement
on the active rows `r-1` and `r+1`.

In package notation, this is the refinement

- `A_{r-1,3}` or
- `A_{r+1,3}`

added to the current width-`3` / promoted-collar color-`1` branch.

The package claim is not “a new global theorem is already done.”
The useful claim is narrower:

- on the top collar, the added same-row `A` changes the exact block law by a
  single rerouting `e_2 - e_0`;
- on the double-top plane, the same correction appears again;
- so the old top and double-top local obstructions are not rigid.

This is exactly the kind of refinement that the current stable branch needed:
not a broad new family, but a specific local mechanism that visibly changes the
active resonant transducer.

## 3. What this means for the pure color-1 branch

Together with the current stable notes, the package suggests the following read.

### A. The promoted-collar no-go still matters

[d5_289_promoted_collar_base_section_reduction_and_no_go.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_289_promoted_collar_base_section_reduction_and_no_go.md)
still does the right job:

- it turns the current promoted-collar packet into a control family;
- it shows the obstruction is already visible on the reduced base object.

So the package should **not** be read as “go back and keep polishing the same
family.”

### B. The next positive move is more explicit than 293

[d5_293_resonant_support_refinement_search.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_293_resonant_support_refinement_search.md)
showed that support-local refinements can move the reduced resonant object, but
only in a tradeoff-heavy and not-yet-promotable way.

The package suggests a cleaner interpretation of that result:

- the search was probably seeing shadows of a real local mechanism,
- namely collar-row same-row `A` rerouting,
- but only through coarse support surrogates.

So the next search should not just “refine support again.”
It should move to explicit family language that contains this mechanism.

### C. The unresolved object is now lower scattering / base return

The package’s lower-scattering note is compatible with the current base-object
view:

- once top and double-top local obstructions are broken,
- the remaining pure color-`1` issue is a lower-band scattering or base-return
  problem,
- not another top-collar local-burst problem.

This strongly supports the current operational rule from
[d5_291_residual_compute_campaign_conclusion.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_291_residual_compute_campaign_conclusion.md):
judge new families by whether they change the reduced base object.

## 4. A+B versus C+B

The package’s branch notes also help with the next family choice.

For the pure color-`1` sigma-core branch with `5 ∤ m`, the package repeatedly
pushes the same direction:

- favor `A+B` paired families first,
- with the visible row at `t in {r-1, r+1}`,
- and only keep `C+B` as a secondary comparison family.

This is consistent with the current stable picture:

- `A` is color-`1`-visible while preserving color `0`,
- `B` is not itself a color-`1` repairer,
- and the live issue is not “activate any new row” but “activate the right
  visible row, then compensate in a controlled way.”

So the best current operational read is:

- pure color-`1`, `5 ∤ m`:
  start from explicit `A_{r\pm1,3}` refinements and `A+B` paired families;
- `5 | m` hybrid or gate branch:
  keep `B`-active behavior separate and do not merge that branch back into the
  pure color-`1` campaign too early.

## 5. What is still not proved

The package does **not** itself close the resonant residual theorem.

After inspection, the honest remaining gap is still:

- a theorem or exact promoted packet that changes the reduced base object in a
  stable way across the live resonant range, and
- the separate `B`-active / gate splice branch.

So this note is not a promotion of the package to “done.”
It is a correction to the current search focus.

## 6. Updated current recommendation

The next pure color-`1` campaign should now be read in this order:

1. keep `289` as the no-go control packet;
2. keep `293` as evidence that narrow support-local changes can move the
   reduced object;
3. move the next explicit family search to promoted-collar / collar-row
   refinements before broader compensator families;
4. continue to score candidates by reduced base-object change, not by local
   burst improvements;
5. keep the `B`-active / gate branch as a separate branch with separate
   diagnostics.

The immediate follow-up is now
[d5_295_promoted_collar_dualA_vs_singleB_probe.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_295_promoted_collar_dualA_vs_singleB_probe.md),
which sharpens item `3` further:

- a lone extra `B_{s,3}` row is reducedly inert on checked resonant moduli;
- the opposite collar-row `A` move is the first refinement that changes the
  reduced base permutation `P_m`.

So the present note should now be read together with `295`, with the updated
explicit family order:

1. promoted-collar baseline;
2. opposite collar-row `A`;
3. only then additional compensation.

That is the most accurate current synthesis of the tar package with the stable
RoundY frontier.
