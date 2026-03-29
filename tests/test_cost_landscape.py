"""
Comprehensive tests for the Cost Landscape visualization module.
"""

import pytest
import numpy as np
import numpy.testing as npt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tempfile
import os

from quantumviz.cost_landscape import (
    qaoa_cost,
    vqe_energy,
    plot_qaoa_landscape,
    plot_vqe_landscape,
)


class TestQAOACost:
    """Tests for qaoa_cost function."""

    def test_qaoa_cost_scalar(self):
        """Test QAOA cost with scalar inputs."""
        result = qaoa_cost(0.5, 0.5)
        assert isinstance(result, (float, np.floating))

    def test_qaoa_cost_array(self):
        """Test QAOA cost with array inputs."""
        gamma = np.array([0, np.pi/4, np.pi/2])
        beta = np.array([0, np.pi/4, np.pi/2])
        result = qaoa_cost(gamma, beta)
        assert len(result) == 3

    def test_qaoa_cost_meshgrid(self):
        """Test QAOA cost with meshgrid."""
        gamma = np.linspace(0, np.pi, 10)
        beta = np.linspace(0, np.pi, 10)
        G, B = np.meshgrid(gamma, beta)
        Z = qaoa_cost(G, B)
        assert Z.shape == (10, 10)

    def test_qaoa_cost_range(self):
        """Test QAOA cost is in valid range."""
        gamma = np.linspace(0, np.pi, 50)
        beta = np.linspace(0, np.pi, 50)
        G, B = np.meshgrid(gamma, beta)
        Z = qaoa_cost(G, B)
        assert Z.min() >= 0
        assert Z.max() <= 1

    def test_qaoa_cost_symmetry_gamma(self):
        """Test QAOA cost is symmetric in gamma."""
        # At gamma=0, cos(0)=1, sin(0)=0
        c1 = qaoa_cost(0, 0)
        # At gamma=pi, cos(pi)=-1, sin(pi)=0
        c2 = qaoa_cost(np.pi, 0)
        # Both should have same cost
        npt.assert_almost_equal(c1, c2, decimal=5)

    def test_qaoa_cost_known_points(self):
        """Test QAOA cost at known points."""
        c = qaoa_cost(0, 0)
        expected = 0.5 + 0.3 * 0 + 0.2 * 1
        assert c == pytest.approx(expected)

    def test_qaoa_cost_boundary(self):
        """Test QAOA cost at boundary."""
        c = qaoa_cost(np.pi, 0)
        expected = 0.5 + 0.3 * 0 + 0.2 * 1
        assert c == pytest.approx(expected)


class TestVQEEnergy:
    """Tests for vqe_energy function."""

    def test_vqe_energy_h2_scalar(self):
        """Test VQE energy H2 with scalar input."""
        result = vqe_energy(0.5, "h2")
        expected = -1.0 + 0.5 * np.cos(0.5) + 0.2 * np.sin(1.0)
        assert result == pytest.approx(expected)

    def test_vqe_energy_lih_scalar(self):
        """Test VQE energy LiH with scalar input."""
        result = vqe_energy(0.5, "lih")
        expected = -7.8 + 0.3 * np.cos(0.5) + 0.15 * np.sin(1.0)
        assert result == pytest.approx(expected)

    def test_vqe_energy_array(self):
        """Test VQE energy with array input."""
        theta = np.array([0, np.pi/4, np.pi/2])
        result = vqe_energy(theta, "h2")
        assert len(result) == 3

    def test_vqe_energy_default_hamiltonian(self):
        """Test VQE energy uses default H2."""
        theta = np.array([0, np.pi/4, np.pi/2])
        result_h2 = vqe_energy(theta, "h2")
        result_default = vqe_energy(theta)
        npt.assert_array_almost_equal(result_h2, result_default)

    def test_vqe_energy_invalid_hamiltonian(self):
        """Test VQE energy with invalid Hamiltonian raises error."""
        with pytest.raises(ValueError, match="Unknown Hamiltonian"):
            vqe_energy(0.5, "invalid")

    def test_vqe_energy_h2_known_points(self):
        """Test VQE energy H2 at known points."""
        e0 = vqe_energy(0, "h2")
        assert e0 == pytest.approx(-1.0 + 0.5 + 0)

    def test_vqe_energy_lih_range(self):
        """Test VQE energy LiH is in reasonable range."""
        theta = np.linspace(0, 2*np.pi, 100)
        energies = vqe_energy(theta, "lih")
        assert energies.min() < -7.5
        assert energies.max() > -7.5


class TestQAOALandscape:
    """Tests for plot_qaoa_landscape function."""

    def test_plot_creates_figure(self):
        """Test plotting creates a figure."""
        fig = plot_qaoa_landscape()
        assert fig is not None
        plt.close(fig)

    def test_plot_saves_to_file(self):
        """Test plotting saves to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "qaoa.png")
            plot_qaoa_landscape(output_path=output_path)
            assert os.path.exists(output_path)

    def test_plot_custom_resolution(self):
        """Test plotting with custom resolution."""
        fig = plot_qaoa_landscape(resolution=25)
        assert fig is not None
        plt.close(fig)

    def test_plot_custom_ranges(self):
        """Test plotting with custom ranges."""
        fig = plot_qaoa_landscape(
            gamma_range=(0, 2*np.pi),
            beta_range=(0, 2*np.pi)
        )
        assert fig is not None
        plt.close(fig)

    def test_plot_custom_dpi(self):
        """Test plotting with custom DPI."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "qaoa.png")
            plot_qaoa_landscape(output_path=output_path, dpi=300)
            assert os.path.exists(output_path)


class TestVQELandscape:
    """Tests for plot_vqe_landscape function."""

    def test_plot_creates_figure(self):
        """Test plotting creates a figure."""
        fig = plot_vqe_landscape()
        assert fig is not None
        plt.close(fig)

    def test_plot_h2(self):
        """Test plotting H2 landscape."""
        fig = plot_vqe_landscape(hamiltonian="h2")
        assert fig is not None
        plt.close(fig)

    def test_plot_lih(self):
        """Test plotting LiH landscape."""
        fig = plot_vqe_landscape(hamiltonian="lih")
        assert fig is not None
        plt.close(fig)

    def test_plot_saves_to_file(self):
        """Test plotting saves to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "vqe.png")
            plot_vqe_landscape(output_path=output_path)
            assert os.path.exists(output_path)

    def test_plot_custom_resolution(self):
        """Test plotting with custom resolution."""
        fig = plot_vqe_landscape(resolution=50)
        assert fig is not None
        plt.close(fig)

    def test_plot_custom_theta_range(self):
        """Test plotting with custom theta range."""
        fig = plot_vqe_landscape(theta_range=(0, 4*np.pi))
        assert fig is not None
        plt.close(fig)

    def test_plot_custom_dpi(self):
        """Test plotting with custom DPI."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "vqe.png")
            plot_vqe_landscape(output_path=output_path, dpi=300)
            assert os.path.exists(output_path)


class TestCostFunctionProperties:
    """Property-based tests for cost functions."""

    def test_qaoa_cost_periodicity(self):
        """Test QAOA cost is periodic."""
        gamma = np.array([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
        beta = np.zeros(5)
        costs = qaoa_cost(gamma, beta)
        assert costs[0] == pytest.approx(costs[-1], rel=1e-5)

    def test_vqe_energy_periodicity(self):
        """Test VQE energy is periodic."""
        theta = np.array([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
        energies = vqe_energy(theta, "h2")
        assert energies[0] == pytest.approx(energies[-1], rel=1e-5)

    def test_qaoa_cost_gradient_exists(self):
        """Test QAOA cost has finite gradient."""
        gamma = np.linspace(0, np.pi, 20)
        beta = np.linspace(0, np.pi, 20)
        G, B = np.meshgrid(gamma, beta)
        Z = qaoa_cost(G, B)
        assert np.all(np.isfinite(Z))

    def test_vqe_energy_gradient_exists(self):
        """Test VQE energy has finite gradient."""
        theta = np.linspace(0, 2*np.pi, 100)
        energies = vqe_energy(theta, "h2")
        assert np.all(np.isfinite(energies))


class TestEdgeCases:
    """Tests for edge cases."""

    def test_qaoa_cost_zero_inputs(self):
        """Test QAOA cost with zero inputs."""
        result = qaoa_cost(0, 0)
        assert isinstance(result, (float, np.floating))

    def test_vqe_energy_zero_input(self):
        """Test VQE energy with zero input."""
        result = vqe_energy(0, "h2")
        assert isinstance(result, (float, np.floating))

    def test_qaoa_cost_large_inputs(self):
        """Test QAOA cost with large inputs."""
        result = qaoa_cost(100, 100)
        assert np.isfinite(result)

    def test_vqe_energy_large_input(self):
        """Test VQE energy with large input."""
        result = vqe_energy(100, "h2")
        assert np.isfinite(result)
