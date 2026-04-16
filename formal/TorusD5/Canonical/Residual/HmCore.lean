import TorusD5.Core.Objects
import Mathlib.Tactic.Ring

namespace TorusD5.Canonical.Residual

/-- Effective phase `J₀ = a - 1[e = m - 1]` from the master `H_m` hinge note. -/
def hmPhase (a e : ZMod m) : ZMod m :=
  a - TorusD5.delta m (e = (-1 : ZMod m))

/-- The baseline hinge profile `η₀` from the promoted master hinge theorem. -/
def eta0 (j : ZMod m) : ZMod m :=
  (-6 : ZMod m)
    + TorusD5.delta m (j = 0 ∨ j = 3)
    + (2 : ZMod m) * TorusD5.delta m (j = 4)
    - TorusD5.delta m (j = 2 ∨ j = (-1 : ZMod m))

def firstHingeHeight (a e : ZMod m) : ZMod m :=
  e + eta0 (m := m) (hmPhase (m := m) a e)

def IsDoubleHinge (a e : ZMod m) : Prop :=
  firstHingeHeight (m := m) a e = (-1 : ZMod m)

noncomputable def predictedFirstHinge (a e : ZMod m) : TorusD5.VisibleState m :=
  by
    classical
    exact
      if h : IsDoubleHinge (m := m) a e then
        (hmPhase (m := m) a e - 1, (-2 : ZMod m), (-2 : ZMod m), (-1 : ZMod m))
      else
        (hmPhase (m := m) a e - 2, (-2 : ZMod m), (-2 : ZMod m), firstHingeHeight (m := m) a e)

noncomputable def predictedXi (h : TorusD5.Hm m) : TorusD5.VisibleState m :=
  predictedFirstHinge (m := m) (TorusD5.hmA (m := m) h) (TorusD5.hmE (m := m) h)

structure HasHmMasterHingeProfile (Xi : TorusD5.Hm m → TorusD5.VisibleState m) : Prop where
  exact_eq : ∀ h, Xi h = predictedXi (m := m) h

@[simp] theorem hmPhase_sideTop (a : ZMod m) :
    hmPhase (m := m) a (-1 : ZMod m) = a - 1 := by
  simp [hmPhase, TorusD5.delta]

theorem hmPhase_of_not_sideTop {a e : ZMod m} (he : e ≠ (-1 : ZMod m)) :
    hmPhase (m := m) a e = a := by
  simp [hmPhase, TorusD5.delta, he]

theorem eta0_generic {j : ZMod m}
    (h0 : j ≠ 0) (h3 : j ≠ 3) (h4 : j ≠ 4) (h2 : j ≠ 2) (htop : j ≠ (-1 : ZMod m)) :
    eta0 (m := m) j = (-6 : ZMod m) := by
  simp [eta0, TorusD5.delta, h0, h3, h4, h2, htop]

@[simp] theorem predictedXi_hmPoint (a e : ZMod m) :
    predictedXi (m := m) (TorusD5.hmPoint (m := m) a e) =
      predictedFirstHinge (m := m) a e := rfl

theorem masterProfile_on_hmPoint {Xi : TorusD5.Hm m → TorusD5.VisibleState m}
    (hXi : HasHmMasterHingeProfile (m := m) Xi) (a e : ZMod m) :
    Xi (TorusD5.hmPoint (m := m) a e) = predictedFirstHinge (m := m) a e := by
  simpa using hXi.exact_eq (TorusD5.hmPoint (m := m) a e)

end TorusD5.Canonical.Residual
