"""
Comprehensive tests for the State City visualization module.
"""

import matplotlib
import numpy as np
import numpy.testing as npt
import pytest

matplotlib.use('Agg')
import json
import os
import tempfile

import matplotlib.pyplot as plt

from quantumviz.state_city import (
    parse_amplitude,
    plot_state_cities_from_file,
    plot_state_city,
    state_to_density,
)


class TestParseAmplitude:
    """Tests for parse_amplitude function."""

    def test_parse_amplitude_int(self):
        """Test parsing integer."""
        result = parse_amplitude(1)
        assert result == complex(1, 0)

    def test_parse_amplitude_float(self):
        """Test parsing float."""
        result = parse_amplitude(0.5)
        assert result == complex(0.5, 0)

    def test_parse_amplitude_string_real(self):
        """Test parsing real string."""
        result = parse_amplitude("0.5")
        assert result == complex(0.5, 0)

    def test_parse_amplitude_string_imag(self):
        """Test parsing imaginary string with j."""
        result = parse_amplitude("1j")
        assert result == complex(0, 1)

    def test_parse_amplitude_string_complex(self):
        """Test parsing complex string."""
        result = parse_amplitude("1+2j")
        assert result == complex(1, 2)

    def test_parse_amplitude_string_with_spaces(self):
        """Test parsing string with spaces."""
        result = parse_amplitude("1 + 2j")
        assert result == complex(1, 2)

    def test_parse_amplitude_list(self):
        """Test parsing list [real, imag]."""
        result = parse_amplitude([1, 2])
        assert result == complex(1, 2)

    def test_parse_amplitude_tuple(self):
        """Test parsing tuple (real, imag)."""
        result = parse_amplitude((3, 4))
        assert result == complex(3, 4)

    def test_parse_amplitude_negative(self):
        """Test parsing negative number."""
        result = parse_amplitude(-5)
        assert result == complex(-5, 0)

    def test_parse_amplitude_zero(self):
        """Test parsing zero."""
        result = parse_amplitude(0)
        assert result == complex(0, 0)

    def test_parse_amplitude_invalid_type(self):
        """Test parsing invalid type raises error."""
        with pytest.raises(ValueError, match="Unsupported amplitude format"):
            parse_amplitude({"re": 1, "im": 2})

    def test_parse_amplitude_invalid_list(self):
        """Test parsing invalid list raises error."""
        with pytest.raises(ValueError, match="Unsupported amplitude format"):
            parse_amplitude([1, 2, 3])


class TestStateToDensity:
    """Tests for state_to_density function."""

    def test_state_to_density_single_qubit_0(self):
        """Test density matrix for |0> state."""
        state = [1, 0]
        rho = state_to_density(state)
        expected = np.array([[1, 0], [0, 0]], dtype=complex)
        npt.assert_array_almost_equal(rho, expected)

    def test_state_to_density_single_qubit_1(self):
        """Test density matrix for |1> state."""
        state = [0, 1]
        rho = state_to_density(state)
        expected = np.array([[0, 0], [0, 1]], dtype=complex)
        npt.assert_array_almost_equal(rho, expected)

    def test_state_to_density_2qubit(self):
        """Test density matrix for 2-qubit state."""
        state = [1, 0, 0, 0]
        rho = state_to_density(state)
        assert rho.shape == (4, 4)

    def test_state_to_density_superposition(self):
        """Test density matrix for superposition |+> = (|0>+|1>)/sqrt(2)."""
        state = [1/np.sqrt(2), 1/np.sqrt(2)]
        rho = state_to_density(state)
        expected = np.array([[0.5, 0.5], [0.5, 0.5]], dtype=complex)
        npt.assert_array_almost_equal(rho, expected)

    def test_state_to_density_hermitian(self):
        """Test that density matrix is Hermitian (ρ = ρ†)."""
        state = [0.707+0.1j, 0.5-0.2j]
        rho = state_to_density(state)
        npt.assert_array_almost_equal(rho, rho.conj().T)

    def test_state_to_density_trace_1(self):
        """Test that Tr(ρ) = 1."""
        state = [1/np.sqrt(2), 1/np.sqrt(2)]
        rho = state_to_density(state)
        assert np.trace(rho) == pytest.approx(1)

    def test_state_to_density_positive(self):
        """Test that density matrix has non-negative eigenvalues."""
        state = [1/np.sqrt(2), 1/np.sqrt(2)]
        rho = state_to_density(state)
        eigenvalues = np.linalg.eigvalsh(rho)
        assert all(eigenvalues >= -1e-10)

    def test_state_to_density_empty(self):
        """Test empty state vector raises error."""
        with pytest.raises(ValueError, match="cannot be empty"):
            state_to_density([])


class TestDensityMatrixProperties:
    """Property-based tests for density matrices."""

    def test_density_pure_state(self):
        """Test that pure state has Tr(ρ²) = 1."""
        state = [1, 0, 0, 0]
        rho = state_to_density(state)
        rho_squared = rho @ rho
        trace_rho_squared = np.trace(rho_squared)
        assert trace_rho_squared == pytest.approx(1)

    def test_density_mixed_state(self):
        """Test that mixed state has Tr(ρ²) < 1."""
        rho = np.array([[0.5, 0], [0, 0.5]], dtype=complex)
        rho_squared = rho @ rho
        trace_rho_squared = np.trace(rho_squared)
        assert trace_rho_squared < 1

    def test_density_orthogonal_states(self):
        """Test orthogonal states have orthogonal density matrices."""
        rho0 = state_to_density([1, 0])
        rho1 = state_to_density([0, 1])
        overlap = np.trace(rho0 @ rho1)
        assert abs(overlap) < 1e-10

    def test_density_normalization(self):
        """Test that any normalized state has trace 1."""
        test_states = [
            [1, 0],
            [0, 1],
            [1/np.sqrt(2), 1/np.sqrt(2)],
            [1/np.sqrt(2), -1/np.sqrt(2)],
            [0.707+0j, 0.707+0j],
        ]
        for state in test_states:
            rho = state_to_density(state)
            trace = np.trace(rho).real
            assert abs(trace - 1) < 0.01, f"Trace = {trace}, expected ~1"


class TestPlotStateCity:
    """Tests for plot_state_city function."""

    def test_plot_creates_figure(self):
        """Test that plotting creates a figure."""
        state = [1, 0, 0, 0]
        fig = plot_state_city(state, "Test State")
        assert fig is not None
        plt.close(fig)

    def test_plot_single_qubit(self):
        """Test plotting single qubit state."""
        state = [1, 0]
        fig = plot_state_city(state)
        assert fig is not None
        plt.close(fig)

    def test_plot_2qubit(self):
        """Test plotting 2-qubit state."""
        state = [1, 0, 0, 0]
        fig = plot_state_city(state)
        assert fig is not None
        plt.close(fig)

    def test_plot_3qubit(self):
        """Test plotting 3-qubit state."""
        state = [1, 0, 0, 0, 0, 0, 0, 0]
        fig = plot_state_city(state)
        assert fig is not None
        plt.close(fig)

    def test_plot_superposition(self):
        """Test plotting superposition state."""
        state = [0.5, 0.5, 0.5, 0.5]
        fig = plot_state_city(state, "Superposition")
        assert fig is not None
        plt.close(fig)

    def test_plot_saves_to_file(self):
        """Test plotting saves to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test.png")
            state = [1, 0, 0, 0]
            plot_state_city(state, "Test", output_path)
            assert os.path.exists(output_path)

    def test_plot_saves_to_pdf(self):
        """Test plotting saves to PDF file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test.pdf")
            state = [1, 0, 0, 0]
            plot_state_city(state, "Test", output_path)
            assert os.path.exists(output_path)
            with open(output_path, 'rb') as f:
                assert f.read(4) == b'%PDF'

    def test_plot_custom_dpi(self):
        """Test plotting with custom DPI."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test.png")
            state = [1, 0]
            plot_state_city(state, "Test", output_path, dpi=300)
            assert os.path.exists(output_path)

    def test_plot_custom_title(self):
        """Test plotting with custom title."""
        state = [1, 0]
        fig = plot_state_city(state, "My Custom Title")
        assert fig is not None
        plt.close(fig)


class TestPlotStateCitiesFromFile:
    """Tests for plot_state_cities_from_file function."""

    def test_plot_from_json_file(self):
        """Test plotting from JSON file."""
        data = {
            "qubits": 2,
            "stages": [
                {"name": "Initial", "state_vector": [1, 0, 0, 0]},
                {"name": "Superposition", "state_vector": [0.5, 0.5, 0.5, 0.5]}
            ]
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test.json")
            with open(input_file, 'w') as f:
                json.dump(data, f)

            output_files = plot_state_cities_from_file(input_file, tmpdir)
            assert len(output_files) == 2
            assert all(os.path.exists(f) for f in output_files)

    def test_plot_single_stage(self):
        """Test plotting single stage."""
        data = {
            "qubits": 1,
            "stages": [
                {"name": "Zero", "state_vector": [1, 0]}
            ]
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test.json")
            with open(input_file, 'w') as f:
                json.dump(data, f)

            output_files = plot_state_cities_from_file(input_file)
            assert len(output_files) == 1

    def test_wrong_dimension_raises_error(self):
        """Test that wrong dimension raises error."""
        data = {
            "qubits": 2,
            "stages": [
                {"name": "Invalid", "state_vector": [1, 0]}
            ]
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test.json")
            with open(input_file, 'w') as f:
                json.dump(data, f)

            with pytest.raises(ValueError, match="does not match"):
                plot_state_cities_from_file(input_file)


class TestEdgeCases:
    """Tests for edge cases."""

    def test_parse_complex_amplitudes(self):
        """Test parsing complex amplitudes."""
        state = ["1+0j", "0+1j", "0-1j", "1-0j"]
        result = [parse_amplitude(amp) for amp in state]
        expected = [complex(1, 0), complex(0, 1), complex(0, -1), complex(1, 0)]
        assert result == expected

    def test_density_matrix_complex_phase(self):
        """Test density matrix with complex phase."""
        state = [1/np.sqrt(2), 1j/np.sqrt(2)]
        rho = state_to_density(state)
        assert np.trace(rho).real == pytest.approx(1)

    def test_plot_entangled_state(self):
        """Test plotting entangled Bell state."""
        state = [1/np.sqrt(2), 0, 0, 1/np.sqrt(2)]
        fig = plot_state_city(state, "Bell State")
        assert fig is not None
        plt.close(fig)
