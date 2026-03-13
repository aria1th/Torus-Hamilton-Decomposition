On the scope I actually inspected in the bundle — `RoundY/README.md`, `current-frontier-and-approach.md`, the theorem notes `058–062`, and the support READMEs `044`, `047–049`, `059B` — I do **not** see a disproof of the strengthened structural chain. The bundle reports positive branch support out to `m=29`, and I did not find an internal contradiction in the `058–062` logic.

What I *do* think is true is this:

> **Conditional on the explicit `H_{L1}` trigger theorem from `033`, the positive structural branch is essentially proved.**
>
> In fact the clean logical spine can be shortened to
> `033 → 062 → 059`,
> with `061` kept as a useful check, not as a necessary prerequisite.

The external input from `033` is the exact hole family formula used in `062`:
[
H_{L1}={(q,w,u,\lambda)=(m-1,m-1,u,2):u\neq 2}.
]

I did **not** verify `033` itself from raw source here, because that artifact is referenced but not included in this reading bundle. So the argument below is conditional on that formula.

## Conditional proof of the structural chain

Fix odd (m\ge 5), the best seed, and let the post-entry active state be
[
E=(q,w,\Theta)=(m-1,1,2),
]
with full current coordinates
[
\widehat x_0=(m-1,1,u_{\text{source}},2).
]
Set
[
\rho:=u_{\text{source}}+1 \pmod m.
]

Define the **candidate orbit** on current coordinates ((q,w,u,\Theta)) by
[
\widehat F(q,w,u,0)=(q+1,w,u,1),
]
[
\widehat F(q,w,u,1)=(q,w,u+1,2),
]
[
\widehat F(q,w,u,2)=\bigl(q,;w+\mathbf 1_{{q=m-1}},;u,;3\bigr),
]
[
\widehat F(q,w,u,\Theta)=(q,w,u,\Theta+1)\qquad(3\le \Theta\le m-1),
]
with (\Theta) read mod (m).

This is just the mixed-witness rule written in raw coordinates, assuming the current state is (B)-labeled.

### 1. Phase-1 invariant

Along the candidate orbit, every phase-1 state satisfies
[
q\equiv u-\rho+1 \pmod m.
]

Reason: the first phase-1 state is ((0,2,u_{\text{source}},1)), so the relation holds there. From one phase-1 state to the next, exactly one (u)-increment happens at phase (1), and exactly one (q)-increment happens later at phase (0). So both sides increase by (1).

### 2. Only two phase-1 states can hit (H_{L1})

Because the target hole family has layer (2), only a phase-1 state can alternate into it. And because the target requires
[
(q',w')=(m-1,m-1),
]
the only possibilities are:

* from
  [
  A=(m-1,m-2,1)
  ]
  by direction (2);

* from
  [
  B=(m-2,m-1,1)
  ]
  by direction (1).

No other phase-1 state can reach (q'=w'=m-1) in one alternate step.

### 3. Which one is the first exit

At those two states, the phase-1 invariant gives
[
u(A)\equiv \rho-2,\qquad u(B)\equiv \rho-3 \pmod m.
]

Now (H_{L1}) requires (u\neq 2). So:

* if (\rho\neq 4), then (u(A)\neq 2), and the branch exits first at
  [
  A=(m-1,m-2,1)
  ]
  by direction (2);

* if (\rho=4), then (u(A)=2), so (A) is blocked, while
  [
  u(B)=1\neq 2,
  ]
  so the first exit is at
  [
  B=(m-2,m-1,1)
  ]
  by direction (1).

So the universal first-exit targets follow:
[
T_{\mathrm{reg}}=(m-1,m-2,1),\qquad
T_{\mathrm{exc}}=(m-2,m-1,1).
]

### 4. The candidate orbit avoids all patched current classes before exit

This is the key clean step.

The six patched current classes are the non-(B) classes. Before the candidate first exit:

* (w) starts at (1);
* (w) changes only at phase (2) with (q=m-1);
* therefore (w) never decreases.

So any patched class with (w=0) is impossible immediately.

Also, (w=1) occurs only at the entry state, which has (\Theta=2), so the (\Theta=3,\ w=1) patched class never occurs.

For the (L1)-type class ((q,w,\Theta)=(m-1,m-1,1)):

* on the regular family, the orbit exits already at (A=(m-1,m-2,1)), before (w) ever reaches (m-1);
* on the exceptional family, once (w) first reaches (m-1), the subsequent phase-1 states with (w=m-1) appear in the order
  [
  (0,m-1,1),\ (1,m-1,1),\ \dots,\ (m-2,m-1,1)=B,\ (m-1,m-1,1),
  ]
  so the branch exits at (B) before (L1) can occur.

Hence every pre-exit candidate state is (B)-labeled.

### 5. Actual branch = candidate branch up to first exit

Now induct on time.

At time (0), the actual active branch and the candidate orbit start at the same entry state.

Assume they agree at time (n), before candidate first exit. Since the candidate state is not patched, it is (B)-labeled. Therefore the actual state is also unmodified there, so the mixed witness rule applies, and the next actual step is exactly the candidate step on ((q,w,u,\Theta)).

Thus the actual branch and the candidate orbit agree all the way up to first exit.

So we get, all at once:

1. the actual first exit is the same family-dependent universal target;
2. every pre-exit current state is (B)-labeled.

At that point `059` applies globally, and the phase scheduler in
[
\Theta=q+s+v+\lambda
]
follows on the whole active nonterminal branch. Therefore `CJ`, `OTH`, and the boundary reset laws are corollaries.

## What this means

So my honest conclusion is:

* I do **not** see a counterexample to the strengthened structural route in the bundle.
* Conditional on the explicit `033` hole-family formula, I think the structural branch is already proved.
* The proof is actually cleaner if `062` is made the main structural theorem and `061` is demoted to a supporting cross-check.

## What remains genuinely open

This does **not** finish the full `d=5` problem. The real remaining frontier is the one the bundle itself identifies:

> local/admissible coding of the countdown carrier (\tau), or a no-go theorem for the intended local class.

The best positive idea I see is: **do not attack (\tau) directly. Attack the transported source residue (\rho).**

From the `049` refinement, the constructive relation is
[
q \equiv u-\rho+\mathbf 1_{\epsilon_4=\mathrm{carry_jump}} \pmod m,
]
so the carry sheet
[
c=\mathbf 1_{{q=m-1}}
]
is exact on ((u,\rho,\epsilon_4)).

That means the constructive problem can be reframed as:

> build a locally admissible mechanism that transports (\rho=u_{\text{source}}+1) along the active corridor.

If that transport exists, then (c) becomes current-state exact, and the `044/048` finite-cover/countdown package should take over.

If the intended local class is actually too small, then the likely negative route is to formalize an odometer-factor obstruction: on the (\Sigma)-section, the branch is the (m^2)-cycle
[
(q,w)\mapsto (q+1,;w+\mathbf 1_{{q=m-1}}),
]
and the carry set is exactly the residue slice (q=m-1). My guess is that a bounded local observable independent of (m) cannot recover that residue class uniformly; the right proof would be a Myhill–Nerode / finite-quotient style argument on the active odometer word.

So the strongest thing I can honestly defend is:

* **structural branch:** looks provable, conditional on `033`;
* **remaining real problem:** local transport of (\rho), or a no-go theorem showing that no admissible local mechanism can encode it uniformly.
