# Quantum Viz Dashboard

FastAPI web interface for quantum state visualization with Qiskit hardware integration.

## Features

- **Interactive Visualizations**: Bloch Sphere, Probability Distribution, Density Matrix
- **Multiple Algorithms**: Grover's Search, QFT, QAOA, VQE
- **Real Hardware Support**: Run on IBM Quantum devices
- **Animation**: Animate algorithm stages
- **Scalable**: Support for 2-4 qubits

## Quick Start

### Via CLI (Recommended)

```bash
quantumviz serve
# Opens at http://localhost:8000
```

### Via Python

```bash
cd quantumviz
pip install -e ".[dashboard]"
python -m quantumviz.dashboard.main
```

### Standalone Frontend

```bash
cd quantumviz/src/quantumviz/dashboard/frontend
python -m http.server 8080
# Open http://localhost:8080
```

## Usage

### Web Interface

1. Select an algorithm (Grover's, QFT, QAOA, VQE)
2. Choose number of qubits (2-4)
3. View Bloch Sphere and probability distribution
4. Click "Animate" to see algorithm stages
5. Optionally run on real quantum hardware

### API Endpoints

```bash
# Visualize a state vector
POST /api/visualize
{
  "qubits": 2,
  "stages": [{"name": "Test", "state": [1, 0, 0, 0]}]
}

# Run on quantum hardware
POST /api/run-hardware
{
  "qubits": 2,
  "backend": "ibmq_qasm_simulator",
  "token": "your_ibm_token",
  "shots": 1024
}

# Health check
GET /api/health

# List available backends
GET /api/backends
```

## Running on Real Quantum Hardware

1. Get an IBM Quantum API token from [quantum-computing.ibm.com](https://quantum-computing.ibm.com)
2. Enter your token in the dashboard
3. Select a backend (e.g., `ibmq_quito`, `ibmq_bogota`)
4. Click "Run on Hardware"

## Requirements

- Python 3.9+
- fastapi, uvicorn, pydantic
- numpy, plotly
- Optional: qiskit, qiskit-ibm-runtime (for hardware)

Install: `pip install quantumviz[dashboard]`

## Project Structure

```
quantumviz/src/quantumviz/dashboard/
├── main.py           # FastAPI backend
├── requirements.txt  # Python dependencies
├── frontend/
│   └── index.html   # Standalone web interface
└── results/         # Hardware execution results
```

## Requirements

- Python 3.9+
- fastapi, uvicorn, pydantic
- numpy, plotly
- Optional: qiskit, qiskit-ibm-runtime (for hardware)

Install: `pip install quantumviz[dashboard]`

## Algorithm Details

### Grover's Search
- Oracle-based algorithm for database search
- Shows amplitude amplification across stages
- Bloch Sphere shows rotation toward target state

### Quantum Fourier Transform (QFT)
- Transform-based algorithm for frequency analysis
- Phase periodicity visible in density matrix
- State City reveals periodic phase patterns

### QAOA (Quantum Approximate Optimization)
- Variational algorithm for combinatorial optimization
- Parameter evolution visible across stages
- Cost landscape shows optimization surface

### VQE (Variational Quantum Eigensolver)
- Finds ground state energies
- Parameter optimization visible
- Energy landscape shows minimization

## License

MIT License