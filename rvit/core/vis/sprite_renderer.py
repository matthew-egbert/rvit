from kivy.graphics import Mesh
from kivy.properties import ObjectProperty, StringProperty, NumericProperty,\
    OptionProperty, ListProperty
from kivy.core.window import Window
from rvit.core.vis.rvi_element import RVIElement
from rvit.core.configurable_property import ConfigurableProperty
from rvit.core.vis.components import *
from rvit.core.vis.data_sources import *
import rvit.core.glsl_utils as glsl_utils
import kivy.core.image as kci


class SpriteRenderer(xy_bounds,x_data,y_data,rot_data,color1d_data,size_data):
    """The SpriteRenderer is used to display an image one or more
    times. It takes x,y and (optionally) rotation coordinates that
    specify the position of the image(s).

    """

    image = ObjectProperty()
    """a string that specifies the path to the image file, e.g., 'img/robot.png' 
    """
    
    sprite_size = NumericProperty(1.0)
    """ Specifies the size of the sprites. """

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)        
        self.shader_fn = 'sprite_renderer.glsl'
        self.fmt.append( (b'll_ul_ur_lr', 1, 'float') )
        self.n_data_sources += 1
        self.vertices_per_datum = 4

    def registerConfigurableProperties(self):
        super().registerConfigurableProperties()
        self.addConfigurableProperty(SpriteRenderer.sprite_size)
    
    def update(self):
        if self.format_has_changed :
            self.format_has_changed = False
            self.loadShaders()
            self.data_per_vertex = self.n_data_sources
            self.data_to_shader  = np.zeros((self.n_elements*self.vertices_per_datum,
                                             self.data_per_vertex), dtype=np.float32)
            self.data_to_shader[:,0] = [0,1,2,3]*self.n_elements
            
        if self.enabled:
            super().update()
            if self.n_elements > 0:
                tri_indices = np.array([(n, n+1, n+2, n, n+2, n+3)
                                        for n in range(0,self.n_elements,4)])
                self.tri_indices = tri_indices.ravel()
                self.mesh.indices = self.tri_indices
                self.mesh.vertices = self.data_to_shader.ravel()
                self.render_context.ask_update()

    def loadShaders(self, subs = {}):
        subs.update(
            {'sprite_size': 1.0 * self.sprite_size }#/ min(Window.width, Window.height),
        )
        
        ## generate the glsl code
        self.shaders = glsl_utils.loadShaders(self.shader_fn,
                                              {**subs,**self.shader_substitutions})
        ## set the meshes shaders to the generated glsl code
        self.render_context.shader.vs = self.shaders['vs']
        self.render_context.shader.fs = self.shaders['fs']

        ## replace any previous mesh with the new mesh
        if hasattr(self,'mesh'):
            self.render_context.remove(self.mesh)            
        self.mesh = Mesh(mode='triangles', fmt=self.fmt)
        # print(self.fmt)
        self.render_context.add(self.mesh)
        if hasattr(self,'texture'):
            self.mesh.texture = self.texture
        
    def on_image(self, obj, value):
        self.texture = kci.Image(value).texture
        self.loadShaders()        

    def on_sprite_size(self, obj, value):
        # scales sprite sizes
        self.loadShaders()
