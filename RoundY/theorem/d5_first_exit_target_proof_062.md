# D5 proof progress 062: universal first-exit targets from the explicit `H_{L1}` trigger theorem

This note removes the last structural input from `061`.

The theorem object remains the minimal future-side object
\[
(B,\tau,\epsilon_4),\qquad B=(s,u,v,\lambda,f).
\]
The auxiliary proof coordinates are current color-`0` coordinates
\[
(q,w,u,\lambda),\qquad \Theta=q+s+v+\lambda \pmod m,
\]
so the proof keeps track of the full current tuple `(q,w,u,Theta)` along the
active corridor.
and the constructive source residue
\[
\rho:=u_{\mathrm{source}}+1\pmod m,
\]
used only inside the proof.

The key point is that the family-dependent first exits can be proved directly from:

1. the exact defect-family formula for `H_{L1}` from
   `theorem/d5_033_explicit_trigger_family.md`,
2. the mixed witness rule on current `B`-states,
3. the candidate raw orbit starting at the alt-`2` entry,
4. and one phase-`1` invariant relating `q` and `u` to `\rho`.

So the old external input
\[
T_{\mathrm{reg}}=(m-1,m-2,1),\qquad T_{\mathrm{exc}}=(m-2,m-1,1)
\]
becomes a corollary rather than a hypothesis.

---

## 1. Exact hole target formula

From the promoted trigger-family theorem, the hole family `H_{L1}` is
\[
H_{L1} = \{(q,w,u,\lambda)=(m-1,m-1,u,2):\ u\neq 2\}.
\tag{H-L1}
\]

Here the current color-`0` coordinates are
\[
q=x_1,\qquad w=x_2,\qquad u=x_4,\qquad \lambda=\sum_{i=0}^4 x_i \pmod m.
\]
So the absolute directions act on these auxiliary coordinates by
\[
1:(q,w,u,\lambda)\mapsto(q+1,w,u,\lambda+1),
\tag{D1}
\]
\[
2:(q,w,u,\lambda)\mapsto(q,w+1,u,\lambda+1).
\tag{D2}
\]
In particular, both directions `1` and `2` preserve `u`, and only phase-`1`
current states can land in `H_{L1}` because the target layer is `2`.

---

## 2. Candidate active orbit

Fix odd `m>=5` and the best seed
\[
L=[2,2,1],\qquad R=[1,4,4].
\]
Let
\[
E=(q,w,\Theta)=(m-1,1,2)
\]
be the alt-`2` entry state from `R1`.

Define the candidate orbit `\widehat x_n` on full current coordinates
\[
(q,w,u,\Theta)
\]
by the recurrence
\[
\widehat F(q,w,u,0)=(q+1,w,u,1),
\]
\[
\widehat F(q,w,u,1)=(q,w,u+1,2),
\]
\[
\widehat F(q,w,u,2)=\bigl(q,w+\mathbf 1_{\{q=m-1\}},u,3\bigr),
\]
\[
\widehat F(q,w,u,\Theta)=(q,w,u,\Theta+1)
\qquad(3\le \Theta\le m-1),
\]
with initial state
\[
\widehat x_0=(m-1,1,u_{\mathrm{source}},2).
\]
Its projection to `(q,w,Theta)` is exactly the extracted raw corridor law.

On the section
\[
\Sigma:=\{\Theta=2\},
\]
this gives the odometer return map
\[
T(q,w)=(q+1,\;w+\mathbf 1_{\{q=m-1\}}),
\tag{Odo}
\]
starting from `(m-1,1)`.
Equivalently, with
\[
\eta(q,w):=q+m(w-1)-(m-1)\in\{0,\dots,m^2-1\},
\]
one has `\eta\mapsto\eta+1`.

The two distinguished phase-`1` states are
\[
A:=(q,w,\Theta)=(m-1,m-2,1),\qquad \eta(A)=m(m-3),
\]
\[
B:=(q,w,\Theta)=(m-2,m-1,1),\qquad \eta(B)=m(m-2)-1.
\]
These are the only phase-`1` states whose direction `2` or `1` step can reach
`q=w=m-1`.

---

## 3. Phase-`1` source-residue invariant

Let `\rho=u_{\mathrm{source}}+1` for the chosen `R1` source family.

### Lemma A (phase-`1` invariant).
Along the candidate orbit, every phase-`1` current state satisfies
\[
q\equiv u-\rho+1 \pmod m.
\tag{P1-rho}
\]

#### Proof.
The first phase-`1` current state after entry is reached from
\[
(m-1,1,2)
\to(m-1,2,3)\to\cdots\to(m-1,2,0)\to(0,2,1).
\]
Along that initial segment, direction `2` leaves `u` unchanged, so the first
phase-`1` state has
\[
q=0,\qquad u=u_{\mathrm{source}}=\rho-1,
\]
which is exactly `(P1-rho)`.

From one phase-`1` current state to the next:
- the phase-`1` witness step uses direction `4`, so `u\mapsto u+1`;
- the later phase-`0` witness step uses direction `1`, so `q\mapsto q+1`;
- no other step changes `q` or `u`.
Thus both sides of `(P1-rho)` increase by `1`, and the relation is preserved. ∎

Hence at the two distinguished phase-`1` states:
\[
u(A)\equiv \rho-2 \pmod m,
\tag{uA}
\]
\[
u(B)\equiv \rho-3 \pmod m.
\tag{uB}
\]

---

## 4. Trigger criterion for `H_{L1}`

### Lemma B (phase-`1` trigger criterion).
Let `x` be a phase-`1` current state on the candidate orbit.
Then an alternate step from `x` lands in `H_{L1}` if and only if one of the
following holds:

1. `x=(m-1,m-2,1)` and `u(x)\neq 2`, in which case direction `2` lands in
   `H_{L1}`;
2. `x=(m-2,m-1,1)` and `u(x)\neq 2`, in which case direction `1` lands in
   `H_{L1}`.

#### Proof.
By `(H-L1)`, the successor must satisfy
\[
(q',w',\lambda')=(m-1,m-1,2),\qquad u'\neq 2.
\]
Because only phase-`1` current states can step to layer `2`, and because
`1` and `2` are the only directions that can change `q` or `w`, the only two
ways to obtain `(q',w')=(m-1,m-1)` are:

- by direction `2` from `(q,w)=(m-1,m-2)`;
- by direction `1` from `(q,w)=(m-2,m-1)`.

Directions `1,2` preserve `u` by `(D1)` and `(D2)`, so the extra condition is
exactly `u\neq 2`. ∎

---

## 5. Universal first exits on the candidate orbit

### Proposition U (candidate first exits).
On the candidate orbit:

- if `\rho\neq 4` (regular family), the first `H_{L1}` exit occurs at
  \[
  A=(m-1,m-2,1)
  \]
  by direction `2`;

- if `\rho=4` (exceptional family), the state `A` does **not** exit to
  `H_{L1}`, and the first `H_{L1}` exit occurs at
  \[
  B=(m-2,m-1,1)
  \]
  by direction `1`.

#### Proof.
By Lemma B, only the two phase-`1` states `A` and `B` can possibly exit to
`H_{L1}`. Since
\[
\eta(A)=m(m-3)<m(m-2)-1=\eta(B),
\]
state `A` is always encountered first.

At `A`, formula `(uA)` gives
\[
u(A)=\rho-2.
\]
So `u(A)=2` iff `\rho=4`.
Hence:
- if `\rho\neq 4`, then `u(A)\neq 2`, so Lemma B gives an `H_{L1}` exit at
  `A` by direction `2`, and this is the first exit;
- if `\rho=4`, then `u(A)=2`, so Lemma B shows that `A` does not exit.

Now assume `\rho=4`. At `B`, formula `(uB)` gives
\[
u(B)=1\neq 2,
\]
so Lemma B gives an `H_{L1}` exit at `B` by direction `1`. Since `A` was the
only earlier possible trigger and is blocked when `\rho=4`, this is the first
exit. ∎

Because `\rho=u_{\mathrm{source}}+1`, the condition `\rho=4` is exactly
`u_{\mathrm{source}}=3`, i.e. the exceptional family. So the candidate first
exits are exactly the universal `037` targets:
\[
T_{\mathrm{reg}}=(m-1,m-2,1),\qquad
T_{\mathrm{exc}}=(m-2,m-1,1).
\tag{Targets}
\]

---

## 6. Candidate orbit avoids all patched current classes before first exit

Let `N_f` be the first exit time from Proposition U for family `f`.

### Lemma C (pre-exit patch avoidance on the candidate orbit).
For every `0\le n<N_f`, the candidate current state `\widehat x_n` avoids all six
patched current classes.

#### Proof.
1. `w` starts at `1` and changes only by the increment `w\mapsto w+1` at phase
   `2` with `q=m-1`. Hence `w` never decreases and `w=0` never occurs before
   exit. So `R1,R2,R3,L2` are impossible.
2. The value `w=1` occurs only at the entry state `(m-1,1,2)`, hence `L3`
   cannot occur.
3. On the regular family, exit occurs at `A`, before `w` ever reaches `m-1`, so
   `L1` is impossible.
4. On the exceptional family, `w=m-1` is first created at phase `3` from
   `(m-1,m-2,2)`. The next phase-`1` state then has `(q,w)=(0,m-1)`, not
   `(m-1,m-1)`. The first later phase-`1` state with `w=m-1` that could carry
   `q=m-1` would occur strictly after `B`, but the branch exits already at `B`.
   So `L1` is impossible before exceptional exit as well. ∎

---

## 7. Actual branch equals the candidate orbit up to first exit

Let `x_0,x_1,\dots` be the actual active branch after the alt-`2` entry from
`R1`, stopped at its first `H_{L1}` exit.

### Theorem X (actual first exits are the universal targets).
For each source family:

- the actual active branch agrees with the candidate orbit up to first exit;
- every pre-exit current state is `B`-labeled;
- the first `H_{L1}` exit occurs at the universal target in `(Targets)`.

#### Proof.
Induct on time `n` until the candidate first-exit time `N_f`.

Base step: the entry state is exactly `E=(m-1,1,2)`, and by Lemma C it is not
patched, hence it is `B`.

Inductive step: assume the actual state `x_n` agrees with the candidate state
`\widehat x_n` in the full current coordinates `(q,w,u,\Theta)` for some
`n<N_f`.
By Lemma C, `\widehat x_n` is not patched, so `x_n` is `B`-labeled. Therefore
its witness update is the unmodified mixed-witness update, which induces exactly
the candidate step on `(q,w,u,\Theta)`: direction `1` changes only `q`,
direction `4` changes only `u`, direction `2` changes only `w`, and the other
anchors leave `(q,w,u)` fixed. Hence
\[
(q,w,u,\Theta)(x_{n+1})=(q,w,u,\Theta)(\widehat x_{n+1}).
\]
Thus the actual and candidate branches agree through time `N_f`.

For `n<N_f`, Proposition U says the candidate state `\widehat x_n` has no
`H_{L1}` exit, so neither does `x_n`, because the trigger criterion of Lemma B
uses only the current coordinates `(q,w,u,\Theta)`. At time `N_f`, Proposition
U gives an `H_{L1}` exit from `\widehat x_{N_f}` by the stated direction, so
the actual branch also exits there.
Therefore the first actual exit is the same family-dependent target in
`(Targets)`, and every earlier current state is `B`-labeled. ∎

---

## 8. Consequences

### Corollary Y (`B`-region invariance).
Every nonterminal current state on the active best-seed branch is `B`-labeled.

### Corollary Z (global phase scheduler and reset laws).
On the active nonterminal branch, the mixed witness scheduler in
\[
\Theta=q+s+v+\lambda
\]
holds globally. Hence the flat-corner law, the `CJ` reset law, and the `OTH`
reset law all follow.

---

## 9. Honest status

This closes the main structural loop.

What is now proved modulo only the already-extracted exact defect-family
formula `(H-L1)`:

1. the universal first-exit target theorem,
2. `B`-region invariance up to first exit,
3. the global phase scheduler in `\Theta`,
4. and therefore the boundary reset laws.

So the proof bottleneck has moved again. The active branch geometry is no longer
the missing step. The remaining genuine theorem problem is the **local/
admissible coding of the countdown carrier `\tau`** (or a no-go theorem for the
intended local class), not the structural location of the first exits.
