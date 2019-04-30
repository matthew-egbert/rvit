import numpy as np
from kivy.uix.widget import Widget
from kivy.clock import Clock

from kivy.graphics import *
from kivy.graphics.transformation import Matrix
from kivy.core.window import Window
from kivy.resources import resource_find
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, OptionProperty, ListProperty

from kivy.resources import resource_find, resource_add_path

from .rvit_widget import RvitWidget, ConfigurableProperty, SecondaryDataSource, ScaledValues
from kivy.graphics.opengl import *

from ..glsl_utils import loadShaders

import os
module_path = os.path.dirname(os.path.realpath(__file__))
resource_add_path(os.path.join(module_path, '../shaders/'))
# resource_add_path(os.path.join(module_path,'../../hex/'))


class PointRenderer(ScaledValues, SecondaryDataSource):
    color = ListProperty([1.] * 4)
    point_size = NumericProperty(10.0)
    shader = StringProperty('')
    #shader = OptionProperty('NO SECONDARY',['NO EFFECT'])

    def __init__(self, *args, **kwargs):
        glEnable(0x8642)  # equivalend to glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        self.shader_fn = 'point_renderer.glsl'
        super(PointRenderer, self).__init__(**kwargs)        
        self.loadShaders()

        self.mesh = Mesh(mode='points', fmt=[(b'v_pos', 2, 'float'),
                                             (b'parm', 1, 'float')])  # ,pointsize=1000)
        self.render_context.add(self.mesh)

        self.updateModelViewMatrix()

    def registerConfigurableProperties(self):
        super(PointRenderer, self).registerConfigurableProperties()
        self.addConfigurableProperty(PointRenderer.point_size)

    def update(self):
        if self.enabled:
            pos_data = np.array(self.a, dtype=np.float32)
            pos_data = self.apply_preprocessing(pos_data)
            N = np.size(pos_data) / 2
            pos_data = pos_data.reshape(N, 2)

            if self.secondary_varname != '':
                parm_data = np.array(self.b, dtype=np.float32).reshape(N, 1)
                parm_data = self.apply_secondary_preprocessing(parm_data)
            else:
                parm_data = np.ones(N, dtype=np.float32).reshape(N, 1)
            data = np.hstack([pos_data, parm_data])
            if N > 0:
                self.mesh.indices = np.arange(N)  # ,dtype=np.float32)
                self.mesh.vertices = data.ravel()  # should be ravel for efficiency?
                self.render_context.ask_update()

    def setTarget(self):
        if self.target_object is not None and self.target_varname != '':
            s = 'self.a = self.target_object.%s' % (self.target_varname)
            exec(s)
            # if isinstance(self.a,np.ndarray) and len(np.shape(self.a))==2 :
            #     pass
            #     # self.colorfmt = ['ZERO_DEPTH_ARRAY?','luminance',
            #     #                  'luminance_alpha','rgb','rgba'][self.depth]
            # else :
            #     print(np.shape(self.a),self.target_object,self.target_varname)
            #     raise TypeError('Target of Array Renderer must be a 2D numpy.ndarray')

    def inspect(self):
        inspection_dump_file = self.createInspectionDumpFile()
        np.save(open(inspection_dump_file, 'wb'), self.a)
        self.launchInspector(inspection_dump_file)

    def loadShaders(self):
        self.shaders = loadShaders(self.shader_fn,
                                   {'point_size': 0.025 * self.point_size *
                                    min(Window.width, Window.height)})
        self.render_context.shader.vs = self.shaders['vs']
        self.render_context.shader.fs = self.shaders['fs']

    def on_point_size(self, obj, value):
        self.loadShaders()

    def on_size(self, inst, value):
        super(PointRenderer, self).on_size(inst, value)
        self.loadShaders()

    def on_pos(self, inst, value):
        super(PointRenderer, self).on_pos(inst, value)
        self.loadShaders()

    def on_color(self, obj, value):
        print('on_color')
        self.render_context['color'] = [float(v) for v in self.color]

    def on_shader(self, obj, glsl_fn):
        self.shader_fn = glsl_fn
        self.loadShaders()

# ### Local Variables: ###
# ### mode: python ###
# ### python-main-file: "main.py" ###
# ### python-working-dir: "../minimal_project/" ###
# ### End: ###
