Problem:
Construct a 5-color Hamilton decomposition of
\[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\})
\]
through the mixed-witness return-map branch after the reduced target is known
and the endpoint-seed repair problem has been isolated to one best seed.

Current target:
Decide whether the best `032` seed
- left `[2,2,1]`
- right `[1,4,4]`

has a bounded defect quotient and, if so, whether the next honest branch is
still a tiny `2`-state or `3`-state defect-splice transducer.

Known assumptions:
- `025` remains the correct reduced grouped target.
- `028` identifies endpoint orientation as the right missing local signature.
- `029`, `031`, and `032` kill the smallest static endpoint-word and one-bit
  repair families.
- `032` identifies the best seed and its exact balanced defect count:
  `250, 490, 810 = 10 m^2` on `m=5,7,9`.

Attempt A:
  Idea:
  Quotient the best-seed Latin defect exactly and explain the `10 m^2` law.
  What works:
  `033` shows the defect is highly structured, not diffuse.
  Per color it is exactly `2 m^2`, and this comes from:
  - four overfull families:
    `O_R1, O_R2, O_R3, O_L3`
  - four hole families:
    `H_L1, H_R2, H_R3, H_L3`
  - `2 m` quotient templates per color:
    `(m-1) + 1 + 1 + (m-1)`
  - each quotient template carrying `m` free `v`-translates
  so all colors together give exactly `10 m^2`.
  The direct repair graph is also sharp:
  - `L3 -> H_L3` directly
  - `R2 -> H_R2` directly
  - `R3 -> H_R3` directly
  - only `R1 -> H_L1` remains unresolved
  Where it fails:
  This does not itself synthesize a local realization. It only says the defect
  graph is now small and explicit.

Attempt B:
  Idea:
  Treat the unresolved `R1 -> H_L1` channel as the first real defect-splice
  transducer problem and test whether `2` or `3` states are still plausible.
  What works:
  `033` gives a stronger negative than expected.
  The natural shortest splice is:
  - first alter `R1` by direction `2`
  - then follow a long run of the same local context `BBB`
  - then exit from a later `BBB` state by direction `2` into `H_L1`
  On `m=5,7,9`, the shortest unary corridor lengths are:
  - `49`
  - `195`
  - `485`
  and a second `u=3` source subfamily is longer:
  - `69`
  - `237`
  - `557`
  So under the extracted local template/context alphabet, the smallest possible
  controller already needs at least:
  - `50` states on `m=5`
  - `196` states on `m=7`
  - `486` states on `m=9`
  Therefore the natural `2`-state and `3`-state transducer branch is already
  dead in this model.
  Where it fails:
  This lower bound is for the current extracted local alphabet and unary splice
  framing. It does not rule out a richer mechanism that introduces a genuinely
  new observable local signature or changes the corridor itself.

Candidate lemmas:
- [C] The best-seed defect count is exactly `10 m^2`.
- [C] Per color, the defect quotients to four overfull families and four hole
  families with an `m`-fold `v` translation.
- [C] `L3`, `R2`, and `R3` repair directly; only `R1 -> H_L1` remains.
- [C] The natural shortest `R1 -> H_L1` splice is a unary `BBB` corridor.
- [C] Under the extracted local template/context alphabet, `2`-state and
  `3`-state controllers are impossible on `m=5,7,9`.
- [H] The next live branch must add a new observable local signature or a
  different splice mechanism, not just a slightly larger tiny transducer.
- [O] Full D5 decomposition remains open.

Needed computations/search:
- stop searching `2`-state and `3`-state transducers on the current best-seed
  defect graph
- look for the smallest additional local signature that breaks the unary `BBB`
  corridor
- or look for a different splice mechanism that changes the corridor rather than
  counting through it

Next branching options:
1. Main branch:
   add one new observable local signature that distinguishes positions inside
   the current `BBB` corridor.
2. Secondary branch:
   alter the splice mechanism itself so the unresolved `R1` mass does not enter
   a unary corridor.
3. Only then:
   revisit bounded-state synthesis on the enriched local alphabet.

Claim status labels:
  [P] `019`, `025`
  [C] `028`, `029`, `030`, `031`, `032`, `033`
  [H] tiny defect-splice transducers are pruned on the current local alphabet
  [O] full D5 decomposition
