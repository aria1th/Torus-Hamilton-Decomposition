import TorusD4.P0Cycles
import TorusD4.FirstReturn
import TorusD4.Lifts

namespace TorusD4

def pairColorMap (c : Color) : FullCoord m → FullCoord m :=
  fun z => splitPointEquiv (m := m) (colorMap (m := m) c ((splitPointEquiv (m := m)).symm z))

theorem splitPointEquiv_semiconj_pairColorMap (c : Color) :
    Function.Semiconj (splitPointEquiv (m := m)) (colorMap (m := m) c) (pairColorMap (m := m) c) := by
  intro x
  simp [pairColorMap]

theorem splitPointEquiv_symm_semiconj_colorMap (c : Color) :
    Function.Semiconj (splitPointEquiv (m := m)).symm (pairColorMap (m := m) c) (colorMap (m := m) c) := by
  exact (splitPointEquiv_semiconj_pairColorMap (m := m) c).inverse_left
    (splitPointEquiv (m := m)).left_inv (splitPointEquiv (m := m)).right_inv

@[simp] theorem pairColorMap_snd (c : Color) (z : FullCoord m) :
    (pairColorMap (m := m) c z).2 = z.2 + 1 := by
  rcases z with ⟨u, s⟩
  simpa [pairColorMap, coordOfPoint] using S_colorMap (m := m) c (phiLayer (m := m) u s)

@[simp] theorem pairColorMap_iterate_snd (c : Color) (n : ℕ) (z : FullCoord m) :
    (((pairColorMap (m := m) c)^[n]) z).2 = z.2 + n := by
  exact snd_iterate_add_one (m := m) (F := pairColorMap (m := m) c)
    (hstep := pairColorMap_snd (m := m) c) n z

theorem iterate_m_pairColorMap_slicePoint_zero [Fact (2 < m)] (c : Color) (u : P0Coord m) :
    ((pairColorMap (m := m) c)^[m]) (slicePoint (0 : ZMod m) u) =
      slicePoint (0 : ZMod m) (RMap (m := m) c u) := by
  have hsemi := splitPointEquiv_semiconj_pairColorMap (m := m) c
  calc
    ((pairColorMap (m := m) c)^[m]) (slicePoint (0 : ZMod m) u)
        = ((pairColorMap (m := m) c)^[m]) (splitPointEquiv (m := m) (phiLayer (m := m) u 0)) := by
            symm
            simpa [slicePoint] using
              congrArg ((pairColorMap (m := m) c)^[m]) (coordOfPoint_phiLayer (m := m) u (0 : ZMod m))
    _ = splitPointEquiv (m := m) (((colorMap (m := m) c)^[m]) (phiLayer (m := m) u 0)) := by
          symm
          exact (hsemi.iterate_right m).eq (phiLayer (m := m) u 0)
    _ = splitPointEquiv (m := m) (phiLayer (m := m) (RMap (m := m) c u) 0) := by
          rw [firstReturn_eq_RMap (m := m) c u]
    _ = slicePoint (0 : ZMod m) (RMap (m := m) c u) := by
          simpa [slicePoint] using coordOfPoint_phiLayer (m := m) (RMap (m := m) c u) (0 : ZMod m)

theorem iterate_mul_pairColorMap_slicePoint_zero [Fact (2 < m)] (c : Color) :
    ∀ t u, ((pairColorMap (m := m) c)^[m * t]) (slicePoint (0 : ZMod m) u) =
      slicePoint (0 : ZMod m) (((RMap (m := m) c)^[t]) u) := by
  have hm2 : 2 < m := Fact.out
  letI : Fact (0 < m) := ⟨lt_trans (by decide : 0 < 2) hm2⟩
  exact iterate_mul_slicePoint (m := m)
    (F := pairColorMap (m := m) c) (T := RMap (m := m) c) (q0 := (0 : ZMod m))
    (hreturn := iterate_m_pairColorMap_slicePoint_zero (m := m) c)

theorem iterate_add_mul_pairColorMap_slicePoint_zero [Fact (2 < m)] (c : Color)
    (t r : ℕ) (u : P0Coord m) :
    ((pairColorMap (m := m) c)^[m * t + r]) (slicePoint (0 : ZMod m) u) =
      ((pairColorMap (m := m) c)^[r]) (slicePoint (0 : ZMod m) (((RMap (m := m) c)^[t]) u)) := by
  calc
    ((pairColorMap (m := m) c)^[m * t + r]) (slicePoint (0 : ZMod m) u)
        = ((pairColorMap (m := m) c)^[r]) (((pairColorMap (m := m) c)^[m * t]) (slicePoint (0 : ZMod m) u)) := by
            simpa [Nat.add_comm] using
              (Function.iterate_add_apply (pairColorMap (m := m) c) r (m * t) (slicePoint (0 : ZMod m) u))
    _ = ((pairColorMap (m := m) c)^[r]) (slicePoint (0 : ZMod m) (((RMap (m := m) c)^[t]) u)) := by
          rw [iterate_mul_pairColorMap_slicePoint_zero (m := m) c t u]

theorem cycleOn_pairColorMap_of_cycleOn_RMap [Fact (2 < m)] (c : Color)
    {u : P0Coord m} (hc : CycleOn (m ^ 3) (RMap (m := m) c) u) :
    CycleOn (m * (m ^ 3)) (pairColorMap (m := m) c) (slicePoint (0 : ZMod m) u) := by
  have hm2 : 2 < m := Fact.out
  have hm0 : 0 < m := lt_trans (by decide : 0 < 2) hm2
  letI : Fact (0 < m) := ⟨hm0⟩
  letI : Fact (0 < m ^ 3) := ⟨by positivity⟩
  letI : NeZero m := ⟨Nat.ne_of_gt hm0⟩
  letI : Fintype (FullCoord m) := inferInstance
  refine ⟨?_, ?_⟩
  · have hinj :
        Function.Injective fun i : Fin (m * (m ^ 3)) =>
          ((pairColorMap (m := m) c)^[i.1]) (slicePoint (0 : ZMod m) u) := by
        intro i j hij
        let ti : ℕ := i.1 / m
        let tj : ℕ := j.1 / m
        let ri : ℕ := i.1 % m
        let rj : ℕ := j.1 % m
        have hi_decomp : i.1 = m * ti + ri := by
          dsimp [ti, ri]
          exact (Nat.div_add_mod i.1 m).symm
        have hj_decomp : j.1 = m * tj + rj := by
          dsimp [tj, rj]
          exact (Nat.div_add_mod j.1 m).symm
        have hti_lt : ti < m ^ 3 := by
          dsimp [ti]
          have hi_bound : i.1 < (m ^ 3) * m := by
            simpa [Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm] using i.2
          exact (Nat.div_lt_iff_lt_mul hm0).2 hi_bound
        have htj_lt : tj < m ^ 3 := by
          dsimp [tj]
          have hj_bound : j.1 < (m ^ 3) * m := by
            simpa [Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm] using j.2
          exact (Nat.div_lt_iff_lt_mul hm0).2 hj_bound
        have hri_lt : ri < m := by
          dsimp [ri]
          exact Nat.mod_lt _ hm0
        have hrj_lt : rj < m := by
          dsimp [rj]
          exact Nat.mod_lt _ hm0
        change
          ((pairColorMap (m := m) c)^[i.1]) (slicePoint (0 : ZMod m) u) =
            ((pairColorMap (m := m) c)^[j.1]) (slicePoint (0 : ZMod m) u) at hij
        rw [hi_decomp, iterate_add_mul_pairColorMap_slicePoint_zero (m := m) c ti ri u,
          hj_decomp, iterate_add_mul_pairColorMap_slicePoint_zero (m := m) c tj rj u] at hij
        have hcast : ((ri : ℕ) : ZMod m) = ((rj : ℕ) : ZMod m) := by
          simpa [slicePoint] using congrArg Prod.snd hij
        have hrem_mod : ri % m = rj % m := by
          exact (ZMod.natCast_eq_natCast_iff' ri rj m).1 hcast
        have hrem : ri = rj := by
          rwa [Nat.mod_eq_of_lt hri_lt, Nat.mod_eq_of_lt hrj_lt] at hrem_mod
        have hij_shift :
            ((pairColorMap (m := m) c)^[m - ri])
                (((pairColorMap (m := m) c)^[ri]) (slicePoint (0 : ZMod m) (((RMap (m := m) c)^[ti]) u))) =
              ((pairColorMap (m := m) c)^[m - ri])
                (((pairColorMap (m := m) c)^[rj]) (slicePoint (0 : ZMod m) (((RMap (m := m) c)^[tj]) u))) := by
          exact congrArg ((pairColorMap (m := m) c)^[m - ri]) hij
        have hleft :
            ((pairColorMap (m := m) c)^[m - ri])
                (((pairColorMap (m := m) c)^[ri]) (slicePoint (0 : ZMod m) (((RMap (m := m) c)^[ti]) u))) =
              slicePoint (0 : ZMod m) (((RMap (m := m) c)^[ti + 1]) u) := by
          calc
            ((pairColorMap (m := m) c)^[m - ri])
                (((pairColorMap (m := m) c)^[ri]) (slicePoint (0 : ZMod m) (((RMap (m := m) c)^[ti]) u)))
                = ((pairColorMap (m := m) c)^[m - ri + ri])
                    (slicePoint (0 : ZMod m) (((RMap (m := m) c)^[ti]) u)) := by
                      symm
                      simpa using
                        (Function.iterate_add_apply (pairColorMap (m := m) c) (m - ri) ri
                          (slicePoint (0 : ZMod m) (((RMap (m := m) c)^[ti]) u)))
            _ = ((pairColorMap (m := m) c)^[m])
                  (slicePoint (0 : ZMod m) (((RMap (m := m) c)^[ti]) u)) := by
                    rw [Nat.sub_add_cancel (Nat.le_of_lt hri_lt)]
            _ = slicePoint (0 : ZMod m) (RMap (m := m) c (((RMap (m := m) c)^[ti]) u)) := by
                  rw [iterate_m_pairColorMap_slicePoint_zero (m := m) c (((RMap (m := m) c)^[ti]) u)]
            _ = slicePoint (0 : ZMod m) (((RMap (m := m) c)^[ti + 1]) u) := by
                  rw [Function.iterate_succ_apply']
        have hright0 :
            ((pairColorMap (m := m) c)^[m - rj])
                (((pairColorMap (m := m) c)^[rj]) (slicePoint (0 : ZMod m) (((RMap (m := m) c)^[tj]) u))) =
              slicePoint (0 : ZMod m) (((RMap (m := m) c)^[tj + 1]) u) := by
          calc
            ((pairColorMap (m := m) c)^[m - rj])
                (((pairColorMap (m := m) c)^[rj]) (slicePoint (0 : ZMod m) (((RMap (m := m) c)^[tj]) u)))
                = ((pairColorMap (m := m) c)^[m - rj + rj])
                    (slicePoint (0 : ZMod m) (((RMap (m := m) c)^[tj]) u)) := by
                      symm
                      simpa using
                        (Function.iterate_add_apply (pairColorMap (m := m) c) (m - rj) rj
                          (slicePoint (0 : ZMod m) (((RMap (m := m) c)^[tj]) u)))
            _ = ((pairColorMap (m := m) c)^[m])
                  (slicePoint (0 : ZMod m) (((RMap (m := m) c)^[tj]) u)) := by
                    rw [Nat.sub_add_cancel (Nat.le_of_lt hrj_lt)]
            _ = slicePoint (0 : ZMod m) (RMap (m := m) c (((RMap (m := m) c)^[tj]) u)) := by
                  rw [iterate_m_pairColorMap_slicePoint_zero (m := m) c (((RMap (m := m) c)^[tj]) u)]
            _ = slicePoint (0 : ZMod m) (((RMap (m := m) c)^[tj + 1]) u) := by
                  rw [Function.iterate_succ_apply']
        have hright :
            ((pairColorMap (m := m) c)^[m - ri])
                (((pairColorMap (m := m) c)^[rj]) (slicePoint (0 : ZMod m) (((RMap (m := m) c)^[tj]) u))) =
              slicePoint (0 : ZMod m) (((RMap (m := m) c)^[tj + 1]) u) := by
          simpa [hrem] using hright0
        have hslice :
            slicePoint (0 : ZMod m) (((RMap (m := m) c)^[ti + 1]) u) =
              slicePoint (0 : ZMod m) (((RMap (m := m) c)^[tj + 1]) u) := by
          calc
            slicePoint (0 : ZMod m) (((RMap (m := m) c)^[ti + 1]) u)
                = ((pairColorMap (m := m) c)^[m - ri])
                    (((pairColorMap (m := m) c)^[ri]) (slicePoint (0 : ZMod m) (((RMap (m := m) c)^[ti]) u))) := by
                      symm
                      exact hleft
            _ = ((pairColorMap (m := m) c)^[m - ri])
                  (((pairColorMap (m := m) c)^[rj]) (slicePoint (0 : ZMod m) (((RMap (m := m) c)^[tj]) u))) :=
                    hij_shift
            _ = slicePoint (0 : ZMod m) (((RMap (m := m) c)^[tj + 1]) u) := hright
        have hu_eq : ((RMap (m := m) c)^[ti + 1]) u = ((RMap (m := m) c)^[tj + 1]) u := by
          simpa [slicePoint] using congrArg Prod.fst hslice
        have ht_mod : ti + 1 ≡ tj + 1 [MOD m ^ 3] :=
          TorusD4.cycleOn_iterate_modEq (N := m ^ 3) (f := RMap (m := m) c) (x := u) hc hu_eq
        have ht'_mod : ti ≡ tj [MOD m ^ 3] := Nat.ModEq.add_right_cancel' 1 <| by
          simpa [Nat.add_comm] using ht_mod
        have ht : ti = tj := by
          simpa [Nat.ModEq, Nat.mod_eq_of_lt hti_lt, Nat.mod_eq_of_lt htj_lt] using ht'_mod
        apply Fin.eq_of_val_eq
        calc
          i.1 = m * ti + ri := hi_decomp
          _ = m * tj + rj := by rw [ht, hrem]
          _ = j.1 := hj_decomp.symm
    exact (Fintype.bijective_iff_injective_and_card _).2
      ⟨hinj, by simp [FullCoord, P0Coord, pow_succ, pow_two, Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm]⟩
  · calc
      ((pairColorMap (m := m) c)^[m * (m ^ 3)]) (slicePoint (0 : ZMod m) u)
          = slicePoint (0 : ZMod m) (((RMap (m := m) c)^[m ^ 3]) u) := by
              rw [iterate_mul_pairColorMap_slicePoint_zero (m := m) c (m ^ 3) u]
      _ = slicePoint (0 : ZMod m) u := by rw [hc.2]

theorem hasCycle_pairColorMap [Fact (2 < m)] (c : Color) :
    HasCycle (m ^ 4) (pairColorMap (m := m) c) := by
  have hm2 : 2 < m := Fact.out
  have hm : 3 ≤ m := by omega
  letI : Fact (0 < m) := ⟨lt_trans (by decide : 0 < 2) hm2⟩
  rcases hasCycle_RMap_cube (m := m) hm c with ⟨u, hu⟩
  refine ⟨slicePoint (0 : ZMod m) u, ?_⟩
  simpa [pow_succ, pow_two, Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm] using
    cycleOn_pairColorMap_of_cycleOn_RMap (m := m) c hu

theorem hasCycle_colorMap [Fact (2 < m)] (c : Color) :
    HasCycle (m ^ 4) (colorMap (m := m) c) := by
  rcases hasCycle_pairColorMap (m := m) c with ⟨z, hz⟩
  refine ⟨(splitPointEquiv (m := m)).symm z, ?_⟩
  exact cycleOn_conj (splitPointEquiv (m := m)).symm
    (f := pairColorMap (m := m) c) (g := colorMap (m := m) c)
    (splitPointEquiv_symm_semiconj_colorMap (m := m) c) hz

theorem all_colors_haveCycle [Fact (2 < m)] :
    ∀ c : Color, HasCycle (m ^ 4) (colorMap (m := m) c) := by
  intro c
  exact hasCycle_colorMap (m := m) c

end TorusD4
