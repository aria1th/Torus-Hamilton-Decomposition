I pushed the proof side forward and recentered it the way you wanted: `046` as the conceptual theorem, `047` as the boundary sharpening.

Files:

* [Proof-progress note](./theorem/d5_tau_admissibility_no_go_proof_progress_048.md)
* [LaTeX theorem snippet](./theorem/d5_tau_admissibility_no_go_proof_progress_048.tex)
* [Per-modulus horizon pattern extracted from 047](./checks/d5_047_per_modulus_horizon_pattern.json)

The strongest new proof progress is this.

First, the clean canonical form on the checked data is better than the checked-range `min(\tau,8)` summary. For each checked modulus (m\in{5,7,9,11}), the frozen `047` data already supports the sharper per-modulus form
[
B+\min(\tau,m-3)+\epsilon_4,
]
and equivalently the first exact transition-sheet coding
[
B+\epsilon_4(\text{current})+\beta_{m-4},
]
where (\beta_h) is the next (h) future flat/nonflat bits after the current step.

Second, those horizons are not arbitrary. On the checked moduli, the first exact horizons are:
[
\text{current }\epsilon_4+\text{future binary after current}: m-4,
]
[
\text{full }\epsilon_4\text{-event window}: m-3,
]
[
\text{pure binary flat/nonflat window}: m-1.
]

Third, there is now an explicit lower-bound witness family, not just a search failure. On each checked modulus, the active branch contains the pair
[
x^-_m=(m-2,2,1,2,0),\qquad x^+*m=(m-1,2,1,2,0),
]
with common grouped base
[
B**=(3,1,2,0,\mathrm{regular}),
]
common boundary class
[
\epsilon_4=\mathrm{flat},
]
but opposite carry labels
[
c(x^-_m)=0,\qquad c(x^+_m)=1,
]
and anticipation times
[
\tau(x^-_m)=m-3,\qquad \tau(x^+_m)=m-4.
]

That gives a real no-go direction:

for every (h<m-4), these two states agree on
[
(B,\epsilon_4,\beta_h)
]
but have different carry labels. So no coding that only sees current (B), current (\epsilon_4), and the next (h) future flat/nonflat bits can be exact on that modulus.

That is the first theorem-shaped obstruction beyond the raw search logs.

So the proof fork is now extremely sharp:

* positive route: prove an admissible/local coding theorem for (\tau) (or equivalently for (\min(\tau,m-3)) plus the (\tau=0) boundary class);
* negative route: prove a reduction lemma showing the intended local/admissible mechanism class factors through a bounded-horizon grouped transition sheet, then apply the witness family above.

That reduction lemma is the exact missing proof gap now. Without it, we do not yet have a full impossibility theorem for the intended local class. But we do now have a concrete theorem candidate:

**no fixed bounded future-transition horizon can code the carry sheet uniformly in (m).**

That is genuine proof progress, and it uses `046` as the conceptual center rather than `047`.

The next proof note I would write is the reduction-lemma attempt:
“intended admissible/local observables collapse to bounded grouped transition data of depth (h),” because that is now the shortest route to a real no-go theorem.
