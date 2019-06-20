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
from kivy.graphics import Mesh
#from kivy.uix.stencilview import StencilView
    
class ScalarTracker(xy_bounds):
    """
    takes a single scalar value data source and keeps
    track of its recent history.

    """

    num_samples = NumericProperty(100) #: history length in samples
    tracked_scalar = StringProperty('') #: variable which is to be tracked

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.on_num_samples(self,self.num_samples) # TODO: dispatch
        self._x = 0
        
    def registerConfigurableProperties(self):
        super().registerConfigurableProperties()
        self.addConfigurableProperty(ScalarTracker.num_samples)

    def on_num_samples(self, obj, value):
        self.num_samples = value
        self.data = np.zeros((int(self.num_samples*2), 2),dtype=np.float32)
        self.data[:self.num_samples,0] = np.linspace(0, 1.0, self.num_samples)
        self.data[self.num_samples:,0] = np.linspace(0, 1.0, self.num_samples)
        #self.data[self.num_samples,1]  = np.zeros(self.num_samples)
        # self.data[:, 0] = np.random.rand(self.num_samples)
        #self.data[:,1]  = np.random.rand(self.num_samples)
        k = self.num_samples
        tri_indices = np.array([(n, n+1, n+k,n+1, n+k+1, n+k) for n in range(0,self.num_samples)])
        self.tri_indices = tri_indices.ravel()[:-6]
        self.loadShaders()

    def on_tracked_scalar(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()
        
        self.scalar_data = value
        if self.scalar_data != '':
            self.get_value_command = 'self.scalar = self.simulation.%s' % (self.scalar_data)
            exec(self.get_value_command)
        self.loadShaders()

    def update(self):
        super().update()
        exec(self.get_value_command)
        self.data[self._x,1] = self.scalar
        self._x = (self._x + 1) % self.num_samples
        self.updateModelViewMatrix()

        if self.enabled:
            # self.curve_mesh.indices = np.arange(self.num_samples)
            # self.curve_mesh.vertices = self.data.ravel()

            self.fill_mesh.indices = self.tri_indices
            self.fill_mesh.vertices = self.data.ravel()
            self.render_context.ask_update()
            
    def loadShaders(self):
        ## generate the glsl code
        self.shaders = glsl_utils.loadShaders('graph_renderer.glsl',{})
        # # ## set the meshes shaders to the generated glsl code
        self.render_context.shader.vs = self.shaders['vs']
        self.render_context.shader.fs = self.shaders['fs']

        # ## replace any previous mesh with the new mesh
        # if hasattr(self,'curve_mesh'):
        #     self.render_context.remove(self.curve_mesh)
        # fmt =[(b'v_pos', 2, 'float')]
        # self.curve_mesh = Mesh(mode='line_strip', fmt=fmt)
        # self.render_context['color'] = [1.0,0.1,0.0,1.0]
        # self.render_context.add(self.curve_mesh)

        if hasattr(self,'fill_mesh'):
            self.render_context.remove(self.fill_mesh)
        fmt =[(b'v_pos', 2, 'float')]
        self.fill_mesh = Mesh(mode='triangles', fmt=fmt)
        self.render_context['color'] = [0.1,0.1,1.0,1.0]
        self.render_context.add(self.fill_mesh)

        
