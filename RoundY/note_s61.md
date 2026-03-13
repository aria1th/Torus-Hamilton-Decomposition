046 is a real pivot.

I checked the saved tables and pushed one follow-on step on the frozen 046 dataset. The carry sheet is now best read as the **first exact future nonflat-event datum** on the grouped base, and the next branch can be narrowed further than the README states.

The useful sharpening is:

[
B=(s,u,v,\mathrm{layer},\mathrm{family}),\qquad
\tau=\text{initial flat-run length for }dn=(0,0,0,1),
]

and let (\epsilon) be the current grouped-delta event class.

On the checked active branch for (m=5,7,9,11):

* (B+\tau+\epsilon) is exact for
  [
  c=1_{{q=m-1}}.
  ]
* More sharply, **every** collision of (B+\tau) occurs at
  [
  \tau=0.
  ]
* So for (\tau>0), the carry bit is already determined by (B+\tau).
* On the boundary (\tau=0), a **3-class** current nonflat event label
  [
  {\text{wrap},\ \text{carry_jump},\ \text{other}}
  ]
  resolves the remaining ambiguity exactly.

So the live hidden datum now looks even narrower:

**the main hard part is admissible coding of (\tau),**
not a vague broader gauge, and not the whole future window.

I saved that follow-on analysis here:

[046 boundary follow-on analysis](./checks/d5_046_boundary_followon_analysis.json)

And I wrote the next compute-first template here:

[047 work template](./specs/d5_future_transition_carry_coding_047_work_template.md)

The clean branch map now is:

* settled structure:
  [
  B \leftarrow B+c \leftarrow B+c+d
  ]
  with
  [
  c=1_{{q=m-1}},\qquad
  d=1_{{\text{next carry }u\ge m-3}}.
  ]
* settled dynamic fact:
  (c) is already an exact future grouped-transition event.
* sharpened local target:
  code
  [
  \tau=\text{time to first nonflat grouped-delta event}
  ]
  admissibly; the boundary correction at (\tau=0) is then just a small current event class.

So 047 should not start from “more carry features.” It should start from:

1. freeze (B,c,\tau,\epsilon),
2. prune smaller exact quotients,
3. search admissible families aimed specifically at (\tau),
4. treat the (\tau=0) boundary label as a secondary correction, not the main hidden state.

The theorem-level reading also gets cleaner:

* (d) is the binary anticipation sheet from 044,
* (c) is the first exact future nonflat-event sheet on the grouped base,
* the remaining local obstruction is admissible access to that anticipation datum.

Once your 047 search stabilizes, send the summary JSONs and I’ll turn the surviving result into the next proof package.
