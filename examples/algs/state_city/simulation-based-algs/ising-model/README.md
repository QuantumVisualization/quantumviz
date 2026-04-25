# Ising Model (Transverse Field)

## What It Does

Models quantum magnetism. A system of spins (qubits) interacting via nearest-neighbor couplings in a transverse field. Used as a testbed for quantum simulation and as the underlying Hamiltonian for QAOA.

## Stage Breakdown

| Stage | Description |
|-------|-------------|
| 1. Initial | All spins aligned in +Z direction (classical state) |
| 2. Transverse field on | Superposition created (spins tip toward X) |
| 3. Evolution | Spins interact, correlations build |
| 4. Measurement | Project onto computational basis |

## What to Look For

### State City (Density Matrix)

- **Initial**: Diagonal |00...0⟩⟨00...0| only
- **After transverse field**: Off-diagonal elements appear (X-coherences)
- **During evolution**:
  - Diagonal populations: Spin-up / spin-down probabilities
  - Off-diagonal: Quantum correlations between spins
- **Final**: Mixture of computational basis states

The density matrix elements tell you:
- **Diagonal (i,i)**: Probability of spin configuration i
- **Off-diagonal (i,j)**: Quantum coherence between states i and j

### Interpretation

The Ising model with transverse field exhibits:
- **Quantum phase transition**: Between ferromagnetic (ordered) and paramagnetic (disordered) phases
- **Entanglement**: Buildup of long-range correlations
- **Critical behavior**: Near phase transition, scaling relationships visible

## Context for QAOA

QAOA typically solves the *classical* Ising model (no transverse field):
- Cost function: H = Σᵢⱼ Jᵢⱼσᵢσⱼ + Σᵢhᵢσᵢ
- Graph nodes = qubits, edges = coupling terms
- The cost landscape visualizer shows optimization over parameters

## Key Insight

This is the simplest model exhibiting quantum phase transitions. The density matrix shows how quantum correlations develop — watch for the buildup of off-diagonal elements as the system evolves.