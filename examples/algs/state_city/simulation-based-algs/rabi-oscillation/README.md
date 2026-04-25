# Rabi Oscillation

## What It Does

Describes the dynamics of a two-level quantum system (qubit) under resonant drive. The qubit oscillates between |0⟩ and |1⟩ states at a frequency proportional to the drive amplitude. Fundamental to quantum gate operation.

## Stage Breakdown

| Stage | Time | State | Bloch Vector |
|-------|------|-------|------------|
| 1 | t=0 | |0⟩ | (0, 0, 1) — north pole |
| 2 | t=π/4 | |+⟩ | (1, 0, 0) — +X axis |
| 3 | t=π/2 | |1⟩ | (0, 0, -1) — south pole |
| 4 | t=3π/4 | |−⟩ | (-1, 0, 0) — -X axis |
| 5 | t=π | -|0⟩ | (0, 0, 1) — back to north pole |

## What to Look For

### Bloch Sphere

The classic visualization:
- **State traces a circle** on the X-Z plane (the Bloch sphere equator)
- **Rotation rate** proportional to drive strength
- **Periodic return** to starting point at multiples of 2π

### State City (Density Matrix)

- **Diagonal elements**: P(|0⟩) and P(|1⟩) oscillate out of phase
- **Off-diagonal (coherences)**: Show coherence between basis states
- At t=π/2: Full population inversion (diagonal = [0, 1])

### Dynamic Flow

- Shows trajectory **through time**
- Each frame/panel = different time point
- Animates the oscillation
- Reveals periodicity (returns to start)

### Key Pattern

The oscillations are sinusoidal: P₀(t) = cos²(Ωt/2), P₁(t) = sin²(Ωt/2) where Ω is the Rabi frequency.

## Key Insight

Rabi oscillations are how we perform quantum gates. The visualization shows the continuous rotation underlying discrete gate operations — a π/2 rotation gives a Hadamard-like state, a π rotation gives X.