# CONTEXT.md - What quantumviz Visualizes

## What This Project Is

quantumviz is a Python library for visualizing quantum algorithm states. It renders quantum states as images (PNG) for education, analysis, and publication.

## Visualization Types

### 1. Bloch Sphere
- **Purpose**: Single-qubit states
- **Representation**: 3D sphere with state vector as arrow
- **Shows**: θ (theta), φ (phi) angles, |0⟩/|1⟩ basis
- **Input**: TXT file with ket notation, angles, or Cartesian coordinates
- **Example input**:
  ```
  |0>
  theta=60 deg, phi=45
  (x,y,z)
  ```
- **Limitation**: Single qubit only (no direct entanglement)

### 2. State City
- **Purpose**: Multi-qubit density matrices
- **Representation**: 3D bar chart of ρ elements
- **Shows**: Real part (left), Imaginary part (right)
- **Input**: JSON with qubits + stages + state_vectors
- **Example**:
  ```json
  {
    "qubits": 2,
    "stages": [{"name": "Initial", "state_vector": [1, 0, 0, 0]}]
  }
  ```
- **Limitation**: Scales as 2^n (practical ≤5 qubits)

### 3. Cost Landscape
- **Purpose**: Optimization landscapes (QAOA, VQE)
- **Representation**: 3D surface plot
- **Shows**: Cost/energy as function of parameters
- **Input**: QAOA (graph edges), VQE (Pauli terms)
- **Example QAOA**:
  ```json
  {"edges": [[0, 1], [1, 2], [0, 2]]}
  ```
- **Example VQE**:
  ```json
  {"terms": [{"coeff": -1.0, "paulis": []}, {"coeff": 0.5, "paulis": ["Z"]}]}
  ```

### 4. Circuit Diagram
- **Purpose**: Quantum circuit gates
- **Representation**: Circuit diagram (like Qiskit circuit drawer)
- **Shows**: Gates, wires, measurements
- **Input**: JSON with qubits + stages (gates)
- **Extension**: Can overlay state evolution

### 5. Dynamic Flow
- **Purpose**: Time evolution / Rabi oscillations
- **Representation**: Animated or multi-panel visualization
- **Shows**: State changes over time
- **Input**: JSON with stages as time steps

## Quantum Conventions

- **Basis ordering**: Big-endian |q₁q₀⟩ where q₁ is MSB
- **Complex amplitudes**: Use `j` suffix (Python convention)
- **State vectors**: Must be normalized
- **Density matrix**: ρ = |ψ⟩⟨ψ|

## Input Formats Summary

| Visualization | Format | Extension |
|--------------|-------|----------|
| Bloch Sphere | Text (various) | .txt |
| State City | JSON | .json |
| Cost Landscape | JSON (graph/Pauli) | .json |
| Circuit Diagram | JSON | .json |
| Dynamic Flow | JSON | .json |

## Dashboard

FastAPI web interface at http://localhost:8000.

```bash
cd quantumviz
pip install -e ".[dashboard]"
quantumviz serve
# or: python -m quantumviz.cli serve
```

## Related Papers

- **paper-scipost-physics-codebases**: This package as a case study in physics codebase papers
- **visualization-survey-paper**: Survey of quantum visualization techniques (context for this library)

## Key Files

| File | Purpose |
|------|---------|
| `src/quantumviz/bloch_sphere.py` | Bloch sphere implementation |
| `src/quantumviz/state_city.py` | Density matrix visualization |
| `src/quantumviz/cost_landscape.py` | QAOA/VQE landscapes |
| `src/quantumviz/circuit_diagram.py` | Circuit rendering |
| `src/quantumviz/dynamic_flow.py` | Time evolution |
| `src/quantumviz/cli.py` | CLI interface |
| `examples/` | Example input files |