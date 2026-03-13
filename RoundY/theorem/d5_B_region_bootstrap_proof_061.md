# D5 proof progress 061: bootstrap proof of `B`-region invariance from the mixed witness scheduler

This note improves the logical structure of `059/060`.

The theorem-side object remains
\[
(B,\tau,\epsilon_4),\qquad B=(s,u,v,\lambda,f).
\]
The auxiliary proof coordinates are
\[
\Theta:=q+s+v+\lambda \equiv q+w+u+v+\lambda \pmod m
\]
and the `\Theta=2` cross-section coordinate
\[
\eta(q,w):=q+m(w-1)-(m-1)\in\{0,\dots,m^2-1\}.
\]

The new point is that the active nonterminal branch can be shown to stay in the unmodified `B`-region **without** assuming the raw active law in advance.  It is enough to use:

1. the local mixed-witness rule on current `B`-states,
2. the explicit support of the six modified classes from `032`,
3. the extracted first-exit targets from `037/044`.

So the proof burden shrinks to the earlier structural input of the universal first-exit targets.

---

## 1. Entry state and first-exit targets

Fix odd `m` and the best seed
\[
L=[2,2,1],\qquad R=[1,4,4].
\]
The active branch starts at the alternate-`2` entry out of `R1`, namely
\[
E_\rho=(q,w,\Theta)=(m-1,1,2).
\]

The extracted first-exit targets are:

- regular:
  \[
  (\Theta,q,w)=(1,m-1,m-2),
  \qquad \eta_{\mathrm{reg}}=m(m-3),
  \]
- exceptional:
  \[
  (\Theta,q,w)=(1,m-2,m-1),
  \qquad \eta_{\mathrm{exc}}=m(m-2)-1.
  \]

Thus every nonterminal active state has associated cross-section index
\[
\eta < m(m-2).
\]

---

## 2. Local current-step effect on `(q,w,\Theta)` for `B`-states

Let `x` be a current state on the active branch which is `B`-labeled.  Then the outgoing direction is the unmodified mixed witness direction.

For color `0`, the mixed witness rule says:
- at `\Theta=0`, use anchor `1`, so `q` increments;
- at `\Theta=1`, use anchor `4`, so only `u` increments;
- at `\Theta=2`, use the old-bit orientation `0/2` with old bit
  \[
  c=\mathbf 1_{\{q=m-1\}},
  \]
  hence `w` increments iff `q=m-1`, and otherwise neither `q` nor `w` changes;
- at `\Theta=3`, use anchor `0` or `3`, but in either case `q,w` are unchanged;
- at every `\Theta\ge 4`, use anchor `0`, so `q,w` are unchanged.

Every anchor increments the total coordinate sum by `1`, so
\[
\Theta^+=\Theta+1 \pmod m.
\]

Therefore every current `B`-state satisfies the one-step rule
\[
(q,w,0)\mapsto(q+1,w,1),
\]
\[
(q,w,1)\mapsto(q,w,2),
\]
\[
(q,w,2)\mapsto(q,w+\mathbf 1_{\{q=m-1\}},3),
\]
\[
(q,w,\Theta)\mapsto(q,w,\Theta+1)\qquad(3\le \Theta\le m-1).
\]

This is exactly the previously extracted raw current-coordinate law, but here it is derived only **locally on `B`-states**.

---

## 3. Cross-section odometer on any initial `B`-segment

Let
\[
\Sigma:=\{\Theta=2\}.
\]
Suppose a branch segment
\[
x_0,x_1,\dots,x_t
\]
starts at `x_0=E_\rho` and has the property that every current state
\[
x_0,\dots,x_{t-1}
\]
is `B`-labeled.

Then the induced return map on the visited `\Sigma`-states is
\[
T(q,w)=(q+1,\;w+\mathbf 1_{\{q=m-1\}}).
\]
Equivalently,
\[
\eta\mapsto\eta+1.
\]

### Proof.
From one `\Theta=2` state to the next, the phase advances through
\[
2\to 3\to 4\to\cdots\to m-1\to 0\to 1\to 2.
\]
Over that cycle,
- `q` changes exactly once, at phase `0`, by `q\mapsto q+1`;
- `w` changes only at the initial phase `2`, and then only if `q=m-1`.
Hence the next return to `\Sigma` is exactly
\[
(q,w)\mapsto(q+1,\;w+\mathbf 1_{\{q=m-1\}}),
\]
which is `\eta\mapsto\eta+1`. ∎

---

## 4. Support of the modified classes

For the best seed, the six non-`B` current classes are exactly:
\[
R1=(\Theta,q,w)=(1,m-1,0),
\qquad
L1=(\Theta,q,w)=(1,m-1,m-1),
\]
\[
R2=(\Theta,q,w)=(2,0,0),
\qquad
L2=(\Theta,q,w)=(2,m-1,0),
\]
\[
R3=(\Theta,q,w)=(3,0,0),
\qquad
L3=(\Theta,q,w)=(3,m-1,1).
\]

Associate to each current class the relevant `\Sigma`-state:
- for `\Theta=1`, take the next `\Sigma` state;
- for `\Theta=2`, take the current `\Sigma` state;
- for `\Theta=3`, take the preceding `\Sigma` state.

The corresponding `\eta`-indices are:
\[
\eta(R1)=\eta(L2)=\eta(L3)=m^2-m,
\]
\[
\eta(R2)=\eta(R3)=(m-1)^2=m(m-2)+1,
\]
\[
\eta(L1)=m(m-2).
\]
Hence every non-`B` current class satisfies
\[
\eta\ge m(m-2).
\]

---

## 5. Bootstrap contradiction

### Proposition A (bootstrap `B`-region invariance).
Fix odd `m` and the best-seed active branch.  Assume the extracted first-exit targets listed in §1.  Then every nonterminal current state on the active branch is `B`-labeled.

### Proof.
Assume for contradiction that some nonterminal current state is not `B`-labeled, and let
\[
t\ge 0
\]
be the first time this happens.

Then every earlier current state
\[
x_0,\dots,x_{t-1}
\]
is `B`-labeled.  By §2 and §3, the visited `\Sigma`-states up to time `t` therefore follow the odometer
\[
T(q,w)=(q+1,\;w+\mathbf 1_{\{q=m-1\}}),
\]
starting from
\[
(m-1,1),\qquad \eta=0.
\]

Because `x_t` is assumed nonterminal, its associated `\Sigma`-state still lies before first exit, hence has index
\[
\eta < m(m-2)
\]
by §1.

On the other hand, `x_t` is one of the six modified classes listed in §4, and every such class has associated index
\[
\eta\ge m(m-2).
\]
This is impossible.  Therefore no such `t` exists, and every nonterminal current state is `B`-labeled. ∎

---

## 6. Consequences

### Corollary B (global raw current-coordinate law).
On the full active nonterminal branch, the current coordinates satisfy
\[
(q,w,0)\mapsto(q+1,w,1),
\]
\[
(q,w,1)\mapsto(q,w,2),
\]
\[
(q,w,2)\mapsto(q,w+\mathbf 1_{\{q=m-1\}},3),
\]
\[
(q,w,\Theta)\mapsto(q,w,\Theta+1)\qquad(3\le \Theta\le m-1).
\]

### Corollary C (global `\Sigma` odometer).
The return map on `\Sigma=\{\Theta=2\}` is
\[
T(q,w)=(q+1,\;w+\mathbf 1_{\{q=m-1\}}),
\]
starting from `(m-1,1)`.

### Corollary D (phase scheduler and reset laws).
Because every nonterminal current state is `B`-labeled, the mixed witness rule applies exactly at every such state.  Hence the phase-event scheduler of `059` holds globally on the active nonterminal branch, and the flat-corner law, `CJ`, and `OTH` follow as corollaries.

---

## 7. Honest status

This closes one logical loop in the proof chain.

What is no longer needed as an extra assumption:
- a separately postulated global raw active law;
- a separately postulated global `B`-region statement.

What is still used as a structural input from the earlier extraction:
- the universal first-exit targets from `037/044`.

So the remaining theorem-level structural gap is now very focused:

> prove the first-exit target formulas uniformly in odd `m`.

Once those targets are admitted, the active branch stays in the unmodified `B`-region by the bootstrap contradiction above, and the whole mixed-witness phase machine follows formally.
