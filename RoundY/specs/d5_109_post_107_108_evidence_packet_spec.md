# D5 109: Post-107/108 Evidence Packet Spec

This spec records what data should be sent next after reading

- `tmp/d5_107_M3_comparison_theorem.tex`
- `tmp/d5_108_M4_M5_gate_note.tex`

and after running the new `107` formula-support check.

## Executive answer

Do **not** send one blurred “more D5 evidence” packet.

Send three packets in order:

1. **Now:** the closed M3 formula-support packet for `107`.
2. **Next:** an M4 finite-automaton packet on the invariant state space.
3. **Later:** an M5 lift packet only after a concrete graph-level lift
   candidate exists.

The reason is exactly the split proved in `108`:

- M4 has become a local finite-state invariant problem.
- M5 still needs a new geometric lift object.

So the shortest serious progress is to close the explicit M3 formulas now and
then ask for M4 local tables, not for full Hamiltonicity data.

## Packet A: send now

### Goal

Support `107` at the level of explicit formulas, not only bucket-level
comparison.

### Files

- `tmp/d5_107_M3_comparison_theorem.tex`
- `RoundY/theorem/d5_106_intended_quotient_identification_and_comparison.md`
- `scripts/torus_nd_d5_m3_formula_support_107.py`
- `RoundY/checks/d5_109_m3_formula_support_summary.json`
- `RoundY/checks/d5_109_m3_formula_support/per_modulus_formula_validation.json`

### What this packet shows

On regenerated moduli `m=13,15,17`:

1. `q` is recovered exactly from the phase-corner identity.
2. `rho` is extracted exactly from `(B,beta)` by
   `rho = u - q + 1_{beta=m-1}`.
3. `sigma` is extracted exactly from `(B,beta)` by
   `sigma = s - q - I_u(beta) - I_w(beta,q)`.
4. The current raw coordinates `u,w` are reconstructed exactly from
   `(rho,beta,q0,sigma)`.
5. The symbolic two-source collision for bare `(beta,q0,sigma)` is realized on
   every checked modulus.

This is the right packet to send immediately because it validates the actual
formula content of `107`.

## Packet B: request next

### Goal

Attack M4 exactly in the form suggested by `108`: as a finite invariant
automaton problem.

### Data to ask for

For the intended invariant `I = (beta,delta)` or an equivalent descended
invariant, request:

1. colorwise generator readout tables
   `g_c(I) in {0,1,2,3,4}` for `c=0,1,2,3,4`;
2. predecessor transport tables
   `P_j(I) = I(x-e_j)` for `j=0,1,2,3,4`;
3. the local inverse identity data:
   for each color `c` and invariant state `I`, the unique `j` such that
   `g_c(P_j(I)) = j`;
4. a compact histogram of any failures or exceptional states if the formulas do
   not close uniformly.

### Why this is next

`108` proves that once these tables exist, selector descent is purely local on
the invariant state space. So this is the shortest graph-level data request now
matched to the theorem package.

## Packet C: defer

### Goal

M5 Hamiltonicity evidence.

### What to defer until later

Do not ask next for broad full-cycle searches or generic Hamiltonicity output.
Only ask for M5 data once there is a concrete graph-level lift candidate.

At that point the right data request is one of:

1. an intrachain coordinate `tau` over `delta` with the carry update law of
   `108`;
2. or a depth-3 nested return package with three exact successive `m`-step
   returns;
3. plus simplicity of the lifted return segments.

### Why it is third priority

`108` makes the asymmetry explicit:

- M4 already has a finite local target.
- M5 still needs a new geometric lift object.

So M5 is not the next efficient evidence request.

## Bottom line

If sending something today, send Packet A.

If asking for the next computation, ask for Packet B.

Do not spend the next serious push on Packet C unless a concrete graph-lift
candidate has already appeared.
