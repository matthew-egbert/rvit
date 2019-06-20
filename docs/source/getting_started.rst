=================
Getting Started
=================

Installation
============
<<Insert instructions from github.>>

Requirements

* Python 3.5 or later

Basic Instructions
==================
To augment your simulation with RVIT you must do the following two things.

1. Start RVIT
-------------

The script below defines a simple model of particles moving in a random
walk. The highlighted line with the call to :meth:`~rvit.core.init_rvit.init_rvit()`  
shows how rvit is started. 

.. literalinclude :: ./minimal_example/main.py
    :language: python
    :emphasize-lines: 17	   
    
:meth:`~rvit.core.init_rvit.init_rvit()` takes two arguments. The first tells
RVIT where it can find all of the data that it will visualize and modify. In
this example all of the data to be visualized is in the DiffusionModel object,
so we pass `self`. An equally good solution would be to create the model and
start rvit afterwards (as suggested by the final, commented line). The second
argument tells RVIT where it can find the GUI-specification file. This is a file
that you will write to specify which visualization and interactive elements are
to be displayed--see Step 2!

2. Write a RVIT GUI-specification file
--------------------------------------

The contents of `rvit.kv` might look something like this:

.. literalinclude :: ./minimal_example/rvit.kv
    :language: python
	          
   
Download and run a minimal working example
==========================================
If you want a base project to build from, you can install a quickstart project
plus all the dependencies using cookiecutter.

You will need Python 3.5 or later first. If you do not already have this on your
system, you can get it from [python.org](https://python.org), or by using your
system's package manager.

Next, install pip and virtualenv - you can do this through a package manager
such as apt, emerge, or brew, if you have one. For example, with emerge:

.. code-block:: bash

    bash sudo emerge --ask dev-python/pip virtualenv

Alternatively, there are complete instructions for installing virtualenv and pip
here:

* https://virtualenv.pypa.io/en/stable/installation/


Create a virtualenv and install dependencies:

.. code-block:: bash

    virtualenv env && source ./env/bin/activate && pip install cookiecutter

If you have already activated a virtualenv, and you need to reinstall a fresh
virtualenv and example code, you can run this command instead:

.. code-block:: bash

    bash deactivate && rm -rf rvit_example env && virtualenv env && \
        source ./env/bin/activate && pip install cookiecutter


Create, install, and run an example application:

.. code-block:: bash

    bash cookiecutter -f --no-input gh:flaviusb/rvit-template && pip \ 
        install -U --upgrade-strategy eager -e rvit_example && rvit_example 
