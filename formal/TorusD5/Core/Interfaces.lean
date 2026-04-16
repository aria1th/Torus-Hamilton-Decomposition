import TorusD5.Core.Objects
import TorusD5.ExactQuotient

namespace TorusD5

/-- Tracking taxonomy mirrored from the local D5 planning docs. -/
inductive FormalizationStatus
  | definitional
  | promotedTheorem
  | workingTheorem
  | checkedCertificate
  | finiteAppendix
  | frontier
  deriving DecidableEq, Repr, Inhabited

/-- Proof-mode taxonomy mirrored from the local D5 planning docs. -/
inductive ProofMode
  | direct
  | statementFirst
  | certificateFirst
  | frontierOnly
  deriving DecidableEq, Repr, Inhabited

/-- Abstract return-surface packaging. The theorem notes still leave the exact
domain/codomain of `R_re` and `R_q` partially fluid, so the first Lean layer
keeps the carrier abstract while fixing a visible readout to `(a,c,d,e)`. -/
structure ReturnSurface (m : ℕ) where
  Carrier : Type
  visible : Carrier → VisibleState m

structure DeterministicReturn (m : ℕ) where
  surface : ReturnSurface m
  next : surface.Carrier → surface.Carrier

/-- Interface shell for the `R_re` return convention. -/
structure RreInterface (m : ℕ) where
  map : DeterministicReturn m

/-- Interface shell for the `R_q` return convention. -/
structure RqInterface (m : ℕ) where
  map : DeterministicReturn m

structure BetaTildeInterface (X : Type) (m : ℕ) where
  toFun : X → ZMod m

structure BetaInterface (Y : Type) (m : ℕ) where
  toFun : Y → ZMod m

structure XiInterface (m : ℕ) where
  toFun : Hm m → VisibleState m

structure FmInterface (m : ℕ) where
  toFun : Hm m → Hm m

structure PmInterface (m : ℕ) where
  toFun : Bm m → Bm m

instance {X : Type} {m : ℕ} : CoeFun (BetaTildeInterface X m) (fun _ => X → ZMod m) where
  coe f := f.toFun

instance {Y : Type} {m : ℕ} : CoeFun (BetaInterface Y m) (fun _ => Y → ZMod m) where
  coe f := f.toFun

instance {m : ℕ} : CoeFun (XiInterface m) (fun _ => Hm m → VisibleState m) where
  coe f := f.toFun

instance {m : ℕ} : CoeFun (FmInterface m) (fun _ => Hm m → Hm m) where
  coe f := f.toFun

instance {m : ℕ} : CoeFun (PmInterface m) (fun _ => Bm m → Bm m) where
  coe f := f.toFun

/-- Local package for an exact lifted clock realization. This is the theorem-side
interface shape suggested by the realization notes, not yet a concrete D5 proof. -/
structure LiftedClockRealization (X Y A : Type) (m : ℕ) where
  liftedStep : X → X
  localStep : Y → Y
  event : X → A
  quotient : X → Y
  betaTilde : BetaTildeInterface X m
  exactQuotient : IsExactDeterministicQuotient liftedStep event quotient

end TorusD5
