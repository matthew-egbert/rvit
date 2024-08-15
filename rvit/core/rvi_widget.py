import numpy as np
from collections import defaultdict
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, OptionProperty, BooleanProperty, ListProperty
from kivy.core.window import Window
from kivy.graphics.transformation import Matrix
from functools import partial
import os
from kivy.graphics.context_instructions import *
from kivy.graphics import RenderContext
from kivy.clock import Clock

import rvit.core
from rvit.core.configurable_property import ConfigurableProperty
from kivy.uix.stencilview import StencilView
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

from rvit.core import glsl_utils
from kivy.graphics.stencil_instructions import *

class DataTargettingProperty(StringProperty):
    pass

class RVIWidget(FloatLayout):
    """ Both visualizing and modifying widgets inherit from this class. """

    unique_name = StringProperty('') 
    """Every RVIWidget should specify one of these. It is a unique identifier that
    allows RVIT to save properties that have been adjusted during execution."""

    show_controls = BooleanProperty(True)
    """Boolean for whether or not this RVI element should show its
    control-bar buttons and name. Defaults to True."""

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.configurable_properties = {}

    
    def on_unique_name(self, obj, unique_name):
        if unique_name != '':

            self.title_label.text = unique_name.replace('_', ' ').upper()+' '
            # self.title_label.size = (self.title_label.texture_size[0], 20)
            # self.title_label.size = (200, 20)
            # self.title_label.do_layout()
            # self.top_buttons.do_layout()
            
            self.registerConfigurableProperties()
            if len(self.configurable_properties) > 0:
                def open_configuration_panel(value):
                    content = StackLayout(orientation='tb-lr')
                    
                    #content.spacing=(40,20)
                    #content.padding=5

                    cps = list(self.configurable_properties.values())
                    for cp in sorted(cps,key=lambda x: x.rank) :
                        #print(cp.rank)
                        content.add_widget(cp.getConfigurationSubpanel())
                    # for k in self.configurable_properties.keys():
                    #     content.add_widget(
                    #         self.configurable_properties[k].getConfigurationSubpanel())
                    popup = Popup(title='Configure', content=content)
                    popup.open()

                self.configure_button = Button(text='[Cfg.]',
                                               bold=True,
                                               background_normal ='',
                                               background_down='',
                                               color=rvit.core.BLUE,
                                               on_press=open_configuration_panel,
                                               background_color=rvit.core.BLACK,
                                               size_hint=(None, None),
                                               size=(50, 20),
                                               pos_hint={'right': 0.8, 'top': 1.0})

                self.top_buttons.add_widget(self.configure_button, index=2)


                
    def on_show_controls(self, inst, value):
        if value == True:
            self.add_widget(self.top_buttons)
        else:
            if self.top_buttons in self.children:
                self.remove_widget(self.top_buttons)
                

    def reconnect(self):
        need_reset = True
        for k, v in self.properties().items():
            # print(type(v))
            if issubclass(type(v),DataTargettingProperty):
                if v.get(self) != v.defaultvalue:
                    # print(v)
                    if need_reset:
                        self.shader_substitutions = defaultdict(list)
                        self.fmt = []
                        self.n_data_sources = 0
                        need_reset = False
                    # print(k,v.get(self),v.defaultvalue)a
                    # v.set(self,v.get(self))
                    v.dispatch(self)
            # else :
            #     print(f'{type(v)} is not a subclass of DataTargettingProperty')
                
 
        
    def addConfigurableProperty(self, prop, rank = 0):
        self.configurable_properties[prop.name] = ConfigurableProperty(prop, self, rank)

    def removeConfigurableProperty(self, prop):
        self.configurable_properties.pop(prop.name)

    def registerConfigurableProperties(self):
        pass

        
    def createInspectionDumpFile(self):
        try:
            os.makedirs(rvit.inspection_path)
        except os.error:
            pass

        datafile_name = filter(str.isalnum, self.unique_name)
        return os.path.join(skivy.inspection_path, datafile_name)

    def launchInspector(self, datafile_name):
        from subprocess import call

        inspection_script_name = 'inspect_%s.py' % (filter(str.isalnum, self.unique_name))
        inspection_script_path = os.path.join(skivy.inspection_path, inspection_script_name)
        with open(inspection_script_path, "w") as text_file:
            text_file.write('from pylab import *\n')
            text_file.write('a = np.load("%s")\n' % (datafile_name))
            text_file.write("print('%s is loaded in the variable called `a`')\n" % (datafile_name))

        instructions = ['gnome-terminal', '-e',
                        """ bash -c "cd """ + skivy.inspection_path +
                        """ ; ipython3 -i """ + inspection_script_name + """ " """]
        call(instructions)

    def inspect(self):
        inspection_dump_file = self.createInspectionDumpFile()
        np.save(open(inspection_dump_file, 'wb'), self.a)
        self.launchInspector(inspection_dump_file)
                
