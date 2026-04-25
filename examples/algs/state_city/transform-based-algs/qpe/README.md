# QPE (Quantum Phase Estimation)

## What It Does

Estimates the eigenvalue (phase) of a unitary operator's eigenvector. Foundational for quantum algorithms like Shor's factoring and is used in VQE for eigenvalue estimation.

## Stage Breakdown

| Stage | Description |
|-------|-------------|
| 1. Initial | Register qubits in |0⟩, target qubits in eigenvector |
| 2. QFT on register | Quantum Fourier Transform on ancilla qubits |
| 3. Controlled-U ops | Apply controlled powers of unitary |
| 4. Inverse QFT | Extract phase from register |
| 5. Measurement | Read off binary fraction |

## What to Look For

### State City (Density Matrix)

For register + target combined:
- **Initial**: Clean |00⟩⟨00| state
- **After QFT**: Superposition across register basis, coherence with target
- **After controlled-U**: Phases encoded in off-diagonal elements
- **After inverse QFT**: Phase concentrated in computational basis

### Bloch Sphere

Shows individual qubit evolution. For a single-qubit register:
- **Initial**: |0⟩ at north pole
- **After QFT**: Superposition on equator
- **Final**: Points to direction determined by phase (cos/sin)

### Circuit Diagram

Shows:
- Top register (estimation qubits)
- Bottom target qubits (eigenvector)
- Controlled-U with increasing powers (U, U², U⁴, ...)
- QFT/Inverse QFT at appropriate points

## Key Insight

QPE extracts continuous phase information into discrete binary representation. The visualization shows how quantum interference concentrates the phase information.