Problem:
Refine the `Theta_AB + phase_align` branch far enough to decide whether the next move is still anchor/surgery work on the same quotient, or whether the quotient itself must be enlarged again.

Current target:
Extract the *pilot grammar* carried by the saved Latin-feasible fields on `Theta_AB + phase_align`, and identify which part is rigid and which part still has freedom.

Known assumptions:
- `phase_align_c = 1_{(x_{c+3}-x_{c+1})=0}` splits the aligned branch from the nonzero tail branch.
- The search on `Theta_AB + phase_align` found 10 saved cyclic-equivariant Latin-feasible fields on the pilot range `m=5,7,9`, split into two classes:
  - strict-collapse fields `0..4`
  - clean-but-nonclock fields `5..9`
- On the pilot range, the strict-collapse representative satisfies
  `R_0(q,w,v,u) = (q+1,w,v+1,u)`.
- On the pilot range, the clean-but-nonclock representative breaks the old law but loses strict `q`-clock.

Attempt A:
  Idea:
  Re-read the saved `phase_align` bundle as a *grammar extraction* problem, not as a witness search problem.

  What works:
  - On the union of pilot-realized quotient states (`m=5,7,9`), every saved field inside a given class is identical.
    So the saved phase-align run does not contain many unrelated pilot behaviors; it contains exactly two pilot grammars.
  - The strict-collapse class is pilot-rigid on all `20879` pilot-realized quotient states.
  - The clean-nonclock class is also pilot-rigid on the same `20879` pilot-realized quotient states.
  - The cross-class difference is confined entirely to layers `0` and `1`; layers `2,3,4+` agree across the two classes on all pilot-realized states.

  Where it fails:
  - This is still a computation-backed extraction from the saved feasible fields, not an exhaustive theorem over *all* possible feasible fields on the quotient.
  - The solver artifacts do not by themselves prove that no third pilot grammar exists outside the 10 saved fields.

Attempt B:
  Idea:
  Identify the exact representative-color return law forced by the two pilot grammars.

  What works:
  - Strict-collapse class (`fields 0..4`) has the exact pilot grammar
    - layer `0`: `sigma = (1,2,3,4,0)`
    - layer `1`: `sigma^3 = (3,4,0,1,2)`
    - layers `2,3,4+`: identity
    on all pilot-realized states.
  - Therefore its representative-color first return is exactly
    `R_0(q,w,v,u) = (q+1, w, v+1, u)`
    on `m=5,7,9`.
  - Clean-nonclock class (`fields 5..9`) has the exact pilot grammar
    - layer `0`: `sigma^3 = (3,4,0,1,2)`
    - layer `1`: identity
    - layers `2,3,4+`: identity
    on all pilot-realized states.
  - Therefore its representative-color first return is exactly
    `R_0(q,w,v,u) = (q, w, v+1, u)`
    on `m=5,7,9`.

  Where it fails:
  - The phase-align refinement changes only the *first two kicks*.
    It does not change the tail grammar at all: layers `2,3,4+` remain frozen to identity in both saved classes.
  - So the refinement can either keep the old strict collapse `(q+1,w,v+1,u)` or swap to a clean-but-nonclock pure `v`-kick `(q,w,v+1,u)`, but it still cannot produce a nontrivial section map `U_0`.

Candidate lemmas:
- [C] On the pilot-realized quotient states of `Theta_AB + phase_align`, the saved strict-collapse fields all coincide.
- [C] On the pilot-realized quotient states of `Theta_AB + phase_align`, the saved clean-nonclock fields all coincide.
- [P] Given the strict pilot grammar `layer0=sigma, layer1=sigma^3, layer>=2=id`, the representative-color first return is `R_0(q,w,v,u)=(q+1,w,v+1,u)`.
- [P] Given the clean-nonclock pilot grammar `layer0=sigma^3, layer1=id, layer>=2=id`, the representative-color first return is `R_0(q,w,v,u)=(q,w,v+1,u)`.
- [H] The next useful refinement bit must split a *layer-2 tail state family*, not merely change anchor values on the same quotient.

Needed computations/search:
- Search over one-bit refinements that distinguish residual nonzero-tail classes *inside layer 2*.
- In particular, test predecessor/tail-entry bits rather than new anchor freedom.
- If possible, isolate whether the canonical tail state `L=2|sig=00000` is forced to identity by Latin constraints on the current quotient.

Next branching options:
1. `predecessor-tail bit` branch:
   add one rotation-equivariant bit recording which nonzero tail-entry type fed the current `phase_align=0` tail state.
2. `layer-2 split` branch:
   explicitly refine the canonical residual layer-2 family (for example `L=2|sig=00000` and its nearby orbit types).
3. `no-go theorem` branch:
   prove that on the current quotient every pilot-feasible Latin field has identity on layers `2,3,4+`, so enlargement is mandatory.

Claim status labels:
  [P] Derived exactly from a fixed local grammar
  [C] Verified from the saved search bundle / pilot computations
  [H] Strong structural heuristic / next-branch diagnosis
  [F] Refuted on the saved search bundle
  [O] Open

Bottom line:
- [C] The `phase_align` quotient supports two saved pilot grammars, and both are rigid on pilot-realized states.
- [P] Their representative-color return laws are exactly `(q+1,w,v+1,u)` and `(q,w,v+1,u)`.
- [C/H] Both grammars freeze layers `2,3,4+` to identity on pilot-realized states.
- [H] So the next refinement must target the layer-2 tail grammar itself, not anchor freedom on the current quotient.
