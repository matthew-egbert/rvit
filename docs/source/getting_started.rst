=================
Getting Started
=================
These instructions provide a basic overview of how to use RVIT. If you prefer to
get your hands dirty as fast as possible, consider following the cookie-cutter
instructions below :ref:`A minimal working project`

Requirements
============

* Python 3.x


Installation
============
<<Insert instructions from github.>>


Basic Instructions
==================
To augment your simulation with RVIT you must do the following.

1. Start RVIT from your simulation.

    .. code-block:: python
		
        import rvit

        class ClimateModel(object):
            def __init__(self):
                rvit.start(self,kv='rvit.kv') <-- starts RVIT

	cm = ClimateModel()
	# rvit.start(cm,kv='rvit.kv')         <-- alternative way to start RVIT

    the :method:`rvit.start()` method takes two required arguments. The first
    tells RVIT where it can find all of the data that it will visualize and
    modify. Here we have passed a reference to the newly instantiated
    ClimateModel class.

    The second argument tells RVIT where it can find the GUI-specification
    file. This is a file that you will write to specify which visualization and
    interactive elements are to be displayed--see Step 2 below.
	
2. Write a rvit GUI-specification file.

   The following provides an example of 

    .. code-block:: python
    
        #:kivy 1.0.9
        #:import PointRenderer rvit.core.vis.point_renderer <-- This imports the visualizer
    
        FloatLayout:
            Model:
                id: model
            PointRenderer:  ## <-- This is a visualizer
                pos_hint: {'x':0.0, 'y':0.0} ## <-- These are properties
                size_hint:  (1.0,1.0)        
                simulation: model
                x_data: 'chemistry.pos[:,0]' 
                y_data: 'chemistry.pos[:,1]'
                unique_name: 'pos'
	          
   
A minimal working project
=========================

<<Insert cookie-cutter instructions from github.>>
