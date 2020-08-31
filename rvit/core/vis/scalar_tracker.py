import numpy as np

from kivy.graphics.transformation import Matrix
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty, NumericProperty,\
    OptionProperty, ListProperty
from kivy.graphics.opengl import *

from rvit.core.configurable_property import ConfigurableProperty
import rvit.core.glsl_utils as glsl_utils

from rvit.core.vis.simple_renderer import SimpleRenderer
from rvit.core.vis.components import *
from rvit.core.vis.data_sources import *
from kivy.graphics import Mesh
    
class ScalarTracker(xy_bounds,color,gradient):
    """takes a single scalar value data source and plots its
    recent history. Here is an example usage. 

    .. literalinclude :: ./code_examples/scalar_tracker/main.py
        :language: python
        :caption: main.py

    .. literalinclude :: ./code_examples/scalar_tracker/rvit.kv
        :language: python
        :caption: rvit.kv

    .. figure:: ./code_examples/scalar_tracker/screenshot.png
        :width: 300px

    minimal example

    """
    line_width = NumericProperty(0.02)
    """when fill is `none` this specifies the width of the drawn curve as
    a fraction of the visualizer's height
    """

    y_scalar = StringProperty('') #: variable which is to be tracked
    y_scalar_preprocess = StringProperty('') #: the preprocessor 
    
    num_samples = NumericProperty(255) #: history length in samples
    fill = OptionProperty('none', options=['none', 'to bottom', 'to top'])

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.on_num_samples(self,self.num_samples) # TODO: dispatch
        self._x = 0
        self.xmin = 0
        
    def registerConfigurableProperties(self):
        super().registerConfigurableProperties()
        self.addConfigurableProperty(ScalarTracker.num_samples,rank = 5)
        self.addConfigurableProperty(ScalarTracker.line_width, rank = 5)
        self.addConfigurableProperty(ScalarTracker.fill, rank = 5)
        self.addConfigurableProperty(color.color, rank = 50)
        
    def on_num_samples(self, obj, value):
        #self.num_samples = value
        self.N = int(value)        
        print(self.N)
        self._x = 0
        self.data = np.zeros((int(self.N*2), 2),dtype=np.float32)
        self.data[:self.N,0] = np.linspace(0, 1.0, self.N)
        self.data[self.N:,0] = np.linspace(0, 1.0, self.N)
        k = self.N
        tri_indices = np.array([(n, n+1, n+k,n+1, n+k+1, n+k) for n in range(0,self.N)])
        self.tri_indices = tri_indices.ravel()[:-6]
        self.loadShaders()

    def on_fill(self, obj, value):
        self.fill = value
        if self.fill == 'to top':            
            self.data[self.N:,1] = 1.0
        if self.fill == 'to bottom':
            self.data[self.N:,1] = 0.0

    def on_y_scalar(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()
        
        # self.scalar_data = value
        if value != '':
            self.get_y_command = 'self._y = self.simulation.%s' % (value)
            exec(self.get_y_command)
        if hasattr(self,'preprocess') :
            self._y = self.preprocess(self._y)

        self.loadShaders()

    def on_y_scalar_preprocess(self, obj, value):
        s = 'self.preprocess = %s' % (value)
        exec(s)

        
    def update(self):
        super().update()
        if hasattr(self,'get_y_command'):            
            exec(self.get_y_command)
        else:
            raise Exception('No y_scalar has been specified or there was an error in loading it.')
        if self.fill == 'none':
            r = (self.ymax-self.ymin)*self.line_width/2
            self.data[self._x,1] = self._y - r
            self.data[self._x+self.N,1] = self._y + r
        else :
            self.data[self._x,1] = self._y
            
        self.data_minimum = self.data[:,1].min()
        self.data_maximum = self.data[:,1].max()

        self._x = (self._x + 1) % self.N
        self.updateModelViewMatrix()

        if self.enabled:
            self.curve_mesh.indices = np.arange(self.num_samples)
            self.curve_mesh.vertices = self.data.ravel()

            self.fill_mesh.indices = self.tri_indices
            self.fill_mesh.vertices = self.data.ravel()
            self.render_context.ask_update()

    def loadShaders(self):
        ## generate the glsl code
        #self.shader_substitutions.update(args)
        # print('scalar tracker subs')
        # print(self.shader_substitutions)
    
        self.shaders = glsl_utils.loadShaders('graph_renderer.glsl',self.shader_substitutions)
        
        # # ## set the meshes shaders to the generated glsl code
        self.render_context.shader.vs = self.shaders['vs']
        self.render_context.shader.fs = self.shaders['fs']

        ## replace any previous mesh with the new mesh
        if hasattr(self,'curve_mesh'):
            self.render_context.remove(self.curve_mesh)
        fmt =[(b'v_pos', 2, 'float')]
        self.curve_mesh = Mesh(mode='line_strip', fmt=fmt)
        self.render_context['color'] = [1.0,0.1,0.0,1.0]
        self.render_context.add(self.curve_mesh)

        if hasattr(self,'fill_mesh'):
            self.render_context.remove(self.fill_mesh)
        fmt = [(b'v_pos', 2, 'float')]
            
        self.fill_mesh = Mesh(mode='triangles', fmt=fmt)
        self.render_context.add(self.fill_mesh)

        
