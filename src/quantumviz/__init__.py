"""
quantumviz - Quantum Algorithm Visualization Library

A Python library for visualizing quantum algorithm states including
Bloch spheres, density matrices, cost landscapes, and circuit diagrams.
"""

from quantumviz._version import __version__

from quantumviz.bloch_sphere import (
    plot_bloch_sphere,
    parse_ket,
    parse_bloch_vector,
    parse_angles,
    parse_complex_pair,
)

from quantumviz.state_city import (
    plot_state_city,
    parse_amplitude,
    state_to_density,
)

from quantumviz.cost_landscape import (
    plot_qaoa_landscape,
    plot_vqe_landscape,
    qaoa_cost,
    vqe_energy,
)

from quantumviz.circuit_diagram import (
    plot_circuit as plot_circuit,
    GATE_COLORS,
)

from quantumviz.dynamic_flow import (
    plot_dynamic_flow,
    plot_rabi_oscillation,
    plot_time_evolution,
)

__all__ = [
    "__version__",
    "plot_bloch_sphere",
    "parse_ket",
    "parse_bloch_vector",
    "parse_angles",
    "parse_complex_pair",
    "plot_state_city",
    "parse_amplitude",
    "state_to_density",
    "plot_qaoa_landscape",
    "plot_vqe_landscape",
    "qaoa_cost",
    "vqe_energy",
    "plot_circuit",
    "GATE_COLORS",
    "plot_dynamic_flow",
    "plot_rabi_oscillation",
    "plot_time_evolution",
]
