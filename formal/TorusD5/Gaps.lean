import TorusD5.Core.Interfaces

namespace TorusD5

inductive FrontierGap
  | postHingeDoubleTopExit
  | hmToBmStitching
  | bActiveGate
  | routeYGlobalCycle
  | commonGlobalQuotientPromotion
  | denom8MasterTapeTransport
  deriving DecidableEq, Repr, Inhabited

def currentFrontier : List FrontierGap :=
  [ .postHingeDoubleTopExit
  , .hmToBmStitching
  , .bActiveGate
  , .routeYGlobalCycle
  , .commonGlobalQuotientPromotion
  , .denom8MasterTapeTransport ]

end TorusD5
