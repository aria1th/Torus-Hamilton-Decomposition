The way to remove the “maybe there are exceptions” feeling is to stop targeting fitted branch formulas and instead target a rigidity theorem.

What would make the reset law feel inevitable is this:

> the active branch is a **clocked finite-state machine**: a single cyclic phase advances by (+1) every step, and all nonflat behavior occurs at a tiny fixed set of phases, with one exceptional corner.

That is exactly the kind of statement under which exceptions have nowhere left to hide.

Why I think this is the right target:

The notes already say the problem has collapsed from “understand a future window” to “prove the boundary reset law,” and then further to `CJ` plus `OTH` only. That is explicit in `055` around the reduced theorem target and proof sketch (lines 224–250). Then `057` reduces `CJ` again to one flat-corner lemma (lines 166–199). And `057a` explicitly proposes a small phase machine as the next conceptual jump (lines 176–249).

There is also a strong structural reason this is even possible. From the stronger residue picture, the checked proof-side identity is
[
q \equiv u-\rho+\mathbf 1_{{\epsilon_4=\mathrm{carry_jump}}},
]
summarized in `054` lines 188–200, while `057` defines
[
\delta=\rho-(s+u+v+\lambda).
]
Combining them gives
[
\kappa:=q+s+v+\lambda \equiv \mathbf 1_{{\epsilon_4=\mathrm{carry_jump}}}-\delta \pmod m.
]
So the visible phase candidate
[
\kappa=q+s+v+\lambda
]
is not random at all: it is the visible shadow of the constructive residue (\delta). That is why a (\kappa)-theorem is plausible rather than cosmetic.

Also, the reset values themselves already look like distances on a clock:

* `CJ` has values ({0,1,m-2}),
* `OTH` has values ({0,m-4,m-3}).

Those are exactly the distances you would expect if the system lands in flat phases (2,3,4) on an (m)-cycle, plus one short-circuit corner. That is much more “automaton-like” than “mysterious piecewise formula”.

So the theorem I would target is this.

## Target theorem: Phase–Corner Theorem

Let
[
\kappa(x)=q(x)+s(x)+v(x)+\lambda(x)\pmod m.
]

Prove that for every odd (m\ge 5) on the active best-seed branch:

[
\textbf{(P1)}\qquad \kappa(Fx)=\kappa(x)+1\pmod m.
]

[
\textbf{(P2)}\qquad
\begin{cases}
\mathrm{wrap}\to \mathrm{carry_jump},\
\mathrm{carry_jump}\to \mathrm{other}*{1000}\ \text{iff } q=m-1,\ \text{else flat},\
\mathrm{other}*{1000}\to \mathrm{flat}\ \text{iff } s=1,\ \text{else }\mathrm{other}*{0010},\
\mathrm{other}*{0010}\to \mathrm{flat},\
\mathrm{flat}\to \mathrm{wrap}\ \text{iff } \kappa=m-1,\
\mathrm{flat}\to \mathrm{other}_{0010}\ \text{iff } (\kappa,s)=(2,2),\
\mathrm{flat}\to \mathrm{flat}\ \text{otherwise.}
\end{cases}
]

Here (\mathrm{other}*{1000}) means (dn=(1,0,0,0)) and (\mathrm{other}*{0010}) means (dn=(0,0,1,0)).

From that, the countdown is immediate:

[
\tau(x)=
\begin{cases}
0,& \epsilon_4(x)\neq \mathrm{flat},[1mm]
1,& \epsilon_4(x)=\mathrm{flat}\ \text{and}\ (\kappa,s)=(2,2),[1mm]
m-\kappa(x),& \epsilon_4(x)=\mathrm{flat}\ \text{otherwise.}
\end{cases}
]

And then the boundary reset theorem `BR` is just a corollary.

Why this theorem is the right one:

1. It explains both `CJ` and `OTH` at once.
   Proving `CJ` and `OTH` separately would finish the theorem, but it would still feel a bit accidental. Proving the phase–corner machine explains why both branches have exactly those reset values.

2. It turns “exceptions” into three tiny failure modes.
   A counterexample would have to do one of only three things:

   * break the phase increment (\kappa\mapsto \kappa+1),
   * introduce a new flat exit besides (\kappa=m-1) and the corner ((2,2)),
   * introduce a new nonflat transition not listed in the small machine.

   That is a much sharper target than “maybe some formula fails somewhere”.

3. It matches the existing proof compression.
   `048` already says (\tau) is a countdown carrier; `055` reduces the theorem to boundary branches; `057` says `CJ` is really just the flat-corner lemma; `057a` says the likely global explanation is a small phase machine. This theorem is exactly the next compression step, not a change of direction.

What I would prove first, tactically:

* First prove the flat-corner law in the (\delta)-language, because `057` already reduces `CJ` to that.
* But do it with the explicit goal of translating it into the (\kappa)-clock statement, because that is what makes the whole picture feel forced.

So there are really two levels:

* **fastest route to progress:** prove the flat-corner lemma;
* **best theorem for inevitability:** prove the full Phase–Corner Theorem.

My recommendation is to aim at the second, while using the first as the entry point. The flat-corner lemma is the local handle; the phase–corner theorem is the real explanation.

The one caveat is scope: the bundle itself packages the branch formulas through (m=23), but the full (\kappa)-machine is only partially written up as a hypothesis rather than a completed artifact. So I’m recommending it as the right theorem to prove, not claiming it is already established.
