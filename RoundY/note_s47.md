The level I want next is:

**one best seed, one corridor-phase model, one orbit-phase verdict.**

`033` says the next problem is no longer “find a smaller transducer.”
It is:

**understand the unresolved `R1 -> H_L1` channel as a reduced orbit-phase problem, not as a missing separator-bit problem.**

The note for `033` already sharpens this a lot: per color the best-seed defect quotients to four overfull and four hole families, three channels repair directly, and only `R1 -> H_L1` remains; on the extracted local alphabet, its shortest natural splice is a unary `BBB` corridor with lower bounds `50, 196, 486` states on `m=5,7,9`, which kills 2-state and 3-state transducers in this model. 

The extra structural point I’d emphasize is this:

the two delay families you quoted,
[
49,195,485
\quad\text{and}\quad
69,237,557,
]
differ by
[
20,42,72 = m(m-1).
]
That is exactly the size of the large grouped base orbit from `023`.

So my leading hypothesis is:

**the unresolved `R1 -> H_L1` channel is already a phase problem on the known reduced orbit, and the “missing state” is not a small finite transducer state but an orbit-phase coordinate along that corridor.**

That is the next thing I would extract.

Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field.

Current target:
Do **not** search larger tiny transducers blindly.
The next honest branch is:

**extract the unresolved `R1 -> H_L1` channel as a reduced corridor-phase model**, and determine whether the missing repair state is already an orbit-phase variable on the known `023/025` reduced dynamics.

Known assumptions:

* `025` remains the correct reduced target:

  * omit-base plus edge-tied point cocycle defect,
  * grouped base orbit size `m^2`,
  * full grouped orbit size `m^3`.
* `026/027` rule out the current-state `B/P/M` stationary realization.
* `028` identifies endpoint orientation as the right missing local signature.
* `029`, `031`, and `032` rule out the smallest static endpoint-word and one-bit/two-class repairs.
* `033` sharpens the best-seed branch:

  * best seed:

    * left `[2,2,1]`
    * right `[1,4,4]`
  * exact defect law:
    [
    10m^2
    ]
  * per color:

    * four overfull families,
    * four hole families,
    * `m`-fold `v` translation,
  * direct repair channels:

    * `L3 -> H_L3`
    * `R2 -> H_R2`
    * `R3 -> H_R3`
  * only unresolved channel:

    * `R1 -> H_L1`
  * on the extracted local alphabet, the shortest natural splice is a unary `BBB` corridor,
    with lower bounds:
    [
    50,\ 196,\ 486
    ]
    states on `m=5,7,9`, so 2-state and 3-state transducers are impossible in this model. 
* New structural observation:
  the two quoted delay families differ by
  [
  m(m-1),
  ]
  i.e. by one large grouped base orbit from `023`.

Attempt A:
Idea:
Read `033` as a no-go for bounded-state repair on the current local alphabet, but also as positive evidence that the unresolved channel is already highly structured.

What works:

* The defect graph quotients cleanly.
* The `10m^2` law is exact and not diffuse.
* Three of the four channels repair directly.
* So the problem has been reduced to one explicit obstruction.
* The obstruction is not “need more separator bits,” because the colliders are already separated by all the obvious local contexts.
* The obstruction is not “need slightly more transducer states,” because the current extracted model already forces state lower bounds growing like
  [
  50,\ 196,\ 486,\dots
  ]
* So the next branch should no longer be phrased as “bounded-state synthesis.”

Where it fails:

* This still does not identify the missing reduced coordinate explicitly.
* It only says the current local alphabet does not expose it.

Attempt B:
Idea:
Treat the unary `BBB` corridor as a reduced orbit segment and ask whether the missing state is just corridor phase.

What works:

* The delay-difference
  [
  69-49 = 20,\quad 237-195 = 42,\quad 557-485 = 72
  ]
  is exactly
  [
  m(m-1)
  ]
  for `m=5,7,9`.
* That strongly suggests the two source subfamilies are separated by one full lap of the large `023` grouped base orbit.
* So the unresolved `R1 -> H_L1` channel may already factor through:

  * one entry phase,
  * one exit phase,
  * and a corridor coordinate advancing by `+1` along the unary `BBB` segment.
* If true, then the missing state is not a generic transducer state. It is a **phase on the reduced orbit**.
* That would be exactly the kind of D5 return-map insight we want:
  the repair problem has become an orbit-phase problem on the extracted odometer-style model.

Where it fails:

* This is still a hypothesis until the corridor is explicitly embedded in reduced coordinates.
* We do not yet know whether the relevant phase lives on:

  * the `023` grouped base orbit,
  * the full `(s,u,v)` orbit,
  * or a slightly refined reduced coordinate.

Candidate lemmas:

* [C] The best-seed defect quotients to a bounded defect graph with exact size `10m^2`.
* [C] Three of the four repair channels are direct; only `R1 -> H_L1` remains unresolved.
* [C] On the current extracted local alphabet, 2-state and 3-state repair are impossible.
* [H] The unresolved `R1 -> H_L1` channel is likely an orbit-phase problem rather than a missing separator-bit problem.
* [H] The two delay families likely differ by one full lap of the large `023` grouped base orbit, since their difference is exactly `m(m-1)`.
* [H] The next smallest live branch is corridor-phase extraction, not larger bounded-state synthesis.
* [F] Another 2-state/3-state or slightly larger bounded transducer search on the same local alphabet is the right next move.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* Do **not** widen the local alphabet first.
* The next exact work should be:

  1. **Corridor embedding**
     Take the unresolved `R1 -> H_L1` channel for the best seed and map its states into the known reduced coordinates from `019/023/025`:

     * `(q,s,u,v)`,
     * grouped `(s,u,v)`,
     * and any stationary rewrite already used in `026/027`.

  2. **Phase extraction**
     For the two source subfamilies, compute:

     * entry phase,
     * exit phase,
     * corridor length,
     * and whether the difference between the two delay families is exactly one large grouped-orbit lap for all checked moduli.

  3. **Template law**
     Determine whether the shortest delays fit a closed law in `m`, and whether the defect graph quotient already carries a natural phase coordinate `\chi` advancing by `+1` along the corridor.

  4. **Only then decide branch**

     * If `\chi` is just a reduced orbit phase, then the next local branch is a **phase-exposing mechanism**, not a generic transducer.
     * If not, then the next live branch is a genuinely larger splice mechanism.

Next branching options:

1. Main branch:
   extract the unresolved `R1 -> H_L1` channel as a reduced corridor-phase model.
2. Secondary branch:
   prove or refute that the two source subfamilies differ by exactly one full large-orbit lap.
3. Only after that:
   decide whether the next local mechanism should expose orbit phase or introduce a genuinely new splice alphabet.

Claim status labels:
[P] [C] [H] [F] [O]

Work Template:

```
Work Template:
    Task ID:
    D5-CORRIDOR-PHASE-EXTRACTION-034

    Question:
    For the best seed pair
        left = [2,2,1], right = [1,4,4],
    does the unresolved channel
        R1 -> H_L1
    already factor through a reduced orbit-phase coordinate on the known mixed/023/025 return-map model?

    More concretely:
    can the unary BBB splice corridor from 033 be embedded into the reduced coordinates so that the repair problem becomes
        “enter at phase a, exit at phase b”
    on a known orbit, rather than a generic bounded-state transducer problem?

    Purpose:
    033 shows that tiny transducers are dead on the current local alphabet, but also that the defect graph is very small and explicit.
    The next honest step is to determine whether the missing state is simply orbit phase along the known reduced dynamics.
    If so, the project should pivot again: from bounded-state synthesis to phase-exposing local mechanisms.

    Inputs / Search space:
    - reduced target:
      - 025 omit-base + edge-tied point cocycle defect
    - reduced mixed model:
      - 019
    - reduced grouped base model:
      - 023
    - best-seed defect graph:
      - 033
    - primary seed pair only:
      - left = [2,2,1]
      - right = [1,4,4]
    - primary moduli:
      - m in {5,7,9}
    - control modulus:
      - m = 11 if cheap enough

    Allowed methods:
    - exact extraction of the unresolved R1 -> H_L1 channel states
    - embedding of those states into reduced coordinates:
      - (q,s,u,v)
      - grouped (s,u,v)
      - any stationary coordinate from 026/027
    - exact measurement of:
      - entry phase
      - exit phase
      - corridor length
      - source-subfamily offsets
    - test whether the two delay families differ by exactly one large grouped-orbit lap
    - fit closed formulas in m for the shortest delays
    - identify a candidate corridor phase coordinate chi, if one exists
    - no new broad local search
    - no generic transducer synthesis unless the phase model fails

    Success criteria:
    1. Embed the unresolved corridor into reduced coordinates.
    2. Identify whether a natural phase coordinate chi advances by +1 along the BBB corridor.
    3. Explain the delay families 49/195/485 and 69/237/557 in reduced-orbit terms.
    4. Determine whether the difference between the two source subfamilies is exactly one large grouped-orbit lap.
    5. State clearly whether the next missing ingredient is:
       - orbit-phase exposure, or
       - a genuinely larger splice alphabet.

    Failure criteria:
    - the unresolved corridor does not embed coherently into the existing reduced return-map model, or
    - no stable phase coordinate exists across the pilot moduli, or
    - the delay laws do not align with the known grouped-orbit structure.
    - If failure occurs, state that the next branch really must leave the current reduced model and introduce a new grouped coordinate or splice mechanism.

    Artifacts to save:
    - code
    - raw logs
    - summary report
    - corridor_embedding_tables.json
    - corridor_phase_laws.json
    - source_subfamily_offset_analysis.json
    - reduced_orbit_comparison.json
    - proof-supporting computations

    Return format:
    - exact best-seed corridor embedding
    - exact delay laws
    - orbit-phase interpretation, if any
    - verdict on whether the missing state is orbit phase
    - strongest obstruction if not
    - explicit recommendation for the next branch

    Reproducibility requirements:
    - fixed best seed pair [2,2,1] / [1,4,4]
    - fixed moduli 5,7,9 (and 11 if used)
    - deterministic extraction order
    - saved JSON summaries for embeddings, phase laws, and orbit comparisons
    - exact scripts for the reduced-coordinate extraction
    - explicit separation of:
      - defect-graph facts from 033
      - new corridor-phase facts from 034
```

The brief level I want is:

**one seed, one corridor embedding, one phase-law verdict.**

If the corridor is already just an orbit-phase problem, that is a much better next handle than searching slightly larger transducers.
