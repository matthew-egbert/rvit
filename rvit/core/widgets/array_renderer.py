import numpy as np
from kivy.uix.widget import Widget

from kivy.graphics import *
from kivy.graphics.transformation import Matrix
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.resources import resource_find
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, OptionProperty

from kivy.resources import resource_find, resource_add_path

from .rvit_widget import RvitWidget, ConfigurableProperty, ScaledValues

import os
module_path = os.path.dirname(os.path.realpath(__file__))
resource_add_path(os.path.join(module_path, '../shaders/'))


class ArrayRenderer(ScaledValues):
    mag_filter = OptionProperty('nearest', options=['nearest', 'linear'])
    coloring = OptionProperty('greys', options=['greys', 'red/black', 'rgb'])

    def __init__(self, *args, **kwargs):
        super(ArrayRenderer, self).__init__(**kwargs)

        self.render_context.shader.source = resource_find('array_renderer_greys.glsl')
        self.mesh = Mesh(mode='triangles', fmt=[(b'v_pos', 2, 'float'),
                                                (b'v_tc0', 2, 'float'), ])
        self.mesh.indices = [0, 1, 2, 0, 3, 2]
        self.mesh.vertices = [0.0, 0.0, 0.0, 0.0,
                              0.0, 1.0, 0.0, 1.0,
                              1.0, 1.0, 1.0, 1.0,
                              1.0, 0.0, 1.0, 0.0]
        self.render_context.add(self.mesh)
        self.canvas.before.add(self.render_context)

    def registerConfigurableProperties(self):
        self.addConfigurableProperty(ArrayRenderer.target_varname)
        self.addConfigurableProperty(ArrayRenderer.mag_filter)
        self.addConfigurableProperty(ArrayRenderer.coloring)

    def update(self):
        if self.enabled:
            data = np.array(np.ravel(self.a))
            low = 0.0
            high = 1.0
            if self.minimum_value == 'auto':
                low = data.min()
            if self.maximum_value == 'auto':
                high = data.max()
            data -= (low)
            if high - low != 0.0:
                data /= (high - low)

            self.texture.blit_buffer(data,
                                     colorfmt=self.colorfmt,
                                     bufferfmt='float')
            self.render_context.ask_update()

    def setTarget(self):
        if self.target_object is not None and self.target_varname != '':
            s = 'self.a = self.target_object.%s' % (self.target_varname)
            exec(s)
            if isinstance(self.a, np.ndarray) and len(np.shape(self.a)) == 3:
                self.array_width, self.array_height, self.depth = np.shape(self.a)[:]
                self.colorfmt = ['ZERO_DEPTH_ARRAY?', 'luminance',
                                 'luminance_alpha', 'rgb', 'rgba'][self.depth]
                self.texture = Texture.create(
                    size=(
                        self.array_width,
                        self.array_height),
                    bufferfmt='float')
                self.texture.blit_buffer(np.ravel(self.a),
                                         colorfmt=self.colorfmt,
                                         bufferfmt='float')
                self.render_context['texture0'] = self.texture.id
                self.render_context.add(BindTexture(texture=self.texture, index=self.texture.id,
                                                    colorfmt='rgba', mipmap=True))
            else:
                print(np.shape(self.a), self.target_object, self.target_varname)
                raise TypeError('Target of Array Renderer must be a 3D numpy.ndarray')

    def on_mag_filter(self, inst, value):
        self.texture.mag_filter = self.mag_filter

    def inspect(self):
        inspection_dump_file = self.createInspectionDumpFile()
        np.save(open(inspection_dump_file, 'wb'), self.a)
        self.launchInspector(inspection_dump_file)

    def on_coloring(self, inst, value):
        if value == 'greys':
            self.render_context.shader.source = resource_find('array_renderer_greys.glsl')
        elif value == 'red/black':
            self.render_context.shader.source = resource_find('array_renderer_redblack.glsl')

# ### Local Variables: ###
# ### mode: python ###
# ### python-main-file: "main.py" ###
# ### python-working-dir: "../minimal_project/" ###
# ### End: ###
