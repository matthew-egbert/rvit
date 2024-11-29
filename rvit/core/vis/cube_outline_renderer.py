#from rvit.core.vis.simple_renderer_3d import SimpleRenderer3D
from rvit.core.vis.simple_renderer import SimpleRenderer
from rvit.core.vis.components import *
from rvit.core.vis.data_sources import *
from kivy.graphics.opengl import *

import rvit.core.glsl_utils as glsl_utils

# import OpenGL
# OpenGL.ERROR_CHECKING = False
import OpenGL.GL as gl
from OpenGL.GL import glDisable, GL_DEPTH_TEST

#class CubeOutline(xyz_bounds,x_data,y_data,z_data,color1d_data,size_data,gradient,color):
class CubeOutline(xyz_bounds,color):
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
                             ],dtype=np.float32)

        self.cube_inds = [0,1,1,2,2,3,3,0,
                          4,5,5,6,6,7,7,4,
                          0,4,1,5,2,6,3,7]
        
        self.n_elements = 24
        self.data_to_shader = self.cube_xyz.ravel()


    def update(self):
        if self.format_has_changed :
            self.shader_substitutions['attributes'].append('attribute float x;')
            self.shader_substitutions['attributes'].append('attribute float y;')
            self.shader_substitutions['attributes'].append('attribute float z;')
            self.fmt.append( (b'x', 1, 'float') )
            self.fmt.append( (b'y', 1, 'float') )
            self.fmt.append( (b'z', 1, 'float') )

            self.loadShaders('lines')
            self.format_has_changed = False
            self.data_per_element = 3
            
            self.mesh.indices = self.cube_inds
            

        if self.enabled:
            #self.render_context.clear()
            super().update()
            if self.n_elements > 0:
                self.fbo.bind()
                self.fbo.clear_color = [0,0,0,0]
                self.fbo.clear_buffer()
                self.fbo.release()
                self.mesh.vertices = self.data_to_shader.ravel()
                self.render_context.ask_update()

    def loadShaders(self, mesh_mode, subs = {}):
        print('Loading shaders')
        ## generate the glsl code
        self.shaders = glsl_utils.loadShaders(self.shader_fn,
                                              {**subs,**self.shader_substitutions})

        ## set the meshes shaders to the generated glsl code
        self.render_context.shader.vs = self.shaders['vs']
        self.render_context.shader.fs = self.shaders['fs']

        # self.fbo.shader.vs = self.shaders['vs']
        # self.fbo.shader.fs = self.shaders['fs']

        if self.render_context.shader.success == False :
            print('Shader compilation failed')
            print(self.shaders['vs'])
            print(self.shaders['fs'])
            quit()

        # self.render_context['vmin'] = self.vmin
        # self.render_context['vmax'] = self.vmax
        # self.fbo['vmin'] = self.vmin
        # self.fbo['vmax'] = self.vmax

        ## replace any previous mesh with the new mesh
        if hasattr(self.render_context,'mesh'):
            self.render_context.remove(self.mesh)

        ######
        self.mesh = Mesh(mode=mesh_mode, fmt=self.fmt)
        self.render_context.add(self.mesh)
        print(self.render_context.children)

        # if hasattr(self,'cube_mesh'):
        #     self.render_context.remove(self.cube_mesh)

        # self.cube_mesh = Mesh(mode='lines', fmt=self.fmt)
        # self.cube_mesh.indices = self.cube_inds
        # self.cube_mesh.vertices = self.cube_xyz.flatten()
        # self.render_context.add(self.cube_mesh)

        self.format_has_changed = True

    def on_indices(self, inst, value):
        if value != '':
            v = ''.join(value)
            s = 'self.mesh_indices = self.simulation.%s' %(v)
            exec(s)

            self.format_has_changed = True


