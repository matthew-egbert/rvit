#from rvit.core.vis.simple_renderer_3d import SimpleRenderer3D
from rvit.core.vis.simple_renderer import SimpleRenderer
from rvit.core.vis.components import *
from rvit.core.vis.data_sources import *
from kivy.graphics.opengl import *

import rvit.core.glsl_utils as glsl_utils

# import OpenGL
# OpenGL.ERROR_CHECKING = False
import OpenGL.GL as gl
# from OpenGL.GLU import *

class SimpleRenderer3D(xyz_bounds,x_data,y_data,z_data,color1d_data,size_data,gradient,color):
    indices = ListProperty([])
    """The LineRenderer is ..."""

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.shader_fn='simple_renderer_3d.glsl'

        l,h = -1.0,1.0
        self.cube_xyz = np.array([[l,l,l],                             
                             [l,l,h],
                             [l,h,h],
                             [l,h,l],
                             [h,l,l],
                             [h,l,h],
                             [h,h,h],
                             [h,h,l],
                             ])

        self.cube_inds = [0,1,1,2,2,3,3,0,
                          4,5,5,6,6,7,7,4,
                          0,4,1,5,2,6,3,7]

    def update(self):
        if self.format_has_changed :
            self.loadShaders()
            self.format_has_changed = False
            self.data_per_element = self.n_data_sources
            self.data_to_shader = np.zeros((self.n_elements,
                                            self.n_data_sources), dtype=np.float32)
            if hasattr(self,'mesh_indices') :
                self.mesh.indices = self.mesh_indices
            else:
                self.mesh.indices = np.arange(self.n_elements)

        if self.enabled:
            super().update()
            if self.n_elements > 0:                
                self.mesh.vertices = self.data_to_shader.ravel()
                self.render_context.ask_update()        
    
    def loadShaders(self, mesh_mode, subs = {}):
        
        ## generate the glsl code
        self.shaders = glsl_utils.loadShaders(self.shader_fn,
                                              {**subs,**self.shader_substitutions})        

        ## set the meshes shaders to the generated glsl code
        self.render_context.shader.vs = self.shaders['vs']
        self.render_context.shader.fs = self.shaders['fs']
        
        if self.render_context.shader.success == False:
            print('Shader compilation failed')
            print(self.shaders['vs'])
            print(self.shaders['fs'])
            quit()

        self.render_context['vmin'] = self.vmin
        self.render_context['vmax'] = self.vmax

        ## replace any previous mesh with the new mesh
        if hasattr(self,'mesh'):
            self.render_context.remove(self.mesh)

        ######
        self.mesh = Mesh(mode=mesh_mode, fmt=self.fmt)
        ## other data sources currently disabled as I try to get the basic
        ## array renderer working

        self.render_context.add(self.mesh)

        self.mesh2 = Mesh(mode='lines', fmt=self.fmt)
        
        self.mesh2.indices = self.cube_inds
        self.mesh2.vertices = self.cube_xyz.flatten()                
        self.render_context.add(self.mesh2)
        
        self.format_has_changed = True

    def on_indices(self, inst, value):
        if value != '':
            v = ''.join(value)
            s = 'self.mesh_indices = self.simulation.%s' %(v)
            exec(s)

            self.format_has_changed = True

class LineRenderer3D(SimpleRenderer3D) :    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #self.shader_fn='line_renderer.glsl'
    
    def loadShaders(self,subs={}):        
        super().loadShaders('lines',subs=subs)

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
        glEnable(gl.GL_PROGRAM_POINT_SIZE)
        subs.update(
            {'point_size': 0.025 * self.point_size * min(Window.width, Window.height),
        })
        super().loadShaders('points',subs=subs)        
