Generalization and Limitations

    The example works because we deliberately chose an initial state that keeps the two qubits unentangled. For a generic input, the QFT creates entanglement, and the reduced state of a single qubit becomes mixed – it lies inside the Bloch sphere. Our program only handles pure states (points on the surface).

    If you wish to visualize multi‑qubit QFT for arbitrary inputs, you would need a more advanced tool that can display the full quantum state (e.g., using Q-spheres, 3‑D bar charts of probability amplitudes, or animations).

    Despite these limitations, the exercise illustrates how even a simple single‑qubit visualizer can help build intuition for specific parts of a larger algorithm, provided you understand the conditions under which the qubits remain unentangled.
