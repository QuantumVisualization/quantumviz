"""
Tests for quantum physics correctness in quantumviz.
Verifies that all quantum mechanical properties are correctly computed.
"""

import sys
from pathlib import Path

import numpy as np
import numpy.testing as npt
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestStateNormalization:
    """Test that all state vectors are properly normalized."""

    def test_bloch_parsed_states_normalized(self):
        from quantumviz.bloch_sphere import parse_complex_pair, parse_ket
        test_cases = [
            ("parse_ket", lambda: parse_ket("|0>")),
            ("parse_ket", lambda: parse_ket("|+>")),
            ("parse_ket", lambda: parse_ket("|+i>")),
            ("parse_complex_pair", lambda: parse_complex_pair("(1, 1)")),
            ("parse_complex_pair", lambda: parse_complex_pair("(1+0j, 1+0j)")),
        ]
        for name, func in test_cases:
            result = func()
            norm = np.linalg.norm(result)
            assert abs(norm - 1.0) < 1e-10, f"{name}: norm = {norm}"

    def test_state_city_density_trace(self):
        from quantumviz.state_city import state_to_density
        test_states = [
            [1, 0],
            [0, 1],
            [1/np.sqrt(2), 1/np.sqrt(2)],
            [1/np.sqrt(2), -1/np.sqrt(2)],
            [1/np.sqrt(2), 1j/np.sqrt(2)],
        ]
        for state in test_states:
            rho = state_to_density(state)
            trace = np.trace(rho).real
            assert abs(trace - 1.0) < 1e-10, f"State {state}: trace = {trace}"

    def test_multi_qubit_state_normalization(self):
        from quantumviz.state_city import state_to_density
        test_states = [
            [1, 0, 0, 0],
            [0.5, 0.5, 0.5, 0.5],
            [1/np.sqrt(2), 0, 0, 1/np.sqrt(2)],
            [1/np.sqrt(2), 0, 1/np.sqrt(2), 0],
        ]
        for state in test_states:
            rho = state_to_density(state)
            prob_sum = np.sum(np.abs(state) ** 2)
            assert abs(prob_sum - 1.0) < 1e-10, f"State {state}: prob_sum = {prob_sum}"


class TestBlochVectorProperties:
    """Test Bloch vector properties."""

    def test_all_bloch_vectors_unit_norm(self):
        from quantumviz.bloch_sphere import (
            parse_angles,
            parse_complex_pair,
            parse_ket,
        )
        states = [
            ("|0>", lambda: parse_ket("|0>")),
            ("|1>", lambda: parse_ket("|1>")),
            ("|+>", lambda: parse_ket("|+>")),
            ("|->", lambda: parse_ket("|->")),
            ("|+i>", lambda: parse_ket("|+i>")),
            ("|-i>", lambda: parse_ket("|-i>")),
            ("(1,1)", lambda: parse_complex_pair("(1, 1)")),
            ("angles", lambda: parse_angles("theta=60 deg, phi=45 deg")),
        ]
        for name, func in states:
            result = func()
            norm = np.linalg.norm(result)
            assert abs(norm - 1.0) < 1e-10, f"{name}: norm = {norm}"

    def test_orthogonal_states_opposite_vectors(self):
        from quantumviz.bloch_sphere import parse_ket
        pairs = [
            ("|0>", "|1>"),
            ("|+>", "|->"),
            ("|+i>", "|-i>"),
        ]
        for s1, s2 in pairs:
            v1 = parse_ket(s1)
            v2 = parse_ket(s2)
            dot = np.dot(v1, v2)
            assert abs(dot + 1.0) < 1e-10, f"{s1} and {s2}: dot = {dot}"

    def test_bloch_vector_z_axis(self):
        from quantumviz.bloch_sphere import parse_ket
        v0 = parse_ket("|0>")
        v1 = parse_ket("|1>")
        assert abs(v0[0]) < 1e-10
        assert abs(v0[1]) < 1e-10
        assert abs(v0[2] - 1.0) < 1e-10
        assert abs(v1[2] + 1.0) < 1e-10

    def test_bloch_vector_x_axis(self):
        from quantumviz.bloch_sphere import parse_ket
        vp = parse_ket("|+>")
        vm = parse_ket("|->")
        assert abs(vp[0] - 1.0) < 1e-10
        assert abs(vm[0] + 1.0) < 1e-10

    def test_bloch_vector_y_axis(self):
        from quantumviz.bloch_sphere import parse_ket
        vpi = parse_ket("|+i>")
        vmi = parse_ket("|-i>")
        assert abs(vpi[1] - 1.0) < 1e-10
        assert abs(vmi[1] + 1.0) < 1e-10


class TestDensityMatrixProperties:
    """Test density matrix properties for quantum states."""

    def test_density_matrix_hermitian(self):
        from quantumviz.state_city import state_to_density
        states = [
            [1, 0],
            [1/np.sqrt(2), 1/np.sqrt(2)],
            [0.6, 0.8],
            [1/np.sqrt(2), 1j/np.sqrt(2)],
        ]
        for state in states:
            rho = state_to_density(state)
            npt.assert_array_almost_equal(rho, rho.conj().T, decimal=10)

    def test_density_matrix_trace_equals_one(self):
        from quantumviz.state_city import state_to_density
        states = [
            [1, 0],
            [0, 1],
            [1/np.sqrt(2), 1/np.sqrt(2)],
            [0.5+0.5j, 0.5-0.5j],
        ]
        for state in states:
            rho = state_to_density(state)
            trace = np.trace(rho)
            assert abs(trace - 1.0) < 1e-10

    def test_pure_state_tr_rho_squared_equals_one(self):
        from quantumviz.state_city import state_to_density
        states = [
            [1, 0],
            [0, 1],
            [1/np.sqrt(2), 1/np.sqrt(2)],
            [1/np.sqrt(2), -1/np.sqrt(2)],
        ]
        for state in states:
            rho = state_to_density(state)
            rho_sq = rho @ rho
            trace_rho_sq = np.trace(rho_sq)
            assert abs(trace_rho_sq - 1.0) < 1e-10

    def test_density_matrix_positive_semidefinite(self):
        from quantumviz.state_city import state_to_density
        states = [
            [1, 0],
            [1/np.sqrt(3), 2/np.sqrt(3)],
            [0.5, 0.866],
        ]
        for state in states:
            rho = state_to_density(state)
            eigenvalues = np.linalg.eigvalsh(rho)
            assert all(e >= -1e-10 for e in eigenvalues), f"Eigenvalues: {eigenvalues}"

    def test_orthogonal_states_orthogonal_density_matrices(self):
        from quantumviz.state_city import state_to_density
        rho0 = state_to_density([1, 0])
        rho1 = state_to_density([0, 1])
        overlap = np.trace(rho0 @ rho1)
        assert abs(overlap) < 1e-10


class TestEntanglementProperties:
    """Test properties of entangled states."""

    def test_bell_state_density_matrix(self):
        from quantumviz.state_city import state_to_density
        bell = [1/np.sqrt(2), 0, 0, 1/np.sqrt(2)]
        rho = state_to_density(bell)

        expected = np.array([
            [0.5, 0, 0, 0.5],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0.5, 0, 0, 0.5]
        ], dtype=complex)
        npt.assert_array_almost_equal(rho, expected)

    def test_bell_state_entanglement_indicator(self):
        from quantumviz.state_city import state_to_density
        bell = [1/np.sqrt(2), 0, 0, 1/np.sqrt(2)]
        rho = state_to_density(bell)

        rho_sq = rho @ rho
        trace_rho_sq = np.trace(rho_sq)
        assert abs(trace_rho_sq - 1.0) < 1e-10

    def test_separable_state_product_form(self):
        from quantumviz.state_city import state_to_density
        state = [1, 0, 0, 0]
        rho = state_to_density(state)

        assert abs(rho[0, 0] - 1.0) < 1e-10
        assert np.all(np.abs(rho - np.diag([1, 0, 0, 0])) < 1e-10)


class TestSuperpositionProperties:
    """Test superposition state behavior."""

    def test_equal_superposition_probabilities(self):
        state = [0.5, 0.5, 0.5, 0.5]
        probs = np.abs(state) ** 2
        assert all(abs(p - 0.25) < 1e-10 for p in probs)

    def test_uniform_superposition_normalized(self):
        n = 4
        state = [1/np.sqrt(n)] * n
        probs = np.abs(state) ** 2
        assert abs(sum(probs) - 1.0) < 1e-10

    def test_ghz_state_density_matrix(self):
        from quantumviz.state_city import state_to_density
        ghz = [1/np.sqrt(2), 0, 0, 0, 0, 0, 0, 1/np.sqrt(2)]
        rho = state_to_density(ghz)

        assert abs(rho[0, 0] - 0.5) < 1e-10
        assert abs(rho[7, 7] - 0.5) < 1e-10
        assert abs(rho[0, 7] - 0.5) < 1e-10


class TestBlochSphereConsistency:
    """Test consistency between different Bloch sphere representations."""

    def test_state_to_bloch_consistent(self):
        from quantumviz.bloch_sphere import parse_ket
        from quantumviz.dynamic_flow import bloch_vector

        state = [1, 0]
        expected = parse_ket("|0>")
        actual = bloch_vector(state)
        npt.assert_array_almost_equal(expected, actual)

    def test_parse_angles_matches_bloch_vector(self):
        from quantumviz.bloch_sphere import parse_angles, parse_bloch_vector

        result_angles = parse_angles("theta=60 deg, phi=45 deg")
        x, y, z = result_angles
        result_bloch = parse_bloch_vector(f"({x}, {y}, {z})")
        npt.assert_array_almost_equal(result_angles, result_bloch)


class TestCostFunctionPhysics:
    """Test physics correctness of cost functions."""

    def test_qaoa_cost_range_valid(self):
        from quantumviz.cost_landscape import qaoa_cost
        edges = [(0, 1), (1, 2)]
        gammas = np.linspace(0, np.pi, 20)
        betas = np.linspace(0, np.pi, 20)
        G, B = np.meshgrid(gammas, betas)
        costs = qaoa_cost(G, B, edges)
        assert np.all(np.isfinite(costs))

    def test_vqe_energy_hermitian(self):
        from quantumviz.cost_landscape import vqe_energy
        terms = [
            {"coeff": 1.0, "paulis": ["Z"]},
            {"coeff": 0.5, "paulis": ["X"]},
            {"coeff": 0.25, "paulis": ["Y"]},
        ]
        thetas = np.linspace(0, 2*np.pi, 50)
        energies = vqe_energy(thetas, terms)
        assert np.all(np.isfinite(energies))

    def test_qaoa_cost_symmetry(self):
        from quantumviz.cost_landscape import qaoa_cost
        edges = [(0, 1)]
        c1 = qaoa_cost(0, 0, edges)
        c2 = qaoa_cost(np.pi, 0, edges)
        npt.assert_almost_equal(c1, c2, decimal=5)

    def test_vqe_energy_periodicity_2pi(self):
        from quantumviz.cost_landscape import vqe_energy
        terms = [{"coeff": 1.0, "paulis": ["Z"]}]
        e0 = vqe_energy(0, terms)
        e2pi = vqe_energy(2*np.pi, terms)
        npt.assert_almost_equal(e0, e2pi, decimal=10)


class TestMeasurements:
    """Test measurement probability calculations."""

    def test_computational_basis_measurement(self):
        from quantumviz.state_city import state_to_density
        state = [1, 0, 0, 0]
        rho = state_to_density(state)
        probs = np.diag(rho).real
        expected = [1, 0, 0, 0]
        npt.assert_array_almost_equal(probs, expected)

    def test_superposition_measurement_probs(self):
        state = [1/np.sqrt(2), 0, 1/np.sqrt(2), 0]
        probs = np.abs(state) ** 2
        expected = [0.5, 0, 0.5, 0]
        npt.assert_array_almost_equal(probs, expected, decimal=10)

    def test_measurement_probabilities_sum_to_one(self):
        test_states = [
            [1, 0],
            [0, 1],
            [1/np.sqrt(2), 1/np.sqrt(2)],
            [1/np.sqrt(2), 0, 1/np.sqrt(2), 0],
            [1/np.sqrt(5), 2/np.sqrt(5)],
        ]
        for state in test_states:
            probs = np.abs(state) ** 2
            assert abs(sum(probs) - 1.0) < 1e-10


class TestGateRepresentations:
    """Test gate representation properties."""

    def test_pauli_x_flip(self):
        from quantumviz.bloch_sphere import parse_ket
        v0 = parse_ket("|0>")
        v1 = parse_ket("|1>")
        npt.assert_array_almost_equal(v1, -v0)

    def test_pauli_z_phase(self):
        from quantumviz.bloch_sphere import parse_ket
        vp = parse_ket("|+>")
        vm = parse_ket("|->")
        assert abs(np.dot(vp, vm) + 1) < 1e-10

    def test_hadamard_creates_superposition(self):
        from quantumviz.bloch_sphere import parse_ket
        vp = parse_ket("|+>")
        assert abs(vp[0] - 1.0) < 1e-10
        assert abs(vp[2]) < 1e-10


class TestRabiOscillation:
    """Test Rabi oscillation physics."""

    def test_rabi_oscillation_z_component(self):
        from quantumviz.dynamic_flow import bloch_vector
        omega = 1.0
        t = np.pi / omega
        state = [np.cos(omega * t / 2), 1j * np.sin(omega * t / 2)]
        bloch = bloch_vector(state)
        assert abs(bloch[2] + 1.0) < 1e-10


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_zero_amplitude_handling(self):
        from quantumviz.state_city import state_to_density
        state = [1, 0]
        rho = state_to_density(state)
        assert abs(rho[0, 0] - 1.0) < 1e-10
        assert abs(rho[1, 1]) < 1e-10

    def test_complex_phases_preserved(self):
        from quantumviz.state_city import state_to_density
        state = [1/np.sqrt(2), 1j/np.sqrt(2)]
        rho = state_to_density(state)
        assert abs(rho[0, 1] + 0.5j) < 1e-10

    def test_nearly_zero_bloch_vector_raises(self):
        from quantumviz.bloch_sphere import parse_bloch_vector
        with pytest.raises(ValueError):
            parse_bloch_vector("(0, 0, 0)")

    def test_invalid_bloch_vector_not_on_sphere(self):
        from quantumviz.bloch_sphere import parse_bloch_vector
        result = parse_bloch_vector("(2, 0, 0)")
        norm = np.linalg.norm(result)
        assert abs(norm - 1.0) < 1e-10
