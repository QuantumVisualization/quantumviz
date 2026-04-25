Grover's Algorithm on 2 Qubits – Step‑by‑Step

We consider four stages:

    Initial state ∣00⟩∣00⟩

    Equal superposition after applying Hadamard gates to both qubits

    Oracle that flips the phase of the marked state ∣11⟩∣11⟩

    Diffusion operator (inversion about the mean)

The exact state vectors (in the computational basis order ∣00⟩,∣01⟩,∣10⟩,∣11⟩∣00⟩,∣01⟩,∣10⟩,∣11⟩) are:

    Stage 1: ∣00⟩∣00⟩
    [1, 0, 0, 0]

    Stage 2: H⊗2∣00⟩=12(∣00⟩+∣01⟩+∣10⟩+∣11⟩)H⊗2∣00⟩=21​(∣00⟩+∣01⟩+∣10⟩+∣11⟩)
    [0.5, 0.5, 0.5, 0.5]

    Stage 3: Oracle U∣11⟩U∣11⟩​ (phase flip on ∣11⟩∣11⟩)
    12(∣00⟩+∣01⟩+∣10⟩−∣11⟩)21​(∣00⟩+∣01⟩+∣10⟩−∣11⟩)
    [0.5, 0.5, 0.5, -0.5]

    Stage 4: Diffusion D=H⊗2(2∣0⟩⟨0∣−I)H⊗2D=H⊗2(2∣0⟩⟨0∣−I)H⊗2
    After one iteration, the marked state is amplified to unit probability:
    [0, 0, 0, 1] (i.e., ∣11⟩∣11⟩)
