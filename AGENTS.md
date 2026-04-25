# AGENTS.md - quantumviz Developer Guide

## Quick Commands

```bash
# Test
pytest                    # All tests
pytest tests/test_xxx.py  # Single file
pytest -k "pattern"      # Match pattern
pytest --cov=src         # With coverage

# Lint & Typecheck
ruff check src/
ruff check --fix src/
mypy src/

# Install
pip install -e ".[dev]"      # Dev deps
pip install -e ".[dashboard]"  # With dashboard
pip install -e ".[all]"      # Everything
```

## CLI Commands

```bash
quantumviz bloch-sphere input.txt -o output.png
quantumviz state-city input.json -o output/
quantumviz circuit input.json -o circuit.png
quantumviz cost-landscape qaoa graph.json -o landscape.png
quantumviz cost-landscape vqe hamiltonian.json -o energy.png
quantumviz serve                 # Dashboard at localhost:8000
```

## Dashboard

FastAPI web interface for quantum state visualization.

```bash
# Via CLI
quantumviz serve

# Direct execution
python -m quantumviz.dashboard.main

# Standalone frontend
cd src/quantumviz/dashboard/frontend
python -m http.server 8080
```

Dashboard structure:
```
src/quantumviz/dashboard/
├── main.py          # FastAPI backend
├── frontend/
│   └── index.html   # Standalone frontend
├── requirements.txt  # Dashboard dependencies
├── README.md         # Dashboard docs
└── results/         # Hardware execution results
```

## Important Conventions

- **Basis ordering**: Big-endian |q₁q₀⟩ where q₁ is MSB
- **Complex amplitudes**: Use `j` suffix (Python convention)
- **State vectors**: Must be normalized

## Matplotlib Requirements

- Always call `matplotlib.use('Agg')` before importing pyplot
- Always call `plt.close()` after saving figures

## Project Structure

- Input modules in `src/quantumviz/`
- Tests in `tests/test_*.py` (one per module)
- Examples in `examples/`
- Dashboard in `src/quantumviz/dashboard/`

## References

- Input format details: `CONTEXT.md`
- pyproject.toml has exact ruff/mypy config