import TorusD5.Core.Interfaces

namespace TorusD5

inductive CertificateTier
  | checked
  | exact
  | support
  deriving DecidableEq, Repr, Inhabited

structure CertificateRef where
  sourceDoc : String
  checkerReport : Option String := none
  deriving Repr, Inhabited

structure CheckedCertificate (α : Type) where
  payload : α
  tier : CertificateTier
  provenance : CertificateRef

structure CycleLengthLedger where
  modulus : ℕ
  cycleLengths : List ℕ
  deriving Repr, Inhabited

def promotedCollarNoGoLedgers : List CycleLengthLedger :=
  [ { modulus := 21, cycleLengths := [220, 126, 95] }
  , { modulus := 27, cycleLengths := [343, 342, 44] }
  , { modulus := 33, cycleLengths := [538, 423, 128] }
  , { modulus := 39, cycleLengths := [412, 356, 333, 309, 111] }
  , { modulus := 51, cycleLengths := [661, 547, 444, 227, 165, 165, 165, 165, 62] } ]

def promotedCollarNoGoCertificate : CheckedCertificate (List CycleLengthLedger) where
  payload := promotedCollarNoGoLedgers
  tier := .checked
  provenance :=
    { sourceDoc := "RoundY/theorem/d5_289_promoted_collar_base_section_reduction_and_no_go.md"
      checkerReport := some "RoundY/checks/d5_289_promoted_collar_base_section_summary.json" }

end TorusD5
