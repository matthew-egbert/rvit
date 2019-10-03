import numpy as np

from kivy.graphics.transformation import Matrix
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty, NumericProperty,\
    OptionProperty, ListProperty
from kivy.graphics.opengl import *

from rvit.core.configurable_property import ConfigurableProperty
import rvit.core.glsl_utils as glsl_utils

from rvit.core.vis.rvi_element import RVIElement
from rvit.core.vis.simple_renderer import SimpleRenderer
from rvit.core.vis.components import *
from rvit.core.vis.data_sources import *

import OpenGL.GL as gl
    
class PointRenderer(SimpleRenderer,xy_bounds,color,x_data,y_data,color1d_data,size_data):
    """The PointRenderer is used to display a scatter diagram of 2D points. 
    
    It can use a :class:`.color1d_data` to determine the color or size 
    of the displayed points and :class:`.size_data` to determine their size.

    .. figure:: vis_examples/point_renderer.png
       :width: 300px
       
       A PointRenderer showing 50,000 points. A SecondaryDataSource is being 
       used to color the points by their position within a grid.

    The rvit configuration file used to make the figure image is the following:

    .. code-block:: python

       PointRenderer:
            pos_hint: {'x':0.0, 'y':0.0}
            size_hint:  (1.0,1.0)
            target_object: model
            x_data: 'chemistry.pos[:,0]'
            y_data: 'chemistry.pos[:,1]'
            color_data: 'chemistry.zone'
            size_data: 'chemistry.pos[:,0]'
            show_controls: True
            point_size: 0.5
            xmin: 0
            ymin: 0
            xmax: 1
            ymax: 1
            color: [1.0,1.0,1.0,0.8]
            unique_name: 'pos' 
       
    """
    
    point_size = NumericProperty(10.0)
    """a float :: when the **size_data** parameter is not provided, this
property specifies the color for all plotted points. When color_data
is provided, the alpha value is still used.

    """

    def __init__(self, *args, **kwargs):
        #glEnable(0x8642)  # equivalent to
        glEnable(gl.GL_PROGRAM_POINT_SIZE)
        
        super().__init__(**kwargs)        
        
    def registerConfigurableProperties(self):
        super().registerConfigurableProperties()
        self.addConfigurableProperty(PointRenderer.point_size)

    def loadShaders(self,subs={}):
        subs.update(
            {'point_size': 0.025 * self.point_size * min(Window.width, Window.height),
        })
        super().loadShaders('points',subs=subs)
        
    def on_point_size(self, obj, value):
        # for a single points size (and to scale diverse point sizes)
        self.loadShaders()

    def on_point_size(self, inst, value):
        ## the point size is dynamically set in loadShaders in a way that
        ## responds to the overall window size. Accordingly this callback
        ## calls loadShaders (to allow response to window resizing).
        super().on_size(inst, value)
        self.loadShaders()

    def on_pos(self, inst, value):
        ## the point size is dynamically set in loadShaders in a way that
        ## responds to the overall window size. Accordingly this callback
        ## calls loadShaders (to allow response to window resizing).
        super().on_pos(inst, value)
        self.loadShaders()
        
        
# ### Local Variables: ###
# ### mode: python ###
# ### python-main-file: "main.py" ###
# ### python-working-dir: "../minimal_project/" ###
# ### End: ###
