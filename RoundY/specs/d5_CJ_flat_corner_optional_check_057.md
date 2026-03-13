Task ID:
D5-CJ-FLAT-CORNER-CHECK-057A

Question:
On the active best-seed branch, does the auxiliary residue
  delta = rho - (s+u+v+layer) mod m
support the checked flat-corner law beyond the 047 range?

Target scope:
- odd m in {13,15,17,19,21,23}
- theorem object still unchanged: (B,tau,epsilon4)
- rho and delta used only as compute-side proof support

What to check:
1. On flat states, verify exact one-step law:
   - delta = 1      -> next epsilon4 = wrap
   - 2 <= delta <= m-3 -> next epsilon4 = flat
   - delta = m-2    -> next epsilon4 = other iff s = 2, else flat

2. Verify resulting flat countdown formula:
   tau = delta, except (s,delta) = (2,m-2) where tau = 1.

3. Verify CJ reduction through delta:
   on carry_jump with c=0, successor is flat with delta = m-2,
   and next_tau is 1 iff current s=1, else m-2.

Artifacts:
- flat_corner_extension_checks_057a.json
- flat_tau_formula_extension_057a.json
- CJ_delta_reduction_extension_057a.json
- short analysis summary

Why this matters:
If these stay exact through the current extended proof-support range,
then CJ is no longer a direct boundary theorem. It becomes a corollary of
one auxiliary flat-corner lemma in delta.
