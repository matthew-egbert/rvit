
========
CONCEPTS
========

Visualizers
===========

Visualizers are user-interface elemets that are used to display data. An example
of a visualizer is the :class:`~rvit.core.vis.point_renderer.PointRenderer`,
which displays one-to-many points.

Each visualizer has


* zero or more `Components` that are configurable properties of the
  visualization (e.g. the size or color that the dots should be)

* one or more `Data Source` that specify the data that is to be plotted by the visualizer (e.g. the x and y position of the points to be plotted)

      
Components
==========

Components are units of configurable :ref:`visualizer<Visualizers>`
functionality. For example, the
:class:`~rvit.core.vis.point_renderer.PointRenderer` visualizer inherits the
:class:`~rvit.core.vis.components.xy_bounds` component which provides four
configurable variables: xmin, xmax, ymin and ymax. This means that when creating
a PointRenderer in an rvit.kv configuration file, you can specify its value
limits to run from -1 to 1 on both axes thus::

    PointRenderer:
        [other_properties]
        xmin: -1
	xmax: 1
	ymin: -1
	ymax: 1

Too see which components a given visualization uses, look at the :ref:`relevant
visualizer's documentation<List of visualizers>` and the classes it inherits
from (listed as "Bases") at the top of the visualizer's API documentation.


Data Sources
============
DataSources specify which data are to be plotted by
:ref:`Visualizers`. 

For example, :class:`~rvit.core.vis.point_renderer.PointRenderer` visualizers
inherits from :class:`x_data` which means that when you add a PointRenderer to
your rvit.kv configuration file, you can specify an `x_data` property thus::

    PointRenderer:
        [other_properties]
        x_data: 'model.data_source'

The last line above effectively says "This PointRenderer should use the data
located in *model.data_source* (a vector of floats) to specify the x-coordinates
of the points." To work properly, a PointRenderer would also take a `y_data`
property and optionally, some other data sources. To see which ones, you can
look at classes documentation:
:class:`rvit.core.vis.point_renderer.PointRenderer`      

Preprocessing
#############

Often the data in your program is not in exactly the same format as what you
would like to plot. For example, a visualization might expect data to lie in [0,1] 
but your model is working with data in [0,1000]. 

Preprocessor functions can be used to scale (or otherwise modify) the visualized
data. Note the actual data in the simulation is not modified by this
preprocessing, only its visualization. Preprocessing works by specifying a
function in a string. The following example scales the simulation data (which we
assume lies between 0 and 1000) to lie between 0 and 1 as required by the
:class:`~rvit.core.vis.data_sources.color_data` data source::

    XXXRenderer:
        [other_properties]
        color_data: 'model.a_data_source_that_ranges_btwn_0_and_1000'
        color_preprocess: 'lambda x: x/1000.'

NOTE: it is important that any preprocessing function does not change the shape
of the data. For instance `'lambda x: 0.5'` might be thought to change all of the
data in `x` to 0.5, but actually transforms x into a scalar. One way to write this
would instead be `'lambda x: 0.0 * x + 0.5'`.
	
     

Interactors
===========

Interactors are user-interface elemets that are used to modify parameters or
data during a program's execution.

