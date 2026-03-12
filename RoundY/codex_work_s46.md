Task ID:
D5-DEFECT-SPLICE-TRANSDUCER-033

Question:
For the best endpoint seed pair
- left = [2,2,1]
- right = [1,4,4]

can its balanced Latin defect be quotiented to a bounded template graph and
repaired by the smallest finite-state defect-splice transducer?

Purpose:
`032` already showed the obstruction is not “missing one more separator bit”.
The next honest step is to treat the best seed as a base rule plus a balanced
defect-flow problem and determine whether the first live repair mechanism is
really a tiny dynamic transducer.

Inputs / Search space:
- best seed from `032` only
- moduli `m = 5,7,9`
- best-seed rule with no extra repair and no cocycle defect
- exact defect graph extraction
- exact quotient by the obvious target families
- exact lower-bound analysis for the smallest dynamic splice branch

Allowed methods:
- exact extraction of overfull and hole targets
- quotient by target-family templates and `v`-translation
- exact direct-repair graph extraction by source label and alternate direction
- exact splice-depth / unary-corridor analysis for the unresolved channel
- proof-style pruning of 2-state and 3-state controllers when the lower bound
  already exceeds them

Success criteria:
1. explain the exact `10 m^2` defect law structurally
2. save the bounded template quotient
3. identify the unresolved defect channel
4. decide whether a `2`-state or `3`-state transducer is still plausible

Failure criteria:
- the defect does not quotient cleanly
- or the unresolved channel still looks like a small-state controller problem

Artifacts to save:
- `artifacts/d5_defect_splice_transducer_033/`
- `RoundY/autonomous/d5_autonomous_perturbation_note_v8.md`
- decision log update `D24`

Return format:
- exact defect law explanation
- bounded template families
- unresolved splice channel
- `2`-state verdict
- `3`-state verdict
- next recommended branch

Reproducibility requirements:
- fixed best seed `[2,2,1] / [1,4,4]`
- fixed `m = 5,7,9`
- deterministic target-family quotient
- saved JSON reports for templates, graph, and lower bound
