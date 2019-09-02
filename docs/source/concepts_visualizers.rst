===========
Visualizers
===========

Visualizers are user-interface elemets that are used to display data.

List of visualizers
###################

.. autosummary:: rvit.core.vis.rvi_element.RVIElement
   :nosignatures:

.. autosummary:: rvit.core.vis.point_renderer.PointRenderer
   :nosignatures:
      
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

List of components
##################
.. automodsumm:: rvit.core.vis.components
   :skip: BooleanProperty,NumericProperty,ObjectProperty,OptionProperty,RvitWidget,StringProperty,DictProperty,ListProperty,Property,ConfigParserProperty,BoundedNumericProperty,VariableListProperty,AliasProperty,ReferenceListProperty,Window
   :nosignatures:

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

List of data-sources
####################

.. automodsumm:: rvit.core.vis.data_sources
   :skip:
      BooleanProperty,NumericProperty,ObjectProperty,OptionProperty,RvitWidget,StringProperty,DictProperty,ListProperty,Property,ConfigParserProperty,BoundedNumericProperty,VariableListProperty,AliasProperty,ReferenceListProperty
   :nosignatures:
     
