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

class Tracker2D(xy_bounds,color,gradient):
    """takes two scalar value data source and plots its
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

    x_scalar = StringProperty('') #: variable which is to be tracked
    x_scalar_preprocess = StringProperty('') #: the preprocessor
    y_scalar = StringProperty('') #: variable which is to be tracked
    y_scalar_preprocess = StringProperty('') #: the preprocessor

    num_samples = NumericProperty(255) #: history length in samples
    #fill = OptionProperty('none', options=['none', 'to bottom', 'to top'])

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.on_num_samples(self,self.num_samples) # TODO: dispatch
        self._index = 0

    def registerConfigurableProperties(self):
        super().registerConfigurableProperties()
        self.addConfigurableProperty(Tracker2D.num_samples,rank = 5)
        self.addConfigurableProperty(Tracker2D.line_width, rank = 5)
        #self.addConfigurableProperty(Tracker2D.fill, rank = 5)
        self.addConfigurableProperty(color.color, rank = 50)

    def on_num_samples(self, obj, value):
        self.N = int(value)
        self._index = 0
        self.data = np.zeros((self.N, 2),dtype=np.float32)        

        self.indices = range(self.N)        
        # self.indices = np.zeros(self.N*2, dtype=np.uint32)
        # for i in range(2,self.N*2,2):
        #     self.indices[i-1] = i //2            
        #     self.indices[i] = i //2
        # self.indices[-1] = self.N

        self.loadShaders()

    def on_x_scalar(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()
        if value != '':
            self.get_x_command = 'self._x = self.simulation.%s' % (value)
            exec(self.get_x_command)
        if hasattr(self,'preprocess_x') :
            self._x = self.preprocess_x(self._x)
        self.loadShaders()

    def on_x_scalar_preprocess(self, obj, value):
        s = 'self.preprocess_x = %s' % (value)
        exec(s)

    def on_y_scalar(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()
        if value != '':
            self.get_y_command = 'self._y = self.simulation.%s' % (value)
            exec(self.get_y_command)
        if hasattr(self,'preprocess') :
            self._y = self.preprocess_y(self._y)
        self.loadShaders()

    def on_y_scalar_preprocess(self, obj, value):
        s = 'self.preprocess_y = %s' % (value)
        exec(s)

    def update(self):
        super().update()
        self._index = (self._index + 1) % self.N

        if hasattr(self,'get_x_command'):
            exec(self.get_x_command)
        else:
            raise Exception('No x_scalar has been specified or there was an error in loading it.')
        if hasattr(self,'get_y_command'):
            exec(self.get_y_command)
        else:
            raise Exception('No y_scalar has been specified or there was an error in loading it.')

        self.data[self._index,0] = self._x
        self.data[self._index,1] = self._y

        self.updateProjectionMatrix()
        self.updateModelViewMatrix()

        if self.enabled:            
            self.clear_fbo()
            self.mesh.indices = self.indices
            self.mesh.vertices = self.data.ravel()
            self.render_context.ask_update()


    def loadShaders(self):
        ## generate the glsl code
        self.shaders = glsl_utils.loadShaders('tracker2d.glsl',self.shader_substitutions)

        # # ## set the meshes shaders to the generated glsl code
        self.render_context.shader.vs = self.shaders['vs']
        self.render_context.shader.fs = self.shaders['fs']        

        if self.render_context.shader.success == False :
            print('Shader compilation failed')
            print(self.shaders['vs'])
            print(self.shaders['fs'])
            quit()

        ## replace any previous mesh with the new mesh
        if hasattr(self,'mesh'):            
            self.render_context.remove(self.mesh)
        fmt =[(b'v_pos', 2, 'float')]
        self.mesh = Mesh(mode='points', fmt=fmt)        
        self.render_context.add(self.mesh)



