# AGENTS.md - quantumviz

## Commands

```bash
# Test
pytest tests/ --cov=quantumviz  # All tests with coverage
pytest tests/test_dcn.py -v    # Single file (verbose default)
pytest -k "pattern"            # Match pattern

# Lint & Typecheck  
ruff check src/                # Ruff config in pyproject.toml
mypy src/                      # Python 3.9 target

# Install
pip install -e ".[dev]"        # Dev deps (pytest, ruff, mypy)
pip install -e ".[dashboard]"   # + FastAPI, uvicorn, pydantic
pip install -e ".[all]"        # + qiskit, qiskit-ibm-runtime
```

## CLI

```bash
quantumviz bloch-sphere input.txt -o out.png
quantumviz bloch-sphere input.txt -o out.pdf -f pdf    # PDF output
quantumviz state-city input.json -o out/ -f pdf          # PDF for multiple files
quantumviz circuit input.json -o out.png
quantumviz cost-landscape qaoa|vqe input.json -o out.png
quantumviz dynamic-flow input.json -o out.png
quantumviz dcn input.json -o out.pdf -f pdf          # PDF output
quantumviz serve                                    # Dashboard at localhost:8000
```

### Output Format Options
- `-f, --format`: Output format (png, pdf, svg) - defaults to `png`
- Output path extension is ignored in favor of the `--format` option

## Conventions

- **Basis ordering**: Big-endian |q₁q₀⟩ (q₁ = MSB)
- **Complex amplitudes**: `j` suffix (`0.707+0.707j`)
- **State vectors**: Must be normalized, length must be power of 2
- **Matplotlib**: Call `matplotlib.use('Agg')` before importing pyplot; call `plt.close()` after saving

## Structure

- `src/quantumviz/` - Visualization modules (one per type)
- `tests/test_*.py` - One test file per module
- `examples/` - Input files organized by algorithm
- `src/quantumviz/dashboard/` - FastAPI web interface

## References

- Input formats: `CONTEXT.md`
- Ruff/mypy config: `pyproject.toml`
