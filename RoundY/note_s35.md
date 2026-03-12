Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field.

Current target:
Pivot explicitly from “find another surviving local family” to:

**find the D5 return-map model.**

The search chain through `016` should now be treated as quotient discovery: it identified which local bits are real, which are fake or sterile, and which mechanisms are live. The next main task is to extract the reduced state space, section, grouped return, and candidate conjugacy for the mixed witness.

Known assumptions:

* The exact mixed mechanism exists:

  * `008` gives a clean strict mixed witness on `m=5,7,9`.
* The exact search chain `009–015` shows many obvious one-bit refinements are fake, sterile, or collapse back to the old baseline.
* `016` is the sharpest local negative so far:

  * Stage 1: `648` exact rules, `72` full-color Latin survivors, `0` clean survivors.
  * Stage 2: `1944` exact rules, `216` full-color Latin survivors, `0` clean survivors.
  * So the smallest synchronized use of the exact bit
    [
    p=\texttt{pred_sig1_phase_align}
    ]
    dies before clean-frame.
* Therefore the current local neighborhood around the live `wu2` mixed gadget is now highly pruned.
* The right reading of the recent work is:

  * `008`: a genuine mixed cycle+monodromy mechanism exists.
  * `009–015`: many natural extra bits are fake or dynamically sterile.
  * `016`: the remaining smallest synchronized one-bit exact route is also dead.
* This means the recent work was not wasted drift. It was quotient discovery.
* But from here, continuing broad local-family widening without extracting a reduced return map would be the wrong process.

Attempt A:
Idea:
Reframe `005–016` as evidence about the unknown reduced D5 return state, rather than as a sequence of partial construction attempts.

What works:

* This matches the actual trajectory:
  the project has been searching for the correct state variables of the D5 odometer / skew-odometer.
* It also matches the successful `d=3` and `d=4` pattern: the decisive advance comes when the return map is reduced to the right canonical coordinates, not when more local cases are enumerated.
* The exact chain now says something structurally useful:
  the current live mixed mechanism is robust, but its geometry is stuck at the same baseline; many extra local bits survive combinatorially but do not enter the effective return dynamics.

Where it fails:

* We still do not know the correct reduced state space.
* We do not yet know whether the right object is:

  * a first return,
  * a grouped / second return,
  * or a skew-product over a smaller carry system.

Attempt B:
Idea:
Use the exact witnesses already found as data for return-map extraction: identify the smallest state that controls geometry and twist in the mixed witness, then try to write the D5 analogue of the d4 story.

What works:

* The mixed witness from `008` gives a canonical starting point.
* The cycle-only, monodromy-only, and anti-compressive control families from `005–013` give comparison data that can separate:

  * base geometry,
  * twist cocycle,
  * and bad carry behavior.
* This suggests a model of the form
  [
  R(\xi,t)=(B(\xi),,t+\phi(\xi)),
  ]
  where:

  * `\xi` is the still-unknown reduced D5 state,
  * `B` is the base return / carry system,
  * `\phi` is the twist cocycle.
* The next computations should be organized around discovering `\xi`, not around maximizing survivor counts.

Where it fails:

* We do not yet know the right section or grouped return.
* It may take one or two rounds of model extraction to decide whether the correct D5 normal form is:

  * an odometer,
  * a skew-odometer,
  * or a finite-state carry automaton with twist.

Candidate lemmas:

* [P] The mixed cycle+monodromy mechanism is real (`008`).
* [C] The exact search chain `009–016` has already identified a large class of fake or sterile one-bit refinements in the current local neighborhood.
* [C] In particular, the exact bit `pred_sig1_phase_align` is locally real but dynamically sterile in every one-bit role tested there, and in the smallest synchronized two-layer role it destroys clean-frame.
* [H] The recent search should be interpreted as quotient discovery for the D5 return-map model, not as wasted local drift.
* [H] The next main branch should be return-map extraction:
  section, first return, grouped return, reduced state, conjugacy.
* [H] Any further search should be used only to test candidate reduced-state variables or grouped-return definitions.
* [F] The right next main branch is another broader local-family search in the current exact-bit neighborhood.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* Fix a small witness set:

  1. the canonical mixed witness from `008`,
  2. a strongest validated cycle-only witness,
  3. a representative monodromy-only witness,
  4. a representative anti-compressive mixed witness from `010–013`.
* On the common clean section already used to define `U_0`, extract for each witness:

  * first return word,
  * induced return increment,
  * monodromy increment,
  * carry / branch events,
  * low-layer return trace.
* Compare these traces across pilot moduli `m=5,7,9` and spot-check `11,13`.
* Perform partition refinement on section states by identical return behavior.
* If first return is still too large or unstable, try grouped return / second return:

  * return to a smaller subset,
  * one full `U_0` cycle,
  * carry-event return,
  * or another natural grouped return suggested by the traces.
* Search for the smallest reduced state `\xi` on which both geometry and twist factor.
* Then test whether the reduced return can be conjugated to:

  * a finite-state odometer,
  * a skew-odometer,
  * or a carry automaton with cocycle.
* Use any further local search only as a diagnostic for missing state variables.

Next branching options:

1. Main branch:
   extract the D5 reduced return-map model from the current exact witness set.
2. Secondary branch:
   if first return is too noisy, move to grouped / second return rather than widening local families.
3. Only after a candidate reduced model is found:
   use tiny targeted searches to verify which local observables realize its state variables.

Claim status labels:
[P] [C] [H] [F] [O]

Work Template:
Task ID:
D5-RETURN-MAP-MODEL-017

```
Question:
What is the correct reduced return-map model behind the current D5 mixed witness family?

More concretely:
can one identify a section `\Sigma`, a first return or grouped return `R`, and a reduced state variable `\xi` such that the mixed witness factors through a simple canonical system — ideally an odometer, skew-odometer, or finite-state carry system with twist?

Purpose:
The project has now completed a substantial quotient-discovery phase. The exact search chain through `016` shows that continuing broad local-family widening is no longer the right primary process. The next main goal is to extract the D5 return-map normal form.

Inputs / Search space:
- Fixed witness set:
  1. canonical mixed witness from `008`
  2. strongest validated cycle-only witness (best compression baseline)
  3. representative monodromy-only witness
  4. representative anti-compressive mixed witness from `010–013`
- Common clean section:
  - the section currently used to define `U_0` / color-0 return in validation
- Pilot moduli:
  - `m in {5,7,9}`
- Stability moduli:
  - `m in {11,13}` for the best candidate reduced models
- Return observables to log on the section:
  - first return word
  - induced return increment
  - monodromy increment
  - carry / branch events
  - low-layer return trace
  - cycle signature
- Candidate grouped-return choices:
  - raw first return
  - return to a smaller distinguished subset
  - one full `U_0` cycle
  - carry-event return
  - second return / grouped return suggested by trace patterns

Allowed methods:
- exact witness replay on the section
- exact logging of return traces and increments
- partition refinement / automaton minimization on section states
- comparison across witnesses and across moduli
- grouped-return experiments
- search for reduced coordinates that make the return deterministic
- fitting / recognition of canonical models:
  - odometer
  - skew-odometer
  - finite-state carry automaton with cocycle
- very small diagnostic searches only if needed to test a candidate reduced-state variable
- no broad new local-family sweep unless forced by the extracted model

Success criteria:
1. Define an explicit section `\Sigma`.
2. Produce an explicit first return or grouped return on `\Sigma`.
3. Identify a reduced state variable `\xi` or finite reduced state space `\Xi`.
4. Show that the mixed witness return factors through `\Xi` on `m=5,7,9`.
5. Express the reduced return in a canonical form such as:
   \[
   R(\xi,t)=(B(\xi),\, t+\phi(\xi))
   \]
   or another explicit carry / odometer normal form.
6. Compare the reduced model against the cycle-only, monodromy-only, and anti-compressive control witnesses.
7. If no satisfactory reduced model exists at first return, identify the smallest grouped-return modification that fixes this.

Failure criteria:
- no stable reduced quotient appears across the pilot moduli,
- or first return is too noisy and no grouped return yields a coherent reduced state,
- or the extracted quotient remains too large / irregular to support a canonical model.
- If failure occurs, the report must state the sharpest obstruction and the next missing coordinate or grouped-return candidate.

Artifacts to save:
- code
- raw logs
- summary report
- extracted section-state tables
- return-trace tables
- partition-refinement outputs
- minimized automata / transition tables
- candidate conjugacy formulas
- counterexamples / obstruction tables
- proof-supporting computations

Return format:
- exact witnesses used
- section definition
- first-return data summary
- grouped-return data summary, if used
- reduced-state candidates `\Xi`
- comparison of reduced models across witnesses
- best canonical model found
- strongest obstruction if no canonical model is found
- exact recommendation for the next missing coordinate / grouped-return refinement

Reproducibility requirements:
- fixed witness definitions
- fixed pilot moduli `5,7,9`
- deterministic enumeration order
- saved JSON/CSV for:
  - section states
  - return traces
  - reduced partitions
  - transition tables
- exact validation scripts for every reported reduced model
- explicit comparison against the current mixed baseline and strongest cycle-only baseline
```

The practical conclusion is:

**The search phase has done its job: it found the live mixed mechanism and eliminated many fake state variables.
From here, the main task is no longer “find another surviving family.”
It is “extract the D5 return-map model.”**
