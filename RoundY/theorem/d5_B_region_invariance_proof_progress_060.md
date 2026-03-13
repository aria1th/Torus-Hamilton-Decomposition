# D5 active branch stays in the unmodified `B`-region: proof progress 060

This note isolates the proof step left open in `059`:

> justify that the active nonterminal best-seed branch never re-enters one of the six endpoint-patch classes `L1,R1,L2,R2,L3,R3`, so every current state on that branch is `B`-labeled and the outgoing direction is the unmodified mixed witness rule.

The theorem object remains the minimal future-side object
\[
(B,\tau,\epsilon_4),\qquad B=(s,u,v,\lambda,f).
\]
The coordinates `(q,w,\Theta)` are used here only as auxiliary proof coordinates, with
\[
\Theta:=q+s+v+\lambda = q+w+u+v+\lambda \pmod m.
\]

---

## 1. Explicit support of the endpoint patch

Fix the best seed
\[
L=[2,2,1],\qquad R=[1,4,4],
\]
with the representative choice `(w0,s0)=(0,0)` and color `0`.

By direct reading of the construction in `032` (`_prepare_m` and `_build_candidate`), the six non-`B` classes are exactly:
\[
R1 = \{\Theta=1,\ q=m-1,\ w=0,\ s\neq 0\},
\]
\[
L1 = \{\Theta=1,\ q=m-1,\ w=m-1,\ s\neq 0\},
\]
\[
R2 = \{\Theta=2,\ q=0,\ w=0,\ s\neq 0\},
\]
\[
L2 = \{\Theta=2,\ q=m-1,\ w=0,\ s\neq 1\},
\]
\[
R3 = \{\Theta=3,\ q=0,\ w=0,\ s\neq 1\},
\]
\[
L3 = \{\Theta=3,\ q=m-1,\ w=1,\ s\neq 2\}.
\]

So the endpoint patch is supported only on the low-phase slabs `\Theta=1,2,3`, and only on the four raw `(q,w)` corners
\[
(m-1,0),\ (m-1,m-1),\ (0,0),\ (m-1,1).
\]

---

## 2. Auxiliary current-coordinate law on the active branch

Use the already extracted raw active law from `037/039` on the nonterminal branch, written in the current phase `\Theta`:
\[
(q,w,0)\mapsto (q+1,w,1),
\]
\[
(q,w,1)\mapsto (q,w,2),
\]
\[
(q,w,2)\mapsto (q,w+\mathbf 1_{\{q=m-1\}},3),
\]
\[
(q,w,\Theta)\mapsto (q,w,\Theta+1)\qquad (3\le \Theta\le m-1),
\]
all coordinates taken mod `m`.

The active branch starts from the alternate-`2` entry out of `R1`, so the first active state is
\[
E_\rho=(m-1,1,2).
\]

Its first possible exits are the already extracted trigger states:
\[
(m-1,m-2,1) \quad \text{(regular)},
\qquad
(m-2,m-1,1) \quad \text{(exceptional)}.
\]
Hence a *nonterminal* active state is any state reached from `E_\rho` before those exits fire.

---

## 3. Three elementary invariants

### Lemma A. `w` never vanishes on the nonterminal active branch.

`w` starts at `1`. Under the auxiliary law, `w` can only change on phase `\Theta=2`, and then only by the increment `w\mapsto w+1` when `q=m-1`. Thus `w` never decreases.

Before `w` could wrap from `m-1` to `0`, the branch has already reached one of the two known first-exit targets above. Therefore on every nonterminal active state,
\[
w\in\{1,2,\dots,m-1\}.
\]

**Consequence.** The classes `R1,R2,R3,L2` are never visited, since all four require `w=0`.

---

### Lemma B. `w=1` occurs only at the entry state.

The entry state is `(m-1,1,2)`. Its successor is
\[
(m-1,2,3),
\]
because the phase is `2` and `q=m-1`, so the `\Theta=2` step increments `w`.

After that first step, the same monotonicity argument as in Lemma A shows that `w` never returns to `1` before the branch exits.

**Consequence.** `L3` is never visited, since `L3` requires `\Theta=3` and `w=1`, while the unique `w=1` state has `\Theta=2`.

---

### Lemma C. `(q,w,\Theta)=(m-1,m-1,1)` never occurs on the nonterminal active branch.

The only way to create the value `w=m-1` is from a phase-`2` state with `(q,w)=(m-1,m-2)`. The successor of that state is
\[
(m-1,m-1,3).
\]
After that, while `q` remains `m-1`, the phase runs through
\[
3,4,\dots,m-1,0.
\]
The next step, from phase `0`, increments `q` to `0` and moves to phase `1`. Hence the branch can never have both
\[
q=m-1,\quad w=m-1,\quad \Theta=1.
\]

**Consequence.** `L1` is never visited.

---

## 4. B-region invariance

Combining Lemmas A, B, and C with the explicit support formulas from §1 shows:

### Proposition D (B-region invariance from the raw active law).
Assume the auxiliary current-coordinate law of §2 on the active nonterminal best-seed branch. Then every nonterminal active state avoids all six endpoint-patch classes
\[
L1,R1,L2,R2,L3,R3.
\]
Equivalently, every such state is `B`-labeled.

### Proof.
- Lemma A removes `R1,R2,R3,L2`.
- Lemma B removes `L3`.
- Lemma C removes `L1`.
No non-`B` class remains. ∎

---

## 5. Consequence for the phase scheduler

Once Proposition D is admitted, the mixed witness rule applies *exactly* at every nonterminal active state. Therefore the current event class is governed by the unmodified mixed-witness scheduler, which is precisely the `059` phase machine in
\[
\Theta=q+s+v+\lambda.
\]

So the proof burden has been reduced as follows:

1. justify the auxiliary current-coordinate law on the active branch,
2. deduce `B`-region invariance,
3. then the `\Theta`-scheduler follows from the mixed witness itself,
4. and `CJ` / `OTH` become corollaries.

This is a real reduction: the boundary reset formulas are no longer separate endpoint identities. They are consequences of the active branch staying inside the untouched mixed-witness region.

---

## 6. Honest status

What is established here:
- exact support formulas for the six patch classes from the seed construction,
- a proof that *under the already extracted raw active law* the nonterminal branch cannot hit any of those six classes,
- hence a clean reduction of the scheduler proof to the raw active law.

What is still open on the proof side:
- a uniform odd-`m` proof of the auxiliary raw active current-coordinate law itself.

So `060` does not finish the whole uniform theorem. It isolates the remaining gap much more sharply:

> once the raw active law is proved uniformly, `B`-region invariance is automatic, and the `\Theta` phase-event scheduler becomes a direct corollary of the mixed witness rule.
