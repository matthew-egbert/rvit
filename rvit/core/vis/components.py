from rvit.core.vis.rvi_element import RVIElement
from kivy.properties import *
import kivy.graphics.transformation 
from kivy.core.window import Window
import rvit.core
import re
import numpy as np

class xy_bounds(RVIElement):
    """Provides four configurable parameters that determine the limits of a 2D display.
    """
    
    xmin = NumericProperty(-1.) #: x-coord of left border 
    xmax = NumericProperty(1.)  #: x-coord of right border 
    ymin = NumericProperty(-1.) #: x-coord of bottom border 
    ymax = NumericProperty(1.)  #: x-coord of top border 

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.updateModelViewMatrix()
        
    def registerConfigurableProperties(self):
        super().registerConfigurableProperties()
        self.addConfigurableProperty(xy_bounds.xmin)
        self.addConfigurableProperty(xy_bounds.xmax)
        self.addConfigurableProperty(xy_bounds.ymin)
        self.addConfigurableProperty(xy_bounds.ymax)

    def updateProjectionMatrices(self):
        w = float(Window.width)
        h = float(Window.height)
        m = kivy.graphics.transformation.Matrix().identity()
        p = rvit.core.BUTTON_BORDER_HEIGHT
        m.scale(2.0 * self.width / w,
                2.0 * (self.height - p) / h, 1.0)
        m.translate(-1.0 + (self.pos[0]) * 2.0 / w,
                    -1.0 + (self.pos[1]) * 2.0 / h,
                    0.0)
        self.render_context['projection_mat'] = m

    def updateModelViewMatrix(self):
        m = kivy.graphics.transformation.Matrix().identity()
        hr = max(0.00001, (self.xmax - self.xmin))
        vr = max(0.00001, (self.ymax - self.ymin))
        m.scale(1.0 / hr,
                1.0 / vr,
                1.0)
        m.translate(-self.xmin / hr,
                    -self.ymin / vr,
                    0.0)
        self.render_context['modelview_mat'] = m

    def on_size(self, inst, value):
        self.updateProjectionMatrices()

    def on_pos(self, inst, value):
        self.updateProjectionMatrices()        
        
    def on_xmin(self, obj, value):
        self.updateModelViewMatrix()

    def on_xmax(self, obj, value):
        self.updateModelViewMatrix()

    def on_ymin(self, obj, value):
        self.updateModelViewMatrix()

    def on_ymax(self, obj, value):
        self.updateModelViewMatrix()

class color(RVIElement):
    """Provides a single 4-tuple parameter [R,G,B,A] that can be used to
    specify the the primary color of the visualizer. May be
    (partially) overridden by the color data sources...but in some
    cases (e.g. the color_1d data source) the alpha component still is used.

    """
    
    color = ListProperty([1.] * 4)
    """a 4-tuple (red,green,blue,alpha) :: when the **color_data**
parameter is not provided, this property specifies the color for all
plotted points. When color_data is provided, the alpha value is still
used."""

    def on_color(self, obj, value):
        # for single color setting
        self.render_context['color'] = [float(v) for v in self.color]
   
# class ColorMap(RVIElement):
#     colormap = NumericProperty(-1.) #: x-coord of left border 

#     def __init__(self, *args, **kwargs):
#         super().__init__(**kwargs)

#     def registerConfigurableProperties(self):
#         super().registerConfigurableProperties()
#         self.addConfigurableProperty(ColorMap.colormap)
        
#     def on_colormap(self, obj, value):
#         pass
        


