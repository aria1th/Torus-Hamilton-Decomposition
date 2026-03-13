Work Template:
    Task ID:
    D5-FUTURE-TRANSITION-CARRY-CODING-047

    Question:
    On the checked active best-seed branch for the unresolved channel
        R1 -> H_L1,
    can the carry sheet
        c = 1_{q = m-1}
    be realized admissibly by coding the exact future transition datum already extracted in 046,
    preferably in the sharpened form
        current B = (s,u,v,layer,family)
        + tau
        + epsilon,
    where
        tau = initial flat-run length for future grouped delta dn = (0,0,0,1)
    and
        epsilon = current grouped-delta event class
                  in {flat, wrap, carry_jump, other}?

    Purpose:
    045 proved a sharp no-go for current-state / short-transition carry realizations.
    046 proved that c is already an exact future grouped-transition event:
        - minimal exact future dn horizon = m-3
        - minimal exact future grouped-state horizon = m-2
        - exact future signature = current B + flat-run length + first nonflat dn.
    Follow-on analysis further sharpens this:
        - B + tau alone is ambiguous only at tau = 0
        - for tau > 0, B + tau already determines c exactly
        - B + tau + epsilon, with epsilon the 4-valued current dn class,
          is exact on m = 5,7,9,11.
    So the next honest local target is no longer a vague broader gauge.
    It is admissible coding of the first exact future nonflat-event datum.

    Fixed scope:
    - unresolved best-seed branch from 033
    - raw carry/control logic from 037-040
    - admissibility wall from 041
    - finite-cover normal form from 042-044
    - carry no-go catalog from 045
    - exact future-transition extraction from 046
    - checked moduli m in {5,7,9,11}

    Objects already fixed:
    - grouped base:
        B = (s,u,v,layer,family)
    - carry sheet:
        c = 1_{q = m-1}
    - residual binary anticipation sheet:
        d = 1_{next carry u >= m-3}
    - flat grouped delta:
        dn_flat = (0,0,0,1)
    - current dn event classes:
        flat       = (0,0,0,1)
        wrap       = (0,0,0,0)
        carry_jump = (1,1,0,0)
        other      = all remaining current dn values seen on the checked active branch


    Boundary refinement already checked on the frozen 046 dataset:
    - every B + tau collision occurs at tau = 0
    - for tau > 0, B + tau already determines c exactly
    - on the boundary tau = 0, a 3-class current nonflat event label
          {wrap, carry_jump, other}
      resolves the remaining ambiguity exactly on m = 5,7,9,11

    Main hypotheses to test:
    1. The smallest exact carry coding target is not full future window data,
       but the quotient (tau, epsilon).
    2. Admissible realization should first target tau, because epsilon is already
       a current grouped-transition class.
    3. The obstruction after 045 is therefore a future-anticipation / transition-sheet
       coding problem, not a current-gauge problem.

    Allowed methods:
    - exact extraction from the frozen active carry dataset
    - search over admissible families that can see current grouped-transition data
    - lifted or anchored gauges that can encode a bounded future anticipation counter
    - transition-sheet observables that may depend on current-to-next or current-to-next^k grouped evolution
    - quotient searches aimed specifically at tau or at (tau, epsilon)
    - no generic transducer search
    - no reopening of full raw-q realization
    - no attempt to realize the full residual sheet d locally before c is settled

    Concrete passes:

    Pass 0: Freeze the reduced target
    - save the checked exact target for each active state:
        B, c, tau, epsilon
    - verify again that:
        B + tau is exact for tau > 0,
        all B + tau collisions occur at tau = 0,
        B + tau + epsilon is exact.

    Pass 1: Small quotient pruning
    - test whether a still smaller exact quotient exists, for example:
        B + tau + epsilon_binary,
        B + tau + epsilon_3class,
        B + tau_thresholds + epsilon,
        B + coarsened tau + epsilon.
    - only keep quotients that are exact on m = 5,7,9,11.

    Pass 2: Admissible coding search for tau
    - search admissible lifted gauge families whose outputs are exact functions of tau,
      or whose outputs together with epsilon recover c.
    - prioritize transition-sheet / future-event coding mechanisms over more current-state features.

    Pass 3: Minimality and obstruction logging
    - if exact realization fails in the first admissible anticipation families,
      record the precise boundary:
        - which tau values remain collapsed,
        - whether failure is confined to tau = 0,
        - whether epsilon is already admissible and only tau remains hidden.

    Pass 4: Integration test
    - for any surviving exact coding of c,
      integrate with the checked raw controller logic from 039-040 and verify:
        - exact birth,
        - exact family tagging,
        - exact regular/exceptional firing,
        - no false prehits on m = 5,7,9,11.

    Success criteria:
    1. Produce an admissible observable or smallest admissible lifted family that realizes c exactly.
    2. Preferably show it factors through the sharpened exact signature (tau, epsilon), not a larger raw future window.
    3. Save exact collision tables and representative rows on m = 5,7,9,11.
    4. State clearly whether the surviving coding is:
       - a direct coding of tau,
       - a coding of (tau, epsilon), or
       - a larger but still exact future-transition sheet.

    Failure criteria:
    - the first admissible anticipation / transition-sheet families still do not realize c exactly, or
    - exactness requires reopening a much larger future window than (tau, epsilon).
    If failure occurs, state the smallest remaining hidden anticipation datum beyond the tested admissible class.

    Artifacts to save:
    - code
    - raw logs
    - summary report
    - frozen B_c_tau_epsilon dataset
    - exactness/collision tables for all tested quotients
    - surviving admissible family definitions
    - representative ambiguous rows
    - representative exact rows
    - proof-supporting computations

    Return format:
    - exact reduced carry target after quotient pruning
    - exact admissible realization if found
    - strongest exact no-go if not found
    - explicit statement of whether the live hidden datum is tau, epsilon, or a larger future-transition sheet
    - recommendation for the next branch

    Reproducibility requirements:
    - fixed best seed pair [2,2,1] / [1,4,4]
    - fixed moduli 5,7,9,11
    - deterministic extraction order
    - saved JSON summaries for quotient exactness and admissible search results
    - explicit separation of:
        - 045 carry no-go facts,
        - 046 future-transition facts,
        - 047 quotient-pruning and admissibility facts.
