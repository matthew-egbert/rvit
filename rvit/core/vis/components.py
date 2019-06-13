from .rvit_widget import RvitWidget
from kivy.properties import *
from kivy.graphics.transformation import Matrix
from kivy.core.window import Window
import rvit.core
import re
import numpy as np

class TwoDee(RvitWidget):
    """Provides four configurable parameters that determine the limits of a 2D display.
    """
    
    xmin = NumericProperty(-1.) #: x-coord of left border 
    xmax = NumericProperty(1.)  #: x-coord of right border 
    ymin = NumericProperty(-1.) #: x-coord of bottom border 
    ymax = NumericProperty(1.)  #: x-coord of top border 

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.updateModelViewMatrix()
        
    def registerConfigurableProperties(self):
        super().registerConfigurableProperties()
        self.addConfigurableProperty(TwoDee.xmin)
        self.addConfigurableProperty(TwoDee.xmax)
        self.addConfigurableProperty(TwoDee.ymin)
        self.addConfigurableProperty(TwoDee.ymax)

    def updateProjectionMatrices(self):
        w = float(Window.width)
        h = float(Window.height)
        m = Matrix().identity()
        p = rvit.core.BUTTON_BORDER_HEIGHT
        m.scale(2.0 * self.width / w,
                2.0 * (self.height - p) / h, 1.0)
        m.translate(-1.0 + (self.pos[0]) * 2.0 / w,
                    -1.0 + (self.pos[1]) * 2.0 / h,
                    0.0)
        self.render_context['projection_mat'] = m

    def updateModelViewMatrix(self):
        m = Matrix().identity()
        hr = max(0.00001, (self.xmax - self.xmin))
        vr = max(0.00001, (self.ymax - self.ymin))
        m.scale(1.0 / hr,
                1.0 / vr,
                1.0)
        m.translate(-self.xmin / hr,
                    -self.ymin / vr,
                    0.0)
        self.render_context['modelview_mat'] = m

    def on_size(self, inst, value):
        self.updateProjectionMatrices()

    def on_pos(self, inst, value):
        self.updateProjectionMatrices()        
        
    def on_xmin(self, obj, value):
        self.updateModelViewMatrix()

    def on_xmax(self, obj, value):
        self.updateModelViewMatrix()

    def on_ymin(self, obj, value):
        self.updateModelViewMatrix()

    def on_ymax(self, obj, value):
        self.updateModelViewMatrix()

# class ColorMap(RvitWidget):
#     colormap = NumericProperty(-1.) #: x-coord of left border 

#     def __init__(self, *args, **kwargs):
#         super().__init__(**kwargs)

#     def registerConfigurableProperties(self):
#         super().registerConfigurableProperties()
#         self.addConfigurableProperty(ColorMap.colormap)
        
#     def on_colormap(self, obj, value):
#         pass
        

def generateViewAssigner(component_name,
                         property_name,
                         variable_name,
                         docstring):
    """ A factory for generating data-view components. 

    component_name: the name of the component object, e.g.: ColorData
    property_name: what is specified in the rvit.kv file e.g. color_data
    variable_name: how to reference the view from inside the vis e.g. colors
    """

    s = """
class {{component_name}}(RvitWidget):
    '''"""+docstring+"""

    '''

    {{property_name}} = StringProperty('')
    {{property_name}}_preprocess = StringProperty('')
    

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def on_{{property_name}}(self, obj, value):
        self.{{property_name}} = value
        if self.target_object is not None and self.{{property_name}} != '':
            s = 'self.{{variable_name}} = self.target_object.%s' % (self.{{property_name}})
            exec(s)

    def on_{{property_name}}_preprocess(self, obj, value):
        # self.preprocess_fn = value
        s = 'self.preprocess_{{variable_name}} = %s' % (value)
        exec(s)

"""
    s = s.replace('{{component_name}}',component_name)
    s = s.replace('{{property_name}}',property_name)
    s = s.replace('{{variable_name}}',variable_name)
    return(s)

s = generateViewAssigner('XData', 
                         'x_data',
                         'xs','''
    Specifies a vector that contains the x-values of data to be plotted.
    ''') 
exec(s)
print(s)

s = generateViewAssigner('YData', 
                         'y_data',
                         'ys','''
    Specifies a vector that contains the x-values of data to be plotted.
    ''') 
exec(s)
    
s = generateViewAssigner('ColorData', 
                         'color_data',
                         'colors','''
    Specifies a vector that determines the color of each plotted element.
    ''')
print(s)
exec(s)

s = generateViewAssigner('SizeData', 
                         'size_data',
                         'sizes','''
    Specifies a vector that determines the size of each plotted element.
                         ''') 
exec(s)



# class SecondaryDataSource(RvitWidget):
#     """Specifies a """
#     secondary_varname = StringProperty('')

#     def __init__(self, *args, **kwargs):
#         super().__init__(**kwargs)

#     def on_secondary_varname(self, obj, value):
#         self.secondary_varname = value
#         if self.target_object is not None and self.secondary_varname != '':
#             s = 'self.b = self.target_object.%s' % (self.secondary_varname)
#             exec(s)
