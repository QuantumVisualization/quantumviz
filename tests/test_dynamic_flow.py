"""
Comprehensive tests for the Dynamic Flow visualization module.
"""

import matplotlib
import numpy as np
import numpy.testing as npt

matplotlib.use('Agg')
import json
import os
import tempfile

import matplotlib.pyplot as plt

from quantumviz.dynamic_flow import (
    bloch_vector,
    draw_bloch_sphere,
    parse_complex,
    plot_density_evolution,
    plot_dynamic_flow,
    plot_rabi_oscillation,
    plot_time_evolution,
)


class TestParseComplex:
    """Tests for parse_complex function."""

    def test_parse_complex_int(self):
        """Test parsing integer."""
        assert parse_complex(1) == complex(1, 0)

    def test_parse_complex_float(self):
        """Test parsing float."""
        assert parse_complex(0.5) == complex(0.5, 0)

    def test_parse_complex_string_real(self):
        """Test parsing real string."""
        assert parse_complex("0.5") == complex(0.5, 0)

    def test_parse_complex_string_imag(self):
        """Test parsing imaginary string."""
        assert parse_complex("1j") == complex(0, 1)

    def test_parse_complex_string_complex(self):
        """Test parsing complex string."""
        assert parse_complex("1+2j") == complex(1, 2)


class TestBlochVector:
    """Tests for bloch_vector function."""

    def test_bloch_vector_state_0(self):
        """Test Bloch vector for |0> state."""
        state = [1, 0]
        result = bloch_vector(state)
        npt.assert_array_almost_equal(result, [0, 0, 1])

    def test_bloch_vector_state_1(self):
        """Test Bloch vector for |1> state."""
        state = [0, 1]
        result = bloch_vector(state)
        npt.assert_array_almost_equal(result, [0, 0, -1])

    def test_bloch_vector_superposition(self):
        """Test Bloch vector for |+> state."""
        state = [1/np.sqrt(2), 1/np.sqrt(2)]
        result = bloch_vector(state)
        npt.assert_array_almost_equal(result, [1, 0, 0], decimal=3)

    def test_bloch_vector_minus(self):
        """Test Bloch vector for |-> state."""
        state = [1/np.sqrt(2), -1/np.sqrt(2)]
        result = bloch_vector(state)
        npt.assert_array_almost_equal(result, [-1, 0, 0], decimal=3)

    def test_bloch_vector_plus_i(self):
        """Test Bloch vector for |+i> state."""
        state = [1/np.sqrt(2), 1j/np.sqrt(2)]
        result = bloch_vector(state)
        npt.assert_array_almost_equal(result, [0, 1, 0], decimal=3)

    def test_bloch_vector_normalized(self):
        """Test Bloch vector is normalized."""
        state = [0.6, 0.8]
        result = bloch_vector(state)
        norm = np.linalg.norm(result)
        assert abs(norm - 1) < 1e-10


class TestBlochVectorProperties:
    """Property tests for Bloch vectors."""

    def test_bloch_vector_unit_norm(self):
        """Test all Bloch vectors have unit norm."""
        test_states = [
            [1, 0],
            [0, 1],
            [1/np.sqrt(2), 1/np.sqrt(2)],
            [1/np.sqrt(2), -1/np.sqrt(2)],
            [0.707+0j, 0.707+0j],
        ]
        for state in test_states:
            result = bloch_vector(state)
            norm = np.linalg.norm(result)
            assert abs(norm - 1) < 1e-10


class TestDrawBlochSphere:
    """Tests for draw_bloch_sphere function."""

    def test_draw_basic(self):
        """Test basic drawing."""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        vector = np.array([0, 0, 1])
        draw_bloch_sphere(ax, vector)
        plt.close(fig)

    def test_draw_with_title(self):
        """Test drawing with title."""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        vector = np.array([0, 0, 1])
        draw_bloch_sphere(ax, vector, "Test Title")
        plt.close(fig)

    def test_draw_with_trajectory(self):
        """Test drawing with trajectory."""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        vector = np.array([0, 0, 1])
        trajectory = [
            np.array([0, 0, 1]),
            np.array([0.5, 0, 0.866]),
            np.array([1, 0, 0])
        ]
        draw_bloch_sphere(ax, vector, "Test", trajectory)
        plt.close(fig)


class TestPlotRabiOscillation:
    """Tests for plot_rabi_oscillation function."""

    def test_plot_creates_figure(self):
        """Test plotting creates figure."""
        fig = plot_rabi_oscillation()
        assert fig is not None
        plt.close(fig)

    def test_plot_custom_omega(self):
        """Test plotting with custom omega."""
        fig = plot_rabi_oscillation(omega=2.0)
        assert fig is not None
        plt.close(fig)

    def test_plot_custom_time(self):
        """Test plotting with custom time."""
        fig = plot_rabi_oscillation(t_max=5.0)
        assert fig is not None
        plt.close(fig)

    def test_plot_custom_resolution(self):
        """Test plotting with custom resolution."""
        fig = plot_rabi_oscillation(n_points=50)
        assert fig is not None
        plt.close(fig)

    def test_plot_saves_to_file(self):
        """Test plotting saves to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "rabi.png")
            plot_rabi_oscillation(output_path=output_path)
            assert os.path.exists(output_path)


class TestPlotTimeEvolution:
    """Tests for plot_time_evolution function."""

    def test_plot_creates_figure(self):
        """Test plotting creates figure."""
        states = [
            [1, 0],
            [0.707+0j, 0.707+0j],
            [0, 1]
        ]
        fig = plot_time_evolution(states)
        assert fig is not None
        plt.close(fig)

    def test_plot_custom_title(self):
        """Test plotting with custom title."""
        states = [[1, 0], [0, 1]]
        fig = plot_time_evolution(states, "Custom Title")
        assert fig is not None
        plt.close(fig)

    def test_plot_single_state(self):
        """Test plotting single state."""
        states = [[1, 0]]
        fig = plot_time_evolution(states)
        assert fig is not None
        plt.close(fig)

    def test_plot_many_states(self):
        """Test plotting many states."""
        states = [[np.cos(t/2), 1j*np.sin(t/2)] for t in np.linspace(0, 2*np.pi, 10)]
        fig = plot_time_evolution(states)
        assert fig is not None
        plt.close(fig)

    def test_plot_saves_to_file(self):
        """Test plotting saves to file."""
        states = [[1, 0], [0, 1]]
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "evolution.png")
            plot_time_evolution(states, output_path=output_path)
            assert os.path.exists(output_path)


class TestPlotDensityEvolution:
    """Tests for plot_density_evolution function."""

    def test_plot_creates_figure(self):
        """Test plotting creates figure."""
        data = {
            "qubits": 1,
            "stages": [
                {"name": "t=0", "state_vector": [1, 0]},
                {"name": "t=1", "state_vector": [0, 1]}
            ]
        }
        fig = plot_density_evolution(data)
        assert fig is not None
        plt.close(fig)

    def test_plot_2qubit(self):
        """Test plotting 2-qubit density matrix."""
        data = {
            "qubits": 2,
            "stages": [
                {"name": "t=0", "state_vector": [1, 0, 0, 0]}
            ]
        }
        fig = plot_density_evolution(data)
        assert fig is not None
        plt.close(fig)


class TestPlotDynamicFlow:
    """Tests for plot_dynamic_flow function."""

    def test_plot_from_trajectory_file(self):
        """Test plotting from trajectory JSON file."""
        data = {
            "name": "Test Trajectory",
            "trajectory": [
                [1, 0],
                [0.707, 0.707],
                [0, 1]
            ]
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test.json")
            with open(input_file, 'w') as f:
                json.dump(data, f)

            output_path = os.path.join(tmpdir, "output.png")
            fig = plot_dynamic_flow(input_file, output_path)
            assert os.path.exists(output_path)

    def test_plot_from_stages_file(self):
        """Test plotting from stages JSON file."""
        data = {
            "qubits": 1,
            "stages": [
                {"name": "t=0", "state_vector": [1, 0]},
                {"name": "t=1", "state_vector": [0, 1]}
            ]
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "test.json")
            with open(input_file, 'w') as f:
                json.dump(data, f)

            output_path = os.path.join(tmpdir, "output.png")
            fig = plot_dynamic_flow(input_file, output_path)
            assert os.path.exists(output_path)


class TestEdgeCases:
    """Tests for edge cases."""

    def test_complex_amplitudes(self):
        """Test with complex amplitudes."""
        states = [
            [1+0j, 0+0j],
            [0.707+0.1j, 0.707-0.1j]
        ]
        fig = plot_time_evolution(states)
        assert fig is not None
        plt.close(fig)

    def test_trajectory_with_many_points(self):
        """Test trajectory with many points."""
        states = [[np.cos(t/2), np.sin(t/2)] for t in np.linspace(0, 4*np.pi, 20)]
        fig = plot_time_evolution(states)
        assert fig is not None
        plt.close(fig)
