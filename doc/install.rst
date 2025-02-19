####################
 Installation guide
####################

The ``weldx`` package can be installed using *conda* or *mamba* package
manager from the ``conda-forge`` channel. These managers originate from
the freely available `Anaconda Python stack
<https://docs.conda.io/en/latest/miniconda.html>`_. If you do not have
Anaconda or Miniconda installed yet, we ask you to install
*Miniconda*-3. Documentation for the installation procedure can be found
`here
<https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation>`__.

After this step you have access to the conda command and can proceed to
installing the WelDX package:

.. code::

   conda create -n weldx -c conda-forge weldx weldx_widgets

The package is also available on pypi and can be installed via *pip*:

.. code::

   pip install weldx weldx-widgets

As weldx currently depends on the package ``bottleneck``, which contains
C/C++ code, you will need a working C/C++ compiler. The conda package
does not have this requirement as it only installs pre-compiled
binaries. So if you do not know how to install a working compiler, we
strongly encourage using the conda package.

************************
 Setting up Jupyter Lab
************************

Weldx provides lots of visualization methods for planning and analysis.
These methods need a frontend like Jupyter lab or Jupyter notebook. We
currently recommend to use Jupyter lab, as it is modern and makes
working with several notebooks easier. You can install Jupyter lab both
via *conda* or *pip*. If you use conda we suggest that you create a
separate environment for your weldx installation and jupyter. This keeps
the environments clean and easier to upgrade (is that really true? think
of mixed versions of extensions in lab env and weldx env!).

Here is a guide on howto setup different kernels for Jupyter `guide
<https://ipython.readthedocs.io/en/7.25.0/install/kernel_install.html>`__.

Create an environment named "jlab" via conda that installs ``jupyterlab`` and the ``k3d`` extension:

.. code::

   conda create -n jlab jupyterlab k3d -c conda-forge

Then we switch to the weldx environment created in the first step and
make it available within Jupyter:

.. code::

   conda activate weldx
   python -m ipykernel install --user --name weldx --display-name "Python (weldx)"

This will enable us to select the Python interpreter installed in the
weldx environment within Jupyter. So when a new notebook is created, we
can choose "Python (weldx)" to access all the software bundled with the
weldx Python package.

fixing DLL errors on Windows systems
====================================

In case you run into an error when using the weldx kernel on Windows
systems that fails to read DLLs like:

.. code::

   ImportError: DLL load failed: The specified module could not be found

you might have to apply the fix mentioned `here
<https://github.com/jupyter/notebook/issues/4569#issuecomment-609901011>`__.

Go to ``%userprofile%\.ipython\profile_default\startup`` using the
windows explorer and create a new file called ``ipython_startup.py``.
Open it with a text editor and paste the following commands into the
file:

.. code::

   import sys
   import os
   from pathlib import Path


   # get directory of virtual environment
   p_env = Path(sys.executable).parent

   # directory which should contain all the DLLs
   p_dlls = p_env / 'Library' / 'bin'

   # effectively prepend this DLL directory to $PATH
   # semi-colon used here as sep on Windows
   os.environ['PATH'] = '{};{}'.format(p_dlls, os.environ['PATH'])

************************
 Everything in one-shot
************************

If you feel lucky, you can try and copy-paste all install commands into
a shell. Note that if one command fails, all subsequent commands will
not be executed.

using conda:

.. code::

   conda create -n weldx -c conda-forge weldx weldx_widgets
   conda activate weldx
   python -m ipykernel install --user --name weldx --display-name "Python (weldx)"
   conda create -n jlab -c conda-forge jupyterlab k3d
   conda activate jlab
