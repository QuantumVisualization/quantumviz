Visualizing the Quantum Fourier Transform with the Bloch Sphere Program

The Quantum Fourier Transform (QFT) is a multi‑qubit operation – for nn qubits it acts on a 2n2n-dimensional state space. Our program, however, is designed to visualize single‑qubit pure states on the Bloch sphere. This imposes a fundamental limitation: we cannot directly display the full state of a multi‑qubit QFT. Nevertheless, we can still gain insight by focusing on one qubit at a time, provided the overall state remains a product state (i.e., unentangled) throughout the circuit. For such inputs, each qubit evolves independently and its state stays on the surface of the Bloch sphere.

Choosing an Input That Yields Product States

Consider the 2‑qubit QFT circuit:

    Apply Hadamard to qubit 1.

    Apply a controlled‑phase gate R2 (phase π/2) with qubit 1 as control and qubit 2 as target.

    Apply Hadamard to qubit 2.

    Swap the qubits (optional, often included to match the mathematical definition).

If we start with the product state ∣01⟩ (qubit 1 = ∣0⟩, qubit 2 = ∣1⟩), the state remains a product after every step. We can therefore track each qubit separately.


Qubit 1 Evolution

    Stage 1 (initial) : ∣0⟩

    Stage 2 (after H on qubit 1) : ∣+⟩=∣0⟩+∣1⟩/sqrt(2)

    Stage 3 (after controlled‑phase) : the controlled‑phase turns ∣+⟩ into (∣0⟩+eiπ/2∣1⟩)/sqrt(2)=∣+i⟩ (Bloch vector (0,1,0))

    Stage 4 (after H on qubit 2) : qubit 1 unchanged, still ∣+i⟩

    Stage 5 (after swap) : swap exchanges the qubits, so qubit 1 becomes what qubit 2 was before the swap – qubit 2 was ∣−⟩=(∣0⟩−∣1⟩)/sqrt(2) (Bloch vector (−1,0,0)).

Thus qubit 1 goes through the sequence:
∣0⟩  →  ∣+⟩  →  ∣+i⟩  →  ∣+i⟩  →  ∣−⟩.


Qubit 2 Evolution

    Stage 1 : ∣1⟩

    Stage 2 (after H on qubit 1) : unchanged, still ∣1⟩

    Stage 3 (after controlled‑phase) : still ∣1⟩ (the phase is applied to the state, but the qubit’s Bloch vector remains the same because it is an eigenstate of the Pauli‑ZZ basis)

    Stage 4 (after H on qubit 2) : H∣1⟩=∣−⟩

    Stage 5 (after swap) : becomes qubit 1’s previous state, ∣+i⟩.

Sequence for qubit 2:
∣1⟩  →  ∣1⟩  →  ∣1⟩  →  ∣−⟩  →  ∣+i⟩.


