# Small parallel compute requests after 049

These are the highest-value compute checks for the proof branch. They are intentionally narrow.

## A. Reset-law generalization

Goal:
check whether the boundary reset laws from `048` stabilize in a theorem-friendly form on larger odd moduli.

Target objects:
- `carry_jump -> next_tau` as a function of `(s,v,layer)`
- `other -> next_tau` as a function of `(s,u,layer)`
- global boundary reset map on `(epsilon4,s,u,v,layer)`

Suggested moduli:
- `m = 13,15,17`

What to save:
- exactness summary by modulus
- representative reset tables
- collision witnesses if exactness fails
- any detected closed-form pattern for reset values

Why it matters:
this is the smallest positive proof route for `tau`.

---

## B. Bounded-horizon witness persistence

Goal:
verify that the explicit witness family from the checked range persists for larger odd moduli.

Expected pattern:
\[
x^-_m=(m-2,2,1,2,0),
\qquad
x^+_m=(m-1,2,1,2,0),
\]
with common
\[
B_*=(3,1,2,0,\mathrm{regular}),
\qquad
\epsilon_4=\mathrm{flat},
\]
carry labels
\[
0,1,
\]
and anticipation times
\[
m-3,\ m-4.
\]

Suggested moduli:
- `m = 13,15,17,19`

What to save:
- exact table of the pair by modulus
- first failing horizon for `B + epsilon4 + future_binary_after_current_prefix`
- compact witness JSON suitable for a proof appendix

Why it matters:
this is the best current route to a real lower-bound theorem.

---

## C. Source-residue refinement check

Goal:
stress-test the checked refinement
\[
\rho = u_{\mathrm{source}}+1 \pmod m,
\]
and the relations
\[
\tau \text{ exact on } (s,u,v,layer,\rho),
\qquad
c \text{ exact on } (u,\rho,\epsilon_4),
\]
\[
q \equiv u-\rho + \mathbf 1_{\{\epsilon_4=\mathrm{carry\_jump}\}} \pmod m.
\]

Suggested moduli:
- `m = 13,15,17`

What to save:
- exactness summary by modulus
- collision witnesses if any fail
- note whether `rho` remains unrecoverable from `(B,tau,epsilon4)`

Why it matters:
this is the strongest constructive refinement, but it should remain a remark rather than the main theorem object unless it becomes uniform.

---

## D. Do not spend time on

- broad one-bit scans
- generic tiny-transducer widening
- direct search for the residual sheet `d`
- more current-only grouped-descending gauges

Those are already below the live frontier.
