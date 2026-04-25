# VQE (Variational Quantum Eigensolver)

## What It Does

Hybrid quantum-classical algorithm for finding the ground state energy of a quantum system (e.g., molecular Hamiltonian). Uses a parameterized quantum circuit (ansatz) and classical optimization to minimize the expectation value of the Hamiltonian.

## Stage Breakdown

| Stage | Description |
|-------|-------------|
| 1. Initial | Start in reference state (often |00...0⟩) |
| 2. Ansatz Layers | Apply parameterized gates |
| 3. Measurement | Estimate expectation value |
| 4. Classical Update | Adjust parameters to minimize energy |
| 5. Repeat | Iterate until convergence |

## What to Look For

### Cost Landscape

- **X-axis**: Theta parameter (rotation angle)
- **Y-axis**: Phi parameter  
- **Z-axis**: Energy expectation value
- **Goal**: Find minimum energy (ground state)
- **Physical meaning**: Lower = more stable molecule

### State City (Density Matrix)

- **Initial**: |00⟩⟨00| (pure state at top-left)
- **After ansatz**: Mixture of basis states
- **Near convergence**: Strong population in ground state basis
- **Off-diagonal**: Quantum correlations/entanglement

### Bloch Sphere (Single Qubit)

Shows single-qubit rotations through parameter space. Multiple stages show evolution of one qubit as parameters change.

### Circuit Diagram

- Shows ansatz structure (e.g., real-amplitudes, hardware-efficient)
- Each gate parameterized by theta values
- Measurement at end gives energy estimate

## Input Format

Hamiltonian defined as Pauli terms:

```json
{
  "terms": [
    {"coeff": -1.0, "paulis": []},      // Identity (constant term)
    {"coeff": 0.5, "paulis": ["Z"]},     // Z on qubit 0
    {"coeff": 0.25, "paulis": ["Z", "Z"]} // ZZ on qubits 0,1
  ]
}
```

## Key Insight

The energy landscape shows why VQE is hard — multiple local minima trap the optimizer. The final visualization shows how the quantum state converges toward the ground state.