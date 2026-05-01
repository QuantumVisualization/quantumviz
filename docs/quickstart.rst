Quick Start
===========

Command Line Interface
----------------------

Bloch Sphere
^^^^^^^^^^^^^

Create a text file with quantum states:

.. code-block:: text

   |0>
   |1>
   |+>
   theta=60 deg, phi=45 deg

Then visualize:

.. code-block:: bash

   quantumviz bloch-sphere input.txt -o bloch.png

   # PDF output
   quantumviz bloch-sphere input.txt -o bloch.pdf -f pdf

State City
^^^^^^^^^^

Create a JSON file:

.. code-block:: json

   {
     "qubits": 2,
     "stages": [
       {"name": "Initial", "state_vector": [1, 0, 0, 0]},
       {"name": "Superposition", "state_vector": [0.5, 0.5, 0.5, 0.5]}
     ]
   }

Visualize:

.. code-block:: bash

   quantumviz state-city input.json -o output/

   # PDF output for multiple files
   quantumviz state-city input.json -o output/ -f pdf

Circuit Diagram
^^^^^^^^^^^^

.. code-block:: json

   {
     "qubits": 2,
     "gates": [
       {"type": "H", "qubit": 0},
       {"type": "CNOT", "control": 0, "target": 1}
     ]
   }

Render:

.. code-block:: bash

   quantumviz circuit circuit.json -o circuit.png

   # PDF output
   quantumviz circuit circuit.json -o circuit.pdf -f pdf

Cost Landscape
^^^^^^^^^^^

.. code-block:: bash

   quantumviz cost-landscape qaoa -o qaoa.png
   quantumviz cost-landscape vqe -o vqe.png

   # PDF output
   quantumviz cost-landscape qaoa -o qaoa.pdf -f pdf

Dashboard
^^^^^^^^^

.. code-block:: bash

   quantumviz serve

Then open http://localhost:8000 in your browser.

Python API
----------

.. code-block:: python

   from quantumviz import plot_bloch_sphere, plot_state_city, state_to_density

   # Plot Bloch sphere (PNG)
   plot_bloch_sphere("input.txt", "output.png")

   # Plot Bloch sphere (PDF)
   plot_bloch_sphere("input.txt", "output.pdf")

   # Create density matrix
   rho = state_to_density([1/np.sqrt(2), 1/np.sqrt(2)])

   # Plot state city (PNG)
   plot_state_city([1, 0, 0, 0], "Density Matrix", "output.png")

   # Plot state city (PDF)
   plot_state_city([1, 0, 0, 0], "Density Matrix", "output.pdf")
