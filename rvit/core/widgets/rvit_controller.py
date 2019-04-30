from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, OptionProperty, BooleanProperty
from kivy.core.window import Window
from kivy.graphics.transformation import Matrix
from functools import partial
import os
import rvit.core
from ..configurable_property import ConfigurableProperty
from kivy.graphics.context_instructions import *


class RvitSlider(BoxLayout):
    unique_name = StringProperty('')
    target_object = ObjectProperty(None)
    target_varname = StringProperty('')
    slider_min = NumericProperty(0.0)
    slider_max = NumericProperty(1.0)

    def __init__(self, *args, **kwargs):
        kwargs['orientation'] = 'vertical'
        self.slider = Slider(orientation=self.orientation,
                             size_hint=(1.0, 1.0))
        super(RvitSlider, self).__init__(**kwargs)

        self.configurable_properties = {}
        self.title_label = Label(text='test', size_hint=(1.0, None), size=(0, 20))
        self.value_label = Label(text='____', size_hint=(1.0, None), size=(0, 20))

        # self.add_widget(Button(text='save',size=(0,20),size_hint=(1.0,None)))
        # self.add_widget(Button(text='load',size=(0,20),size_hint=(1.0,None)))

        self.add_widget(self.slider)
        self.add_widget(self.title_label)
        self.add_widget(self.value_label)

    def registerConfigurableProperties(self):
        pass

    def on_unique_name(self, obj, unique_name):
        """Once the widget is given a non-empty unique name, set up its
        configuration panel UI.

        """

        if unique_name != '':
            self.title_label.text = unique_name
            self.registerConfigurableProperties()
            if len(self.configurable_properties) > 0:
                def test(value):
                    content = StackLayout()
                    for k in self.configurable_properties.keys():
                        content.add_widget(
                            self.configurable_properties[k].getConfigurationSubpanel())
                    popup = Popup(title='Configure', content=content)
                    popup.open()

                self.configure_button = Button(text='configure',
                                               on_press=test,
                                               background_color=rvit.core.BLUE,
                                               pos_hint={'x': 0.0, 'top': 1.0})

                self.top_buttons.add_widget(self.configure_button, index=2)

    def on_target_object(self, inst, value):
        self.target_object = value

    def on_target_varname(self, inst, value):
        self.target_varname = value
        if self.target_object is not None and self.target_varname != '':
            s = 'v = self.target_object.%s' % (self.target_varname)
            exec(s)
            # if v > self.slider.max :
            #     self.slider.max = v + abs(v)*0.5
            # if v < self.slider.min :
            #     self.slider.min = v - abs(v)*0.5
            self.slider.value = v
            self.value_label.text = '%0.2f' % (self.slider.value)

        self.slider.bind(value=self.on_value)

    def on_value(self, a, b):
        if self.target_object is not None and self.target_varname != '':
            s = 'self.target_object.%s = a.value' % (self.target_varname)
            exec(s)
        self.value_label.text = '%0.2f' % (self.slider.value)
        # #print(a,b)
        # print(a.value_normalized)
        # #a.value_normalized = 0.5

    def on_slider_min(self, a, b):
        self.slider.min = b
        self.slider.step = (self.slider.max - self.slider.min) / 500.0

    def on_slider_max(self, a, b):
        self.slider.max = b
        self.slider.step = (self.slider.max - self.slider.min) / 500.0

    def on_orientation(self, a, b):
        self.orientation = 'vertical'
        self.slider.orientation = b

# ### Local Variables: ###
# ### mode: python ###
# ### python-main-file: "main.py" ###
# ### python-working-dir: "../minimal_project/" ###
# ### End: ###
