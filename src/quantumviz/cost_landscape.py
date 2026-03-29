"""
Cost Landscape Visualization Module

Provides functions for visualizing parameter optimization landscapes
for QAOA (Quantum Approximate Optimization Algorithm) and VQE
(Variational Quantum Eigensolver).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from typing import Optional, Tuple


def qaoa_cost(gamma: np.ndarray, beta: np.ndarray) -> np.ndarray:
    """
    Compute QAOA cost function for a simple MaxCut problem.

    This is a demonstration cost function for a 2-qubit MaxCut problem
    on a line graph: 0 -- 1

    Cost function: C(γ, β) = 0.5 + 0.3*sin(2γ)*cos(2β) + 0.2*cos(4γ)

    Args:
        gamma: Array of gamma parameters
        beta: Array of beta parameters

    Returns:
        Array of cost values
    """
    g = np.asarray(gamma)
    b = np.asarray(beta)
    cost = 0.5 + 0.3 * np.sin(2*g) * np.cos(2*b) + 0.2 * np.cos(4*g)
    return cost


def vqe_energy(theta: np.ndarray, hamiltonian: str = "h2") -> np.ndarray:
    """
    Compute VQE energy landscape for a simple molecular Hamiltonian.

    This is a demonstration energy function.

    For H2: E(θ) = -1.0 + 0.5*cos(θ) + 0.2*sin(2θ)
    For LiH: E(θ) = -7.8 + 0.3*cos(θ) + 0.15*sin(2θ)

    Args:
        theta: Array of variational parameters
        hamiltonian: Either "h2" or "lih"

    Returns:
        Array of energy values
    """
    t = np.asarray(theta)

    if hamiltonian.lower() == "h2":
        energy = -1.0 + 0.5 * np.cos(t) + 0.2 * np.sin(2*t)
    elif hamiltonian.lower() == "lih":
        energy = -7.8 + 0.3 * np.cos(t) + 0.15 * np.sin(2*t)
    else:
        raise ValueError(f"Unknown Hamiltonian: {hamiltonian}")

    return energy


def plot_qaoa_landscape(
    gamma_range: Tuple[float, float] = (0, np.pi),
    beta_range: Tuple[float, float] = (0, np.pi),
    resolution: int = 50,
    output_path: Optional[str] = None,
    dpi: int = 150
) -> plt.Figure:
    """
    Plot QAOA cost landscape.

    Args:
        gamma_range: Range of gamma values (min, max)
        beta_range: Range of beta values (min, max)
        resolution: Number of points in each dimension
        output_path: Path to save the figure (if None, returns figure object)
        dpi: Resolution for saved figure

    Returns:
        matplotlib Figure object if output_path is None, else None
    """
    gammas = np.linspace(gamma_range[0], gamma_range[1], resolution)
    betas = np.linspace(beta_range[0], beta_range[1], resolution)
    G, B = np.meshgrid(gammas, betas)
    Z = qaoa_cost(G, B)

    plt.figure(figsize=(10, 8))
    contour = plt.contourf(G, B, Z, levels=20, cmap='viridis')
    plt.colorbar(contour, label='Cost (Cut Value)')
    plt.xlabel('γ (problem parameter)')
    plt.ylabel('β (mixer parameter)')
    plt.title('QAOA Cost Landscape: MaxCut (2 qubits)')
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=dpi)
        plt.close()
    else:
        return plt.gcf()


def plot_vqe_landscape(
    theta_range: Tuple[float, float] = (0, 2*np.pi),
    resolution: int = 100,
    hamiltonian: str = "h2",
    output_path: Optional[str] = None,
    dpi: int = 150
) -> plt.Figure:
    """
    Plot VQE energy landscape.

    Args:
        theta_range: Range of theta values (min, max)
        resolution: Number of points
        hamiltonian: Either "h2" or "lih"
        output_path: Path to save the figure (if None, returns figure object)
        dpi: Resolution for saved figure

    Returns:
        matplotlib Figure object if output_path is None, else None
    """
    thetas = np.linspace(theta_range[0], theta_range[1], resolution)
    energies = vqe_energy(thetas, hamiltonian)

    plt.figure(figsize=(10, 6))
    plt.plot(thetas, energies, 'b-', linewidth=2)
    plt.xlabel('θ (variational parameter)')
    plt.ylabel('Energy')
    plt.title(f'VQE Energy Landscape: {hamiltonian.upper()}')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=dpi)
        plt.close()
    else:
        return plt.gcf()


def main(args: Optional[list] = None) -> None:
    """
    CLI entry point for Cost Landscape visualization.

    Args:
        args: Command line arguments (if None, uses sys.argv)
    """
    import sys

    if args is None:
        args = sys.argv[1:]

    if len(args) < 1:
        print("Usage: python -m qviz.cost_landscape <qaoa|vqe> [output_file]")
        sys.exit(1)

    algorithm = args[0].lower()
    output_file = args[1] if len(args) > 1 else None

    if algorithm == "qaoa":
        if output_file:
            plot_qaoa_landscape(output_path=output_file)
            print(f"Saved: {output_file}")
        else:
            plot_qaoa_landscape()
    elif algorithm == "vqe":
        if output_file:
            plot_vqe_landscape(output_path=output_file)
            print(f"Saved: {output_file}")
        else:
            plot_vqe_landscape()
    else:
        print(f"Unknown algorithm: {algorithm}")
        print("Use 'qaoa' or 'vqe'")
        sys.exit(1)


if __name__ == "__main__":
    main()
