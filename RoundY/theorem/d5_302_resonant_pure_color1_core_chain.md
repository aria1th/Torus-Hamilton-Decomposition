# D5 302 Resonant Pure Color-1 Core Theorem Chain

This note promotes the proof-carrying substance of the `2026-03-26`
resonant pure color-`1` bundle into one stable RoundY chain.

It is not a new theorem by itself.
Its job is to say, in theorem order, what the current resonant pure color-`1`
proof stack actually contains and how the pieces fit together.

The point is to avoid forcing a new reader to reconstruct the chain from many
`tmp/` notes.

## 1. Fixed setup

We work on the color-`1` branch of the exact `\Sigma=0` section return in
coordinates
\[
(a,c,d,e)=(x_0,x_2,x_3,x_4),
\]
with
\[
H_m=\{c=0,d=0\},
\qquad
B_m=\{c=0,d=0,e=0\}.
\]

For late resonant odd moduli, write `r=(m-1)/2` and consider the promoted `+`
control together with the central and flank late families.

## 2. Foundational reductions now treated as proof-safe

The current stack already proves the following structural facts.

### 2.1. Exact `B`-spectator law

Pure color `1` depends only on the visible `A/C` channel.
Appended `B=(02)` rows do not change:

- the exact `m`-block return on `\Sigma=0`;
- the induced maps on `H_m` and `B_m`;
- any color-`1` cycle decomposition.

So donor cleanup is genuinely separated from the pure color-`1` problem.

### 2.2. Exact same-row toggle semantics

Over the promoted `+` background, same-row additions are not naive unions.
They act by exact left multiplication in `S_3`.
This gives the effective rowword profiles of the current late families.

### 2.3. Local family differences live only at the top / double-top interface

The current late families have:

- the same exact low-band law;
- the same exact side-top law;
- and differ only on the top / double-top interface.

This is the reduction that turns the resonant branch into a hinge/top analysis
rather than a broad full-torus search.

## 3. Zero-state `H_m` theorems already in hand

The current stack also contains theorem-level zero-state `H_m` results.

### 3.1. Promoted and central zero-state first `H_m` return coincide

The promoted zero-state first `H_m` return never enters the double-top interior
or the double hinge.
Since promoted and central agree on the relevant local regimes, their zero-state
first `H_m` return is the same.

### 3.2. Flank zero-state first `H_m` return is explicit

For the flank family, the zero-state first `H_m` return is exactly
\[
(1,0,0,m-4).
\]

So the promoted/central coincidence and the flank shift are both theorem-level,
not only checked atlas patterns.

## 4. Top burst is already solved once entrance data are known

The top-collar phase-exit theorem is already available as an arithmetic
transducer statement.

On one uninterrupted top-collar episode, the late dynamics are governed by
\[
w_{n+1}=w_n+\kappa,
\qquad
c_{n+1}=c_n+4-\mathbf 1[w_n=1],
\]
with
\[
\kappa=
\begin{cases}
5, & \text{promoted / central},\\
4, & \text{flank}.
\end{cases}
\]

So the top burst itself is no longer the mystery.
The lower dynamics decide which top or double-top entrance is produced; after
that, the burst is already under arithmetic control.

## 5. Lower-to-hinge classification is now closed

The pre-hinge region carries:

- an exact `c`-clock,
- an exact `d`-counter,
- and the conserved phase
  \[
  J_0=a-\mathbf 1[e=m-1].
  \]

The new master theorem
[d5_300_resonant_Hm_master_hinge_profile_theorem.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_300_resonant_Hm_master_hinge_profile_theorem.md)
then closes the whole first hinge on `H_m`.

In particular:

- the first support hit from `H_m` is always a hinge at time `m(m-1)-2`;
- the first hinge on all of `H_m` is given by one common profile
  \[
  E_h(a,e)=e+\eta_0(J_0)\pmod m;
  \]
- the initial side-top slice `e=m-1` is no longer missing.

So the lower-to-hinge problem is now off the live frontier.

## 6. What is theorem-level versus checked ledger

The current stack now splits cleanly.

### Theorem-level

- visible-channel reduction and `B`-spectator law
- toggle semantics and effective rowword profiles
- local interface comparison
- promoted/central zero-state `H_m` coincidence
- flank zero-state `H_m` target
- top phase-exit arithmetic
- full first-hinge classification on all of `H_m`

### Checked-exact ledger

- late `B_m/H_m` winner and defect cases
- zero-state late atlas
- mod-`30` routing picture
- first exact late promotions such as `183` central and `201` flank

So the remaining live arithmetic structure is no longer basic local dynamics.
It is the bridge from the now-closed `H_m` hinge/top classification to the
late `B_m` winner/defect ledger.

## 7. Current next proof target

The clean next theorem target is now:

1. explicit double-top phase-exit on the double-hinge graph;
2. then `H_m -> B_m` stitching;
3. then a theorem-level late central/flank residual law.

That is the core proof chain the current D5 resonant branch should be read
through.
