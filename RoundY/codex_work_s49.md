Task ID:
D5-CORRIDOR-PHASE-CLARIFICATION-036

Question:
How should the saved `034` corridor-phase model be interpreted?

More concretely:
1. do `first_exit_phase` and `phase_residue_mod_period` refer to the same
   corridor state?
2. is `(s, layer)` a true deterministic factor of the full long corridor?
3. if not, what is the smallest exact lifted model visible in the traced data?

Purpose:
An external reader correctly flagged a systematic mismatch in `034`:
the saved first-exit phase and the saved delay residue point to different
target phases. Before opening the next local-mechanism branch, we need to know
whether that is only a convention issue, a logging bug, or evidence that one
more reduced coordinate is missing.

Inputs / Search space:
- best seed from `032`
- defect/corridor context from `033`
- saved `034` source-family rows and delay summaries
- moduli `m = 5,7,9`
- control `m = 11`
- representative regular source `u = 1`
- representative exceptional source `u = 3`

Allowed methods:
- exact full corridor traces up to the first `H_L1`-legal exit
- comparison between first-pass projected phases and later projected repeats
- exact search for a small deterministic lifted coordinate among already visible
  reduced state variables
- no broad new local-rule search

Success criteria:
1. resolve the `034` mismatch cleanly
2. decide whether `(s, layer)` is the full deterministic factor
3. if not, identify the exact lifted traced model and save representative traces
4. package the clarification so external readers can rerun the chain

Failure criteria:
- no clean explanation of the `034` mismatch emerges
- or no stable lifted model appears in the traced long corridor

Artifacts to save:
- `artifacts/d5_corridor_phase_clarification_036/`
- `RoundY/autonomous/d5_autonomous_perturbation_note_v11.md`
- decision log update `D27`
- refreshed external researcher bundle with runnable scripts

Return format:
- verdict on the `034` convention mismatch
- whether `(s, layer)` is a full factor
- explicit lifted rule if found
- representative raw traces and next-branch recommendation

Reproducibility requirements:
- fixed best seed `[2,2,1] / [1,4,4]`
- fixed moduli `5,7,9,11`
- deterministic representative sources `u = 1` and `u = 3`
- saved JSON summaries and raw corridor traces
