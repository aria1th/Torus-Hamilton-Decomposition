# D5 Compute Branch `049/050`

## Question

While the proof branch packages `044–048`, what are the highest-value compute
extensions of the current D5 theorem chain?

## Chosen split

Use the `049/050` split from the new notes.

1. `049`: push the stronger source-residue refinement as far as it remains
   exact.
2. `050`: run the two narrow proof-support checks from
   `./specs/d5_parallel_compute_requests_050.md`.

## Main results

### `049`

Through `m = 5,7,9,11,13,15,17,19`:

- `tau` is minimally exact on `(s,u,v,layer,rho)`
- `next_tau` is minimally exact on `(s,u,layer,rho,epsilon4)`
- `c` is minimally exact on `(u,rho,epsilon4)`
- `q ≡ u - rho + 1_{epsilon4=carry_jump} mod m`

This is a stronger current-state constructive refinement, not an equivalent
reparametrization of `(B,tau,epsilon4)`.
`rho` is not recoverable from `(B,tau,epsilon4)` for `m>=7`, and the
ambiguous bucket count matches `2m-11` on the tested extended range.

### `050`

Through the same range:

- the `048` reset law persists exactly on the same theorem-side quotients
- the explicit `047/048` lower-bound witness pair persists exactly

So the proof branch now has larger-modulus support for both:

- the small boundary reset law, and
- the bounded-horizon witness family.

## Meaning

The stable split is now:

- theorem side:
  keep the minimal object `(B,tau,epsilon4)`
- compute side:
  use `(B,rho)` aggressively as a stronger current-memory route
- proof support:
  use `050` to justify that the reset law and the witness family are not
  fragile pilot artifacts
