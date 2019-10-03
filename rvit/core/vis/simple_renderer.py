from kivy.graphics import Mesh
from kivy.properties import ObjectProperty, StringProperty, NumericProperty,\
    OptionProperty, ListProperty

from rvit.core.vis.rvi_element import RVIElement
from rvit.core.configurable_property import ConfigurableProperty
from rvit.core.vis.components import *
from rvit.core.vis.data_sources import *
import rvit.core.glsl_utils as glsl_utils


class SimpleRenderer(xy_bounds):
    indices = ListProperty([])
    
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        if 'shader_fn' not in kwargs:
            shader_fn = 'simple_renderer.glsl'
        self.shader_fn = shader_fn

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
        #self.shaders = glsl_utils.loadShaders(self.shader_fn,self.shader_substitutions)
        ## set the meshes shaders to the generated glsl code
        self.render_context.shader.vs = self.shaders['vs']
        self.render_context.shader.fs = self.shaders['fs']

        ## replace any previous mesh with the new mesh
        if hasattr(self,'mesh'):
            self.render_context.remove(self.mesh)            
        self.mesh = Mesh(mode=mesh_mode, fmt=self.fmt)
        self.render_context.add(self.mesh)
        self.format_has_changed = True

    def on_indices(self, inst, value):
        if value != '':
            v = ''.join(value)
            s = 'self.mesh_indices = self.simulation.%s' %(v)
            print(s)
            exec(s)

            # self.mesh_indices = s
            self.format_has_changed = True
