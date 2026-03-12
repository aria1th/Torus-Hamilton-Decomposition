# Work Template: D5-DEEP-TRANSITION-CARRY-SHEET-046

Task ID: D5-DEEP-TRANSITION-CARRY-SHEET-046

Question:
Can the carry sheet `c = 1_{q=m-1}` be characterized exactly by the smallest future grouped-transition sheet on the checked best-seed active branch, and can that exact sheet be compressed to a theorem-friendly signature such as “initial flat run length + first nonflat grouped delta”?

Purpose:
`045` killed the first carry-only admissible catalogs through current features, 1-step, and 2-step grouped transitions. A direct follow-up check on the frozen active dataset shows that the carry bit is nevertheless exact from a finite future grouped-transition window: the minimal checked horizons are `m-3` for the future `dn` stream and `m-2` for the future grouped-state window. The next honest job is therefore to extract and normalize that deeper transition sheet before reopening admissibility.

Fixed inputs:
- best-seed active branch from `033–045`
- checked moduli `m in {5,7,9,11}`
- grouped base `B=(s,u,v,layer,family)`
- carry sheet target `c=1_{q=m-1}`
- finite-cover normal form `B <- B+c <- B+c+d` from `044`

Allowed methods:
- exact lookahead extraction on the frozen active dataset
- future grouped-delta windows `dn, dn_next, ...`
- future grouped-state windows `B, B_next, ...`
- compression to first-event signatures (flat-run length, first nonflat delta, first non-B event, first carry event)
- minimal-horizon search
- no generic transducer synthesis
- no proof writing yet

Success criteria:
1. Verify the minimal exact future `dn` horizon on the checked moduli.
2. Test whether the horizon is exactly `m-3` on `m=5,7,9,11`.
3. Verify the minimal exact future grouped-state horizon, and test whether it is exactly `m-2`.
4. Compress the exact horizon to the smallest theorem-friendly event signature.
5. Decide whether the exact signature lives entirely in the regular `B` corridor region where `dn=(0,0,0,1)` for an initial run.
6. Save exact collision tables showing failure at horizon `H-1` and success at horizon `H`.

Failure criteria:
- no stable minimal horizon pattern appears across the checked moduli; or
- the exact future signature does not compress beyond a raw length-`m-3` window.

Artifacts to save:
- code
- raw logs
- horizon_exactness_summary.json
- minimal_future_horizons.json
- first_nonflat_signature_summary.json
- failure_at_H_minus_1_tables.json
- success_at_H_tables.json
- representative_ambiguous_states_H_minus_1.json
- representative_exact_states_H.json

Return format:
- minimal exact future `dn` horizon
- minimal exact future grouped-state horizon
- smallest exact compressed future signature
- whether the pattern is `m-3` / `m-2` on the checked moduli
- recommendation for the next admissibility branch

Interpretive target:
A positive result would move the frontier from “broader lifted gauge or deeper transition sheet” to the sharper statement:
> the carry slice is already an exact future-transition event of bounded type on the active grouped base, and admissibility now means coding that event, not inventing new controller logic.
