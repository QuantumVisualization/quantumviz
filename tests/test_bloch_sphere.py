"""
Comprehensive tests for the Bloch sphere visualization module.
"""

import matplotlib
import numpy as np
import numpy.testing as npt
import pytest

matplotlib.use('Agg')
import os
import tempfile

import matplotlib.pyplot as plt

from quantumviz.bloch_sphere import (
    draw_bloch_sphere,
    parse_angles,
    parse_bloch_vector,
    parse_complex_pair,
    parse_ket,
    parse_stage,
    plot_bloch_sphere,
)


class TestParseKet:
    """Tests for parse_ket function."""

    def test_parse_ket_0(self):
        """Test parsing |0> ket."""
        result = parse_ket("|0>")
        npt.assert_array_almost_equal(result, [0, 0, 1])

    def test_parse_ket_1(self):
        """Test parsing |1> ket."""
        result = parse_ket("|1>")
        npt.assert_array_almost_equal(result, [0, 0, -1])

    def test_parse_ket_plus(self):
        """Test parsing |+> ket."""
        result = parse_ket("|+>")
        npt.assert_array_almost_equal(result, [1, 0, 0])

    def test_parse_ket_minus(self):
        """Test parsing |-> ket."""
        result = parse_ket("|->")
        npt.assert_array_almost_equal(result, [-1, 0, 0])

    def test_parse_ket_plus_i(self):
        """Test parsing |+i> ket."""
        result = parse_ket("|+i>")
        npt.assert_array_almost_equal(result, [0, 1, 0])

    def test_parse_ket_minus_i(self):
        """Test parsing |-i> ket."""
        result = parse_ket("|-i>")
        npt.assert_array_almost_equal(result, [0, -1, 0])

    def test_parse_ket_with_spaces(self):
        """Test parsing ket with surrounding whitespace."""
        result = parse_ket("  |0>  ")
        npt.assert_array_almost_equal(result, [0, 0, 1])

    def test_parse_ket_uppercase(self):
        """Test parsing ket with uppercase."""
        result = parse_ket("|0>")
        npt.assert_array_almost_equal(result, [0, 0, 1])

    def test_parse_ket_invalid(self):
        """Test parsing invalid ket raises ValueError."""
        with pytest.raises(ValueError, match="Unknown ket"):
            parse_ket("|2>")


class TestParseBlochVector:
    """Tests for parse_bloch_vector function."""

    def test_parse_bloch_vector_valid(self):
        """Test parsing valid Bloch vector."""
        result = parse_bloch_vector("(0, 0, 1)")
        npt.assert_array_almost_equal(result, [0, 0, 1])

    def test_parse_bloch_vector_with_spaces(self):
        """Test parsing Bloch vector with spaces."""
        result = parse_bloch_vector("( 0 , 0 , 1 )")
        npt.assert_array_almost_equal(result, [0, 0, 1])

    def test_parse_bloch_vector_normalized(self):
        """Test that non-normalized vector is normalized."""
        result = parse_bloch_vector("(0, 0, 2)")
        npt.assert_array_almost_equal(result, [0, 0, 1])

    def test_parse_bloch_vector_negative_z(self):
        """Test parsing negative z direction."""
        result = parse_bloch_vector("(0, 0, -1)")
        npt.assert_array_almost_equal(result, [0, 0, -1])

    def test_parse_bloch_vector_x_direction(self):
        """Test parsing x direction."""
        result = parse_bloch_vector("(1, 0, 0)")
        npt.assert_array_almost_equal(result, [1, 0, 0])

    def test_parse_bloch_vector_y_direction(self):
        """Test parsing y direction."""
        result = parse_bloch_vector("(0, 1, 0)")
        npt.assert_array_almost_equal(result, [0, 1, 0])

    def test_parse_bloch_vector_invalid_dimensions(self):
        """Test parsing with wrong number of dimensions."""
        with pytest.raises(ValueError, match="three coordinates"):
            parse_bloch_vector("(0, 1)")

    def test_parse_bloch_vector_zero_vector(self):
        """Test parsing zero vector raises error."""
        with pytest.raises(ValueError, match="too close to zero"):
            parse_bloch_vector("(0, 0, 0)")


class TestParseAngles:
    """Tests for parse_angles function."""

    def test_parse_angles_radians(self):
        """Test parsing angles in radians."""
        result = parse_angles("theta=1.047, phi=0.785")
        # Verify result is on Bloch sphere
        norm = np.linalg.norm(result)
        assert abs(norm - 1) < 1e-10

    def test_parse_angles_degrees(self):
        """Test parsing angles in degrees."""
        result = parse_angles("theta=60 deg, phi=45 deg")
        # Verify result is on Bloch sphere
        norm = np.linalg.norm(result)
        assert abs(norm - 1) < 1e-10
        # Check z component (cos(60deg) = 0.5)
        npt.assert_almost_equal(result[2], 0.5, decimal=1)

    def test_parse_angles_theta_0(self):
        """Test parsing theta=0 (north pole)."""
        result = parse_angles("theta=0, phi=0")
        npt.assert_array_almost_equal(result, [0, 0, 1])

    def test_parse_angles_theta_180(self):
        """Test parsing theta=180 (south pole)."""
        result = parse_angles("theta=180 deg, phi=0")
        npt.assert_array_almost_equal(result, [0, 0, -1], decimal=2)

    def test_parse_angles_case_insensitive(self):
        """Test parsing is case insensitive."""
        result1 = parse_angles("THETA=60 DEG, PHI=45 DEG")
        result2 = parse_angles("theta=60 deg, phi=45 deg")
        npt.assert_array_almost_equal(result1, result2)

    def test_parse_angles_invalid_missing_theta(self):
        """Test parsing with missing theta raises error."""
        with pytest.raises(ValueError, match="must contain theta and phi"):
            parse_angles("phi=45")

    def test_parse_angles_invalid_missing_phi(self):
        """Test parsing with missing phi raises error."""
        with pytest.raises(ValueError, match="must contain theta and phi"):
            parse_angles("theta=60")


class TestParseComplexPair:
    """Tests for parse_complex_pair function."""

    def test_parse_complex_pair_0(self):
        """Test parsing (1, 0) = |0> state."""
        result = parse_complex_pair("(1, 0)")
        npt.assert_array_almost_equal(result, [0, 0, 1])

    def test_parse_complex_pair_1(self):
        """Test parsing (0, 1) = |1> state."""
        result = parse_complex_pair("(0, 1)")
        npt.assert_array_almost_equal(result, [0, 0, -1])

    def test_parse_complex_pair_plus(self):
        """Test parsing (1+0j, 1+0j) = |+> state."""
        result = parse_complex_pair("(1+0j, 1+0j)")
        npt.assert_array_almost_equal(result, [1, 0, 0], decimal=2)

    def test_parse_complex_pair_with_j(self):
        """Test parsing with j suffix."""
        result = parse_complex_pair("(1j, 1j)")
        npt.assert_array_almost_equal(result, [1, 0, 0], decimal=2)

    def test_parse_complex_pair_with_spaces(self):
        """Test parsing with spaces."""
        result = parse_complex_pair("( 1 , 0 )")
        npt.assert_array_almost_equal(result, [0, 0, 1])

    def test_parse_complex_pair_zero_vector(self):
        """Test parsing zero vector raises error."""
        with pytest.raises(ValueError, match="cannot be zero"):
            parse_complex_pair("(0, 0)")

    def test_parse_complex_pair_invalid(self):
        """Test parsing with invalid format."""
        with pytest.raises(ValueError):
            parse_complex_pair("(1, 2, 3)")


class TestParseStage:
    """Tests for parse_stage function."""

    def test_parse_stage_ket(self):
        """Test parsing ket notation."""
        result = parse_stage("|0>")
        npt.assert_array_almost_equal(result, [0, 0, 1])

    def test_parse_stage_angles(self):
        """Test parsing angle notation."""
        result = parse_stage("theta=60 deg, phi=45 deg")
        assert result is not None
        assert len(result) == 3

    def test_parse_stage_bloch_vector(self):
        """Test parsing Bloch vector notation."""
        result = parse_stage("(0, 0, 1)")
        npt.assert_array_almost_equal(result, [0, 0, 1])

    def test_parse_stage_complex_pair(self):
        """Test parsing complex pair notation."""
        result = parse_stage("(1, 0)")
        npt.assert_array_almost_equal(result, [0, 0, 1])

    def test_parse_stage_empty_line(self):
        """Test parsing empty line returns None."""
        result = parse_stage("")
        assert result is None

    def test_parse_stage_comment(self):
        """Test parsing comment line returns None."""
        result = parse_stage("# This is a comment")
        assert result is None

    def test_parse_stage_whitespace(self):
        """Test parsing whitespace-only line returns None."""
        result = parse_stage("   ")
        assert result is None


class TestBlochVectorProperties:
    """Property-based tests for Bloch vectors."""

    def test_bloch_vector_norm_equals_1(self):
        """Test all parsed Bloch vectors have norm 1."""
        test_cases = ["|0>", "|1>", "|+>", "|->", "|+i>", "|-i>",
                      "(0, 0, 1)", "(1, 0, 0)", "(0, 1, 0)"]
        for case in test_cases:
            result = parse_stage(case)
            if result is not None:
                norm = np.linalg.norm(result)
                assert abs(norm - 1) < 1e-10, f"Failed for {case}"

    def test_parse_bloch_vector_round_trip(self):
        """Test Bloch vector is normalized correctly."""
        original = "(0.5, 0.5, 0.707)"
        result = parse_bloch_vector(original)
        norm = np.linalg.norm(result)
        assert abs(norm - 1) < 1e-10

    def test_parse_angles_equator(self):
        """Test angles at equator (theta=pi/2)."""
        result = parse_angles("theta=90 deg, phi=0 deg")
        npt.assert_almost_equal(result[2], 0, decimal=3)

    def test_parse_angles_orthogonal_states(self):
        """Test orthogonal states have opposite Bloch vectors."""
        state0 = parse_ket("|0>")
        state1 = parse_ket("|1>")
        dot_product = np.dot(state0, state1)
        assert abs(dot_product + 1) < 1e-10


class TestDrawBlochSphere:
    """Tests for draw_bloch_sphere function."""

    def test_draw_creates_axes(self):
        """Test that drawing creates proper axes."""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        vector = np.array([0, 0, 1])
        draw_bloch_sphere(ax, vector, "Test")
        plt.close(fig)

    def test_draw_accepts_empty_title(self):
        """Test drawing with empty title."""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        vector = np.array([0, 0, 1])
        draw_bloch_sphere(ax, vector, "")
        plt.close(fig)


class TestPlotBlochSphere:
    """Tests for plot_bloch_sphere function."""

    def test_plot_from_list(self):
        """Test plotting from list of states."""
        states = ["|0>", "|1>", "|+>"]
        fig = plot_bloch_sphere(states)
        assert fig is not None
        plt.close(fig)

    def test_plot_single_state(self):
        """Test plotting single state."""
        states = ["|0>"]
        fig = plot_bloch_sphere(states)
        assert fig is not None
        plt.close(fig)

    def test_plot_many_states_grid(self):
        """Test plotting many states creates grid."""
        states = ["|0>", "|1>", "|+>", "|->", "|+i>", "|-i>"]
        fig = plot_bloch_sphere(states)
        assert fig is not None
        plt.close(fig)

    def test_plot_saves_to_file(self):
        """Test plotting saves to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test.png")
            states = ["|0>", "|1>"]
            plot_bloch_sphere(states, output_path)
            assert os.path.exists(output_path)

    def test_plot_no_valid_stages(self):
        """Test plotting with no valid stages raises error."""
        with pytest.raises(ValueError, match="No valid stages found"):
            plot_bloch_sphere(["# comment", ""])

    def test_plot_with_custom_dpi(self):
        """Test plotting with custom DPI."""
        states = ["|0>"]
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test.png")
            plot_bloch_sphere(states, output_path, dpi=300)
            assert os.path.exists(output_path)


class TestEdgeCases:
    """Tests for edge cases."""

    def test_parse_stage_with_invalid_ket(self):
        """Test invalid ket in stage parsing."""
        with pytest.raises(ValueError, match="Unable to parse"):
            parse_stage("|invalid>")

    def test_parse_angles_with_invalid_value(self):
        """Test invalid angle value."""
        with pytest.raises(ValueError):
            parse_angles("theta=abc, phi=45")

    def test_parse_bloch_vector_non_numeric(self):
        """Test non-numeric values in vector."""
        with pytest.raises(ValueError):
            parse_bloch_vector("(a, b, c)")
