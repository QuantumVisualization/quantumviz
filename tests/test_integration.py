"""
Integration tests for quantumviz - testing workflows across modules.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

import numpy as np
import numpy.testing as npt
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from click.testing import CliRunner

from quantumviz.bloch_sphere import plot_bloch_sphere
from quantumviz.circuit_diagram import plot_circuit
from quantumviz.cli import main
from quantumviz.cost_landscape import (
    plot_qaoa_landscape,
    plot_vqe_landscape,
    qaoa_cost,
    validate_qaoa_input,
    validate_vqe_input,
    vqe_energy,
)
from quantumviz.dynamic_flow import bloch_vector
from quantumviz.state_city import parse_amplitude, plot_state_city, state_to_density


class TestBlochToDensityConsistency:
    """Test that Bloch sphere and state city give consistent results."""

    def test_state_0_consistency(self):
        from quantumviz.state_city import state_to_density

        state = [1, 0]
        rho = state_to_density(state)
        assert abs(np.trace(rho) - 1.0) < 0.01

    def test_bell_state_consistency(self):
        state = [1/np.sqrt(2), 0, 0, 1/np.sqrt(2)]
        rho = state_to_density(state)

        prob = np.abs(state) ** 2
        assert abs(sum(prob) - 1.0) < 0.01

        expected = np.array([[0.5, 0, 0, 0.5], [0, 0, 0, 0], [0, 0, 0, 0], [0.5, 0, 0, 0.5]], dtype=complex)
        npt.assert_array_almost_equal(rho, expected, decimal=10)


class TestCLIToLibraryConsistency:
    """Test that CLI commands use the same functions as the library."""

    def test_bloch_sphere_cli_creates_file(self):
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test.txt")
            output_file = os.path.join(tmpdir, "output.png")

            with open(input_file, 'w') as f:
                f.write("|0>\n|1>\n")

            result = runner.invoke(main, ['bloch-sphere', input_file, '-o', output_file])
            assert result.exit_code == 0
            assert os.path.exists(output_file)

    def test_state_city_cli_creates_file(self):
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test.json")
            output_dir = tmpdir

            data = {
                "qubits": 1,
                "stages": [
                    {"name": "Zero", "state_vector": [1, 0]}
                ]
            }
            with open(input_file, 'w') as f:
                json.dump(data, f)

            result = runner.invoke(main, ['state-city', input_file, '-o', tmpdir])
            assert result.exit_code == 0

    def test_circuit_cli_creates_file(self):
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test.json")
            output_file = os.path.join(tmpdir, "output.png")

            data = {
                "qubits": 2,
                "gates": [
                    {"type": "H", "qubit": 0},
                    {"type": "CNOT", "control": 0, "target": 1}
                ]
            }
            with open(input_file, 'w') as f:
                json.dump(data, f)

            result = runner.invoke(main, ['circuit', input_file, '-o', output_file])
            assert result.exit_code == 0
            assert os.path.exists(output_file)

    def test_cost_landscape_cli_qaoa(self):
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test.json")
            output_file = os.path.join(tmpdir, "output.png")

            data = {"edges": [[0, 1], [1, 2]]}
            with open(input_file, 'w') as f:
                json.dump(data, f)

            result = runner.invoke(main, ['cost-landscape', 'qaoa', input_file, '-o', output_file])
            assert result.exit_code == 0
            assert os.path.exists(output_file)

    def test_cost_landscape_cli_vqe(self):
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test.json")
            output_file = os.path.join(tmpdir, "output.png")

            data = {"terms": [{"coeff": 0.5, "paulis": ["Z"]}]}
            with open(input_file, 'w') as f:
                json.dump(data, f)

            result = runner.invoke(main, ['cost-landscape', 'vqe', input_file, '-o', output_file])
            assert result.exit_code == 0
            assert os.path.exists(output_file)

    def test_dynamic_flow_cli(self):
        runner = CliRunner()
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test.json")
            output_file = os.path.join(tmpdir, "output.png")

            data = {
                "qubits": 1,
                "stages": [
                    {"name": "t=0", "state_vector": [1, 0]},
                    {"name": "t=1", "state_vector": [0, 1]}
                ]
            }
            with open(input_file, 'w') as f:
                json.dump(data, f)

            result = runner.invoke(main, ['dynamic-flow', input_file, '-o', output_file])
            assert result.exit_code == 0
            assert os.path.exists(output_file)


class TestValidationConsistency:
    """Test that validation is consistent across modules."""

    def test_qaoa_validation_format(self):
        edges = validate_qaoa_input({"edges": [[0, 1], [1, 2]]})
        assert edges == [(0, 1), (1, 2)]

    def test_qaoa_validation_error(self):
        with pytest.raises(ValueError):
            validate_qaoa_input({"terms": []})

    def test_vqe_validation_format(self):
        terms = validate_vqe_input({"terms": [{"coeff": 0.5, "paulis": ["Z", "Z"]}]})
        assert len(terms) == 1
        assert terms[0]["coeff"] == 0.5

    def test_vqe_validation_invalid_pauli(self):
        with pytest.raises(ValueError):
            validate_vqe_input({"terms": [{"coeff": 0.5, "paulis": ["Q"]}]})


class TestCostFunctionCorrectness:
    """Test that cost functions are mathematically correct."""

    def test_qaoa_cost_at_optimal(self):
        edges = [(0, 1)]
        gamma = np.pi / 2
        beta = 0
        cost = qaoa_cost(gamma, beta, edges)
        assert isinstance(cost, (float, np.floating))

    def test_qaoa_cost_empty_graph(self):
        cost = qaoa_cost(0.5, 0.5, [])
        assert cost == 0.0

    def test_vqe_energy_at_optimal(self):
        terms = [{"coeff": 1.0, "paulis": ["Z"]}]
        energy = vqe_energy(np.pi, terms)
        assert isinstance(energy, (float, np.floating, np.ndarray))

    def test_vqe_energy_empty_terms(self):
        energy = vqe_energy(0.5, [])
        assert energy == 0.0


class TestVisualizationOutputFormats:
    """Test that all visualizations produce valid outputs."""

    def test_bloch_sphere_png_format(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "test.png")
            fig = plot_bloch_sphere(["|0>", "|1>"], output)
            assert os.path.exists(output)
            assert os.path.getsize(output) > 0

    def test_state_city_figure_returns(self):
        state = [1, 0, 0, 0]
        fig = plot_state_city(state)
        assert fig is not None
        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_circuit_figure_returns(self):
        data = {
            "qubits": 2,
            "gates": [
                {"type": "H", "qubit": 0},
                {"type": "CNOT", "control": 0, "target": 1}
            ]
        }
        fig = plot_circuit(data)
        assert fig is not None
        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_qaoa_landscape_figure_returns(self):
        fig = plot_qaoa_landscape([(0, 1)])
        assert fig is not None
        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_vqe_landscape_figure_returns(self):
        fig = plot_vqe_landscape([{"coeff": 0.5, "paulis": ["Z"]}])
        assert fig is not None
        import matplotlib.pyplot as plt
        plt.close(fig)


class TestAmplitudeParsingConsistency:
    """Test that amplitude parsing works consistently."""

    def test_parse_amplitude_same_result(self):
        from quantumviz.dynamic_flow import parse_complex

        assert parse_amplitude("1+0j") == parse_complex("1+0j")
        assert parse_amplitude("1j") == parse_complex("1j")
        assert parse_amplitude(0.5) == parse_complex(0.5)

    def test_state_vector_to_bloch_vector(self):
        state = [1/np.sqrt(2), 1/np.sqrt(2)]
        bloch = bloch_vector(state)
        norm = np.linalg.norm(bloch)
        assert abs(norm - 1.0) < 0.01


class TestCLIErrorHandling:
    """Test CLI error handling across commands."""

    def test_bloch_sphere_file_not_found(self):
        runner = CliRunner()
        result = runner.invoke(main, ['bloch-sphere', 'nonexistent.txt'])
        assert result.exit_code != 0

    def test_state_city_invalid_json(self):
        runner = CliRunner()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("not valid json")
            temp_path = f.name

        try:
            result = runner.invoke(main, ['state-city', temp_path])
            assert result.exit_code != 0
        finally:
            os.unlink(temp_path)

    def test_cost_landscape_invalid_algorithm(self):
        runner = CliRunner()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"edges": [[0, 1]]}, f)
            temp_path = f.name

        try:
            result = runner.invoke(main, ['cost-landscape', 'invalid', temp_path])
            assert result.exit_code != 0
        finally:
            os.unlink(temp_path)

    def test_circuit_missing_qubits_key(self):
        runner = CliRunner()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"gates": []}, f)
            temp_path = f.name

        try:
            result = runner.invoke(main, ['circuit', temp_path])
            assert result.exit_code != 0
        finally:
            os.unlink(temp_path)


class TestGroverWorkflow:
    """Test a complete Grover's algorithm workflow."""

    def test_grover_circuit_draws(self):
        data = {
            "qubits": 2,
            "gates": [
                {"type": "H", "qubit": 0},
                {"type": "H", "qubit": 1},
                {"type": "CNOT", "control": 0, "target": 1},
                {"type": "H", "qubit": 0},
                {"type": "H", "qubit": 1}
            ],
            "name": "Grover Search"
        }
        fig = plot_circuit(data)
        assert fig is not None
        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_grover_state_evolution(self):
        states = [
            [1, 0, 0, 0],
            [0.5, 0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5, -0.5],
            [0, 0, 0, 1]
        ]
        for state in states:
            rho = state_to_density(state)
            assert rho.shape == (4, 4)
            assert abs(np.trace(rho) - 1.0) < 0.01


class TestQFTWorkflow:
    """Test a QFT circuit workflow."""

    def test_qft_circuit_draws(self):
        data = {
            "qubits": 2,
            "gates": [
                {"type": "H", "qubit": 0},
                {"type": "P", "qubit": 1, "phi": 1.57},
                {"type": "CNOT", "control": 0, "target": 1}
            ],
            "name": "QFT"
        }
        fig = plot_circuit(data)
        assert fig is not None
        import matplotlib.pyplot as plt
        plt.close(fig)


class TestQOAOWorkflow:
    """Test QAOA workflow with graph."""

    def test_triangle_graph_qaoa(self):
        edges = [(0, 1), (1, 2), (0, 2)]
        fig = plot_qaoa_landscape(edges)
        assert fig is not None
        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_qaoa_cost_symmetry(self):
        edges = [(0, 1)]
        c1 = qaoa_cost(0, 0, edges)
        c2 = qaoa_cost(np.pi, 0, edges)
        npt.assert_almost_equal(c1, c2, decimal=5)


class TestVQEWorkflow:
    """Test VQE workflow with Hamiltonian."""

    def test_h2_hamiltonian_vqe(self):
        terms = [
            {"coeff": -1.0, "paulis": []},
            {"coeff": 0.5, "paulis": ["Z"]},
            {"coeff": 0.2, "paulis": ["Z", "Z"]}
        ]
        fig = plot_vqe_landscape(terms)
        assert fig is not None
        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_vqe_energy_periodicity(self):
        terms = [{"coeff": 1.0, "paulis": ["Z"]}]
        e1 = vqe_energy(0, terms)
        e2 = vqe_energy(2 * np.pi, terms)
        npt.assert_almost_equal(e1, e2, decimal=10)
