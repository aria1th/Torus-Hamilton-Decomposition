Task ID:
D5-PHASE-SCHEDULER-SUPPORT-059A

Question:
Can the active phase-event scheduler of 059 be machine-confirmed through the next odd moduli beyond 23, using the exact current-state rule in
    (Theta, s, c)
with
    Theta = q + s + v + layer mod m,
    c = 1_{q=m-1},
and with the explicit mixed_008 layer-3 condition
    pred_sig1_wu2 <-> s=2?

Purpose:
059 gives a proof-form derivation of the scheduler from the mixed witness rule.
A narrow support pass on a few larger odd moduli would strengthen confidence that no hidden active-branch exception was missed.

Requested checks:
1. Verify the exact scheduler table on m in {25,27,29}.
2. Verify that every active nonterminal state is still B-labeled.
3. Verify that for color 0 on the active branch,
       pred_sig1_wu2 = 1 iff s = 2.
4. Save one compact JSON summary and one representative witness table per modulus.

Return format:
- exact / not exact per modulus
- first failure witness if any
- active-label summary
- predecessor-flag equivalence summary

This is optional support only.  The proof object does not change.
