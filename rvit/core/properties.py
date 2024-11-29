import rvit
from rvit.core import *
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, OptionProperty, BooleanProperty, ReferenceListProperty

from kivy.uix.colorpicker import ColorPicker,ColorWheel
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from functools import partial
from rvit.core import draw_constants as dc

class ColorProperty(ReferenceListProperty):
    def get_configuration_subpanel(self,prop,owner,key):
        layout = StackLayout(orientation='lr-tb',
                             size_hint=(None,None),
                             width=dc.col_width,
                             height=20)

        clr_picker = ColorPicker()
        if(key in rvit.core.pars.keys()) :
            current_color = rvit.core.pars[key]
            clr_picker.color = current_color

        def on_color(instance, value):
            prop.set(owner, list(instance.color))
            rvit.core.pars[key] = list(instance.color)

        clr_picker.bind(color=on_color)
        layout.add_widget(Label(text=prop.name,size_hint=(1.0,None),height=dc.text_height))
        layout.add_widget(clr_picker)
        
        layout.height = 550

        return layout


class BoundsProperty(ReferenceListProperty):
    def get_configuration_subpanel(self,prop,owner,key):
        def on_text(instance, value, index = 0, sub_prop_name = ''):
            try:
                if value == 'down' :
                    prop.setitem(owner, index, True)
                elif value == 'normal' :
                    prop.setitem(owner, index, False)
                else :
                    fv = float(value)
                    prop.setitem(owner, index, fv)
                #sub_key = owner.unique_name+'.'+sub_prop_name
                rvit.core.pars[key] = [owner.xmin,owner.xmax,owner.ymin,owner.ymax,
                                       owner.autoymin,owner.autoymax]
                # print(key)
                # print(owner.bounds)
            except ValueError:
                print('Value Error! in BoundsProperty')
                pass


        layout = StackLayout(orientation='tb-lr',
                             size_hint=(None,None),
                             width=dc.col_width,
                             height=3*dc.text_height)
        layout.add_widget(Label(text=prop.name,size_hint=(0.2,1.0)))
        
        label_display_props = {
            'height' : 20,
            'size_hint' : (0.2, 1./3),
        }
        
        display_props = {
            'multiline' : False,
            'height' : 20,
            'size_hint' : (0.2, 1./3),
        }
        toggle_props = {
            'height' : 20,
            'size_hint' : (0.2, 1./3),
        }
        
        xmin = TextInput(text=str(owner.xmin),**display_props)
        xmax = TextInput(text=str(owner.xmax),**display_props)
        xmin.bind(text=partial(on_text,index = 0, sub_prop_name = 'xmin'))
        xmax.bind(text=partial(on_text,index = 1, sub_prop_name = 'xmax'))
        layout.add_widget(Label(text='x_min',**label_display_props))
        layout.add_widget(xmin)
        layout.add_widget(Label(**label_display_props)) ## placeholder
        layout.add_widget(Label(text='x_max',**label_display_props))
        layout.add_widget(xmax)
        layout.add_widget(Label(**label_display_props)) ## placeholder

        
        ymin = TextInput(text=str(owner.ymin),**display_props)
        ymax = TextInput(text=str(owner.ymax),**display_props)
        lut = {
            True : 'down',
            False : 'normal',
        }
        autoymin = ToggleButton(text='auto',state=lut[owner.autoymin],**toggle_props)
        autoymax = ToggleButton(text='auto',state=lut[owner.autoymax],**toggle_props)
        ymin.bind(text=partial(on_text,index = 2, sub_prop_name = 'ymin'))
        ymax.bind(text=partial(on_text,index = 3, sub_prop_name = 'ymax'))
        autoymin.bind(state=partial(on_text,index = 4, sub_prop_name = 'autoymin'))
        autoymax.bind(state=partial(on_text,index = 5, sub_prop_name = 'autoymax'))

        layout.add_widget(Label(text='y_min',**label_display_props))
        layout.add_widget(ymin)
        layout.add_widget(autoymin)

        layout.add_widget(Label(text='y_max',**label_display_props))
        layout.add_widget(ymax)
        layout.add_widget(autoymax)

        return layout
