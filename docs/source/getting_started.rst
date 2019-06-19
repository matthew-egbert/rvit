=================
Getting Started
=================

Installation
============
<<Insert instructions from github.>>

Basic Instructions
==================
To augment your simulation with RVIT you must do the following two things.

1. Start RVIT
-------------

The code snippet below defines a simple model of particles moving in a random
walk. The highlighted line with the call to :meth:`~rvit.core.init_rvit.init_rvit()`  
shows how rvit is started. 

.. literalinclude :: ./minimal_example/main.py
    :language: python
    :emphasize-lines: 17	   
    
:meth:`~rvit.core.init_rvit.init_rvit()` takes two arguments. The first tells
RVIT where it can find all of the data that it will visualize and modify. In
this example all of the data to be visualized is in the DiffusionModel
object, so we pass `self`. The second argument tells RVIT where it can find
the GUI-specification file. This is a file that you will write to specify
which visualization and interactive elements are to be displayed--see Step 2!

2. Write a RVIT GUI-specification file
--------------------------------------

The contents of `rvit.kv` might look something like this:

.. literalinclude :: ./minimal_example/rvit.kv
    :language: python
	          
   
A minimal working example
=========================

<<Insert cookie-cutter instructions from github.>>
