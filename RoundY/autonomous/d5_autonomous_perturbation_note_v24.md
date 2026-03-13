# D5 Autonomous Perturbation Note v24

Artifact `049` strengthens the compute side without changing the theorem-side
object.

The useful point is that the old source-memory intuition is now exact far past
the pilot range. Through `m=19`:

- `tau` is minimally exact on `(s,u,v,layer,rho)`,
- `next_tau` is minimally exact on `(s,u,layer,rho,epsilon4)`,
- `c` is minimally exact on `(u,rho,epsilon4)`,
- and `q ≡ u - rho + 1_{epsilon4=carry_jump} mod m`.

So the theorem-side anticipation carrier has a genuine stronger
current-state refinement.

The important caution is still the same one from `feedback_s63`:
this does **not** replace `(B,tau,epsilon4)` as the paper’s main object.
`rho` is not recoverable from that theorem-side cover once `m>=7`; on the
tested range the ambiguous bucket count matches `2m-11`.

So the stable split is now:

- proof branch:
  keep the minimal `(B,tau,epsilon4)` chain;
- compute branch:
  exploit `(B,rho)` as a stronger constructive current-memory route.
