# What the Plots Show

Each image contains two 3D bar charts: real part (left) and imaginary part (right) of the density matrix ρ=∣ψ⟩⟨ψ∣ρ=∣ψ⟩⟨ψ∣.
For Grover’s algorithm, all imaginary parts are zero, so the right subplot will show only a flat plane at zero.

    Stage 1 – ∣00⟩∣00⟩
    Only the top‑left element (row 0, col 0) of the density matrix is 1; all other entries are 0.
    → A single red bar at (0,0) in the real part; imaginary part empty.

    Stage 2 – Equal superposition
    All diagonal entries are 0.250.25 (red bars). Off‑diagonal entries (coherences) are also 0.250.25, indicating perfect coherence between all basis states.
    → The real part shows a symmetric “city” of red bars of equal height on every matrix position.

    Stage 3 – After Oracle
    The diagonal remains 0.250.25 everywhere, but the off‑diagonal elements involving ∣11⟩∣11⟩ (the last row/column) flip sign:

        Entries (3,0),(3,1),(3,2),(0,3),(1,3),(2,3)(3,0),(3,1),(3,2),(0,3),(1,3),(2,3) become −0.25−0.25 (blue bars).

        All other off‑diagonals stay +0.25+0.25 (red).
        This phase pattern is the signature of the oracle marking ∣11⟩∣11⟩.

    Stage 4 – After Diffusion
    The state is exactly ∣11⟩∣11⟩, so only the bottom‑right element (row 3, col 3) is 1; all other entries are 0.
    → A single red bar at (3,3) in the real part; imaginary part zero.

# Interpretation

The city plots vividly show how coherence builds up (many off‑diagonal bars in stages 2 and 3) and finally collapses into the solution state (single bar at stage 4). The sign change (blue vs. red) in stage 3 visually captures the oracle’s phase flip.

