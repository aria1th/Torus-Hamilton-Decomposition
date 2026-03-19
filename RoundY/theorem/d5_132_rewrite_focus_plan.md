# D5 odd-m rewrite: what to focus on proving next

## Executive decision

If the paper is rewritten around the cleaner **one-cornered odometer** viewpoint, then the proof effort should **not** be distributed evenly across old `M1`--`M6`.
The right focus is:

1. **Front-end one-corner reduction theorem** (new main target)
2. **Colorwise selector-compatibility theorem** linking the closed color-4 branch to the final decomposition theorem
3. **A transfer theorem for the remaining colors** (best case: cyclic/rotational transport; fallback: attack color 3 next)

Everything else should be treated as either already closed or demoted to appendix / historical no-go.

---

## What is already closed enough to sit in the main proof spine

### A. Odometer spine (theorem side)
Already good enough for the main text:
- corrected M2/M3 anchor package (`125`)
- theorem-side intended quotient fixed to `(B,beta)` (`126`)
- historical local provenance is explicitly false in checked range and should not be used (`127`)

This means the theorem-side core should now be written as a **single exact odometer-spine chapter**, not as a live frontier.

### B. One graph-side Hamilton branch
Already good enough for the main text:
- corrected selector existence on `SelCorr` (`117`)
- color-4 surgery branch `SelStar` and its nested-return / final-section proof (`119`--`122`)

This means the paper already contains one complete model example of the graph-side Hamilton mechanism.

### C. Globalization
The odd-`m` globalization / generic upgrade input is already imported and stable.

---

## What should become the actual proof targets

## Target 1. Front-end one-corner reduction theorem

### What to prove
Replace the old split placeholders
- `032` best-seed isolation
- `033` non-trigger defect classification

by a **single cleaner theorem**:

> Every unresolved odd-`m`, `d=5` front-end instance reduces, after the accepted static repairs and symmetries, to one oriented bridge-type one-corner seed.

Then the numerical representative `[2,2,1]/[1,4,4]` can be a corollary, not the headline theorem.

### Why this is the right focus
- It is now the **only real theorem-side gap**.
- It matches the odometer narrative much better than artifact labels `032/033`.
- It absorbs the result of `131`: the numeric seed is not the difficult part; the difficult part is the endpoint-word shape classification.

### What not to do here
- Do not prove `032` only as a raw numeric seed claim.
- Do not keep the front-end as artifact-by-artifact bookkeeping in the main text.

---

## Target 2. Colorwise selector-compatibility theorem

### What to prove
Construct a **colorwise graph package** compatible with the closed color-4 branch.
In practical terms, prove a theorem of the form:

> There exist five local color rules `g_0,...,g_4` such that
> - outgoing exhaustiveness holds pointwise,
> - incoming uniqueness holds for each color,
> - the induced global maps are torus permutations,
> - and `g_4` is exactly the already-closed `SelStar` color-4 rule.

This is the real bottleneck between the closed color-4 Hamilton theorem and the final decomposition theorem.

### Why this is the right focus
- The old demand for one common selector family is stronger than necessary.
- The paper already knows a good M4 package (`SelCorr`) and a good M5 branch (`SelStar` color 4), but these still need to be joined in the weaker colorwise sense.
- Without this compatibility theorem, the closed color-4 branch cannot yet sit inside the final theorem cleanly.

### What not to do here
- Do not return to raw selector compression.
- Do not try to recover historical local provenance.
- Do not insist on one common selector family unless a proof forces it.

---

## Target 3. Remaining-color transfer theorem

### Preferred version
Try to prove a **rotation / conjugacy / transported-surgery theorem**:

> The color-4 surgery mechanism has cyclicly shifted analogues for the other colors, and the nested-return proof transports accordingly.

If this works, the paper gets the remaining Hamilton branches in one conceptual stroke.

### Fallback version
If no clean transport theorem appears, attack the next strongest branch directly:
- **color 3 on SelStar**.

### Why this is the right focus
- The final generic-upgrade theorem still wants Hamiltonicity for all five global color maps.
- The closed color-4 proof gives the template; the next efficient move is to reuse that template, not to start unrelated brute-force searches.

---

## What should be demoted or removed from the main proof

These should appear only as appendix material, side remarks, or historical no-go notes:

1. future-word separation as the theorem-side exact state
2. `Q_tau` / `Q_fw` historical provenance recovery
3. raw selector compression as the main M4 route
4. any attempt to force a single common selector family before it is needed

---

## Recommended manuscript structure after the rewrite

## Part I. Front-end one-corner reduction
- static repairs
- one-corner front-end theorem
- normalized representative as corollary

## Part II. Exact odometer spine
- marked carry-jump object
- anchor rigidity
- exact quotient `(B,beta)`

## Part III. Selector surgery
- clean selector baseline
- defect-slice correction
- colorwise selector package theorem

## Part IV. Hamilton branch
- closed color-4 branch in full detail
- transfer theorem to remaining colors, or direct color-3 next

## Part V. Generic upgrade and globalization
- colorwise descent
- return-cycle lift
- final Hamilton decomposition theorem

---

## Concrete priority order for proof work

1. **Front-end one-corner reduction theorem**
   - this is the cleanest replacement for the old `032/033` frontier
2. **Colorwise selector-compatibility theorem**
   - this is the cleanest bridge from the closed color-4 branch to the final theorem
3. **Transport the color-4 Hamilton proof to other colors**
   - preferred: one transport theorem
   - fallback: color 3 next

---

## Bottom line

While rewriting, the paper should be organized around the statement:

> `d=5`, odd `m` is a one-cornered odometer with a finite selector surgery and a final low-dimensional stitching theorem.

Under that viewpoint, the two proof targets that deserve the most attention are:
- the **front-end one-corner reduction theorem**, and
- the **colorwise selector-compatibility / transfer package**.

Those are the places where new proof work changes the final theorem.
Everything else is either already closed or should be pushed out of the proof spine.
