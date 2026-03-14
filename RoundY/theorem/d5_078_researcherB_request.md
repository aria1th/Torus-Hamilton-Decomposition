# D5 078 Researcher B Request

## Role

You are working on the **globalization criterion**.

This is the theorem question:

`rho = rho(delta)` globally, or not?

## Accepted context

Treat the following as accepted:

- the abstract bridge `(beta,rho)` is the safe global theorem object;
- the concrete bridge `(beta,delta)` is accepted componentwise;
- the `077` Track B reduction:
  repeated fixed-`delta` ambiguity can differ only by **tail length**, not by
  local event-law content.

## Your exact question

For a realized boundary label `delta`, is the padded future current-event word
determined by `delta` alone on the full accessible union?

Equivalent forms:

- does raw global `(beta,delta)` define an exact deterministic quotient?
- can the same realized `delta` occur with different tail lengths?
- is the final global theorem raw `(beta,delta)` or only abstract `(beta,rho)`?

## Strongest useful outcome

Best case:

- prove that fixed realized `delta` has one tail length globally, so raw global
  `(beta,delta)` is valid.

Negative case:

- prove or exhibit that some realized `delta` occurs with different tail
  lengths, forcing the final global theorem to stay abstract as `(beta,rho)`.

Intermediate case:

- reduce the theorem fully to one explicit structural statement from Researcher
  A, so that no further local bridge analysis is needed.

## Things not to spend time on

- re-proving local current-event readout;
- proxy-only ambiguity unless it feeds directly into the true global criterion;
- broad compute that does not target the actual globalization question.

## Suggested starting files

1. `RoundY/theorem/d5_078_accepted_frontier_and_split.md`
2. `RoundY/theorem/d5_077_live_questions_and_tracks.md`
3. `tmp/077_d5_trackB_tail_length_reduction.md`
4. `tmp/d5_076_bridge_main.md`
5. `tmp/d5_076_realization_trackB.md`
6. `tmp/d5_077_trackC_actual_union_check_20260314.md`

## Deliverable

Please return:

- `d5_078_rB.md`

Optional:

- `.tar.gz` if you package formal reductions, counterexample tables, or theorem
  statement variants.
