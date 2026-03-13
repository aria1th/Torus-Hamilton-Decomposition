Work Template:
    Task ID:
    D5-TAU-RESET-CODING-049

    Question:
    On the checked active best-seed branch for
        R1 -> H_L1,
    can the countdown carrier from 048 be realized by an admissible/local
    mechanism through exact coding of its boundary reset law, rather than by
    re-coding the whole future window?

    Purpose:
    046 shows that the carry sheet c is an exact future grouped-transition
    event.
    047 sharpens this to tau plus the boundary event epsilon4.
    048 shows that tau is already an exact countdown carrier:
        - if tau > 0, then next_tau = tau - 1,
        - all nontrivial dynamics lie at tau = 0,
        - wrap -> 0,
        - carry_jump resets exactly on (s,v,layer),
        - other resets exactly on (s,u,layer).
    So the next honest local/search target is no longer “broader future
    windows.” It is the boundary reset micro-law for tau.

    Fixed objects:
    - grouped base:
      B = (s,u,v,layer,family)
    - carry sheet:
      c = 1_{q=m-1}
    - binary anticipation sheet from 044:
      d = 1_{next carry u >= m-3}
    - countdown carrier from 048:
      tau
    - boundary event class from 047:
      epsilon4 in {wrap, carry_jump, other}
    - checked moduli:
      m in {5,7,9,11}

    Inputs / artifact dependencies:
    - 044 finite-cover normal form
    - 045 first carry no-go
    - 046 future carry event
    - 047 boundary sharpening
    - 048 tau countdown carrier

    Allowed methods:
    - exact search over admissible/local observable families intended to be
      realistic mechanism candidates
    - exact coding tests for boundary reset values next_tau at tau=0
    - search for exact reset observables on:
      - carry_jump branch against (s,v,layer)-type targets
      - other branch against (s,u,layer)-type targets
      - global reset law on (epsilon4,s,u,v,layer)
    - integration with an internal countdown carrier state
    - negative tests for bounded-depth reset catalogs if no candidate survives

    Not the target of this branch:
    - do not reopen generic transducer search
    - do not search for full raw q
    - do not search for d
    - do not re-run vague future-window scans as the primary target

    Search plan:

    Pass 0. Freeze the reset dataset
    - restrict to checked active nonterminal states with tau = 0
    - save rows carrying:
      - m
      - family
      - s,u,v,layer
      - epsilon4
      - c
      - next_tau
      - next_epsilon4
    - save separated views for:
      - wrap
      - carry_jump
      - other

    Pass 1. Exact reset-law search
    - search smallest admissible/local observables that realize:
      - carry_jump -> next_tau
      - other -> next_tau
      - global reset law (epsilon4, ... ) -> next_tau
    - record minimal exact families and first collision families
    - keep branch-specific results separate from global results

    Pass 2. Carrier integration test
    - combine each surviving reset law with the internal rule:
        if tau > 0 then next_tau = tau - 1
    - verify exactness of the full next-tau map on the checked active
      nonterminal branch
    - verify that the induced coding of c is exact on the checked active branch

    Pass 3. Negative reduction if Pass 1 fails
    - identify the strongest intended local/admissible family tested
    - show exact factorization / collapse data for that family
    - save explicit collision witnesses proving the family cannot realize the
      reset law
    - where possible, compare against the 047/048 witness families to expose
      the precise missing reset datum

    Success criteria:
    1. Produce an exact admissible/local reset coding for tau = 0,
       either globally or branchwise.
    2. Verify that countdown + reset gives the exact next-tau map.
    3. Verify that the resulting carrier recovers c exactly on m=5,7,9,11.
    4. Save the smallest surviving reset family.

    Strong negative success criteria:
    1. No candidate in the intended mechanism class realizes the reset law.
    2. The exact collapse/factorization shape of that class is recorded.
    3. Collision witnesses are explicit and reusable in proof.

    Failure criteria:
    - the branch does not isolate whether the obstruction is in the reset law
      or in the internal countdown integration.

    Artifacts to save:
    - code
    - raw logs
    - summary report
    - frozen_reset_boundary_dataset_049.json
    - reset_law_exactness_summary_049.json
    - branchwise_reset_minimality_049.json
    - carrier_integration_validation_049.json
    - reset_collision_witnesses_049.json
    - proof_supporting_computations

    Return format:
    - smallest exact reset observable, if one exists
    - exactness status of the integrated countdown carrier
    - induced exactness status for c
    - strongest no-go if no reset coding exists
    - explicit recommendation for the next local or proof branch

    Reproducibility requirements:
    - fixed best seed [2,2,1] / [1,4,4]
    - checked moduli 5,7,9,11
    - deterministic extraction order
    - exact saved JSON summaries
    - explicit separation of:
      - 046 conceptual future-event facts
      - 047 boundary sharpening facts
      - 048 countdown/reset facts
      - new 049 reset-coding facts
