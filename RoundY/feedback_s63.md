I went through the orientation docs and the `036–048` chain, then checked the source-memory idea directly against the frozen `047` data.

Here is the synthesis.

## Problem

Compare the earlier idea

> “the hidden object is really a counter/tower level, and maybe the right way to code it is from the past via a transported source label”

against the full bundle.

## Current target

The bundle’s official frontier is now:

* `046`: carry is already an exact future-transition event;
* `047`: the exact checked carry coding is `B + min(tau, m-3) + epsilon4`;
* `048`: `tau` is itself an exact countdown carrier with a tiny reset law.

So the official problem is no longer “another separator bit.” It is “local/admissible coding of the countdown carrier `tau`.”

## What the bundle confirms

[C] The broad intuition was right.

`048` makes the counter picture explicit. On the checked active nonterminal branch, `tau` is not an opaque future window. It is a genuine countdown variable:

* if `tau > 0`, then next `tau = tau - 1`;
* all nontrivial behavior sits at `tau = 0`;
* the boundary reset law is small.

So the hidden object really does behave like a tower level / unary counter, not like a slightly richer static gate.

[C] The “not a slightly bigger tiny transducer” part is also right.

The README and current-frontier note are very explicit that the live obstruction is no longer:

* another one-bit separator,
* another tiny transducer widening,
* or generic phase exposure.

That part of the earlier reading survives intact.

## What I checked directly in the bundle

I checked the frozen dataset
`artifacts/d5_future_transition_carry_coding_047/data/frozen_B_c_tau_epsilon_dataset_047.json`
on the checked moduli `m = 5,7,9,11`.

Let

* `rho = source_u + 1 mod m`.

Then:

[C] `tau` is exact on current grouped state plus `rho`.

A direct exactness check shows that, on the checked data,

* `tau` is a function of `(s,u,v,layer,rho)`,
* equivalently of `(w,u,v,layer,rho)` since `w = s-u`.

So there really is a checked **past-memory refinement** of the future-side carrier:
[
X_{\text{src}} = (s,u,v,\lambda,\rho).
]

A useful extra point: once `rho` is present, the binary `family` coordinate becomes unnecessary for `tau` on the checked data.

[C] Carry becomes very small in the `rho`-picture.

Among current observables that do not use raw `q`, the minimal exact checked carry readout with `rho` is:
[
c \text{ exact on } (u,\rho,\epsilon_4).
]

Empirically, on every checked row,
[
q \equiv u - \rho + 1_{{\epsilon_4=\text{carry_jump}}} \pmod m,
]
so
[
c = 1_{{q=m-1}}
]
becomes a tiny local equality test in the `rho`-cover.

That is the strongest confirmation of the past-memory idea.

## What needs correction from my earlier thought

[C] My old correction term `1_{layer=1}` was not globally right.

It was too corridor-local. Against the full checked active data, the exact correction is event-based:
[
q \equiv u - \rho + 1_{{\epsilon_4=\text{carry_jump}}} \pmod m,
]
not the layer-based formula I guessed earlier.

So the bundle does not support that earlier identity as a global statement.

[C] The future cover and the source-memory cover are **not** equivalent.

This is the biggest correction.

I checked whether `rho` can be recovered from `(B,\tau,\epsilon4)`. It cannot once `m \ge 7`:

* `m=7`: 3 ambiguous buckets,
* `m=9`: 7 ambiguous buckets,
* `m=11`: 11 ambiguous buckets.

So the source-memory cover is a **strict refinement** of the published future-side cover. It factors onto `tau`, but it is not the same object.

That means my earlier “same object in different coordinates” claim was too strong. The right statement is:

> the past-memory cover is a stronger checked refinement that still realizes the same carry target.

## What I think now

There are really two useful coordinate systems sitting in the bundle.

[C] The official theorem/no-go coordinate system is the future one:
[
(B,\tau,\epsilon_4).
]
This is the right minimal-looking object for the proof notes `046–048`.

[H] The constructive coordinate system is the past-memory one:
[
(B,\rho),
]
with
[
\tau = f(B,\rho), \qquad c = g(u,\rho,\epsilon_4)
]
on the checked data.

That makes the obstruction look like **transported source residue**, not anticipation.

So I would now sharpen the earlier idea like this:

> The bundle supports a source-memory refinement, but it is not just a binary regular/exceptional tag. The checked data want a transported residue label `rho`, or at least some quotient close to it.

That is important, because `039` had already framed the problem as transport, but mainly at the level of a family tag. The `047` data suggest the exact past-memory object is richer than that binary tag.

## Best current theorem candidate

[H] Checked source-memory refinement theorem.

On the checked active best-seed branch for `m=5,7,9,11`, define
[
\rho = source_u + 1 \pmod m.
]
Then:
[
\tau = f(s,u,v,layer,\rho),
]
and
[
c = g(u,\rho,\epsilon_4).
]

So the future-transition carrier from `046–048` admits a checked refinement by a transported source label.

I would not state equivalence. I would state **refinement**.

## What this suggests as the next branch

Attempt A:
prove or realize a local mechanism that initializes and transports enough of `rho`.

That is the positive route. If a source-residue carrier can be born locally and preserved along the unary corridor, then `tau` stops being anticipation and becomes a current-state readout.

Attempt B:
prove that the intended admissible/local mechanism class cannot initialize/transport enough of `rho`.

That is the negative route. This would be a transport no-go, not just a bounded-future-horizon no-go.

## My current verdict

The bundle mostly strengthens the earlier intuition, but with two corrections:

1. the hidden datum really is a counter/countdown carrier — that part is now explicit, not speculative;
2. the past-side version is real on checked data, but it is a **stronger source-memory refinement**, not an equivalent reparametrization of the minimal future cover.

The most useful new sentence I would add to the project notes is:

> On checked moduli, `tau` factors through current grouped state plus a transported source residue `rho = source_u+1`, while carry already factors through `(u, rho, epsilon4)`.

That feels like the cleanest bridge between the old `036/037/039` transport story and the new `046/047/048` countdown story.
