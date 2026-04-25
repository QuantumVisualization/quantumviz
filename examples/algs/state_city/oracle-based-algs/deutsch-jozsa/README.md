# Deutsch-Jozsa Algorithm

## What It Does

Determines whether a black-box function is constant (same output for all inputs) or balanced (outputs 0 half the time, 1 half the time), using only one query — a quantum speedup over classical which requires 2^(n-1)+1 queries.

## Stage Breakdown

| Stage | Description |
|-------|-------------|
| 1. Initial | Start in |00...0⟩ |
| 2. After H on all | Equal superposition: (|0⟩+|1⟩)/√2 on each qubit |
| 3. After Oracle | Apply black-box function (phase kickback) |
| 4. Final H | Interference to isolate answer |

## What to Look For

### State City (Density Matrix)

- **Stage 1**: Single bar at (0,0) = |00⟩⟨00|
- **Stage 2**: Uniform distribution across all basis states (all diagonal bars equal height)
- **Constant oracle**: No change from stage 2 (all diagonals still equal)
- **Balanced oracle**: Sign flips on some off-diagonal elements
- **Stage 4 (constant)**: Returns to |00⟩ — single bar at (0,0)
- **Stage 4 (balanced)**: Returns to |11...1⟩ — single bar at (last row/col)

### Bloch Sphere

For n=1 (2-qubit case):
- **Stage 1**: |0⟩ → north pole
- **Stage 2**: |+⟩ → center of equator
- **Stage 4 (constant)**: Back to |0⟩
- **Stage 4 (balanced)**: Flips to |1⟩ or |−⟩

## Key Insight

The visualization shows how quantum interference amplifies the right answer while canceling out the wrong ones — the "magic" behind the exponential speedup.