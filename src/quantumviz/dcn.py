"""
Dimensional Circular Notation (DCN) Visualization Module

Provides functions for visualizing quantum states using Dimensional Circular Notation,
a polar representation where phase is encoded as angular position and amplitude
magnitude as radial extent. Multi-qubit states shown as concentric circles.
"""

import matplotlib
import numpy as np

matplotlib.use('Agg')
import json
from typing import Any, List, Optional

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Wedge, Arc
from matplotlib.lines import Line2D


def parse_amplitude(amp: Any) -> complex:
    """Convert various input formats to a complex number."""
    if isinstance(amp, (int, float)):
        return complex(amp, 0)
    elif isinstance(amp, str):
        amp = amp.replace(' ', '')
        if amp.endswith('j'):
            return complex(amp)
        else:
            return complex(float(amp), 0)
    elif isinstance(amp, (list, tuple)) and len(amp) == 2:
        return complex(amp[0], amp[1])
    else:
        raise ValueError(f"Unsupported amplitude format: {amp}")


def state_to_density(state_vector: List[complex]) -> np.ndarray:
    """Convert state vector to density matrix: ρ = |ψ⟩⟨ψ|."""
    psi = np.array(state_vector, dtype=complex).reshape(-1, 1)
    return psi @ psi.conj().T


def compute_dcn_coordinates(state_vector: List[complex], n_qubits: int):
    """
    Compute polar coordinates for DCN visualization.
    
    Returns for each basis state:
    - radius: |amplitude|
    - angle: phase angle in radians (arg(amplitude))
    - ring: which ring (for concentric circles in multi-qubit)
    """
    n_states = 2 ** n_qubits
    coords = []
    
    for i, amp in enumerate(state_vector[:n_states]):
        r = abs(amp)
        theta = np.angle(amp)  # Phase in radians
        
        # For multi-qubit, assign ring based on qubit
        # Ring 0 = outermost (MSB), Ring n-1 = innermost (LSB)
        ring = 0  # Single ring for single qubit
        
        coords.append({
            'basis': format(i, f'0{n_qubits}b')[-(n_qubits):],
            'r': r,
            'theta': theta,
            'ring': ring,
            'sign': '+' if amp.real >= 0 else '-'
        })
    
    return coords


def plot_dcn(
    state_vector: List[complex],
    title: str = "DCN Visualization",
    output_path: Optional[str] = None,
    dpi: int = 150
) -> plt.Figure:
    """
    Create a Dimensional Circular Notation (DCN) plot.
    
    For single qubit: shows phase as angular position on a circle.
    For multi-qubit: shows concentric rings (outer = most significant qubit).
    
    Args:
        state_vector: List of complex amplitudes (length must be power of 2)
        title: Title for the plot
        output_path: Path to save the figure (if None, returns figure object)
        dpi: Resolution for saved figure
    
    Returns:
        matplotlib Figure object if output_path is None, else None
    """
    n = len(state_vector)
    if n == 0:
        raise ValueError("State vector cannot be empty")
    
    n_qubits = int(np.log2(n))
    if 2 ** n_qubits != n:
        raise ValueError(f"State vector length {n} is not a power of 2")
    
    n_rings = n_qubits  # Number of concentric circles
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    fig.suptitle(title, fontsize=16, y=0.95)
    
    # Draw rings (concentric circles)
    max_r = 1.0
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, n_rings))
    
    for ring_idx in range(n_rings):
        r_norm = (ring_idx + 0.5) / n_rings  # Normalize ring position
        circle = Circle(
            (0, 0), r_norm,
            fill=False, color=colors[ring_idx], 
            linewidth=2, linestyle='--'
        )
        ax.add_patch(circle)
    
    # Draw amplitude wedges
    for i, amp in enumerate(state_vector):
        r = abs(amp)
        theta = np.angle(amp)
        
        if r < 0.01:
            continue
        
        # Calculate angle for this amplitude (in radians for polar plot)
        # Normalize to [0, 2π]
        theta_norm = (theta + 2 * np.pi) % (2 * np.pi)
        
        # Convert to matplotlib polar coordinates (where 0 is at top, clockwise)
        theta_polar = np.pi / 2 - theta_norm
        
        # Draw wedge from center to radius
        wedge_width = r / n_rings
        for ring_idx in range(n_rings):
            r_inner = ring_idx * wedge_width
            r_outer = (ring_idx + 1) * wedge_width
            
            # Color based on sign
            color = '#E74C3C' if amp.real >= 0 else '#3498DB'
            
            wedge = Wedge(
                (0, 0), r_outer,
                (theta_polar * 180 / np.pi - 15),
                (theta_polar * 180 / np.pi + 15),
                width=r_outer - r_inner,
                color=color, alpha=0.7
            )
            ax.add_patch(wedge)
    
    # Add phase markers (tick marks around circumference)
    phase_labels = ['0°', '45°', '90°', '135°', '180°', '225°', '270°', '315°']
    phase_angles = np.linspace(0, 2*np.pi, 8, endpoint=False)
    
    for angle, label in zip(phase_angles, phase_labels):
        # Convert to matplotlib polar
        theta_marker = np.pi / 2 - angle
        x = 1.1 * np.cos(theta_marker)
        y = 1.1 * np.sin(theta_marker)
        ax.text(x, y, label, ha='center', va='center', fontsize=10, 
               fontweight='bold', color='#555555')
    
    # Draw outer circle boundary
    outer_circle = Circle((0, 0), 1.0, fill=False, color='black', linewidth=2)
    ax.add_patch(outer_circle)
    
    # Draw axis lines
    for angle in [0, np.pi/2, np.pi, 3*np.pi/2]:
        theta_line = np.pi / 2 - angle
        ax.plot([0, 1.15*np.cos(theta_line)], [0, 1.15*np.sin(theta_line)], 
               'k-', linewidth=0.5, alpha=0.3)
    
    # Configure polar plot
    ax.set_ylim(0, 1.2)
    ax.set_rticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels([])  # Hide radial tick labels
    ax.grid(True, alpha=0.2)
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=dpi)
        plt.close()
    else:
        return fig


def plot_dcns_from_file(
    input_file: str,
    output_dir: Optional[str] = None,
    dpi: int = 150
) -> List[str]:
    """
    Plot multiple DCN stages from a JSON input file.
    
    Args:
        input_file: Path to JSON file with stages
        output_dir: Directory to save output files (if None, uses current dir)
        dpi: Resolution for saved figures
    
    Returns:
        List of output filenames
    """
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    n_qubits = data['qubits']
    stages = data['stages']
    
    # If output_dir doesn't exist, create it
    if output_dir and not output_dir.endswith('/'):
        output_dir += '/'
    
    output_files = []
    
    for idx, stage in enumerate(stages):
        name = stage.get('name', f'Stage {idx+1}')
        
        # Parse state vector
        state_vector = []
        for amp in stage['state_vector']:
            state_vector.append(parse_amplitude(amp))
        
        # Generate output filename
        safe_name = name.replace(' ', '_').replace('/', '_')
        stage_num = f'stage_{idx+1:02d}'
        output_path = f'{output_dir}{stage_num}_{safe_name}.png' if output_dir else f'{stage_num}_{safe_name}.png'
        
        plot_dcn(state_vector, name, output_path, dpi)
        output_files.append(output_path)
        
        print(f'Saved: {output_path}')
    
    return output_files