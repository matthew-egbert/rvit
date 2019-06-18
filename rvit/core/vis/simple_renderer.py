from kivy.graphics import Mesh
from kivy.properties import ObjectProperty, StringProperty, NumericProperty,\
    OptionProperty, ListProperty

from rvit.core.vis.rvi_element import RVIElement
from rvit.core.configurable_property import ConfigurableProperty
from rvit.core.vis.components import *
from rvit.core.vis.data_streams import *
import rvit.core.glsl_utils as glsl_utils


class SimpleRenderer(RVIElement):
    color = ListProperty([1.] * 4)
    """a 4-tuple (red,green,blue,alpha) :: when the **color_data**
parameter is not provided, this property specifies the color for all
plotted points. When color_data is provided, the alpha value is still
used."""

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)        
        self.shader_fn = 'simple_renderer.glsl'
    
    def update(self):
        if self.format_has_changed :
            self.format_has_changed = False
            self.loadShaders()
            self.data_per_element = self.n_data_streams
            self.data_to_shader = np.zeros((self.n_elements,
                                            self.n_data_streams), dtype=np.float32)

        if self.enabled:
            super().update()
            if self.n_elements > 0:
                self.mesh.indices = np.arange(self.n_elements)
                self.mesh.vertices = self.data_to_shader.ravel()
                self.render_context.ask_update()

    def loadShaders(self, mesh_mode, subs = {}):
        ## generate the glsl code
        self.shaders = glsl_utils.loadShaders(self.shader_fn,
                                              {**subs,**self.shader_substitutions})
        ## set the meshes shaders to the generated glsl code
        self.render_context.shader.vs = self.shaders['vs']
        self.render_context.shader.fs = self.shaders['fs']

        ## replace any previous mesh with the new mesh
        if hasattr(self,'mesh'):
            self.render_context.remove(self.mesh)            
        self.mesh = Mesh(mode=mesh_mode, fmt=self.fmt)
        self.render_context.add(self.mesh)

    def on_color(self, obj, value):
        # for single color setting
        self.render_context['color'] = [float(v) for v in self.color]
