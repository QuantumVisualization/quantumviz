# QAOA (Quantum Approximate Optimization Algorithm)

## What It Does

Hybrid quantum-classical algorithm for finding approximate solutions to combinatorial optimization problems (e.g., MaxCut, satisfiability). Alternates between applying problem-specific quantum gates and mixing gates, then uses a classical optimizer to find the best parameters.

## Stage Breakdown

| Stage | Description |
|-------|-------------|
| 1. Initial | Start in uniform superposition |
| 2. Problem Layer (U_C) | Apply cost operator (depends on problem graph) |
| 3. Mixing Layer (U_B) | Apply mixing operator |
| 4. Repeat | Multiple layers (p levels) for better approximation |

## What to Look For

### Cost Landscape

- **X-axis**: Beta parameter (mixing)
- **Y-axis**: Gamma parameter (problem)
- **Z-axis**: Cost function value
- **Goal**: Find global minimum (best cut value)
- **More layers** = more oscillations, finer features

### State City (Density Matrix)

Shows how the quantum state evolves through each layer. As p increases:
- Populations shift toward low-cost basis states
- Coherences (off-diagonal elements) show interference patterns

### Bloch Sphere (Single Qubit)

- Initial: |+⟩ on equator
- After problem layer: State rotates based on cost function
- After mixing layer: Rotates toward computational basis states
- Final measurement collapses to solution

### Circuit Diagram

Shows the alternating layer structure:
- RZ gates for problem layer (parameterized by gamma)
- RX gates for mixing layer (parameterized by beta)
- Repeat p times

## Key Insight

The cost landscape visualization helps identify good parameter regions. The jaggedness shows how sensitive the solution is to parameter choices.