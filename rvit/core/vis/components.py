from rvit.core.vis.rvi_visualizer import RVIVisualizer
from kivy.properties import *
import kivy.graphics.transformation 
from kivy.core.window import Window
import rvit.core
from rvit.core.properties import ColorProperty,BoundsProperty
import re
import numpy as np
from kivy.graphics.texture import Texture
from kivy.graphics import *
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, OptionProperty, BooleanProperty, ReferenceListProperty

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

# from data_sources import color1d_data

class xy_bounds(RVIVisualizer):
    """Provides four configurable parameters that determine the limits of a 2D display.
    """
    
    xmin = NumericProperty(-1.) #: x-coord of left border 
    xmax = NumericProperty(1.)  #: x-coord of right border 
    ymin = NumericProperty(-1.) #: x-coord of bottom border 
    ymax = NumericProperty(1.)  #: x-coord of top border
    # autoymin = OptionProperty([False,True])
    # autoymax = OptionProperty([False,True])
    autoymin = OptionProperty(False,options=[False,True])
    autoymax = OptionProperty(False,options=[False,True])

    bounds = BoundsProperty(xmin,xmax,ymin,ymax,autoymin,autoymax)

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.updateModelViewMatrix()
        self.data_minimum = self.data_maximum = 0.0
        
    def registerConfigurableProperties(self):
        super().registerConfigurableProperties()
        self.addConfigurableProperty(xy_bounds.bounds)

    def updateProjectionMatrices(self):
        w = float(Window.width)
        h = float(Window.height)
        m = kivy.graphics.transformation.Matrix().identity()
        p = rvit.core.BUTTON_BORDER_HEIGHT
        m.scale(2.0 * self.width / w,
                2.0 * (self.height - p) / h, 1.0)

        self.stencil.size = self.size
        self.stencil.pos = self.pos
        m.translate(-1.0 + (self.pos[0]) * 2.0 / w,
                    -1.0 + (self.pos[1]) * 2.0 / h,
                    0.0)
        self.render_context['projection_mat'] = m

    def updateModelViewMatrix(self):
        m = kivy.graphics.transformation.Matrix().identity()
        
        ymin = self.ymin
        ymax = self.ymax
        if hasattr(self,'data_minimum'):
            #print(self.xmin,self.xmax,self.ymin,self.ymax,self.autoymin,self.autoymax)
            if self.autoymin:
                ymin = self.data_minimum
            if self.autoymax:
                ymax = self.data_maximum
        hr = max(0.00001, (self.xmax - self.xmin))
        vr = max(0.00001, (ymax - ymin))
        m.scale(1.0 / hr,
                1.0 / vr,
                1.0)
        m.translate(-self.xmin / hr,
                    -ymin / vr,
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

    # def on_autoymin(self, obj, value):
    #     self.autoymin = value
    #     print('----------------------',self.autoymin)

    # def on_autoymax(self, obj, value):
    #     self.autoymax = value
        
class color(RVIVisualizer):
    """Provides a single 4-tuple parameter [R,G,B,A] that can be used to
    specify the the primary color of the visualizer. May be
    (partially) overridden by the color data sources...but in some
    cases (e.g. the color_1d data source) the alpha component still is used.

    """

    r = BoundedNumericProperty(1,min=0,max=1)
    g = BoundedNumericProperty(1,min=0,max=1)
    b = BoundedNumericProperty(1,min=0,max=1)
    a = BoundedNumericProperty(1,min=0,max=1)
    
    color = ColorProperty(r,g,b,a)
    """a 4-tuple '[red,green,blue,alpha]' :: when the **color_data**
parameter is not provided, this property specifies the color for all
plotted points. When color_data is provided, the alpha value is still
used.

    """
    
    def on_color(self, obj, value):
        # for single color setting
        self.render_context['color'] = list(value)

class gradient(RVIVisualizer):
    gradient = OptionProperty('viridis',options=['viridis','plasma','inferno','hsv','coolwarm','spring','summer','autumn','tab20c','limits','None'])
    vmin = NumericProperty(0.0)
    vmax = NumericProperty(1.0)

    def get_texture_for_cmap(self, cmap_name):
        self.cmap_name = cmap_name
        self.cmap = plt.get_cmap(cmap_name)
        self.norm = mpl.colors.Normalize(vmin=0, vmax=1)
        self.scalarMap = cm.ScalarMappable(norm=self.norm, cmap=self.cmap)

        self.texture_data = np.array([self.scalarMap.to_rgba(val) for val in np.linspace(0,1,256)],
                                     dtype=np.float32)
        return self.texture_data
        
    
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.texture = Texture.create(size=(1,256),
                                      bufferfmt='float')
        
    def registerConfigurableProperties(self):
        super().registerConfigurableProperties()
        self.addConfigurableProperty(gradient.gradient,rank=100)        
        self.addConfigurableProperty(gradient.vmin,rank=101)
        self.addConfigurableProperty(gradient.vmax,rank=101)

    def on_gradient(self,obj,value):
        print('on_gradient()',value)
        if value != 'None':
            self.depth = 4
            self.colorfmt = ['ZERO_DEPTH_ARRAY?', 'luminance',
                             'luminance_alpha', 'rgb', 'rgba'][self.depth]
            if value == 'limits':
                t = np.ones((256,4),dtype=np.float32)*0.9
                t[:,3] = 1.0
                t[0,:]  = [1.0,0,0,0.9]
                t[-1,:] = [1.0,0,0,0.9]
            else:
                t = self.get_texture_for_cmap(self.gradient)

            self.texture.blit_buffer(t.ravel(),
                                     colorfmt=self.colorfmt,
                                     bufferfmt='float')
            self.render_context['gradient_texture'] = self.texture.id
            self.render_context.add(BindTexture(texture=self.texture, index=self.texture.id,
                                                colorfmt='rgba', mipmap=True))
            self.render_context['vmin'] = self.vmin
            self.render_context['vmax'] = self.vmax

            self.shader_substitutions['uses_gradient'] = True            
        else:
            self.shader_substitutions['uses_gradient'] = False
        self.format_has_changed = True
        self.loadShaders()

    def on_vmin(self,obj,value):
        self.vmin = value
        self.render_context['vmin'] = self.vmin

    def on_vmax(self,obj,value):
        self.vmax = value
        self.render_context['vmax'] = self.vmax
        
        
        


