import numpy as np
from kivy.graphics import Mesh
from kivy.properties import ObjectProperty, StringProperty, NumericProperty,\
    OptionProperty, ListProperty

from kivy.resources import resource_find, resource_add_path

import rvit.core.glsl_utils as glsl_utils

from rvit.core.vis.rvi_visualizer import RVIVisualizer,DataTargettingProperty
from rvit.core.configurable_property import ConfigurableProperty
from rvit.core.vis.components import *
from rvit.core.vis.data_sources import *

class array_data(RVIVisualizer):
    """ND array containing the data to be plotted
    """

    array_data = DataTargettingProperty('') #: ND array containing the data to be plotted
    array_data_preprocess = DataTargettingProperty('') #: the preprocessor for array_data

    click_fn = DataTargettingProperty('') # string specifying function (from simulation) to call when clicked the function must take an x and y argument
    
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def on_array_data(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()
        
        self.array_data = value
        if self.array_data != '':
            s = 'self.arr = self.simulation.%s' % (self.array_data)
            exec(s)
            s = 'self.n_elements = len(np.ravel(self.arr))'
            exec(s)
            self.data_index_arr = self.n_data_sources
            self.n_data_sources += 1
        
        self.shader_substitutions['attributes'].append('')
        self.format_has_changed = True

    def on_array_data_preprocess(self, obj, value):
        s = 'self.preprocess_arr = %s' % (value)
        exec(s)

    def on_click_fn(self,obj,value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()
        
        if value != '':
            s = 'self.click_callback = self.simulation.%s' % (value)
            exec(s)                
        
    def update(self):
        super().update()
        if hasattr(self,'arr'):
            data = self.arr
            if hasattr(self,'preprocess_arr'):
                data = self.preprocess_arr(data)
            self.texture.blit_buffer(np.ravel(np.array(data,dtype=np.float32)),
                                     colorfmt=self.colorfmt,
                                     bufferfmt='float')

    


class ArrayRenderer(xy_bounds,color,gradient,array_data):
    """Displays a numpy array. The array must be 2 or 3 dimensional. 

    If the target `array_data` is 3D, then the 3rd axis can be of size
    1, 3 or 4. The way the data is plotted depends upon this size of
    the 3rd axis in the following way: 

    If the 3rd Axis is of length..

        1: the gradient component determines the color to be plotted.  

        3: the values in the array are the red, green and blue values
        to be plotted.

        4: the values in the array are the red, green, blue and alpha
        values to be plotted.


    Here is an example usage.

    .. literalinclude :: ./code_examples/array_renderer/main.py
        :language: python
        :caption: main.py

    .. literalinclude :: ./code_examples/array_renderer/rvit.kv
        :language: python
        :caption: rvit.kv

    .. figure:: ./code_examples/array_renderer/screenshot.png
        :width: 300px

    minimal example

    """

    mag_filter = OptionProperty('nearest', options=['nearest', 'linear'])
    # coloring = OptionProperty('greys', options=['greys', 'red/black', 'rgb'])

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.shader_fn = 'array_renderer.glsl'

    def loadShaders(self, subs = {}):
        ## generate the glsl code
        self.shaders = glsl_utils.loadShaders(self.shader_fn,
                                              {**subs,**self.shader_substitutions})
        ## set the meshes shaders to the generated glsl code
        self.render_context.shader.vs = self.shaders['vs']
        self.render_context.shader.fs = self.shaders['fs']

        ## replace any previous mesh with the new mesh
        if hasattr(self,'mesh'):
            self.render_context.remove(self.mesh)

        ######
        self.mesh = Mesh(mode='triangles', fmt=[(b'v_pos', 2, 'float'),
                                                (b'v_tc0', 2, 'float'), ])
        #self.mesh = Mesh(mode='triangles', fmt=self.fmt)
        ## other data sources currently disabled as I try to get the basic
        ## array renderer working
        self.mesh.indices = [0, 1, 2, 0, 2, 3]
        self.mesh.vertices = [0.0, 0.0, 0.0, 0.0,
                              0.0, 1.0, 0.0, 1.0,
                              1.0, 1.0, 1.0, 1.0,
                              1.0, 0.0, 1.0, 0.0]
        self.render_context.add(self.mesh)
        # print('not sure about following line')
        # self.canvas.before.add(self.render_context)
        self.format_has_changed = True

    def registerConfigurableProperties(self):
        super().registerConfigurableProperties()
        self.addConfigurableProperty(ArrayRenderer.mag_filter)

    def update(self):
        if self.format_has_changed :
            self.loadShaders()
            self.format_has_changed = False

            if len(np.shape(self.arr)) == 2 :
                self.arr = np.expand_dims(self.arr,axis=2)
            if isinstance(self.arr, np.ndarray) and len(np.shape(self.arr)) == 3:
                self.array_width, self.array_height, self.depth = np.shape(self.arr)[:]
                self.colorfmt = ['NONSENSICAL', 'luminance','luminance_alpha',
                                 'rgb', 'rgba'][self.depth]
                self.texture = Texture.create(
                    size=(
                        self.array_width,
                        self.array_height),
                    bufferfmt='float')
                self.texture.blit_buffer(np.ravel(np.array(self.arr,dtype=np.float32)),
                                         colorfmt=self.colorfmt,
                                         bufferfmt='float')
                self.texture.mag_filter = self.mag_filter
                self.render_context['array_texture'] = self.texture.id
                self.render_context.add(BindTexture(texture=self.texture, index=self.texture.id,
                                                    colorfmt='rgba', mipmap=True))
            else:
                #print(np.shape(self.arr))#, self.target_object, self.target_varname)
                raise TypeError('Target of Array Renderer must be a 3D numpy.ndarray.')

            
        if self.enabled:
            super().update()
            # data = np.array(np.ravel(self.arr))
            # low = 0.0
            # high = 1.0
            # if self.minimum_value == 'auto':
            #     low = data.min()
            # if self.maximum_value == 'auto':
            #     high = data.max()
            # data -= (low)
            # if high - low != 0.0:
            #     data /= (high - low)

            # self.texture.blit_buffer(data,
            #                          colorfmt=self.colorfmt,
            #                          bufferfmt='float')
            self.render_context.ask_update()

    def on_mag_filter(self, inst, value):
        if hasattr(self,'texture'):
            self.texture.mag_filter = self.mag_filter

    def inspect(self):
        inspection_dump_file = self.createInspectionDumpFile()
        np.save(open(inspection_dump_file, 'wb'), self.a)
        self.launchInspector(inspection_dump_file)

    def on_motion(self, etype, motionevent):
        print('hi')

    def on_touch_down(self,touch):
        self.on_touch_move(touch)

    def on_touch_move(self, touch):
        super().on_touch_down(touch)
        if hasattr(self,'click_callback'):
            # print( touch.apply_transform_2d(self.to_local) )

            tx,ty = touch.pos
            px,py = self.pos
            w,h = self.size

            ## position relative to whole drawn area
            rx = (tx-px)/w
            ry = (ty-py)/h

            ## y = row = cj
            ## x = column = ci
            cj = int(np.floor(rx * self.array_width))
            ci = int(np.floor(ry * self.array_height))
            # print(f'{rx},{ry} is the cell {ci,cj}')
            ci = max(0.0,min(self.array_height-1,ci))
            cj = max(0.0,min(self.array_width-1 ,cj))
            self.click_callback(ci,cj,rx,ry,touch)
            ## TODO: make the call back pass other arguments, such as rx,ry
            ## and also the cell coordinates but not rounded
        
    # def on_coloring(self, inst, value):
    #     if value == 'greys':
    #         self.render_context.shader.source = resource_find('array_renderer_greys.glsl')
    #     elif value == 'red/black':
    #         self.render_context.shader.source = resource_find('array_renderer_redblack.glsl')

# ### Local Variables: ###
# ### mode: python ###
# ### python-main-file: "main.py" ###
# ### python-working-dir: "../minimal_project/" ###
# ### End: ###
