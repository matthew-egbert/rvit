=================
Getting Started
=================

Installation
============

Basic Instructions
==================
To use RVIT there are two steps.

1. you must initialize kivy by ...

2. configure a rvit specification file

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

test
