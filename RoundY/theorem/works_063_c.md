I read the bundle and I do **not** see a complete proof or a counterexample to the full D5 frontier. The problem has really narrowed to this: either code the countdown carrier `\tau` locally, or prove the intended local/admissible class cannot do it (`RoundY/README.md:99-106, 191-196`).

What I can give is one genuine partial disproof, and one concrete theorem to target next.

## A real partial no-go

Let
[
B=(s,u,v,\lambda,f),\qquad c=\mathbf 1_{{q=m-1}}.
]

The note `RoundY/theorem/d5_boundary_reset_and_tau_proof_052.md` gives a checked witness family on the active branch (`:194-233`):

[
x^-_m=(m-2,2,1,2,0),\qquad x^+*m=(m-1,2,1,2,0),
]
with the same grouped base
[
B**=(3,1,2,0,\mathrm{regular}),
]
the same current event label
[
\epsilon_4=\mathrm{flat},
]
but opposite carry bits
[
c(x^-_m)=0,\qquad c(x^+_m)=1.
]

The same note records
[
\tau(x^-_m)=m-3,\qquad \tau(x^+_m)=m-4,
]
and says the pair shares a common future flat/nonflat prefix of length (m-5).

So you immediately get:

**Proposition.**
For each tested odd modulus
[
m\in{5,7,9,11,13,15,17,19},
]
no rule that uses only the current data ((B,\epsilon_4)) and the next (h<m-4) future flat/nonflat bits can recover (c) exactly on the active branch.

**Proof.**
On (x^-_m) and (x^+_m), the current pair ((B,\epsilon_4)) is identical, and the next (h) future flat/nonflat bits are identical whenever (h<m-4), because the common prefix has length (m-5). Any such rule must therefore take the same value on both states. But (c(x^-_m)\neq c(x^+_m)). Contradiction. ∎

So fixed bounded-horizon future codings are already ruled out on the checked moduli. And if that witness family persists for all odd (m), then no fixed bounded horizon can work uniformly.

That is not the full disproof yet, because the intended admissible/local class may transport extra memory instead of reading a fixed future window.

## The theorem I would attack next

The most promising negative route is exactly the one `052` points at (`RoundY/theorem/d5_boundary_reset_and_tau_proof_052.md:294-300`):

> prove a reduction lemma saying the intended admissible/local class collapses to bounded transition/reset data.

Why this is the right target:

`049` already reduces the hidden future datum to a **countdown carrier** (`RoundY/theorem/d5_tau_countdown_proof_progress_049.md:99-207`):
[
\tau'=\tau-1\quad\text{when }\tau>0,
]
and all the nontrivial behavior sits at the boundary (\tau=0), where the reset is a tiny current-state map
[
R(\epsilon_4,s,u,v,\lambda).
]

So the problem is no longer “can a local rule reconstruct a long future window?” It is much narrower:

1. transport an exact counter through a long flat corridor;
2. apply the correct reset when (\tau=0).

If you can prove that every admissible mechanism on the active branch factors through bounded transition/reset data, then the witness pair above kills it immediately. That would be a real no-go theorem for the intended class.

I would formulate the needed reduction like this:

**Target reduction lemma.**
Any admissible/local mechanism that realizes (c) on the active branch is determined by current ((B,\epsilon_4)) together with a bounded amount of transition/reset data of depth (h), where (h) depends only on the mechanism class, not on (m).

Once that is proved, Proposition H from `052` gives the contradiction for all sufficiently large odd (m).

## Why the positive route looks harder

There is a constructive refinement through the source-residue coordinate
[
\rho=u_{\text{source}}+1 \pmod m,
]
and on checked data it makes (\tau) and (c) exact on smaller formulas (`RoundY/theorem/d5_boundary_reset_and_tau_proof_052.md:240-262`). So a positive route would try to make (\rho) locally transportable.

But the same note warns that (\rho) is a **stronger** coordinate, not obviously recoverable from the minimal theorem-side object. So I would not bet on that being the cleanest closure.

By contrast, the structural side looks close to done: `062` derives the universal first-exit targets from the explicit `H_{L1}` trigger theorem and a phase-1 invariant, so the remaining obstruction is not global orbit shape but local memory (`RoundY/theorem/d5_first_exit_target_proof_062.md:21-33, 197-220`; also `RoundY/README.md:81-97, 141-155`).

## My verdict

I do not see a full proof or disproof in the bundle.

I do see:

* a real partial disproof of every fixed bounded-horizon coding class;
* a clear next no-go theorem to prove: the reduction lemma from admissible/local mechanisms to bounded transition/reset data;
* a good reason that this is the right frontier, because `\tau` has already been reduced to countdown-plus-reset rather than an arbitrary future signature.

Scope checked: `RoundY/README.md`, `RoundY/theorem/d5_tau_countdown_proof_progress_049.md`, `RoundY/theorem/d5_boundary_reset_and_tau_proof_052.md`, and `RoundY/theorem/d5_first_exit_target_proof_062.md`. Unverified: I did not derive an all-odd-(m) proof from scratch, and I did not find a counterexample to the full admissible/local class.
