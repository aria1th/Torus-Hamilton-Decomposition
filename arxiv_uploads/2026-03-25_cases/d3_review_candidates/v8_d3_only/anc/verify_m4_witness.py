#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Dict, List, Tuple

Vertex = Tuple[int, int, int]

def load_data(path: Path) -> dict:
    return json.loads(path.read_text())

def bump(v: Vertex, direction: int, m: int) -> Vertex:
    i, j, k = v
    if direction == 0:
        return ((i + 1) % m, j, k)
    if direction == 1:
        return (i, (j + 1) % m, k)
    if direction == 2:
        return (i, j, (k + 1) % m)
    raise ValueError(f"invalid direction {direction}")

def build_color_maps(table: Dict[str, List[List[str]]], m: int):
    color_map = {0: {}, 1: {}, 2: {}}
    for i_str, rows in table.items():
        i = int(i_str)
        if len(rows) != m:
            raise AssertionError(f"i={i}: expected {m} rows, found {len(rows)}")
        for j, row in enumerate(rows):
            if len(row) != m:
                raise AssertionError(f"i={i}, j={j}: expected {m} entries, found {len(row)}")
            for k, word in enumerate(row):
                if sorted(word) != ["0", "1", "2"]:
                    raise AssertionError(f"i={i}, j={j}, k={k}: entry {word!r} is not a permutation of 012")
                for c, ch in enumerate(word):
                    color_map[c][(i, j, k)] = bump((i, j, k), int(ch), m)
    return color_map

def trace_cycle(color_map: Dict[Vertex, Vertex], start: Vertex, m: int) -> List[Vertex]:
    seen = set()
    cur = start
    cycle = [cur]
    while True:
        cur = color_map[cur]
        cycle.append(cur)
        if cur == start:
            break
        if cur in seen:
            raise AssertionError(f"cycle repeats early at vertex {cur}")
        seen.add(cur)
        if len(cycle) > m**3 + 1:
            raise AssertionError("cycle exceeded expected length")
    return cycle

def verify_bijection(color_map: Dict[Vertex, Vertex], m: int, color: int) -> None:
    images = list(color_map.values())
    if len(set(images)) != m**3:
        raise AssertionError(f"color {color}: image set size {len(set(images))} != {m**3}")

def main() -> None:
    here = Path(__file__).resolve().parent
    data = load_data(here / "m4_witness.json")
    m = int(data["m"])
    if m != 4:
        raise AssertionError(f"expected m=4, got {m}")

    table = data["direction_table"]
    stored = {
        int(c): [tuple(v) for v in cyc]
        for c, cyc in data["cycles_from_start_000"].items()
    }

    color_maps = build_color_maps(table, m)
    start = (0, 0, 0)

    for c in range(3):
        verify_bijection(color_maps[c], m, c)
        traced = trace_cycle(color_maps[c], start, m)
        if len(traced) != m**3 + 1:
            raise AssertionError(f"color {c}: traced cycle length {len(traced)} != {m**3 + 1}")
        if len(set(traced[:-1])) != m**3:
            raise AssertionError(f"color {c}: cycle does not visit all {m**3} vertices exactly once")
        if traced != stored[c]:
            raise AssertionError(f"color {c}: stored machine-readable cycle does not match traced cycle")
        print(f"color {c}: Hamilton cycle of length {m**3} verified")

    print("m=4 witness verified successfully")

if __name__ == "__main__":
    main()
