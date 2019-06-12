import numpy as np
import os

from kivy.uix.widget import Widget
from kivy.clock import Clock

from kivy.graphics import *
from kivy.graphics.transformation import Matrix
from kivy.core.window import Window
from kivy.resources import resource_find
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, OptionProperty, ListProperty
from kivy.resources import resource_find, resource_add_path
from kivy.graphics.opengl import *

from rvit.core.vis.rvit_widget import RvitWidget
from rvit.core.configurable_property import ConfigurableProperty
from rvit.core.vis.components import *
import rvit.core.glsl_utils as glsl_utils

class PointRenderer(TwoDee,XData,YData,ColorData,SizeData):
    """The PointRenderer is used to display a scatter diagram of 2D points. 
    
    It can use a :class:`.SecondaryDataSource` to determine the color or size 
    of the displayed points.

    .. figure:: vis_examples/point_renderer.png
       :width: 300px
       
       A PointRenderer showing 50,000 points. A SecondaryDataSource is being 
       used to color the points by their position within a grid.

    The rvit configuration file used to make the figure image is the following:

    .. code-block:: python

       PointRenderer:
            pos_hint: {'x':0.0, 'y':0.0}
            size_hint:  (1.0,1.0)
            target_object: model.chemistry
            x_data: 'chemistry.pos[:,0]'
            y_data: 'chemistry.pos[:,1]'
            color_data: 'chemistry.zone'
            size_data: 'chemistry.pos[:,0]'
            show_controls: True
            point_size: 0.5
            xmin: 0
            ymin: 0
            xmax: 1
            ymax: 1
            color: [1.0,1.0,1.0,0.8]
            unique_name: 'pos' 
       
    """
    color = ListProperty([1.] * 4)
    point_size = NumericProperty(10.0)

    def __init__(self, *args, **kwargs):
        glEnable(0x8642)  # equivalend to glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        self.shader_fn = 'point_renderer.glsl'
        super().__init__(**kwargs)
        
        self.loadShaders()

    def registerConfigurableProperties(self):
        super().registerConfigurableProperties()
        self.addConfigurableProperty(PointRenderer.point_size)

    def update(self):
        if self.enabled:
            data = np.column_stack([self.xs.astype(np.float32),
                                    self.ys.astype(np.float32)])
            data = self.apply_preprocessing(data) ## TODO: preprocessing of various data sources
            N = int(np.ceil(np.size(data) / 2))
            data = data.reshape(N, 2)

            if hasattr(self,'colors'):
                parm_data = np.array(self.colors, dtype=np.float32).reshape(N, 1)
                ## TODO: preprocessing of various data sources
                # parm_data = self.apply_secondary_preprocessing(parm_data) 
                data = np.hstack([data, parm_data])
            if hasattr(self,'sizes'):
                parm_data = np.array(self.sizes, dtype=np.float32).reshape(N, 1)
                ## TODO: preprocessing of various data sources
                # parm_data = self.apply_secondary_preprocessing(parm_data)
                data = np.hstack([data, parm_data])
            
            if N > 0:
                self.mesh.indices = np.arange(N)
                self.mesh.vertices = data.ravel()
                self.render_context.ask_update()

    def inspect(self):
        inspection_dump_file = self.createInspectionDumpFile()
        np.save(open(inspection_dump_file, 'wb'), self.a)
        self.launchInspector(inspection_dump_file)

    def loadShaders(self):
        ## check which data streams are being used
        uses_color_data = hasattr(self,'colors')
        uses_size_data = hasattr(self,'sizes')

        ## generate the appropriate glsl code
        self.shaders = glsl_utils.loadShaders(self.shader_fn,
                                   {'point_size': 0.025 * self.point_size * min(Window.width, Window.height),
                                    'uses_color_data' : uses_color_data,
                                    'uses_size_data' : uses_size_data})
        self.render_context.shader.vs = self.shaders['vs']
        self.render_context.shader.fs = self.shaders['fs']

        ## create/reset a mesh with the appropriate format
        ## for the data that is streamed to the glsl code
        fmt = [(b'v_pos', 2, 'float'),]
        if uses_color_data:
            fmt.append( (b'colors', 1, 'float') )
        if uses_size_data:
            fmt.append( (b'sizes', 1, 'float') )

        if hasattr(self,'mesh'):
            self.render_context.remove(self.mesh)            
        self.mesh = Mesh(mode='points', fmt=fmt)
        self.render_context.add(self.mesh)

    def on_point_size(self, obj, value):
        # for a single points size (and to scale diverse point sizes)
        self.loadShaders()

    def on_color(self, obj, value):
        # for single color setting
        self.render_context['color'] = [float(v) for v in self.color]

    def on_size(self, inst, value):
        ## the point size is dynamically set in loadShaders in a way that
        ## responds to the overall window size. Accordingly this callback
        ## calls loadShaders (to allow response to window resizing).
        super().on_size(inst, value)
        self.loadShaders()

    def on_pos(self, inst, value):
        ## the point size is dynamically set in loadShaders in a way that
        ## responds to the overall window size. Accordingly this callback
        ## calls loadShaders (to allow response to window resizing).
        super().on_pos(inst, value)
        self.loadShaders()

# ### Local Variables: ###
# ### mode: python ###
# ### python-main-file: "main.py" ###
# ### python-working-dir: "../minimal_project/" ###
# ### End: ###
