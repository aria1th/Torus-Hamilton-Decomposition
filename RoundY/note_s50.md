This bundle is enough to continue. I do not need more repo context before the next branch.

The main update is sharper than I expected:

**the live corridor phase is already visible on raw current coordinates.**
What is still missing is not phase extraction, but a way to **localize** the intervention to the right corridor.

Here is the cleanest form I verified.

### 1. `036` is correct, and it reruns

I reran the included `036` script from the bundle root with the provided `scripts/` tree. It reproduces the stated result: `034` is only a first-pass `(s,layer)` lap, while the traced long corridor is exact on lifted coordinates `(q,a,layer)` up to first exit.

### 2. The lifted corridor can be rewritten on raw coordinates `(q,w,layer)`

Using the saved `035` path tables for all checked moduli `m=5,7,9,11`, I verified that along every traced `R1 -> H_L1` corridor state up to first exit,
[
a \equiv q+w-\mathbf 1_{{\text{layer}=1}} \pmod m.
]

So the `036` lifted phase is not just readable from `(q,a,layer)`; it is already readable from the raw current triple
[
(q,w,\text{layer}).
]

On that triple, the corridor follows the exact rule
[
(q,w,0)\mapsto(q+1,w,1),
]
[
(q,w,1)\mapsto(q,w,2),
]
[
(q,w,2)\mapsto(q,w+\mathbf 1_{{q=m-1}},3),
]
and otherwise
[
(q,w,\ell)\mapsto(q,w,\ell+1 \bmod m).
]

That was not just true on one representative. I checked it against the saved path rows for every source slice in `m=5,7,9,11`.

### 3. The corridor is an explicit odometer

On the layer-`2` cross-section, the induced map is
[
(q,w)\mapsto(q+1,; w+\mathbf 1_{{q=m-1}})
]
with entry point
[
(q,w)=(m-1,1).
]

So this is an exact base-`m` odometer, with cross-section phase
[
\eta \equiv q + m(w-1) - (m-1)\pmod{m^2},
]
for which one step of the layer-`2` return map is exactly
[
\eta \mapsto \eta+1.
]

A full orbit coordinate is then obtained by adding the fast layer digit. One clean version is:

[
\hat q = q-\mathbf 1_{{\ell=1}} \pmod m,
]
[
\hat w = w-\mathbf 1_{{\ell\neq 2}}\mathbf 1_{{\hat q=m-1}} \pmod m,
]
[
\chi \equiv
m\Big(\hat q + m(\hat w-1) - (m-1)\Big) + (\ell-2 \bmod m)
\pmod{m^3}.
]

With entry state
[
(q,w,\ell)=(m-1,1,2),
]
this gives
[
\chi=0,
]
and each corridor step is exactly
[
\chi\mapsto\chi+1.
]

### 4. The first-exit targets are now explicit raw phase points

In raw phase coordinates, the first exit-capable states are uniform:

regular family `u_source != 3`:
[
(q,w,\ell)=(m-1,m-2,1),\qquad \text{exit direction }[2],
]

exceptional family `u_source = 3`:
[
(q,w,\ell)=(m-2,m-1,1),\qquad \text{exit direction }[1].
]

Their phase values are
[
\chi_{\mathrm{reg}}=(m-3)m^2-1,
]
[
\chi_{\mathrm{exc}}=\chi_{\mathrm{reg}}+m(m-1).
]

So the old “one target class” picture from `034` needs one correction:
on the true lifted/raw odometer there are **two** first-exit targets, separated by exactly
[
m(m-1),
]
which is one full projected `034` lap.

### 5. What this changes conceptually

This is the strongest new takeaway:

**phase exposure is no longer the main missing ingredient.**

The phase is already exposed by the raw current triple
[
(q,w,\text{layer}).
]

That also explains why `(q,w,layer)` appeared among the `035` separating 3-coordinate projections.

So the obstruction after `035/036` is better read as:

* not “find phase,”
* not “find a slightly bigger transducer,”
* but **find a corridor-local carrier that activates only on the intended defect corridor and then uses the already-visible `(q,w,layer)` phase to fire at the right target.**

### 6. Smallest plausible next mechanism

My best current candidate is:

**an entry-marker transport mechanism.**

More precisely:

* create a marker only at the initial `R1` alt-`2` entry,
* transport that marker through the unary `BBB` corridor,
* use the already-visible raw odometer phase `(q,w,layer)` to trigger:

  * `[2]` at ((m-1,m-2,1)) for regular slices,
  * `[1]` at ((m-2,m-1,1)) for the exceptional slice.

The only extra information that still seems needed beyond phase is a tiny family marker distinguishing
[
u_{\text{source}}=3
\quad\text{vs}\quad
u_{\text{source}}\neq 3.
]

So the next branch is not a “phase-exposure search.” It is a **localized phase-trigger search**.

### 7. What I would make the next exact task

I would update the target to something like:

**D5-LIFTED-CORRIDOR-CARRIER-037**

Question:
Can one realize a one-bit corridor-local carrier that is born at the `R1` alt-`2` entry, survives along `BBB`, and triggers only at the universal raw phase points
[
(m-1,m-2,1)\quad\text{or}\quad(m-2,m-1,1)
]
according to the regular/exceptional entry class?

Success would show the missing state is:

* not hidden phase,
* but a tiny localized carrier on top of an already explicit odometer.

Failure would be informative too:
it would say the missing ingredient is richer than “visible phase + one entry marker.”

The brief version of the updated status is:

**explicit phase coordinate:** yes, on raw `(q,w,layer)` as an exact `m^3` odometer.

**target phase class:** refined to two universal lifted/raw targets,
[
(m-1,m-2,1)\ \text{and}\ (m-2,m-1,1),
]
separated by (m(m-1)).

**best next local candidate:** not a static gate, but an **entry-marker transport mechanism** that uses the already-visible `(q,w,layer)` phase.
