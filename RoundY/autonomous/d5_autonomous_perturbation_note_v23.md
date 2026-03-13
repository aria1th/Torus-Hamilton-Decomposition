# D5 Autonomous Perturbation Note v23

Artifact `048` closes the autonomous `047A` question on the checked active
branch.

The useful point is that `tau` is no longer just “the hidden datum from 047.”
It already has an exact internal dynamics:

- for `tau > 0`, it is a strict countdown;
- only the boundary `tau = 0` is nontrivial;
- that boundary reset is tiny and current-state driven:
  `wrap -> 0`,
  `carry_jump` on `(s,v,layer)`,
  `other` on `(s,u,layer)`.

So the live local problem is narrower again. The next branch should not talk
about coding a future window. It should talk about coding a countdown carrier
with a small reset micro-law.

This is good for both branches:

- proof branch:
  `044–048` now read as one clean chain from finite-cover structure to
  anticipation, then to internal carrier dynamics;
- local branch:
  the target is smaller and more mechanical than before.

The remaining open issue is still admissibility, not reduced dynamics.
