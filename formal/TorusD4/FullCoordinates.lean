import TorusD4.ReturnMaps

namespace TorusD4

abbrev FullCoord (m : ℕ) := P0Coord m × ZMod m

def phiLayer (u : P0Coord m) (s : ZMod m) : Point m :=
  let (a, b, q0) := u
  ![a, b, q0 - a, s - q0 - b]

def coordOfPoint (x : Point m) : FullCoord m :=
  ((x 0, x 1, q x), S x)

@[simp] theorem phiLayer_apply_0 (u : P0Coord m) (s : ZMod m) :
    phiLayer (m := m) u s 0 = u.1 := by
  rcases u with ⟨a, b, q0⟩
  simp [phiLayer]

@[simp] theorem phiLayer_apply_1 (u : P0Coord m) (s : ZMod m) :
    phiLayer (m := m) u s 1 = u.2.1 := by
  rcases u with ⟨a, b, q0⟩
  simp [phiLayer]

@[simp] theorem phiLayer_apply_2 (u : P0Coord m) (s : ZMod m) :
    phiLayer (m := m) u s 2 = u.2.2 - u.1 := by
  rcases u with ⟨a, b, q0⟩
  simp [phiLayer]

@[simp] theorem phiLayer_apply_3 (u : P0Coord m) (s : ZMod m) :
    phiLayer (m := m) u s 3 = s - u.2.2 - u.2.1 := by
  rcases u with ⟨a, b, q0⟩
  simp [phiLayer]

@[simp] theorem phiLayer_zero (u : P0Coord m) :
    phiLayer (m := m) u 0 = phi u.1 u.2.1 u.2.2 := by
  rcases u with ⟨a, b, q0⟩
  ext i <;> fin_cases i <;> simp [phiLayer, phi]

@[simp] theorem S_phiLayer (u : P0Coord m) (s : ZMod m) :
    S (phiLayer (m := m) u s) = s := by
  rcases u with ⟨a, b, q0⟩
  simp [S, phiLayer]
  ring

@[simp] theorem q_phiLayer (u : P0Coord m) (s : ZMod m) :
    q (phiLayer (m := m) u s) = u.2.2 := by
  rcases u with ⟨a, b, q0⟩
  simp [q, phiLayer]

@[simp] theorem coordOfPoint_phiLayer (u : P0Coord m) (s : ZMod m) :
    coordOfPoint (m := m) (phiLayer (m := m) u s) = (u, s) := by
  rcases u with ⟨a, b, q0⟩
  simp [coordOfPoint]

@[simp] theorem phiLayer_coordOfPoint (x : Point m) :
    phiLayer (m := m) (coordOfPoint (m := m) x).1 (coordOfPoint (m := m) x).2 = x := by
  ext i <;> fin_cases i
  · simp [coordOfPoint, phiLayer]
  · simp [coordOfPoint, phiLayer]
  · simp [coordOfPoint, phiLayer, q]
  · simp [coordOfPoint, phiLayer, q, S]
    ring_nf

def splitPointEquiv : Point m ≃ FullCoord m where
  toFun := coordOfPoint (m := m)
  invFun z := phiLayer (m := m) z.1 z.2
  left_inv := phiLayer_coordOfPoint (m := m)
  right_inv z := by
    rcases z with ⟨u, s⟩
    exact coordOfPoint_phiLayer (m := m) u s

@[simp] theorem splitPointEquiv_apply (x : Point m) :
    splitPointEquiv (m := m) x = (coordOfPoint (m := m) x) := rfl

@[simp] theorem splitPointEquiv_symm_apply (z : FullCoord m) :
    (splitPointEquiv (m := m)).symm z = phiLayer (m := m) z.1 z.2 := rfl

@[simp] theorem S_bump (x : Point m) (d : Coord) :
    S (bump x d) = S x + 1 := by
  fin_cases d <;> simp [S, bump]
  all_goals ring_nf

@[simp] theorem S_colorMap (c : Color) (x : Point m) :
    S (colorMap (m := m) c x) = S x + 1 := by
  simp [colorMap]

end TorusD4
