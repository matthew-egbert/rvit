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
from kivy.clock import Clock
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
        #double eyex, double eyey, double eyez, double centerx, double
        #centery, double centerz, double upx, double upy, double upz)¶
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
        #m.rotate(np.pi/4,0,0,1.0)
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


class xyz_bounds(xy_bounds) :
    zmin = NumericProperty(-1.) #: z-coord of left border 
    zmax = NumericProperty(1.)  #: z-coord of right border 
    timer_for_wiggle = 0.0
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(**kwargs)
    
    def on_zmin(self, obj, value):
        self.updateModelViewMatrix()

    def on_zmax(self, obj, value):
        self.updateModelViewMatrix()
    
    def updateProjectionMatrices(self):
        w = float(Window.width)
        h = float(Window.height)
        m = kivy.graphics.transformation.Matrix().identity()
        # m = kivy.graphics.transformation.Matrix().look_at(0,0,1.9,
        #                                                   0,0,0,
        #                                                   0,1,0)
        # perspective(double fovy, double aspect, double zNear, double zFar)
        m.perspective(80,1,0,20)
        t = kivy.graphics.transformation.Matrix().identity()
        p = rvit.core.BUTTON_BORDER_HEIGHT
        k = self.width / w# * self.width / w
        dx = (self.pos[0]-w/2+(self.width/2))/(w/2)
        dy = (self.pos[1]-h/2+(self.height/2))/(h/2)
        t.scale(k,k,k)
        t.translate(dx,dy,0)
        self.stencil.size = self.size
        self.stencil.pos = self.pos
        # self.stencil.size = w,h
        # self.stencil.pos = 0,0
        self.render_context['projection_mat'] = m
        self.render_context['relocation_mat'] = t
        
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

        ## rotates the target a bit to make 3D aspects easier to see

        ## iteratively update the positions of the particles
        def iterate(arg):
            wiggle_matrix = kivy.graphics.transformation.Matrix().identity()
            wiggle_matrix.rotate(0.05*np.sin(xyz_bounds.timer_for_wiggle),
                                 -1,0,0)
            wiggle_matrix.rotate(0.1*np.cos(xyz_bounds.timer_for_wiggle),
                                 0,1,0)
            xyz_bounds.timer_for_wiggle+=0.01
            self.render_context['modelview_mat'] = m.multiply(wiggle_matrix)
        ## start a thread to call the iterate fn as
        ## frequently as possible
        Clock.schedule_interval(iterate,1.0/30)

        m.scale(1.0 / hr,
                1.0 / vr,
                1.0 / vr)
        m.translate(-0*self.xmin / hr,
                    -0*ymin / vr,
                    -1.50)
        self.render_context['modelview_mat'] = m
        
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
        print(self,obj,value)
        # for single color setting
        self.render_context['color'] = list(value)
        self.format_has_changed = True
        #self.loadShaders()
        

class gradient(RVIVisualizer):
    gradient = OptionProperty('',options=['viridis','plasma','inferno','hsv','coolwarm','spring','summer','autumn','tab20c','limits','None','binary','gray','gist_heat','hot','Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn','Greys_r', 'Purples_r', 'Blues_r', 'Greens_r', 'Oranges_r', 'Reds_r', 'YlOrBr_r', 'YlOrRd_r', 'OrRd_r', 'PuRd_r', 'RdPu_r', 'BuPu_r', 'GnBu_r', 'PuBu_r', 'YlGnBu_r', 'PuBuGn_r', 'BuGn_r', 'YlGn_r'])
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
        
        
        


