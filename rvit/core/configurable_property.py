from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.graphics import Color
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, OptionProperty, BooleanProperty, ReferenceListProperty
from rvit.core.properties import ColorProperty,BoundsProperty
from functools import partial
from rvit.core import *
import rvit.core
import numpy as np

from rvit.core import draw_constants as dc

class ConfigurableProperty(object):
    def __init__(self, prop, owner, rank = 0):
        self.prop = prop
        self.owner = owner
        self.key = self.owner.unique_name + '.' + self.prop.name
        self.rank = rank

        # load values from the previous run
        if self.key in rvit.core.pars.keys():
            # print(self.key)
            # print(rvit.core.pars[self.key])
            # print('========================================')
            # print(f'configurableProperty {self.key}  ')
            # print(f'to be loaded from a previous run to be {rvit.core.pars[self.key]}')
            self.prop.set(self.owner, rvit.core.pars[self.key])
            self.prop.dispatch(self.owner)

    def getConfigurationSubpanel(self):
        #subpanel = BoxLayout(size_hint=(1.0, None), height=(40))

        if isinstance(self.prop, ColorProperty):
            subpanel = self.prop.get_configuration_subpanel(self.prop,self.owner, self.key)
        elif isinstance(self.prop, BoundsProperty):
            subpanel = self.prop.get_configuration_subpanel(self.prop,self.owner, self.key)
        elif isinstance(self.prop, OptionProperty):
            subpanel = StackLayout(size_hint=(None,None),width=dc.col_width,
                                   orientation='lr-tb')
            subpanel.add_widget(Label(text=self.prop.name,
                                      size_hint=(1.0, None),
                                      height=dc.text_height))
            rows = float(np.ceil(len(self.prop.options)/4))+1

            for opt in self.prop.options:
                def setNewValue(_, new_value=''):
                    self.prop.set(self.owner, new_value)
                    rvit.core.pars[self.key] = new_value

                set_fn = partial(setNewValue, new_value=opt)
                btn = ToggleButton(text=opt, group=self.prop.name,
                                   on_press=set_fn,size=(100,dc.text_height),
                                   size_hint=(0.25,1./rows))
                if self.prop.get(self.owner) == opt:
                    btn.state = 'down'
                subpanel.add_widget(btn)
            subpanel.height = dc.text_height * rows
            
        elif isinstance(self.prop, StringProperty):
            subpanel = BoxLayout(size_hint=(None,None),
                                 width=dc.col_width,height=dc.text_height)#,minimum_height=350)
            def on_text(instance, value):
                self.prop.set(self.owner, value)
                rvit.core.pars[self.key] = value

            ti = TextInput(text=str(self.prop.get(self.owner)),
                           multiline=False,height=40)
            subpanel.add_widget(ti)
            ti.bind(text=on_text)

        # elif isinstance(self.prop, BooleanProperty):
        #     pass
        elif isinstance(self.prop, NumericProperty):
            subpanel = BoxLayout(size_hint=(None,None),
                                 #orientation='rl-tb',
                                 width=dc.col_width*1.0,
                                 height=dc.text_height)
            def is_number(s):
                try:
                    float(s)
                    return True
                except ValueError:
                    return False

            def on_text(instance, value):
                if(is_number(value)):
                    value = float(value)
                    self.prop.set(self.owner, value)
                    rvit.core.pars[self.key] = value

            subpanel.add_widget(Label(text=str(self.prop.name),
                                      size_hint=(0.4, 1.0)))
            ti = TextInput(text=str(self.prop.get(self.owner)),size_hint=(0.6, 1.0))
            subpanel.add_widget(ti)
            ti.bind(text=on_text)        
        else:
            subpanel.add_widget(Label(text=str(self.prop.get(self.owner)),
                                      size_hint=(1.0, 1.0)))
        return subpanel
