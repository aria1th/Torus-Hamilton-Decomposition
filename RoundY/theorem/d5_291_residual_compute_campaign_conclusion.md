# D5 291 Residual Compute Campaign Conclusion

This note promotes the operational conclusions of the `2026-03-25` residual
compute campaign memo into the stable RoundY layer.

It is not a new theorem note.
Its job is to record, in one place, what the current resonant residual program
should ask compute to do.

The two source tmp files behind this note are:

- `tmp/residual_compute_campaign_memo_2026-03-25.tex`
- `tmp/residual_compute_request_template_2026-03-25.md`

The key point is that the current compute frontier is now narrower than a
generic “search for a Hamilton family.”
The right compute question is now:

> which candidate family actually changes the reduced obstruction object,
> rather than merely changing local burst statistics?

## 1. Current operational split

After the current `284/285/286/289/290` layer, the resonant residual work
should be split operationally into two branches.

### A. Pure color-`1` resonant frontier

This is the branch reached by the `51`-type and reduced `69`-type lines.

At the current state:

- width-`1` has a theorem-level obstruction;
- width-`3` has a theorem-level obstruction;
- the promoted-collar family has been locally audited;
- the promoted-collar package further reduces to an induced map on
  `H_m = {c = 0, d = 0}`;
- and the stronger `B_m = {c = 0, d = 0, e = 0}` visibility is now exact
  checked evidence.

So the next compute target for this branch is **not**:

- “improve local bursts,”
- “remove one more top episode,”
- or “search broadly for a breaker.”

It is:

- find a family that actually changes the induced base permutation
  `P_m : B_m -> B_m`.

### B. `B`-active / gate branch

This is the separate branch carrying the old `45`-type and `75`-type behavior.

The operational target here is not a base permutation but a wall/gate splice.

So the next compute target for this branch is:

- identify scaffold families that produce the right wall / near-miss geometry;
- then identify gate families that splice that wall back into the bulk cycle
  and ideally also kick the residual color-`1` behavior.

## 2. What changed relative to 288/289

[d5_288_next_closable_piece_priority.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_288_next_closable_piece_priority.md)
recorded the best next mathematical fragment as the promoted-collar
base-section reduction / no-go theorem.

[d5_289_promoted_collar_base_section_reduction_and_no_go.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_289_promoted_collar_base_section_reduction_and_no_go.md)
then sharpened that picture by showing that the current promoted-collar family
is already an explicit reduced no-go packet on the checked resonant moduli.

The present note is the operational consequence:

- the current promoted-collar family is now a **control family**, not the next
  discovery family;
- the next pure color-`1` compute campaign must therefore aim at changing
  `P_m`, not at polishing the same promoted-collar packet further;
- and the `B`-active / gate branch should be handled as a separate campaign
  with separate diagnostics.

## 3. Control families that must stay in every campaign

For the pure color-`1` branch, the minimal control atlas is:

- the canonical width-`1` family;
- the canonical width-`3` family;
- the promoted-collar family
  `\widehat{\mathfrak N}_m^{(u)}` with `u in {r-1, r+1}`.

For the `B`-active / gate branch, the minimal control family is:

- the current sigma-core / scaffold package nearest to the candidate branch.

The practical rule is:

- no candidate family should be interpreted in isolation;
- it must always be compared against the nearest control family on the same
  branch.

## 4. Acceptance criteria for the next compute round

The current campaign should not use Hamiltonicity as its first acceptance test.

The first real acceptance tests are structural.

### A. Pure color-`1` branch

Promote a candidate only if it does at least one of the following:

- changes the cycle structure of `F_m : H_m -> H_m`;
- changes the cycle structure of `P_m : B_m -> B_m`;
- or decreases the number of cycles of `P_m` consistently across the checked
  resonant range.

If a candidate only changes local burst counts while leaving `P_m` unchanged,
it should be treated as non-progress.

### B. `B`-active / gate branch

Promote a candidate only if it does at least one of the following:

- changes the wall / near-miss geometry in a persistent way;
- produces a gate destination that genuinely splices the wall into the bulk;
- or produces a visible transversal kick on the residual color-`1` branch.

If a candidate only produces a prettier local wall picture with no splice, it
should be treated as non-progress.

## 5. Recommended campaign order

The memo-level recommended campaign order is now:

1. regression on controls and current seed families;
2. atlas extension on the next resonant range;
3. pure color-`1` base-splicer sweep at `k = 3`;
4. base-visible one-line `k = 4` sweep;
5. `B`-active scaffold + gate sweep;
6. promotion dump only for candidates that genuinely change `P_m` or wall/gate
   geometry.

This order should now be treated as the default operational plan for residual
compute work unless a narrower branch-specific reason overrides it.

## 6. Relation to the current assumption audit

[d5_290_current_assumption_and_gap_audit.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_290_current_assumption_and_gap_audit.md)
separates:

- theorem-level closed content,
- imported theorem background,
- checked exact packets,
- and the genuinely open resonant residual theorem.

The present note sits on the compute side of that audit.

It says:

- how to interrogate the checked resonant packets next,
- how not to confuse local improvement with real progress,
- and how to decide whether a new family is worth promotion.

## 7. Bottom line

The residual compute frontier is no longer:

- a broad five-color search,
- a local-burst cleanup task,
- or a generic one-family Hamilton hunt.

It is now a branchwise comparative campaign with two different reduced targets:

- for the pure color-`1` branch, change the induced base permutation `P_m`;
- for the `B`-active / gate branch, realize an actual wall/gate splice.

That is the most accurate current operational reading of the resonant residual
program.
