# Resonant late pure color-1: the `+5` odometer coordinate, the carrier-adapted reduced slip machine, explicit splice placement, and the induced carrier return framework (2026-03-27)

## 0. Scope

We continue in the resonant non-`5` late range, but now only in the two residue
classes that actually carry a nontrivial first common moved carrier:
\[
m\ge 33,
\qquad
3\mid m,
\qquad
5\nmid m,
\qquad
m\equiv 3\text{ or }9\pmod{15}.
\]
Write
\[
m=3M,
\qquad
q_m:=4^{-1}+1\in\mathbb Z_m.
\]
Equivalently,
\[
4q_m\equiv 5\pmod m.
\]

The previous notes already established two pieces of structure.

1. On the slip lane
   \[
   L_m=\{J\in\mathbb Z_m:J\equiv 1\pmod 3\},
   \]
   the direct common reinjection phase map is a three-block cyclic
   interval-exchange in the cut coordinate `T`.
2. On the first common defect set from the base line, the moved direct carrier is
   sparse and explicit:
   - in class `m=5\ell+3`,
     \[
     \mathcal C_m^{(1)}=\{4+3kq_m:0\le k\le \ell/3\};
     \]
   - in class `m=5\ell+4`,
     \[
     \mathcal C_m^{(1)}=\{(3k+2)q_m:0\le k\le (\ell-2)/3\}\cup\{m-2\}.
     \]

What was still missing is the odometer coordinate suggested by the D3/D4 reading
and by the parallel `k=4J` observation: a coordinate in which the fast phase is
literally the `+5` odometer and the sparse first-defect carrier becomes a short
contiguous window.

That is the point of the present note.

### Main outputs

1. The full common top phase clock becomes **literal translation by `+5`** after
   the change of variable
   \[
   k=4J.
   \]
2. On the slip lane, there is a natural **reduced `+5` odometer coordinate**
   `n\in\mathbb Z_M` in which the sparse first-defect carrier becomes a short
   interval (class `m\equiv 3\pmod{15}`) or an interval plus one explicit extra
   point (class `m\equiv 9\pmod{15}`).
3. In that reduced coordinate, the global direct common reinjection becomes a
   **finite-splice odometer perturbation**:
   \[
   g_m(n+\lambda_m)=g_m(n)+\lambda_m
   \qquad
   \text{off an explicit three-point splice set }\Omega_m.
   \]
4. The splice set `\Omega_m` can be written **completely explicitly** in terms of
   the carrier length parameter `r`.
5. In class `m=15r+3`, the carrier interval starts **completely away from all
   global splices**.
6. In class `m=15r+9`, the carrier interval meets the global splice set in only
   one or two explicit indices, and the isolated extra carrier point is never a
   splice point.
7. Therefore the induced first return on the carrier is now reduced to the right
   symbolic object: a **finite piecewise-translation carrier machine**.  This is
   exactly the setting in which a cohomological equation can plausibly be solved.

So this pass does not yet solve the carrier return completely.  What it does do
is put the carrier machine in the correct odometer coordinate and expose the
finite splice geometry explicitly.

---

## 1. Imported facts

We use the notation and results already proved in the previous 2026-03-27 notes.

### Fact 1.1 (common top phase step)

On the defect-free common branch, the effective phase satisfies
\[
J\longmapsto J+q_m.
\]

### Fact 1.2 (slip-lane cut coordinate and finite-splice law)

On the slip lane, the direct common reinjection phase map becomes, in the cut
coordinate
\[
T\in\{0,1,\dots,M-1\},
\qquad
J=4-6T\pmod m,
\]
a three-block cyclic interval exchange.  There are consecutive blocks
\[
I_f=[0,a-1],
\qquad
I_m=[a,a+b-1],
\qquad
I_\ell=[a+b,M-1],
\]
with splice set
\[
\Sigma_m=\{a-1,\ a+b-1,\ M-1\},
\]
such that the cut-coordinate slip map `U_m` is a translation on each block and
satisfies
\[
T\notin \Sigma_m
\quad\Longrightarrow\quad
U_m(T+1)=U_m(T)+1\pmod M.
\]

### Fact 1.3 (first moved common carrier)

If `m=15r+3` (equivalently `m=5\ell+3` with `\ell=3r`), then
\[
\mathcal C_m^{(1)}=\{4+3kq_m:0\le k\le r\}.
\]

If `m=15r+9` (equivalently `m=5\ell+4` with `\ell=3r+1`), then
\[
\mathcal C_m^{(1)}=\{(3k+2)q_m:0\le k\le r-1\}\cup\{m-2\}.
\]

---

## 2. The literal `+5` odometer

### Lemma 2.1 (the common top phase clock is `+5` in the `k`-coordinate)

Define
\[
k:=4J\in\mathbb Z_m.
\]
Then the common top phase step
\[
J\longmapsto J+q_m
\]
becomes
\[
\boxed{k\longmapsto k+5.}
\]

#### Proof

Because `4q_m\equiv 5\pmod m`, one has
\[
4(J+q_m)\equiv 4J+5\pmod m.
\]
So in the `k`-coordinate the common top phase clock is literal translation by
`+5`. ∎

This is the exact D5 analogue of the odometer clock that the D3/D4 reading
suggested we should be searching for.

---

## 3. Reduced `+5` coordinates on the slip lane

From now on we work only on the slip lane `L_m`, so every phase has residue
`1 mod 3`.

### 3.1. Class `m=15r+3`

Here
\[
m=15r+3,
\qquad
M=5r+1,
\qquad
r\ \text{is even}.
\]

### Definition 3.1 (reduced odometer coordinate, class `15r+3`)

For `J\in L_m`, define `\kappa_m(J)\in\mathbb Z_M` by
\[
\boxed{J=4+3\kappa_m(J)q_m.}
\]
Equivalently,
\[
\boxed{4J=16+15\kappa_m(J)\pmod m.}
\]

### Lemma 3.2 (class `15r+3`: `\kappa_m` is a bijection on the slip lane)

The map
\[
\kappa_m:L_m\to\mathbb Z_M
\]
is a bijection.

#### Proof

If
\[
4+3sq_m\equiv 4+3tq_m\pmod m,
\]
then
\[
3(s-t)q_m\equiv 0\pmod{3M},
\]
so
\[
(s-t)q_m\equiv 0\pmod M.
\]
Now `q_m` is invertible mod `M` because `4q_m\equiv 5\pmod M` and `5\nmid M`.
Hence `s\equiv t\pmod M`.  So the displayed parametrization is injective, and
both sets have cardinality `M`, hence it is bijective.  The `k`-formula follows
from `4q_m\equiv 5`. ∎

### 3.2. Class `m=15r+9`

Here
\[
m=15r+9,
\qquad
M=5r+3,
\qquad
r\ \text{is even}.
\]

### Definition 3.3 (reduced odometer coordinate, class `15r+9`)

For `J\in L_m`, define `\kappa_m(J)\in\mathbb Z_M` by
\[
\boxed{J=2q_m+3\kappa_m(J)q_m.}
\]
Equivalently,
\[
\boxed{4J=10+15\kappa_m(J)\pmod m.}
\]

### Lemma 3.4 (class `15r+9`: `\kappa_m` is a bijection on the slip lane)

The map
\[
\kappa_m:L_m\to\mathbb Z_M
\]
is a bijection.

#### Proof

The proof is identical to Lemma 3.2.  The difference of two values in the
parametrization `2q_m+3sq_m` is again `3(s-t)q_m`, and `q_m` is invertible mod
`M`.  So the parametrization is injective and therefore bijective.  The `k`
formula again follows from `4q_m\equiv 5`. ∎

So in both residue classes the slip lane is literally a copy of the reduced
`+5` odometer.

---

## 4. The first moved carrier becomes a short interval

### Proposition 4.1 (class `15r+3`: the carrier is the initial interval)

If `m=15r+3`, then in the reduced odometer coordinate of Definition 3.1 the
first moved common carrier is exactly
\[
\boxed{\mathcal C_m^{(1)}=[0,r]\subseteq\mathbb Z_M.}
\]

#### Proof

By Fact 1.3,
\[
\mathcal C_m^{(1)}=\{4+3kq_m:0\le k\le r\}.
\]
But by Definition 3.1, the coordinate `\kappa_m` is defined precisely by
\[
J=4+3\kappa_m(J)q_m.
\]
So the carrier points are exactly the points with
\[
\kappa_m(J)=0,1,\dots,r.
\]
That is the displayed interval. ∎

### Proposition 4.2 (class `15r+9`: the carrier is an interval plus one explicit extra point)

If `m=15r+9`, then in the reduced odometer coordinate of Definition 3.3 the
first moved common carrier is exactly
\[
\boxed{\mathcal C_m^{(1)}=[0,r-1]\cup\{2r\}\subseteq\mathbb Z_M.}
\]

#### Proof

By Fact 1.3, the progression part of the carrier is
\[
\{(3k+2)q_m:0\le k\le r-1\}.
\]
Since Definition 3.3 writes every slip phase as
\[
J=2q_m+3\kappa_m(J)q_m,
\]
this progression part corresponds exactly to
\[
\kappa_m(J)=0,1,\dots,r-1.
\]

It remains to locate the extra point `m-2`.  We claim that
\[
\kappa_m(m-2)=2r.
\]
Indeed,
\[
2q_m+3(2r)q_m=(6r+2)q_m.
\]
Multiply by `4`:
\[
4(6r+2)q_m\equiv 5(6r+2)=30r+10\pmod m.
\]
But
\[
4(m-2)=4(15r+7)=60r+28,
\]
and the difference is
\[
(60r+28)-(30r+10)=30r+18=2m.
\]
So
\[
4(6r+2)q_m\equiv 4(m-2)\pmod m.
\]
Because `4` is invertible mod `m`, this yields
\[
(6r+2)q_m\equiv m-2\pmod m.
\]
Hence `\kappa_m(m-2)=2r`, as claimed. ∎

This is the key carrier normal form:

- class `15r+3`: a contiguous window of length `r+1`;
- class `15r+9`: a contiguous window of length `r`, plus one explicit isolated
  extra point `2r`.

---

## 5. Relation with the cut coordinate `T`

The previous slip-lane normal form lived in the cut coordinate
\[
J=4-6T.
\]
We now compute the affine relation between that coordinate and the new reduced
`+5` odometer coordinate.

### Lemma 5.1 (explicit affine relations)

Let `v_M:=5^{-1}\in\mathbb Z_M`.

#### (i) Class `m=15r+3`

One has
\[
\kappa_m=-8v_M\,T.
\]
Since `M=5r+1`, one may choose `v_M\equiv -r\pmod M`, hence
\[
\boxed{\kappa_m=(3r-1)T\pmod M.}
\]

#### (ii) Class `m=15r+9`

One has
\[
\kappa_m=2v_M-8v_M\,T.
\]
Since `M=5r+3`, one may choose `v_M=3r+2`, and therefore
\[
\boxed{\kappa_m=(r+1)+(r-1)T\pmod M.}
\]

#### Proof

In class `15r+3`, combine
\[
4J=16+15\kappa_m
\qquad\text{and}\qquad
J=4-6T.
\]
Then
\[
16-24T\equiv 16+15\kappa_m\pmod m.
\]
Dividing by `3` gives in `\mathbb Z_M`
\[
-8T\equiv 5\kappa_m.
\]
So
\[
\kappa_m=-8v_MT.
\]
Now `M=5r+1`, and indeed
\[
5(-r)= -5r\equiv 1\pmod{5r+1},
\]
so `v_M\equiv -r`, hence
\[
-8v_M\equiv 8r\equiv 3r-1\pmod{5r+1}.
\]
This proves the class `15r+3` formula.

In class `15r+9`, combine
\[
4J=10+15\kappa_m
\qquad\text{and}\qquad
J=4-6T.
\]
Then
\[
16-24T\equiv 10+15\kappa_m\pmod m,
\]
so in `\mathbb Z_M`
\[
2-8T\equiv 5\kappa_m.
\]
Thus
\[
\kappa_m=2v_M-8v_MT.
\]
Now `M=5r+3`, and
\[
5(3r+2)=15r+10\equiv 1\pmod{5r+3},
\]
so one may take `v_M=3r+2`.  Therefore
\[
2v_M=6r+4\equiv r+1\pmod{5r+3},
\]

and
\[
-8v_M=-(24r+16)\equiv r-1\pmod{5r+3}
\]
(after adding `5M=25r+15`).  This proves the second formula. ∎

So the reduced carrier coordinate is not a mysterious new variable: it is an
explicit affine recoding of the already-solved cut coordinate.

---

## 6. The reduced common slip machine and its odometer law

Let `\Phi_{6,m}` be the direct common reinjection phase map on the slip lane, and
let
\[
g_m:=\kappa_m\circ \Phi_{6,m}\circ \kappa_m^{-1}
\qquad\text{on }\mathbb Z_M.
\]
This is the reduced common slip machine in the `+5` odometer coordinate.

### Theorem 6.1 (finite-splice odometer law in the reduced `+5` coordinate)

There is an explicit three-point splice set
\[
\Omega_m\subseteq\mathbb Z_M
\]
such that
\[
\boxed{n\notin \Omega_m\quad\Longrightarrow\quad g_m(n+\lambda_m)=g_m(n)+\lambda_m,}
\]
where
\[
\lambda_m=
\begin{cases}
3r-1,& m=15r+3,\\[1mm]
r-1,& m=15r+9.
\end{cases}
\]
More precisely,
\[
\Omega_m=\kappa_m(\Sigma_m),
\]
where `\Sigma_m` is the three-point splice set from the cut-coordinate note.

#### Proof

By Fact 1.2, in the cut coordinate `U_m` is translation on the three blocks and
satisfies
\[
T\notin\Sigma_m
\quad\Longrightarrow\quad
U_m(T+1)=U_m(T)+1.
\]
By Lemma 5.1, the new coordinate is affine in `T`:
\[
\kappa_m(T)=c_m+\lambda_m T
\]
for explicit constants `c_m,\lambda_m`, with `\lambda_m` invertible mod `M`.
Therefore
\[
\kappa_m(T+1)=\kappa_m(T)+\lambda_m.
\]
Now let `n=\kappa_m(T)` with `T\notin\Sigma_m`.  Then
\[
g_m(n+\lambda_m)
=
\kappa_m\bigl(U_m(T+1)\bigr)
=
\kappa_m\bigl(U_m(T)+1\bigr)
=
\kappa_m(U_m(T))+\lambda_m
=
g_m(n)+\lambda_m.
\]
This proves the displayed odometer law, with splice set exactly the image of
`\Sigma_m` under `\kappa_m`. ∎

So in the correct reduced carrier coordinate, the common direct reinjection is a
finite-splice perturbation of an invertible odometer step.

---

## 7. Explicit global splice placement in the reduced carrier coordinate

We now compute `\Omega_m` completely explicitly.

### Theorem 7.1 (explicit splice sets)

#### (i) Class `m=15r+3`

Here `r` is even.

- If `r\equiv 2\pmod 4` (equivalently `m\equiv 9\pmod{12}`), then
  \[
  \boxed{\Omega_m=\{r+1,\ 2r+2,\ 3r+1\}.}
  \]
- If `r\equiv 0\pmod 4` (equivalently `m\equiv 3\pmod{12}`), then
  \[
  \boxed{\Omega_m=\{2r+2,\ 4r+2,\ 5r-1\}.}
  \]

In both subcases,
\[
\boxed{\Omega_m\cap [0,r]=\varnothing.}
\]

#### (ii) Class `m=15r+9`

Again `r` is even.

- If `r\equiv 0\pmod 4` (equivalently `m\equiv 9\pmod{12}`), then
  \[
  \boxed{\Omega_m=\{2,\ 2r+2,\ 3r+3\}.}
  \]
- If `r\equiv 2\pmod 4` (equivalently `m\equiv 3\pmod{12}`), then
  \[
  \boxed{\Omega_m=\{2,\ r-1,\ 4r+4\}.}
  \]

Hence for the main carrier interval `[0,r-1]` one has:

- in the subcase `r\equiv 0\pmod 4`,
  \[
  \boxed{\Omega_m\cap [0,r-1]=\{2\};}
  \]
- in the subcase `r\equiv 2\pmod 4`,
  \[
  \boxed{\Omega_m\cap [0,r-1]=\{2,r-1\}}
  \]
  (with the edge case `r=2`, where this set is just `\{1\}`).

Finally, in every class `m=15r+9`, the isolated extra carrier point `2r` is not
in `\Omega_m`.

#### Proof

We combine Lemma 5.1 with the explicit `T`-splice set `\Sigma_m` from the
cut-coordinate slip note.

---

### Class `m=15r+3`, subcase `r\equiv 2\pmod 4`

Then `m\equiv 9\pmod{12}` and the cut-coordinate note gives
\[
\Sigma_m=
\left\{\frac{5r}{2},\ \frac{15r+2}{4},\ 5r\right\}.
\]
Also `\kappa_m=(3r-1)T`.  So
\[
\Omega_m=(3r-1)\Sigma_m.
\]
Now
\[
(3r-1)\frac{5r}{2}-(r+1)=\frac{(5r+1)(3r-2)}2,
\]
\[
(3r-1)\frac{15r+2}{4}-(3r+1)=\frac{3(5r+1)(3r-2)}4,
\]
\[
(3r-1)(5r)-(2r+2)=-(3r-1)+(5r+1)=2r+2-(2r+2)=0
\]
modulo `5r+1`.  Hence
\[
\Omega_m=\{r+1,2r+2,3r+1\}.
\]
All three points are strictly larger than `r`, so `\Omega_m\cap[0,r]=\varnothing`.

---

### Class `m=15r+3`, subcase `r\equiv 0\pmod 4`

Then `m\equiv 3\pmod{12}` and the cut-coordinate note gives
\[
\Sigma_m=
\left\{\frac{15r}{4},\ \frac{15r+8}{4},\ 5r\right\}.
\]
Again `\kappa_m=(3r-1)T`.  So
\[
\Omega_m=(3r-1)\Sigma_m.
\]
Now
\[
(3r-1)\frac{15r}{4}-(4r+2)=\frac{(5r+1)(9r-8)}4,
\]
\[
(3r-1)\frac{15r+8}{4}-(5r-1)=\frac{(5r+1)(9r-4)}4,
\]
\[
(3r-1)(5r)-(2r+2)=0
\]
modulo `5r+1`.  Hence
\[
\Omega_m=\{2r+2,4r+2,5r-1\}.
\]
Again all three points are strictly larger than `r`, so `\Omega_m\cap[0,r]=\varnothing`.

---

### Class `m=15r+9`, subcase `r\equiv 0\pmod 4`

Then `m\equiv 9\pmod{12}` and the cut-coordinate splice set is
\[
\Sigma_m=
\left\{\frac{5r+2}{2},\ \frac{15r+8}{4},\ 5r+2\right\}.
\]
Also Lemma 5.1 gives
\[
\kappa_m=(r+1)+(r-1)T.
\]
So
\[
\Omega_m=(r+1)+(r-1)\Sigma_m.
\]
A direct calculation gives
\[
(r+1)+(r-1)\frac{5r+2}{2}-(3r+3)=\frac{(5r+3)(r-2)}2,
\]
\[
(r+1)+(r-1)\frac{15r+8}{4}-(2r+2)=\frac{(5r+3)(3r-4)}4,
\]
\[
(r+1)+(r-1)(5r+2)-2=(5r+3)(r-1).
\]
So
\[
\Omega_m=\{2,2r+2,3r+3\}.
\]
Only the point `2` lies in `[0,r-1]`, proving the claimed intersection.
Clearly `2r` is different from all three splice points.

---

### Class `m=15r+9`, subcase `r\equiv 2\pmod 4`

Then `m\equiv 3\pmod{12}` and the cut-coordinate splice set is
\[
\Sigma_m=
\left\{\frac{15r+6}{4},\ \frac{15r+14}{4},\ 5r+2\right\}.
\]
Again
\[
\kappa_m=(r+1)+(r-1)T.
\]
Now
\[
(r+1)+(r-1)\frac{15r+6}{4}-(4r+4)=\frac{3(r-2)(5r+3)}4,
\]
\[
(r+1)+(r-1)\frac{15r+14}{4}-(r-1)=\frac{(3r+1)(5r+3)}4,
\]
\[
(r+1)+(r-1)(5r+2)-2=(4s+1)(20s+13)
\]
when `r=4s+2`, hence the last value is `2` modulo `5r+3`.
Therefore
\[
\Omega_m=\{2,r-1,4r+4\}.
\]
If `r=2`, the main carrier interval is `[0,1]`, so the intersection is just
`\{1\}`.  If `r\ge 6`, both `2` and `r-1` lie in `[0,r-1]`, while `4r+4` lies
strictly to the right.  Again `2r` is distinct from all three splice points. ∎

This theorem is the most concrete gain of the present pass.

- In class `15r+3`, the carrier window starts entirely away from the global
  splices.
- In class `15r+9`, the initial irregularity is confined to one or two explicit
  carrier indices.

So the mod-`5` asymmetry is now visible directly in the reduced odometer
coordinate.

---

## 8. The induced carrier return exists and is a finite piecewise translation

We now define the actual reduced carrier machine.

### Definition 8.1 (carrier state sets)

Set
\[
X_m=
\begin{cases}
[0,r],& m=15r+3,\\[1mm]
[0,r-1]\cup\{2r\},& m=15r+9.
\end{cases}
\]
By Propositions 4.1 and 4.2, this is exactly the first moved common carrier in
reduced odometer coordinates.

Let
\[
R_m:X_m\to X_m
\]
be the first-return map of `g_m` to `X_m`.

### Theorem 8.2 (finite piecewise-translation carrier return)

For every admissible `m`, the first-return map `R_m` is well defined and there is
some finite subset
\[
B_m\subseteq X_m
\]
such that on every connected component of `X_m\setminus B_m` the map `R_m` is a
translation.

Equivalently: the reduced carrier machine is a **finite piecewise-translation
permutation**.

#### Proof

Because `g_m` is a permutation of the finite set `\mathbb Z_M`, every point of
`X_m` returns to `X_m`, so `R_m` is well defined.

Let `h_m(x)` be the first-return time.  Since `X_m` is finite, there is some
finite maximum
\[
H_m:=\max_{x\in X_m} h_m(x).
\]
Now define
\[
B_m:=X_m\cap\bigcup_{0\le j<H_m} g_m^{-j}(\Omega_m\cup \partial X_m),
\]
where `\partial X_m` means the interval endpoints of the contiguous carrier
window, together with the isolated point `2r` in the class `15r+9` case.

Take a component `C` of `X_m\setminus B_m`.  By construction, for every
`x\in C`, the whole orbit segment
\[
x,\ g_m(x),\ \dots,\ g_m^{h_m(x)-1}(x)
\]
avoids both the global splice set `\Omega_m` and the carrier boundary.  Hence
for each iterate level `j<h_m(x)`, the restriction of `g_m^j` to `C` follows one
fixed translation branch of the global finite-splice machine.  Therefore the
whole composition up to the first return is again a translation on `C`.

Since this is true for each component `C`, the first-return map `R_m` is a
finite piecewise translation. ∎

So the carrier problem has now been reduced to the right symbolic object.

It is **not** yet solved.  But it is no longer an unstructured post-defect
permutation problem; it is a finite-splice return map on a short odometer window.

---

## 9. What changed in the proof picture

The previous notes had already produced:

- a full common phase-height cocycle;
- a first-defect mod-`5` classification;
- a mod-`3` slip-lane permutation;
- a cut-coordinate finite-splice normal form.

The present pass adds the missing odometer reduction.

1. The fast common clock is now literally `+5` in the `k=4J` coordinate.
2. After mod-`3` reduction to the slip lane, the first moved carrier becomes a
   **short explicit window** in the reduced `+5` odometer coordinate.
3. The global splice set is no longer abstract: it is an explicit three-point set
   in that reduced coordinate.
4. In class `15r+3`, the carrier window starts **splice-free**.
5. In class `15r+9`, the initial splice interaction is confined to one or two
   explicit carrier indices.
6. The true next target is therefore no longer to search for an ad hoc phase
   variable.  The variable is now known.  The next target is to analyze the
   cohomological equation for the reduced carrier return `R_m`.

That is the exact D5 common-branch analogue of the D3/D4 strategy: isolate the
fast odometer coordinate first, then solve the finite-splice return machine.
