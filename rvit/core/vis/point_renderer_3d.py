from rvit.core.vis.components import NumericProperty, Window
from rvit.core.vis.simple_renderer_3d import SimpleRenderer3D
import OpenGL.GL as gl
from kivy.graphics.opengl import *

class PointRenderer3D(SimpleRenderer3D) :
    point_size = NumericProperty(1.0)
    """a float :: when the **size_data** parameter is not provided, this
    property specifies the color for all plotted points. When color_data
    is provided, the alpha value is still used.

    """
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #self.shader_fn='line_renderer.glsl'

    def loadShaders(self,subs={}):        
        subs.update(
            {'point_size': 0.025 * self.point_size * min(Window.width, Window.height),
        })
        super().loadShaders('points',subs=subs)