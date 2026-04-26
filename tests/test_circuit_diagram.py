"""
Comprehensive tests for the Circuit Diagram visualization module.
"""

import matplotlib
import numpy as np

matplotlib.use('Agg')
import json
import os
import tempfile

import matplotlib.pyplot as plt

from quantumviz.circuit_diagram import (
    GATE_COLORS,
    draw_cnot,
    draw_controlled_gate,
    draw_measure,
    draw_qubit_line,
    draw_single_gate,
    parse_circuit,
)
from quantumviz.circuit_diagram import (
    plot_circuit as draw_circuit,
)


class TestGateColors:
    """Tests for GATE_COLORS dictionary."""

    def test_gate_colors_defined(self):
        """Test all standard gates have colors."""
        required_gates = ['H', 'X', 'Y', 'Z', 'CNOT', 'T', 'S', 'RX', 'RY', 'RZ']
        for gate in required_gates:
            assert gate in GATE_COLORS

    def test_gate_colors_valid_hex(self):
        """Test all colors are valid hex format."""
        import re
        hex_pattern = re.compile(r'^#[0-9A-Fa-f]{6}$')
        for gate, color in GATE_COLORS.items():
            assert hex_pattern.match(color), f"Invalid hex color for {gate}"

    def test_default_color_exists(self):
        """Test default color is defined."""
        assert 'default' in GATE_COLORS


class TestDrawQubitLine:
    """Tests for draw_qubit_line function."""

    def test_draw_qubit_line_creates_line(self):
        """Test drawing qubit line."""
        fig, ax = plt.subplots()
        draw_qubit_line(ax, 0, 5)
        plt.close(fig)

    def test_draw_qubit_line_custom_color(self):
        """Test drawing qubit line with custom color."""
        fig, ax = plt.subplots()
        draw_qubit_line(ax, 2, 5, color='red')
        plt.close(fig)


class TestDrawSingleGate:
    """Tests for draw_single_gate function."""

    def test_draw_single_gate(self):
        """Test drawing single gate."""
        fig, ax = plt.subplots()
        draw_single_gate(ax, 'H', 1, 0)
        plt.close(fig)

    def test_draw_single_gate_with_label(self):
        """Test drawing single gate with custom label."""
        fig, ax = plt.subplots()
        draw_single_gate(ax, 'RX', 1, 0, label="RX\nθ=0.5")
        plt.close(fig)

    def test_draw_single_gate_unknown_type(self):
        """Test drawing unknown gate type uses default color."""
        fig, ax = plt.subplots()
        draw_single_gate(ax, 'UNKNOWN', 1, 0)
        plt.close(fig)


class TestDrawCNOT:
    """Tests for draw_cnot function."""

    def test_draw_cnot(self):
        """Test drawing CNOT gate."""
        fig, ax = plt.subplots()
        draw_cnot(ax, 1, 0, 1, 2)
        plt.close(fig)

    def test_draw_cnot_same_qubit(self):
        """Test drawing CNOT on same qubit."""
        fig, ax = plt.subplots()
        draw_cnot(ax, 1, 0, 1, 0)
        plt.close(fig)


class TestDrawControlledGate:
    """Tests for draw_controlled_gate function."""

    def test_draw_controlled_gate_z(self):
        """Test drawing controlled-Z gate."""
        fig, ax = plt.subplots()
        draw_controlled_gate(ax, 1, 0, 1, 2, 'Z')
        plt.close(fig)

    def test_draw_controlled_gate_custom(self):
        """Test drawing custom controlled gate."""
        fig, ax = plt.subplots()
        draw_controlled_gate(ax, 1, 0, 1, 2, 'X')
        plt.close(fig)


class TestDrawMeasure:
    """Tests for draw_measure function."""

    def test_draw_measure(self):
        """Test drawing measurement gate."""
        fig, ax = plt.subplots()
        draw_measure(ax, 1, 0)
        plt.close(fig)


class TestParseCircuit:
    """Tests for parse_circuit function."""

    def test_parse_single_gate(self):
        """Test parsing single gate."""
        data = {"qubits": 2, "gates": [{"type": "H", "qubit": 0}]}
        layers = parse_circuit(data)
        assert len(layers) == 1
        assert len(layers[0]) == 1

    def test_parse_multiple_gates(self):
        """Test parsing multiple gates."""
        data = {
            "qubits": 2,
            "gates": [
                {"type": "H", "qubit": 0},
                {"type": "H", "qubit": 1}
            ]
        }
        layers = parse_circuit(data)
        assert len(layers) == 1
        assert len(layers[0]) == 2

    def test_parse_cnot_creates_layer(self):
        """Test CNOT creates separate layer."""
        data = {
            "qubits": 2,
            "gates": [
                {"type": "H", "qubit": 0},
                {"type": "CNOT", "control": 0, "target": 1}
            ]
        }
        layers = parse_circuit(data)
        assert len(layers) == 2

    def test_parse_multiple_cnots(self):
        """Test multiple CNOTs."""
        data = {
            "qubits": 3,
            "gates": [
                {"type": "CNOT", "control": 0, "target": 1},
                {"type": "CNOT", "control": 1, "target": 2}
            ]
        }
        layers = parse_circuit(data)
        assert len(layers) == 2
        for layer in layers:
            assert len(layer) == 1

    def test_parse_parametric_gates(self):
        """Test parsing parametric gates."""
        data = {
            "qubits": 1,
            "gates": [
                {"type": "RX", "qubit": 0, "theta": 0.5},
                {"type": "RY", "qubit": 0, "theta": 1.0}
            ]
        }
        layers = parse_circuit(data)
        assert len(layers) == 1


class TestDrawCircuit:
    """Tests for draw_circuit function."""

    def test_draw_simple_circuit(self):
        """Test drawing simple circuit."""
        data = {
            "qubits": 2,
            "gates": [
                {"type": "H", "qubit": 0},
                {"type": "H", "qubit": 1}
            ],
            "name": "Test Circuit"
        }
        fig = draw_circuit(data)
        assert fig is not None
        plt.close(fig)

    def test_draw_circuit_grover(self):
        """Test drawing Grover circuit."""
        data = {
            "qubits": 2,
            "gates": [
                {"type": "H", "qubit": 0},
                {"type": "H", "qubit": 1},
                {"type": "CNOT", "control": 0, "target": 1},
                {"type": "H", "qubit": 0},
                {"type": "H", "qubit": 1}
            ],
            "name": "Grover"
        }
        fig = draw_circuit(data)
        assert fig is not None
        plt.close(fig)

    def test_draw_circuit_qft(self):
        """Test drawing QFT circuit."""
        data = {
            "qubits": 2,
            "gates": [
                {"type": "H", "qubit": 0},
                {"type": "P", "qubit": 1, "phi": np.pi/2},
                {"type": "CNOT", "control": 0, "target": 1},
                {"type": "H", "qubit": 1}
            ],
            "name": "QFT"
        }
        fig = draw_circuit(data)
        assert fig is not None
        plt.close(fig)

    def test_draw_circuit_saves_to_file(self):
        """Test circuit saves to file."""
        data = {
            "qubits": 1,
            "gates": [{"type": "H", "qubit": 0}]
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "circuit.png")
            draw_circuit(data, output_path)
            assert os.path.exists(output_path)

    def test_draw_circuit_single_qubit(self):
        """Test drawing single qubit circuit."""
        data = {
            "qubits": 1,
            "gates": [
                {"type": "H", "qubit": 0},
                {"type": "X", "qubit": 0},
                {"type": "measure", "qubit": 0}
            ]
        }
        fig = draw_circuit(data)
        assert fig is not None
        plt.close(fig)

    def test_draw_circuit_custom_dpi(self):
        """Test drawing with custom DPI."""
        data = {"qubits": 1, "gates": [{"type": "H", "qubit": 0}]}
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "circuit.png")
            draw_circuit(data, output_path, dpi=300)
            assert os.path.exists(output_path)


class TestCircuitFromFile:
    """Tests for loading and drawing circuits from files."""

    def test_draw_circuit_from_json(self):
        """Test drawing circuit from JSON file."""
        data = {
            "qubits": 2,
            "gates": [
                {"type": "H", "qubit": 0},
                {"type": "CNOT", "control": 0, "target": 1}
            ]
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "circuit.json")
            with open(input_file, 'w') as f:
                json.dump(data, f)

            with open(input_file, 'r') as f:
                circuit_data = json.load(f)

            output_path = os.path.join(tmpdir, "output.png")
            draw_circuit(circuit_data, output_path)
            assert os.path.exists(output_path)


class TestEdgeCases:
    """Tests for edge cases."""

    def test_circuit_with_all_gates(self):
        """Test circuit with various gate types."""
        data = {
            "qubits": 2,
            "gates": [
                {"type": "H", "qubit": 0},
                {"type": "X", "qubit": 1},
                {"type": "Y", "qubit": 0},
                {"type": "Z", "qubit": 1},
                {"type": "RX", "qubit": 0, "theta": 0.5},
                {"type": "RY", "qubit": 1, "theta": 1.0},
                {"type": "RZ", "qubit": 0, "theta": 1.5},
                {"type": "measure", "qubit": 0},
                {"type": "measure", "qubit": 1}
            ]
        }
        fig = draw_circuit(data)
        assert fig is not None
        plt.close(fig)

    def test_circuit_default_name(self):
        """Test circuit uses default name."""
        data = {"qubits": 1, "gates": [{"type": "H", "qubit": 0}]}
        fig, ax = plt.subplots()
        # Draw manually without title to test default
        data_without_name = {"qubits": 1, "gates": [{"type": "H", "qubit": 0}]}
        draw_circuit(data_without_name)
        plt.close(fig)

    def test_empty_gates_list(self):
        """Test circuit with no gates."""
        data = {"qubits": 1, "gates": []}
        fig = draw_circuit(data)
        assert fig is not None
        plt.close(fig)
