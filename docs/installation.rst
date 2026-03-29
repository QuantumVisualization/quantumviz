Installation
============

Core Package
-----------

.. code-block:: bash

   pip install qviz

With Dashboard (Web Interface)
-------------------------------

.. code-block:: bash

   pip install qviz[dashboard]

With Quantum Hardware Support
-----------------------------

.. code-block:: bash

   pip install qviz[all]

Development Install
-------------------

.. code-block:: bash

   git clone https://github.com/yourusername/qviz.git
   cd qviz
   pip install -e ".[dev,all]"

Requirements
------------

- Python 3.9+
- numpy >= 1.20
- matplotlib >= 3.5

Optional Dependencies
---------------------

- fastapi, uvicorn, pydantic (dashboard)
- qiskit, qiskit-ibm-runtime (hardware)
- pytest (testing)
