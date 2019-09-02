from rvit.core.vis.rvi_element import RVIElement
from rvit.core.vis.simple_renderer import SimpleRenderer
from rvit.core.vis.components import *
from rvit.core.vis.data_sources import *
from kivy.graphics.opengl import *

# import OpenGL
# OpenGL.ERROR_CHECKING = False
import OpenGL.GL as gl
# from OpenGL.GLU import *

class LineRenderer(SimpleRenderer,xy_bounds,x_data,y_data,color1d_data,size_data):
    """The LineRenderer is ..."""

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.shader_fn='line_renderer.glsl'
    
    def loadShaders(self,subs={}):
        super().loadShaders('lines',subs=subs)
        
    # def registerConfigurableProperties(self):
    #     super().registerConfigurableProperties()
