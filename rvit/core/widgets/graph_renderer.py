import numpy as np
from kivy.uix.widget import Widget
from kivy.clock import Clock

from kivy.graphics import *
from kivy.graphics.transformation import Matrix
from kivy.core.window import Window
from kivy.resources import resource_find
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, OptionProperty, ListProperty

from kivy.resources import resource_find, resource_add_path

from skivy_widget import SkivyWidget, ConfigurableProperty, ScaledValues
from kivy.graphics.opengl import *
import skivy

import os
module_path = os.path.dirname(os.path.realpath(__file__))
resource_add_path(os.path.join(module_path, '../shaders/'))


class GraphRenderer(ScaledValues):
    color = ListProperty([1.0, 1.0, 1.0, 1.0])

    def __init__(self, *args, **kwargs):
        super(GraphRenderer, self).__init__(**kwargs)
        self.render_context.shader.source = resource_find('graph_renderer.glsl')

        self.mesh = Mesh(fmt=[('v_pos', 2, 'float')])
        self.mesh.mode = 'lines'
        # glLineWidth(5.0);
        self.N = 0
        self.render_context.add(self.mesh)

        self.xmin = 0.0
        self.xmax = 1.0
        self.updateModelViewMatrix()

    def registerConfigurableProperties(self):
        super(GraphRenderer, self).registerConfigurableProperties()
        self.removeConfigurableProperty(SkivyWidget.xmin)
        self.removeConfigurableProperty(SkivyWidget.xmax)
        self.removeConfigurableProperty(SkivyWidget.ymin)
        self.removeConfigurableProperty(SkivyWidget.ymax)

    def update(self):
        if self.enabled:
            self.N = np.shape(self.a)[0]
            if self.N > 0:
                data = np.array(self.a, dtype=np.float32)
                #data[:,1] = np.linspace(0.5,2.0,self.N)
                try:
                    low = float(self.minimum_value)
                except ValueError:
                    low = 0.0
                try:
                    high = float(self.maximum_value)
                except ValueError:
                    high = 1.0
                if self.minimum_value == 'auto':
                    low = data[:, 1].min()
                if self.maximum_value == 'auto':
                    high = data[:, 1].max()
                self.ymin = float(low)
                self.ymax = float(high)

                self.mesh.vertices = data.flatten()
                self.updateModelViewMatrix()
                self.render_context.ask_update()

    def setTarget(self):
        if self.target_object is not None and self.target_varname != '':
            s = 'self.a = self.target_object.%s' % (self.target_varname)
            exec(s)
            if isinstance(self.a, np.ndarray) and len(np.shape(self.a)) == 2:
                self.N = np.shape(self.a)[0]
                self.mesh.indices = [int((x + 1.0) / 2) for x in xrange(2 * self.N - 2)]
            else:
                raise TypeError('Target of Array Renderer must be a 2D numpy.ndarray')
        self.updateModelViewMatrix()

    def inspect(self):
        inspection_dump_file = self.createInspectionDumpFile()
        np.save(open(inspection_dump_file, 'wb'), self.a)
        self.launchInspector(inspection_dump_file)

    def on_color(self, obj, value):
        print('there')
        print(value)
        self.render_context['color'] = [float(v) for v in value]
        print(self.render_context['color'])


class HistoryRenderer(GraphRenderer):
    num_samples = NumericProperty(1000)

    def __init__(self, *args, **kwargs):
        super(HistoryRenderer, self).__init__(**kwargs)
        self.current_sample = 0
        self.data = np.zeros((self.num_samples, 2))
        self.data[:, 0] = np.linspace(0.0, 1.0, self.num_samples)
        self.data[:, 1] = 0.0 * np.linspace(0.0, 1.0, self.num_samples)
        self.mesh.indices = [int((x + 1.0) / 2) for x in xrange(2 * self.num_samples - 2)]

    def update(self):
        if self.enabled:
            exec(self.get_value_command)  # puts the current value in self.a
            self.data[self.current_sample % self.num_samples, 1] = self.a
            self.current_sample += 1
            if self.num_samples > 0:
                try:
                    low = float(self.minimum_value)
                except ValueError:
                    low = 0.0
                try:
                    high = float(self.maximum_value)
                except ValueError:
                    high = 1.0
                if self.minimum_value == 'auto':
                    low = self.data[:, 1].min()
                if self.maximum_value == 'auto':
                    high = self.data[:, 1].max()
                self.ymin = float(low)
                self.ymax = float(high)
                self.cur_min_label.text = '%0.4f' % (self.ymin)
                self.cur_max_label.text = '%0.4f' % (self.ymax)
                #self.cur_min_label.text = self.ymin

                self.updateModelViewMatrix()
                self.mesh.vertices = self.data.flatten()
                self.render_context.ask_update()

    def setTarget(self):
        if self.target_object is not None and self.target_varname != '':
            self.get_value_command = 'self.a = self.target_object.%s' % (self.target_varname)
            exec(self.get_value_command)

    def on_num_samples(self, obj, value):
        self.num_samples = value
        self.data = np.zeros((self.num_samples, 2))
        self.data[:, 0] = np.linspace(0, 1, self.num_samples)
        # self.data[:,1] = np.linspace(0.0,1.0,self.num_samples)
        N = self.num_samples
        self.mesh.indices = [int((x + 1.0) / 2) for x in xrange(2 * N - 2)]
        #self.data[:,1] = np.linspace(0,1,self.num_samples)

    def inspect(self):
        inspection_dump_file = self.createInspectionDumpFile()
        np.save(open(inspection_dump_file, 'wb'), self.data)
        self.launchInspector(inspection_dump_file)


# ### Local Variables: ###
# ### mode: python ###
# ### python-main-file: "main.py" ###
# ### python-working-dir: "../minimal_project/" ###
# ### End: ###
