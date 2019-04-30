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

from rvit_widget import RvitWidget, ConfigurableProperty, SecondaryDataSource
from kivy.graphics.opengl import *

from ..glsl_utils import loadShaders

import os
module_path = os.path.dirname(os.path.realpath(__file__))
resource_add_path(os.path.join(module_path, '../shaders/'))


class SpriteRenderer(SecondaryDataSource):
    color = ListProperty([1.] * 4)
    radius = NumericProperty(0.1)
    image = ObjectProperty()

    def __init__(self, *args, **kwargs):
        glEnable(0x8642)  # equivalend to glEnable(GL_VERTEX_PROGRAM_SPRITE_SIZE)
        super(SpriteRenderer, self).__init__(**kwargs)
        self.loadShaders()

        self.mesh = Mesh(mode='triangles', fmt=[(b'v_pos', 2, 'float'),
                                                (b'v_tc0', 2, 'float'), ])
        self.mesh.indices = [0, 1, 2, 0, 3, 2]
        self.mesh.vertices = [0.0, 0.0, 0.0, 0.0,
                              0.0, 1.0, 0.0, 1.0,
                              1.0, 1.0, 1.0, 1.0,
                              1.0, 0.0, 1.0, 0.0]

        self.render_context.add(self.mesh)

        self.updateModelViewMatrix()

    def registerConfigurableProperties(self):
        self.addConfigurableProperty(SpriteRenderer.radius)

    def update(self):
        if self.enabled:
            x, y, a = self.apply_preprocessing(self.a)
            r = self.radius
            self.mesh.vertices = [x - r * np.cos(a) - -r * np.sin(a), y - r * np.cos(a) + -r * np.sin(a), 0.0, 0.0,
                                  x - r * np.cos(a) - +r * np.sin(a), y + r *
                                  np.cos(a) + -r * np.sin(a), 0.0, 1.0,
                                  x + r * np.cos(a) - +r * np.sin(a), y + r *
                                  np.cos(a) + +r * np.sin(a), 1.0, 1.0,
                                  x + r * np.cos(a) - -r * np.sin(a), y - r * np.cos(a) + +r * np.sin(a), 1.0, 0.0]

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
        shaders = loadShaders('sprite_renderer.glsl', {})
        self.render_context.shader.vs = shaders['vs']
        self.render_context.shader.fs = shaders['fs']

    def on_point_size(self, obj, value):
        self.loadShaders()

    def on_size(self, inst, value):
        super(SpriteRenderer, self).on_size(inst, value)
        self.loadShaders()

    def on_pos(self, inst, value):
        super(SpriteRenderer, self).on_pos(inst, value)
        self.loadShaders()

    def on_color(self, obj, value):
        print('here', self.color)
        self.render_context['color'] = [float(v) for v in self.color]

    def on_image(self, obj, value):
        self.mesh.texture = value

# ### Local Variables: ###
# ### mode: python ###
# ### python-main-file: "main.py" ###
# ### python-working-dir: "../minimal_project/" ###
# ### End: ###
