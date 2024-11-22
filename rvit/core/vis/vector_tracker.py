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
    
class VectorTracker(xy_bounds,color,gradient):
    """takes a vector data source and plots its current state. Here is an
    example usage.

    .. literalinclude :: ./code_examples/vector_tracker/main.py
        :language: python
        :caption: main.py

    .. literalinclude :: ./code_examples/vector_tracker/rvit.kv
        :language: python
        :caption: rvit.kv

    .. figure:: ./code_examples/vector_tracker/screenshot.png
        :width: 300px

    minimal example

    """

    y_vector = StringProperty('') #: variable which is to be tracked
    y_vector_preprocess = StringProperty('') #: the preprocessor 

        
    fill = OptionProperty('none', options=['none', 'columns', 'bars'])

    column_gap = NumericProperty(0.0)
    """when fill is `columns` or bars this specifies the gap between those
    drawn things. This is as a percentage of each column.

    """

    bar_thickness = NumericProperty(0.01)
    """when fill is `bars` this specifies the (vertical) thickness of the
    bars. Given as a percentage of the height of the visualizer

    """

    
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self._x = 0
        self.xmin = 0
        
    def registerConfigurableProperties(self):
        super().registerConfigurableProperties()
        self.addConfigurableProperty(VectorTracker.column_gap, rank = 5)
        self.addConfigurableProperty(VectorTracker.fill, rank = 5)
        self.addConfigurableProperty(color.color, rank = 50)
        
    def on_fill(self, obj, value):
        self.format_has_changed = True
        self.fill = value
        if self.fill == 'to top':            
            self.data[self.N:,1] = 1.0
        if self.fill == 'to bottom':
            self.data[self.N:,1] = 0.0
    
    def inspect(self):
        inspection_dump_file = self.createInspectionDumpFile()
        np.save(open(inspection_dump_file, 'wb'), self._y)        
        self.launchInspector(inspection_dump_file)

    def update(self):            
        self.clear_fbo()                
        if self.format_has_changed :
            self.loadShaders()            
            self.format_has_changed = False

            ## thick line, or area filled up or down
            if self.fill == 'none':
                self.N = len(self._y)
                self.data = np.zeros((int(self.N*2), 2),dtype=np.float32)
                self.data[:self.N,0] = np.linspace(0, 1.0, self.N)
                self.data[self.N:,0] = np.linspace(0, 1.0, self.N)
                k = self.N
                tri_indices = np.array([(n, n+1, n+k,n+1, n+k+1, n+k) for n in range(0,self.N)])
                self.tri_indices = tri_indices.ravel()[:-6]
            else:
                self.N = len(self._y)
                self.data = np.zeros((int(self.N*4), 2),dtype=np.float32)
                w = 1.0 / self.N # width of columns
                hw = w / 2
                column_gap = self.column_gap*2+1.0
                self.data[:self.N*2:2,0] = np.linspace(hw, 1.0-hw, self.N)-hw/column_gap
                self.data[self.N*2::2,0] = np.linspace(hw, 1.0-hw, self.N)-hw/column_gap
                self.data[1:self.N*2:2,0] = np.linspace(hw, 1.0-hw, self.N)+hw/column_gap
                self.data[1+self.N*2::2,0] = np.linspace(hw, 1.0-hw, self.N)+hw/column_gap
                k = self.N*2
                tri_indices = np.array([(n, n+1, n+k,
                                         n+1, n+k+1, n+k) for n in range(0,self.N*2,2)])
                self.tri_indices = tri_indices.ravel()[:]
            
            #self.loadShaders()
                
        exec(self.get_y_command)
        if hasattr(self,'preprocess') :
            self._y = self.preprocess(self._y)

        if self.fill == 'none':
            self.data[:len(self._y),1] = self._y
            self.data[len(self._y):,1] = self._y-0.01
        elif self.fill == 'columns' :
            self.data[:self.N*2:2,1] = self._y
            self.data[1:self.N*2:2,1] = self._y
            self.data[self.N*2::2,1] = self.ymin
            self.data[1+self.N*2::2,1] = self.ymin
        elif self.fill == 'bars':
            bar_thiccness = self.bar_thickness
            self.data[:self.N*2:2,1] = self._y + bar_thiccness
            self.data[1:self.N*2:2,1] = self._y + bar_thiccness
            self.data[self.N*2::2,1] = self._y - bar_thiccness
            self.data[1+self.N*2::2,1] = self._y - bar_thiccness
            
        self.data_minimum = self.data[:,1].min()
        self.data_maximum = self.data[:,1].max()        
        self.updateModelViewMatrix()

        if self.enabled:
            super().update()
            # self.curve_mesh.indices = np.arange(self.num_samples)
            # self.curve_mesh.vertices = self.data.ravel()

            self.fill_mesh.indices = self.tri_indices
            self.fill_mesh.vertices = self.data.ravel()
            self.render_context.ask_update()

    def loadShaders(self):
        ## generate the glsl code
        #self.shader_substitutions.update(args)
        self.shaders = glsl_utils.loadShaders('graph_renderer.glsl',self.shader_substitutions)
        
        # # ## set the meshes shaders to the generated glsl code
        self.render_context.shader.vs = self.shaders['vs']
        self.render_context.shader.fs = self.shaders['fs']

        ## replace any previous mesh with the new mesh
        if hasattr(self,'curve_mesh'):
            self.render_context.remove(self.curve_mesh)
        fmt =[(b'v_pos', 2, 'float')]
        self.curve_mesh = Mesh(mode='line_strip', fmt=fmt)
        #self.render_context['color'] = [1.0,0.1,0.0,1.0]
        self.render_context.add(self.curve_mesh)

        if hasattr(self,'fill_mesh'):
            self.render_context.remove(self.fill_mesh)
        fmt = [(b'v_pos', 2, 'float')]
            
        self.fill_mesh = Mesh(mode='triangles', fmt=fmt)
        self.render_context.add(self.fill_mesh)

        
    def on_y_vector(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()
        
        if value != '':
            self.get_y_command = 'self._y = self.simulation.%s' % (value)
            exec(self.get_y_command)
        self.loadShaders()

    def on_y_vector_preprocess(self, obj, value):
        s = 'self.preprocess = %s' % (value)
        exec(s)

        
    def on_column_gap(self, obj, value) :
        self.column_gap = value
        self.format_has_changed = True

