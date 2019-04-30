import numpy as np
from kivy.uix.widget import Widget
from kivy.clock import Clock

from kivy.graphics import *
from kivy.graphics.transformation import Matrix
from kivy.core.window import Window
from kivy.resources import resource_find
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, OptionProperty

from kivy.resources import resource_find, resource_add_path

from .rvit_widget import RvitWidget, ConfigurableProperty, ScaledValues

import os
module_path = os.path.dirname(os.path.realpath(__file__))
resource_add_path(os.path.join(module_path, '../shaders/'))


class BarChartRenderer(ScaledValues):

    def __init__(self, *args, **kwargs):
        super(BarChartRenderer, self).__init__(**kwargs)
        self.render_context.shader.source = resource_find('graph_renderer.glsl')

        self.mesh = Mesh(fmt=[('v_pos', 2, 'float')])
        self.mesh.mode = 'lines'
        self.N = 0
        self.render_context.add(self.mesh)
        self.updateModelViewMatrix()

        self.xmin = 0.0
        self.xmax = 1.0
        self.updateModelViewMatrix()

    def registerConfigurableProperties(self):
        super(BarChartRenderer, self).registerConfigurableProperties()
        self.removeConfigurableProperty(RvitWidget.xmin)
        self.removeConfigurableProperty(RvitWidget.xmax)
        self.removeConfigurableProperty(RvitWidget.ymin)
        self.removeConfigurableProperty(RvitWidget.ymax)

    def update(self):
        if self.enabled:
            if self.N > 0:
                a = self.apply_preprocessing(self.a)
                self.data[0::2, 1] = self.data[1::2, 1] = a

                self.updateModelViewMatrix()
                low = 0.0
                high = 1.0
                if self.minimum_value == 'auto':
                    low = self.data[:, 1].min()
                elif self.minimum_value == '-pi':
                    low = -np.pi
                else:
                    try:
                        low = float(self.minimum_value)
                    except BaseException:
                        low = 0.0
                if self.maximum_value == 'auto':
                    high = self.data[:, 1].max()
                elif self.maximum_value == 'pi':
                    high = np.pi
                else:
                    try:
                        high = float(self.maximum_value)
                    except BaseException:
                        high = 1.0
                self.ymin = float(low)
                self.ymax = float(high)
                self.cur_min_label.text = '%0.2f' % (self.ymin)
                self.cur_max_label.text = '%0.2f' % (self.ymax)

                self.mesh.vertices = self.data.flatten()
                self.render_context.ask_update()

    def setTarget(self):
        if self.target_object is not None and self.target_varname != '':
            s = 'self.a = self.target_object.%s' % (self.target_varname)
            exec(s)
            if True:  # isinstance(self.a,np.ndarray) and len(np.shape(self.a))==2 :
                self.N = np.shape(self.a)[0]
                self.data = np.zeros((self.N * 2, 2))
                self.data[::2, 0] = np.linspace(0, 1.0, self.N, endpoint=False)
                self.data[1:-1:2, 0] = self.data[2::2, 0]
                self.data[-1] = 1.0
                self.mesh.indices = np.arange(self.N * 2)
            else:
                print(np.shape(self.a), self.target_object, self.target_varname)
                raise TypeError('Target of Array Renderer must be a 2D numpy.ndarray')
        self.updateModelViewMatrix()  # THIS WAS MOVED FROM on_target_varname

    def inspect(self):
        inspection_dump_file = self.createInspectionDumpFile()
        np.save(open(inspection_dump_file, 'wb'), self.a)
        self.launchInspector(inspection_dump_file)


# ### Local Variables: ###
# ### mode: python ###
# ### python-main-file: "main.py" ###
# ### python-working-dir: "../minimal_project/" ###
# ### End: ###
