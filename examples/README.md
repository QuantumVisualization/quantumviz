# Examples

This directory contains example inputs and outputs for quantumviz visualization tools.

## Visualization Types

| Tool | Description | Example Folder |
|------|-------------|-----------------|
| bloch-sphere | Single-qubit states on 3D sphere | `algs/bloch_sphere/` |
| state-city | Multi-qubit density matrices as 3D bars | `algs/state_city/` |
| circuit | Quantum circuit diagrams | `algs/circuit_diagram/` |
| cost-landscape | QAOA/VQE optimization surfaces | `algs/cost_landscape/` |
| dynamic-flow | Time evolution animations | `algs/dynamic_flow/` |

## Quick Start

```bash
# Bloch sphere
quantumviz bloch-sphere algs/bloch_sphere/variational-algs/QAOA/qaoa_stages.txt -o output.png

# State city
quantumviz state-city algs/state_city/variational-algs/vqe/vqe_2qubit.json -o output/

# Cost landscape (QAOA)
quantumviz cost-landscape qaoa algs/cost_landscape/inputs/qaoa_maxcut_triangle.json -o landscape.png

# Cost landscape (VQE)
quantumviz cost-landscape vqe algs/cost_landscape/inputs/vqe_h2.json -o energy.png
```

## Algorithm Explanations

Each subfolder (e.g., `algs/state_city/oracle-based-algs/grover-search/`) contains a `README.md` with:

See also:
- Input format details: `FORMAT_QAOA.json`, `FORMAT_VQE.json`
- Full context: `../CONTEXT.md`