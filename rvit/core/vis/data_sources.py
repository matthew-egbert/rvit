
## DO NOT EDIT THIS FILE. It is automatically generated by generate_data_sources.py
## and any edits will be overwritten the next time that it is run.  

from rvit.core.vis.rvi_element import RVIElement
from kivy.properties import *
from kivy.app import App
import numpy as np



class x_data(RVIElement):
    """vector containing the x-values of data to be plotted.
    """

    x_data = StringProperty('') #: vector containing the x-values of data to be plotted.
    x_data_preprocess = StringProperty('') #: the preprocessor for x_data

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def on_x_data(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()
        
        self.x_data = value
        if self.x_data != '':
            s = 'self.xs = self.simulation.%s' % (self.x_data)
            exec(s)
            s = 'self.n_elements = len(self.xs)'
            exec(s)
            self.data_index_xs = self.n_data_sources
            self.n_data_sources += 1
        
        self.shader_substitutions['attributes'].append('attribute float x;')
        self.fmt.append( (b'x', 1, 'float') )
        self.format_has_changed = True

    def update(self):
        super().update()
        if hasattr(self,'xs'):
            data = np.array(self.xs, dtype=np.float32)#.reshape(N, 1)
            if hasattr(self,'preprocess_xs') :
                data = self.preprocess_xs(data)
            self.data_to_shader[:,self.data_index_xs] = data.ravel()

    def on_x_data_preprocess(self, obj, value):
        s = 'self.preprocess_xs = %s' % (value)
        exec(s)

    

class y_data(RVIElement):
    """vector containing the y-values of data to be plotted.
    """

    y_data = StringProperty('') #: vector containing the y-values of data to be plotted.
    y_data_preprocess = StringProperty('') #: the preprocessor for y_data

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def on_y_data(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()
        
        self.y_data = value
        if self.y_data != '':
            s = 'self.ys = self.simulation.%s' % (self.y_data)
            exec(s)
            s = 'self.n_elements = len(self.ys)'
            exec(s)
            self.data_index_ys = self.n_data_sources
            self.n_data_sources += 1
        
        self.shader_substitutions['attributes'].append('attribute float y;')
        self.fmt.append( (b'y', 1, 'float') )
        self.format_has_changed = True

    def update(self):
        super().update()
        if hasattr(self,'ys'):
            data = np.array(self.ys, dtype=np.float32)#.reshape(N, 1)
            if hasattr(self,'preprocess_ys') :
                data = self.preprocess_ys(data)
            self.data_to_shader[:,self.data_index_ys] = data.ravel()

    def on_y_data_preprocess(self, obj, value):
        s = 'self.preprocess_ys = %s' % (value)
        exec(s)

    

class color1d_data(RVIElement):
    """vector containing the colors of each plotted item.
    """

    color1d_data = StringProperty('') #: vector containing the colors of each plotted item.
    color1d_data_preprocess = StringProperty('') #: the preprocessor for color1d_data

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def on_color1d_data(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()
        
        self.color1d_data = value
        if self.color1d_data != '':
            s = 'self.colors = self.simulation.%s' % (self.color1d_data)
            exec(s)
            s = 'self.n_elements = len(self.colors)'
            exec(s)
            self.data_index_colors = self.n_data_sources
            self.n_data_sources += 1
        self.shader_substitutions['vertex_shader_functions'].append("""
// testing
""")
        self.color_dim = np.shape(np.shape((self.colors)[1]))
        self.shader_substitutions['attributes'].append('attribute float color1D;')
        self.fmt.append( (b'color1D', 1, 'float') )
        self.format_has_changed = True

    def update(self):
        super().update()
        if hasattr(self,'colors'):
            data = np.array(self.colors, dtype=np.float32)#.reshape(N, 1)
            if hasattr(self,'preprocess_colors') :
                data = self.preprocess_colors(data)
            self.data_to_shader[:,self.data_index_colors] = data.ravel()

    def on_color1d_data_preprocess(self, obj, value):
        s = 'self.preprocess_colors = %s' % (value)
        exec(s)

    

class size_data(RVIElement):
    """vector containing the sizes of each plotted item.
    """

    size_data = StringProperty('') #: vector containing the sizes of each plotted item.
    size_data_preprocess = StringProperty('') #: the preprocessor for size_data

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def on_size_data(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()
        
        self.size_data = value
        if self.size_data != '':
            s = 'self.sizes = self.simulation.%s' % (self.size_data)
            exec(s)
            s = 'self.n_elements = len(self.sizes)'
            exec(s)
            self.data_index_sizes = self.n_data_sources
            self.n_data_sources += 1
        
        self.shader_substitutions['attributes'].append('attribute float size;')
        self.fmt.append( (b'size', 1, 'float') )
        self.format_has_changed = True

    def update(self):
        super().update()
        if hasattr(self,'sizes'):
            data = np.array(self.sizes, dtype=np.float32)#.reshape(N, 1)
            if hasattr(self,'preprocess_sizes') :
                data = self.preprocess_sizes(data)
            self.data_to_shader[:,self.data_index_sizes] = data.ravel()

    def on_size_data_preprocess(self, obj, value):
        s = 'self.preprocess_sizes = %s' % (value)
        exec(s)

    