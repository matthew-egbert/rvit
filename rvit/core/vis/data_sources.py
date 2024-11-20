
## DO NOT EDIT THIS FILE. It is automatically generated by generate_data_sources.py
## and any edits will be overwritten the next time that it is run.  

from rvit.core.vis.rvi_visualizer import RVIVisualizer,DataTargettingProperty
from kivy.properties import *
from kivy.app import App
import numpy as np


class x_data(RVIVisualizer):
    """vector containing the x-values of data to be plotted.
    """

    x_data = DataTargettingProperty('') #: vector containing the x-values of data to be plotted.
    x_data_preprocess = StringProperty('') #: the preprocessor for x_data

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def on_x_data(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()
        
        x_data = value
        if x_data != '':
            ## old 'pointer' solution
            # s = 'self.xs = self.simulation.%s' % (x_data)
            # exec(s)
            # s = 'self.n_elements = len(np.ravel(self.xs))'
            # exec(s)

            ## new get-data-function solution
            if not hasattr(self,'simulation'):
                self.simulation = App.get_running_app().get_simulation()        
            self.get_xs_command = f'self.xs = self.simulation.{value}; self.n_elements = len(np.ravel(self.xs))'

            ## the following line should be run every time the data should be
            ## fetched from its source; each time it is called, it populates the variables
            ##    self.xs
            ##    self.n_elements
            exec(self.get_xs_command)
            

            self.data_index_xs = self.n_data_sources
            self.n_data_sources += 1
        
        self.shader_substitutions['attributes'].append('attribute float x;')
        self.fmt.append( (b'x', 1, 'float') )
        self.format_has_changed = True

    def update(self):
        super().update()
        if hasattr(self,'xs'):
            ## gets data from source and puts it in self.xs
            exec(self.get_xs_command)
            data = np.repeat(
                np.array(self.xs, dtype=np.float32),
                self.vertices_per_datum)
            if hasattr(self,'preprocess_xs') :
                data = self.preprocess_xs(data)
            self.data_to_shader[:,self.data_index_xs] = data.ravel()

    def on_x_data_preprocess(self, obj, value):
        s = 'self.preprocess_xs = %s' % (value)
        exec(s)
    
class y_data(RVIVisualizer):
    """vector containing the y-values of data to be plotted.
    """

    y_data = DataTargettingProperty('') #: vector containing the y-values of data to be plotted.
    y_data_preprocess = StringProperty('') #: the preprocessor for y_data

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def on_y_data(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()
        
        y_data = value
        if y_data != '':
            ## old 'pointer' solution
            # s = 'self.ys = self.simulation.%s' % (y_data)
            # exec(s)
            # s = 'self.n_elements = len(np.ravel(self.ys))'
            # exec(s)

            ## new get-data-function solution
            if not hasattr(self,'simulation'):
                self.simulation = App.get_running_app().get_simulation()        
            self.get_ys_command = f'self.ys = self.simulation.{value}; self.n_elements = len(np.ravel(self.ys))'

            ## the following line should be run every time the data should be
            ## fetched from its source; each time it is called, it populates the variables
            ##    self.ys
            ##    self.n_elements
            exec(self.get_ys_command)
            

            self.data_index_ys = self.n_data_sources
            self.n_data_sources += 1
        
        self.shader_substitutions['attributes'].append('attribute float y;')
        self.fmt.append( (b'y', 1, 'float') )
        self.format_has_changed = True

    def update(self):
        super().update()
        if hasattr(self,'ys'):
            ## gets data from source and puts it in self.ys
            exec(self.get_ys_command)
            data = np.repeat(
                np.array(self.ys, dtype=np.float32),
                self.vertices_per_datum)
            if hasattr(self,'preprocess_ys') :
                data = self.preprocess_ys(data)
            self.data_to_shader[:,self.data_index_ys] = data.ravel()

    def on_y_data_preprocess(self, obj, value):
        s = 'self.preprocess_ys = %s' % (value)
        exec(s)


class z_data(RVIVisualizer):
    """vector containing the z-values of data to be plotted.
    """

    z_data = DataTargettingProperty('') #: vector containing the z-values of data to be plotted.
    z_data_preprocess = StringProperty('') #: the preprocessor for z_data

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def on_z_data(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()
        
        z_data = value
        if z_data != '':
            ## old 'pointer' solution
            # s = 'self.zs = self.simulation.%s' % (z_data)
            # exec(s)
            # s = 'self.n_elements = len(np.ravel(self.zs))'
            # exec(s)

            ## new get-data-function solution
            if not hasattr(self,'simulation'):
                self.simulation = App.get_running_app().get_simulation()        
            self.get_zs_command = f'self.zs = self.simulation.{value}; self.n_elements = len(np.ravel(self.zs))'

            ## the following line should be run every time the data should be
            ## fetched from its source; each time it is called, it populates the variables
            ##    self.zs
            ##    self.n_elements
            exec(self.get_zs_command)
            

            self.data_index_zs = self.n_data_sources
            self.n_data_sources += 1
        
        self.shader_substitutions['attributes'].append('attribute float z;')
        self.fmt.append( (b'z', 1, 'float') )        
        self.format_has_changed = True

    def update(self):
        super().update()
        if hasattr(self,'zs'):
            ## gets data from source and puts it in self.zs
            exec(self.get_zs_command)
            data = np.repeat(
                np.array(self.zs, dtype=np.float32),
                self.vertices_per_datum)
            if hasattr(self,'preprocess_zs') :
                data = self.preprocess_zs(data)
            self.data_to_shader[:,self.data_index_zs] = data.ravel()

    def on_z_data_preprocess(self, obj, value):
        s = 'self.preprocess_zs = %s' % (value)
        exec(s)
        
class rot_data(RVIVisualizer):
    """vector containing the way each datum is to be rotated (in radians)
    """

    rot_data = DataTargettingProperty('') #: vector containing the way each datum is to be rotated (in radians)
    rot_data_preprocess = StringProperty('') #: the preprocessor for rot_data

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def on_rot_data(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()
        
        rot_data = value
        if rot_data != '':
            ## old 'pointer' solution
            # s = 'self.rots = self.simulation.%s' % (rot_data)
            # exec(s)
            # s = 'self.n_elements = len(np.ravel(self.rots))'
            # exec(s)

            ## new get-data-function solution
            if not hasattr(self,'simulation'):
                self.simulation = App.get_running_app().get_simulation()        
            self.get_rots_command = f'self.rots = self.simulation.{value}; self.n_elements = len(np.ravel(self.rots))'

            ## the following line should be run every time the data should be
            ## fetched from its source; each time it is called, it populates the variables
            ##    self.rots
            ##    self.n_elements
            exec(self.get_rots_command)
            

            self.data_index_rots = self.n_data_sources
            self.n_data_sources += 1
        
        self.shader_substitutions['attributes'].append('attribute float rot;')
        self.fmt.append( (b'rot', 1, 'float') )
        self.format_has_changed = True

    def update(self):
        super().update()
        if hasattr(self,'rots'):
            ## gets data from source and puts it in self.rots
            exec(self.get_rots_command)
            data = np.repeat(
                np.array(self.rots, dtype=np.float32),
                self.vertices_per_datum)
            if hasattr(self,'preprocess_rots') :
                data = self.preprocess_rots(data)
            self.data_to_shader[:,self.data_index_rots] = data.ravel()

    def on_rot_data_preprocess(self, obj, value):
        s = 'self.preprocess_rots = %s' % (value)
        exec(s)
    
class color1d_data(RVIVisualizer):
    """vector containing the colors of each plotted item.
    """

    color1d_data = DataTargettingProperty('') #: vector containing the colors of each plotted item.
    color1d_data_preprocess = StringProperty('') #: the preprocessor for color1d_data

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def on_color1d_data(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()
        
        color1d_data = value
        if color1d_data != '':
            ## old 'pointer' solution
            # s = 'self.colors = self.simulation.%s' % (color1d_data)
            # exec(s)
            # s = 'self.n_elements = len(np.ravel(self.colors))'
            # exec(s)

            # hohee
            ## new get-data-function solution
            if not hasattr(self,'simulation'):
                self.simulation = App.get_running_app().get_simulation()        
            self.get_colors_command = f'self.colors = self.simulation.{value}; self.n_elements = len(np.ravel(self.colors))'

            ## the following line should be run every time the data should be
            ## fetched from its source; each time it is called, it populates the variables
            ##    self.colors
            ##    self.n_elements
            exec(self.get_colors_command)
            

            self.data_index_colors = self.n_data_sources
            self.n_data_sources += 1
        self.shader_substitutions['vertex_shader_functions'].append("""
// testing
""")
        self.color_dim = 1
        self.shader_substitutions['attributes'].append('attribute float color1D;')
        self.fmt.append( (b'color1D', 1, 'float') )
        self.format_has_changed = True

    def update(self):
        super().update()
        if hasattr(self,'colors'):
            ## gets data from source and puts it in self.colors
            exec(self.get_colors_command)
            data = np.repeat(
                np.array(self.colors, dtype=np.float32),
                self.vertices_per_datum)
            if hasattr(self,'preprocess_colors') :
                data = self.preprocess_colors(data)
            self.data_to_shader[:,self.data_index_colors] = data.ravel()

    def on_color1d_data_preprocess(self, obj, value):
        s = 'self.preprocess_colors = %s' % (value)
        exec(s)
    
class size_data(RVIVisualizer):
    """vector containing the sizes of each plotted item.
    """

    size_data = DataTargettingProperty('') #: vector containing the sizes of each plotted item.
    size_data_preprocess = StringProperty('') #: the preprocessor for size_data

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def on_size_data(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()
        
        size_data = value
        if size_data != '':
            ## old 'pointer' solution
            # s = 'self.sizes = self.simulation.%s' % (size_data)
            # exec(s)
            # s = 'self.n_elements = len(np.ravel(self.sizes))'
            # exec(s)

            ## new get-data-function solution
            if not hasattr(self,'simulation'):
                self.simulation = App.get_running_app().get_simulation()        
            self.get_sizes_command = f'self.sizes = self.simulation.{value}; self.n_elements = len(np.ravel(self.sizes))'

            ## the following line should be run every time the data should be
            ## fetched from its source; each time it is called, it populates the variables
            ##    self.sizes
            ##    self.n_elements
            exec(self.get_sizes_command)
            

            self.data_index_sizes = self.n_data_sources
            self.n_data_sources += 1
        
        self.shader_substitutions['attributes'].append('attribute float size;')
        self.fmt.append( (b'size', 1, 'float') )
        self.format_has_changed = True

    def update(self):
        super().update()
        if hasattr(self,'sizes'):
            ## gets data from source and puts it in self.sizes
            exec(self.get_sizes_command)
            data = np.repeat(
                np.array(self.sizes, dtype=np.float32),
                self.vertices_per_datum)
            if hasattr(self,'preprocess_sizes') :
                data = self.preprocess_sizes(data)
            self.data_to_shader[:,self.data_index_sizes] = data.ravel()

    def on_size_data_preprocess(self, obj, value):
        s = 'self.preprocess_sizes = %s' % (value)
        exec(s)
    
