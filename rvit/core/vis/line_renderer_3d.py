from rvit.core.vis.simple_renderer_3d import SimpleRenderer3D
from rvit.core.vis.components import *
from rvit.core.vis.data_sources import *
from kivy.graphics.opengl import *

# import OpenGL
# OpenGL.ERROR_CHECKING = False
import OpenGL.GL as gl
# from OpenGL.GLU import *

class LineRenderer3D(SimpleRenderer3D,xyz_bounds,x_data,y_data,z_data,color1d_data,size_data,gradient):
    """The LineRenderer is ..."""

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #self.shader_fn='line_renderer_3d.glsl'
    
    def loadShaders(self,subs={}):
        super().loadShaders('lines',subs=subs)
        
    # def registerConfigurableProperties(self):
    #     super().registerConfigurableProperties()
