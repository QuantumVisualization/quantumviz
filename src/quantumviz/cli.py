"""
CLI (Command Line Interface) for quantumviz package.

Provides unified command-line interface for all visualization tools.
"""

import sys
import click

from quantumviz.bloch_sphere import plot_bloch_sphere as _plot_bloch_sphere
from quantumviz.state_city import plot_state_cities_from_file as _plot_state_cities
from quantumviz.cost_landscape import (
    plot_qaoa_landscape as _plot_qaoa,
    plot_vqe_landscape as _plot_vqe,
)
from quantumviz.circuit_diagram import plot_circuit as _draw_circuit
from quantumviz.dynamic_flow import plot_dynamic_flow as _plot_dynamic_flow


@click.group()
@click.version_option(version="0.1.0")
def main():
    """quantumviz - Quantum Algorithm Visualization Library"""
    pass


@main.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output", "output_file", help="Output file path")
@click.option("--dpi", default=150, help="DPI for saved figure")
def bloch_sphere(input_file, output_file, dpi):
    """Plot Bloch sphere visualization from input file."""
    if output_file is None:
        output_file = input_file.replace('.txt', '.png')
    _plot_bloch_sphere(input_file, output_file, dpi)
    click.echo(f"Saved: {output_file}")


@main.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output-dir", "output_dir", help="Output directory")
@click.option("--dpi", default=150, help="DPI for saved figures")
def state_city(input_file, output_dir, dpi):
    """Plot State City visualization from JSON input file."""
    output_files = _plot_state_cities(input_file, output_dir, dpi)
    for f in output_files:
        click.echo(f"Saved: {f}")


@main.command()
@click.argument("algorithm", type=click.Choice(["qaoa", "vqe"]))
@click.option("-o", "--output", "output_file", help="Output file path")
@click.option("--dpi", default=150, help="DPI for saved figure")
def cost_landscape(algorithm, output_file, dpi):
    """Plot QAOA or VQE cost landscape."""
    if output_file is None:
        output_file = f"{algorithm}_cost_landscape.png"

    if algorithm == "qaoa":
        _plot_qaoa(output_path=output_file, dpi=dpi)
    else:
        _plot_vqe(output_path=output_file, dpi=dpi)

    click.echo(f"Saved: {output_file}")


@main.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output", "output_file", help="Output file path")
@click.option("--dpi", default=150, help="DPI for saved figure")
def circuit(input_file, output_file, dpi):
    """Plot quantum circuit diagram from JSON input file."""
    import json

    if output_file is None:
        output_file = input_file.replace('.json', '_circuit.png')

    with open(input_file, 'r') as f:
        data = json.load(f)

    _draw_circuit(data, output_file, dpi)
    click.echo(f"Saved: {output_file}")


@main.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output", "output_file", help="Output file path")
@click.option("--dpi", default=150, help="DPI for saved figure")
def dynamic_flow(input_file, output_file, dpi):
    """Plot dynamic flow/time evolution from JSON input file."""
    if output_file is None:
        output_file = input_file.replace('.json', '_flow.png')

    _plot_dynamic_flow(input_file, output_file, dpi)
    click.echo(f"Saved: {output_file}")


@main.command()
@click.option("--host", default="0.0.0.0", help="Host to bind to")
@click.option("-p", "--port", default=8000, help="Port to bind to")
def serve(host, port):
    """Start the quantumviz dashboard web server."""
    try:
        from quantumviz.dashboard.main import app
        import uvicorn
        click.echo(f"Starting dashboard at http://{host}:{port}")
        uvicorn.run(app, host=host, port=port)
    except ImportError as e:
        click.echo(f"Error: Dashboard dependencies not installed.", err=True)
        click.echo("Install with: pip install quantumviz[dashboard]", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
