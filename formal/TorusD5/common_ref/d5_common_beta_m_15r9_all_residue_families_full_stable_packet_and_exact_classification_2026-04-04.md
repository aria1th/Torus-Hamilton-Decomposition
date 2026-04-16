
# d=5 common branch, class `m=15r+9`: full stable residual-core packet and exact classification across all residue families (2026-04-04)

## 0. Purpose

The archive previously had two different kinds of common-branch packet material:

1. full stable portal packets for the `r=8s` and `r=8s+4` families;
2. newly completed reduction / handwritten / exact-merge work for the four live families
   \[
   r\equiv 2,6,10,14 \pmod{16}.
   \]

This note splices those strands into one common-branch statement.

The main outcome is:

- every residue family of the common class
  \[
  m=15r+9
  \]
  now has a stable residual-core first-rung packet;
- the packet is **exact** on the stable residual core, not merely positive;
- there are only **two** stable packet geometries, distinguished by whether
  \[
  r\equiv 0 \pmod 4
  \quad\text{or}\quad
  r\equiv 2 \pmod 4.
  \]

The only structural difference between those two geometries is the fate of the boundary leaf `x=1`.

---

## 1. Family map and honest stable ranges

The common `m=15r+9` line breaks into the following residue families.

### Type A: `r\equiv 0 \pmod 4`

- `r=8s`, i.e.
  \[
  m=120s+9,
  \qquad s\ge 2;
  \]
- `r=8s+4`, i.e.
  \[
  m=120s+69,
  \qquad s\ge 1.
  \]

These are exactly the two April 3 portal-packet families.

### Type B: `r\equiv 2 \pmod 4`

- `r=16u+2`, i.e.
  \[
  m=240u+39,
  \qquad u\ge 1;
  \]
- `r=16u+6`, i.e.
  \[
  m=240u+99,
  \qquad u\ge 0;
  \]
- `r=16u+10`, i.e.
  \[
  m=240u+159,
  \qquad u\ge 0;
  \]
- `r=16u+14`, i.e.
  \[
  m=240u+219,
  \qquad u\ge 0.
  \]

These are the four families completed on April 4.

So the full stable theorem covers **all** residue classes modulo `16`, with family-specific low-end cutoffs.

---

## 2. Shared time palette and shared nongeneric leaves

On the stable residual core of every family above, the same seven first-rung times occur:

\[
n_1=\frac{m-4}{5},
\qquad
n_0=\frac{m+1}{5},
\qquad
n_2=\frac{2m-3}{5},
\]
\[
n_3=\frac{3m-2}{5},
\qquad
n_4=\frac{8m-2}{5},
\qquad
n_5=\frac{9m-1}{5},
\qquad
n_6=\frac{11m+1}{5}.
\]

The nongeneric leaves are always

\[
Z:=\{7,11\},
\qquad
E_2:=\{12\},
\qquad
E_3:=\{15\}.
\]

Their branch/output data are uniform:

\[
7,11 \longrightarrow \text{zero at } n_0,
\qquad
7\mapsto 8,\quad 11\mapsto 12,
\]
\[
12 \longrightarrow \mathrm{exc2} \text{ at } n_1,
\qquad
12\mapsto 9,
\]
\[
15 \longrightarrow \mathrm{exc3} \text{ at } n_2,
\qquad
15\mapsto 11.
\]

So the genuine remaining difference between residue families lies only in the generic source slices.

---

## 3. Type A packet (`r\equiv 0 \pmod 4`)

For Type A families, define

\[
A_1:=\{x: x\equiv 4\pmod 5\},
\]
\[
A_2:=\bigl(\{x: x\equiv 0\pmod 5\}\setminus\{15\}\bigr)\cup\{1,6,16\},
\]
\[
A_3:=\{x: x\equiv 3\pmod 5\}\setminus\{3,8,13\},
\]
\[
A_4:=\bigl(\{x: x\equiv 1\pmod 5\}\setminus\{1,6,11,16\}\bigr)\cup\{8\},
\]
\[
A_5:=\{2\},
\]
\[
A_6:=\bigl(\{x: x\equiv 2\pmod 5\}\setminus\{2,7,12\}\bigr)\cup\{3,13\}.
\]

Then on the stable residual core of every Type A family:

- `A_1` is generic at `n_1=(m-4)/5`;
- `A_2` is generic at `n_2=(2m-3)/5`;
- `A_3` is generic at `n_3=(3m-2)/5`;
- `A_4` is generic at `n_4=(8m-2)/5`;
- `A_5` is generic at `n_5=(9m-1)/5`;
- `A_6` is generic at `n_6=(11m+1)/5`.

In this geometry the boundary leaf `x=1` survives on the stable residual core and belongs to the second affine class `A_2`.

---

## 4. Type B packet (`r\equiv 2 \pmod 4`)

For Type B families, define

\[
B_1:=\{x: x\equiv 4\pmod 5\},
\]
\[
B_2:=\bigl(\{x: x\equiv 0\pmod 5\}\setminus\{15\}\bigr)\cup\{6,16\},
\]
\[
B_3:=\{x: x\equiv 3\pmod 5\}\setminus\{3,8,13\},
\]
\[
B_4:=\bigl(\{x: x\equiv 1\pmod 5\}\setminus\{6,11,16\}\bigr)\cup\{8\},
\]
\[
B_5:=\{2\},
\]
\[
B_6:=\bigl(\{x: x\equiv 2\pmod 5\}\setminus\{2,7,12\}\bigr)\cup\{3,13\}.
\]

Then on the stable residual core of every Type B family:

- `B_1` is generic at `n_1=(m-4)/5`;
- `B_2` is generic at `n_2=(2m-3)/5`;
- `B_3` is generic at `n_3=(3m-2)/5`;
- `B_4` is generic at `n_4=(8m-2)/5`;
- `B_5` is generic at `n_5=(9m-1)/5`;
- `B_6` is generic at `n_6=(11m+1)/5`.

In this geometry the boundary leaf `x=1` does **not** survive on the stable residual core.  
Equivalently, the only extra boundary leaves in the second affine class are `6` and `16`.

---

## 5. Exact exclusion/completeness on the stable residual core

The exactness step now splits into two finite partition lemmas.

### Type A partition lemma
The nine pieces
\[
Z,\ E_2,\ E_3,\ A_1,\dots,A_6
\]
partition the integer coordinate `x`.

Indeed:

- residue `4 (mod 5)` gives `A_1`;
- residue `0 (mod 5)` gives `E_3` only at `x=15`, otherwise `A_2`;
- residue `3 (mod 5)` gives `A_3`, except `8\in A_4` and `3,13\in A_6`;
- residue `1 (mod 5)` gives `A_4`, except `1,6,16\in A_2` and `11\in Z`;
- residue `2 (mod 5)` gives `A_6`, except `2\in A_5`, `7\in Z`, `12\in E_2`.

### Type B partition lemma
The nine pieces
\[
Z,\ E_2,\ E_3,\ B_1,\dots,B_6
\]
also partition the integer coordinate `x`.

Indeed the same residue split works, except now:

- residue `1 (mod 5)` gives `B_4`, except `6,16\in B_2` and `11\in Z`.

The earlier family packets already proved the positive branch/time statement on the stable residual core for each displayed piece.
Therefore the partition lemmas close the last exclusion gap:

### Exact stable theorem
For every stable family in Section 1, every stable residual-core source has **exactly one** first special rung/branch described by the corresponding Type A or Type B packet above.

So the common `m=15r+9` stable packet is now exact, not only positive.

---

## 6. What changed conceptually

The common branch is no longer blocked at the family-by-family atlas stage.

That stage is now finished at the stable residual-core level:

- the April 3 families `r=8s` and `r=8s+4` supply the Type A packet;
- the April 4 families `r\equiv 2,6,10,14 (mod 16)` supply the Type B packet;
- the only real geometric bifurcation is whether the boundary leaf `x=1` survives.

So the common-branch frontier has shifted one level upward:

\[
\text{family atlas / cumulative-drop packet}
\quad\longrightarrow\quad
\text{residual-core quotient compression}.
\]

---

## 7. Checked addendum on the pre-stable low seeds

Although the honest theorem above is the **stable** theorem, the same first-rung classifier already matches direct computation on the three pre-stable seeds

\[
m=39,\qquad m=69,\qquad m=129.
\]

More precisely:

- `m=39` matches the Type B classifier;
- `m=69` and `m=129` match the Type A classifier.

What still fails is the tiny modulus

\[
m=9,
\]
which is a genuine small exceptional case and remains outside the unified packet.

So the real finite-exception burden has now shrunk to:

- a stable theorem for all residue families;
- a checked extension to `m=39,69,129`;
- one tiny outlier `m=9`.

---

## 8. Evidence window

A combined splice check verifies the exact packet classification on the following stable windows:

- `r=8s`: `2\le s\le 8`;
- `r=8s+4`: `1\le s\le 7`;
- `r=16u+2`: `1\le u\le 8`;
- `r=16u+6`, `r=16u+10`, `r=16u+14`: `0\le u\le 8`.

That is `49` stable moduli in total.

The same check also verifies the classifier on the pre-stable seeds
\[
m=39,\ 69,\ 129
\]
and isolates `m=9` as the unique tiny failure of the unified packet.
