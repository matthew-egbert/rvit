import numpy as np
from kivy.uix.widget import Widget
from kivy.clock import Clock

from kivy.graphics import *
from kivy.graphics.transformation import Matrix
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.resources import resource_find
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, OptionProperty, ListProperty

from kivy.resources import resource_find, resource_add_path

from .rvit_widget import RvitWidget, ConfigurableProperty, ScaledValues, SecondaryDataSource

import rvit.core

import os
module_path = os.path.dirname(os.path.realpath(__file__))
resource_add_path(os.path.join(module_path, '../shaders/'))


class LineRenderer(SecondaryDataSource):
    color = ListProperty([1.0, 1.0, 1.0, 1.0])

    def __init__(self, *args, **kwargs):
        super(LineRenderer, self).__init__(**kwargs)

        self.render_context.shader.source = resource_find('line_renderer.glsl')
        self.mesh = Mesh(fmt=[(b'v_pos', 2, 'float'),
                              (b'v_parm', 1, 'float')])
        self.mesh.mode = 'lines'

        self.render_context.add(self.mesh)

        self.updateModelViewMatrix()

    def update(self):
        if self.enabled:
            N = np.shape(self.a)[0]
            pos_data = np.array(self.a, dtype=np.float32)
            pos_data = self.apply_preprocessing(pos_data)

            if self.secondary_varname != '':
                parm_data = np.array(self.b, dtype=np.float32).reshape(N, 1)
                parm_data = self.apply_secondary_preprocessing(parm_data)
            else:
                parm_data = np.ones(N, dtype=np.float32).reshape(N, 1)

            data = np.hstack([pos_data, parm_data])
            # print(np.shape(pos_data),np.shape(parm_data),np.shape(data))
            if N > 0:
                self.mesh.indices = range(N)
                self.mesh.vertices = data.ravel()  # self.a.flatten()
                self.render_context.ask_update()

    def setTarget(self):
        if self.target_object is not None and self.target_varname != '':
            s = 'self.a = self.target_object.%s' % (self.target_varname)
            exec(s)
            if isinstance(self.a, np.ndarray) and len(np.shape(self.a)) == 2:
                pass
                # self.colorfmt = ['ZERO_DEPTH_ARRAY?','luminance',
                #                  'luminance_alpha','rgb','rgba'][self.depth]
            else:
                print(np.shape(self.a), self.target_object, self.target_varname)
                raise TypeError('Target of Array Renderer must be a 2D numpy.ndarray')

    def inspect(self):
        inspection_dump_file = self.createInspectionDumpFile()
        np.save(open(inspection_dump_file, 'wb'), self.a)
        self.launchInspector(inspection_dump_file)

    def on_color(self, obj, value):
        self.render_context['color'] = [float(v) for v in value]


# ### Local Variables: ###
# ### mode: python ###
# ### python-main-file: "main.py" ###
# ### python-working-dir: "../minimal_project/" ###
# ### End: ###
