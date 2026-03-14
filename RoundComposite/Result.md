There is a clean theorem-level solution.

Let
[
D_6(m)=\operatorname{Cay}\big((\mathbb Z/m\mathbb Z)^6,{e_0,e_1,e_2,e_3,e_4,e_5}\big).
]
Write a vertex as ((x,y)) with (x\in(\mathbb Z_m)^3) and (y\in(\mathbb Z_m)^3). Then
[
D_6(m)\cong D_3(m)\square D_3(m),
]
the Cartesian product of two copies of the directed (3)-torus.

So the whole problem collapses to one product lemma.

## Square lemma

Let (\vec C_n) be the directed (n)-cycle, and consider (\vec C_n\square \vec C_n) on (\mathbb Z_n^2).
At each ((u,v)) there are exactly two outgoing edges:
[
(u,v)\to(u+1,v),\qquad (u,v)\to(u,v+1).
]

Define two 1-factors (H_0,H_1) by
[
H_0(u,v)=
\begin{cases}
(u+1,v), & u+v\not\equiv n-1 \pmod n,\
(u,v+1), & u+v\equiv n-1 \pmod n,
\end{cases}
]
and let (H_1) be the complementary choice:
[
H_1(u,v)=
\begin{cases}
(u,v+1), & u+v\not\equiv n-1 \pmod n,\
(u+1,v), & u+v\equiv n-1 \pmod n.
\end{cases}
]

These clearly partition the two outgoing edges at each vertex. They also partition the two incoming edges: into ((u,v)), the west edge is used by (H_0) unless (u+v\equiv0), while the south edge is used exactly when (u+v\equiv0). So both (H_0) and (H_1) are directed 1-factors.

Now conjugate (H_0) by
[
\Psi(u,v)=(s,t):=(u+v,;v).
]
Then
[
\Psi H_0\Psi^{-1}(s,t)=
\begin{cases}
(s+1,t), & s\neq n-1,\
(0,t+1), & s=n-1.
\end{cases}
]
That is the standard odometer on (\mathbb Z_n^2). Starting from ((0,0)), after (k) steps it is
[
(k\bmod n,;\lfloor k/n\rfloor \bmod n),
]
so it is a single cycle of length (n^2). Hence (H_0) is Hamilton.

Also (H_1) is conjugate to (H_0) by the coordinate swap ((u,v)\mapsto(v,u)), so (H_1) is Hamilton too.

Therefore:

[
\vec C_n\square \vec C_n
]
decomposes into **two** directed Hamilton cycles.

## Apply this to (d=6)

Now take your (d=3) decomposition on each factor. For a fixed (m), let
[
A_0,A_1,A_2
]
be the three Hamilton cycles of the first copy of (D_3(m)), and let
[
B_0,B_1,B_2
]
be the corresponding three Hamilton cycles of the second copy.

Set
[
F_i:=A_i\square B_i \qquad (i=0,1,2).
]
Each (A_i) and (B_i) is a directed cycle of length
[
n=m^3,
]
so each (F_i) is isomorphic to
[
\vec C_n\square \vec C_n.
]
By the square lemma, each (F_i) splits into two Hamilton cycles, say
[
F_i=H_{i,0}\sqcup H_{i,1}.
]

That gives (6) Hamilton cycles total:
[
H_{0,0},H_{0,1},H_{1,0},H_{1,1},H_{2,0},H_{2,1}.
]

Why do they cover all arcs of (D_6(m))? Because every arc in the first (3) coordinates belongs to exactly one (A_i), and every arc in the last (3) coordinates belongs to exactly one (B_i). Hence every arc of
[
D_3(m)\square D_3(m)
]
belongs to exactly one (F_i), and then to exactly one of its two Hamilton cycles.

So we get:

[
\boxed{\text{For every } m\ge 3,; D_6(m)\text{ admits a Hamilton decomposition.}}
]

This is a complete existence proof for (d=6), provided you plug in the already-available (d=3) theorem.

What it does **not** give yet is the kind of tiny low-layer local witness you have in (d=3) and (d=4). I did try a direct (d=4)-style (6)-color low-layer Ansatz first; it did not collapse cleanly. But the product argument above really does close the (d=6) case.

There is also a useful general corollary hiding here: once a digraph (G) has a Hamilton decomposition, (G\square G) automatically does too. In your setting, that means any solved (d) immediately gives (2d).
