Task ID:
D5-THETA-PHASE-EVENT-CHECK-058A

Question:
On the active best-seed branch, does the current event law in
  Theta = q + s + v + layer (mod m)
remain exact through the current proof-support range?

Target law to test:
- Theta = 0 -> wrap, dn=(0,0,0,0)
- Theta = 1 -> carry_jump, dn=(1,1,0,0)
- Theta = 2 -> other=(1,0,0,0) iff c=1, else flat
- Theta = 3 -> other=(0,0,1,0) iff (c=0 and s=2) or (c=1 and s!=2), else flat
- Theta in {4,...,m-1} -> flat

Scope:
- checked moduli: m = 13,15,17,19,21,23
- active best-seed branch only
- no new search; pure validation on frozen/support data or regenerated active rows

Outputs:
- analysis_summary.json
- theta_phase_event_checks_058a.json
- sample_failures.json

Purpose:
This does not change the theorem object. It only tests whether the new proof-side
phase scheduler used in 058 persists on the extended support range.
