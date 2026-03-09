# Torus Artifact Bundle

Contents:
- `codex_swap_traces/`: accepted swap sequences for Codex-style alternating-cycle search from canonical direction-coloring start for m=3,5,7,9.
- `hybrid_solutions/`: full solution JSON files for m=4,6,9 from `torus_swap_search.py`-style hybrid solver.
- `bench/`: hybrid solver performance summary (m=3..12, 5 seeds each; restarts=80, steps=8000, temp=0.2).
- `manifest.json`: top-level index.

Notes:
- In swap trace files, `pair=[r,s]` are swapped colors.
- `tau_cycle_vertices` is the exact vertex set used for that accepted swap, in coordinate form `[i,j,k]`.
