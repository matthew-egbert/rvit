from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, OptionProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.stacklayout import StackLayout
from kivy.graphics import Rotate
from kivy.clock import Clock

# from kivy.core.window import Window
# from kivy.graphics.transformation import Matrix
# from functools import partial
# import os
# from ..configurable_property import ConfigurableProperty
from kivy.graphics.context_instructions import PushMatrix
from kivy.graphics.context_instructions import PopMatrix

import rvit.core
from rvit.core.rvi_widget import RVIWidget


from kivy.app import App
from kivy.uix.label import Label
from kivy.graphics import Rotate

class RotatedLabel(Label):
    def __init__(self, **kwargs):
        super(RotatedLabel, self).__init__(**kwargs)
        # Schedule the rotation to be applied after the widget is fully initialized
        Clock.schedule_once(self.apply_rotation, 0)

    def apply_rotation(self, *args):
        with self.canvas.before:
            PushMatrix()
            # Now it's safe to set up the rotation
            self.rot = Rotate(angle=90, origin=self.pos)
        with self.canvas.after:
            PopMatrix()

        # Bind the size to update the origin when the widget's size changes
        self.bind(size=self.update_origin, pos=self.update_origin)

    def update_origin(self, *args):
        self.rot.origin = self.pos

class RVIModifier(RVIWidget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.top_buttons = BoxLayout(orientation='horizontal',
                                     size_hint=(1.0, None),
                                     size=(0, rvit.core.BUTTON_BORDER_HEIGHT),
                                     pos_hint={'right': 1.0,
                                               'top': 1.0},)


    # def addControlBar(self):
    #     """ Adds bar to top of widget with various controls for that widget. """
    #     ## add all created buttons to layout (i.e. display them all)
    #     self.add_widget(self.top_buttons)



class RVISlider(RVIModifier):
    unique_name = StringProperty('')
    scalar = StringProperty('')
    slider_min = NumericProperty()
    slider_max = NumericProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.blayout = FloatLayout(size_hint=(1.0, 1.0),
                                   pos_hint={'x': 0.0,
                                           'top': 1.0})

        self.slider = Slider(orientation='vertical',
                             size_hint=(1.0, 0.98),
                             pos_hint={'x': -0.42,'y':-0.05},
                             #pos=(0, 0),
                             cursor_size=(20, 20))


        self.title_label = RotatedLabel(text='test', size_hint=(None, None), size=(0, 20),
                                        pos_hint={'x': 0.0,'y':0.0})
        self.title_label.bind(texture_size=lambda instance,
                              value: instance.setter('size')(instance, (value[0], 20)))

        self.value_label = Label(text='____', bold=True,
                                 size_hint=(1.0, None), size=(0, 20),
                                 pos_hint={'x': -0.42,'top':0.94})

        # self.blayout.add_widget(Button(text='save',size=(0,20),size_hint=(1.0,None))) #TODO: add save button
        # self.blayout.add_widget(Button(text='load',size=(0,20),size_hint=(1.0,None))) #TODO: add load button
        # self.blayout.add_widget(Button(text='config',size=(0,20),size_hint=(1.0,None), 
        #                        background_color=rvit.core.CONFIG_BUTTON_COLOR))

        self.blayout.add_widget(self.top_buttons)
        self.blayout.add_widget(self.slider)
        self.blayout.add_widget(self.title_label)
        self.blayout.add_widget(self.value_label)

        self.add_widget(self.blayout)

        self.min_label = Label(text='min', size=(100,0), size_hint=(1.0,None),font_size='12sp')
        self.max_label = Label(text='max', size=(100,0), size_hint=(1.0,None),font_size='12sp')

        self.add_widget(self.min_label)
        self.add_widget(self.max_label)

        def repos_labels(root,*args):
            r = 20.0
            self.min_label.pos=(self.slider.x+20.0,#-self.min_label.width,
                                self.slider.y+r)
            self.max_label.pos=(self.slider.x+20.0,#-self.min_label.width,
                                self.slider.y+self.slider.height-r)

        # self.blayout.bind(on_size=repos_labels,on_pos=repos_labels)
        # self.bind(on_size=repos_labels,on_pos=repos_labels)
        self.slider.bind(size=repos_labels,
                         pos=repos_labels)
        
        self.on_slider_min(self,self.slider_min)
        #self.on_slider_max(self,self.slider_max)    

    def registerConfigurableProperties(self):
        super().registerConfigurableProperties()
        self.addConfigurableProperty(RVISlider.slider_min,rank = 5)
        self.addConfigurableProperty(RVISlider.slider_max,rank = 6)

    def on_unique_name(self, obj, unique_name):
        """Once the widget is given a non-empty unique name, set up its
        configuration panel UI.

        """

        if unique_name != '':
            self.title_label.text = unique_name.replace('_', ' ').upper()
            self.title_label.bold = True
            self.title_label.size = (self.title_label.texture_size[0], 20)
            self.registerConfigurableProperties()
            if len(self.configurable_properties) > 0:
                def test(value):
                    content = StackLayout()
                    for k in self.configurable_properties.keys():
                        content.add_widget(
                            self.configurable_properties[k].getConfigurationSubpanel())
                    popup = Popup(title='Configure', content=content)
                    popup.open()

                self.configure_button = Button(text='[Cfg.]',
                                               bold=True,
                                               on_press=test,
                                               background_color=rvit.core.colors.BLACK,
                                               color=rvit.core.colors.BLUE,
                                               pos_hint={'x': 0.0, 'top': 1.0})

                self.top_buttons.add_widget(self.configure_button, index=2)



    def on_scalar(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()

        # # self.scalar_data = value
        if value != '':
            self.get_y_command = 'self._y = self.simulation.%s' % (value)
            exec(self.get_y_command)
        #self.loadShaders()

        # self.target_varname = value
        if self.simulation is not None and self.scalar != '':
            self.get_value_command = 'self._v = self.simulation.%s' % (self.scalar)
            exec(self.get_value_command)
            # print(self.get_value_command)
            # print(self._v)
            # quit()

            self.set_value_command = 'self.simulation.%s = self._v' % (self.scalar)
            # exec(self.set_value_command)
            # if v > self.slider.max :
            #     self.slider.max = v + abs(v)*0.5
            # if v < self.slider.min :
            #     self.slider.min = v - abs(v)*0.5
            self.slider.value = float(self._v)
            self.value_label.text = '%0.2f' % (self.slider.value)

        # # # self.scalar_data = value
        # if value != '':
        #     self.get_y_command = 'self._y = self.simulation.%s' % (value)
        #     exec(self.get_y_command)
        # #self.loadShaders()


        self.slider.bind(value=self.on_value)

    def on_value(self, a, value):
        self._v = value
        if self.simulation is not None and self.scalar != '':
            exec(self.set_value_command)
        self.value_label.text = '%0.2f' % (self.slider.value)

    def on_slider_min(self, a, b):
        self.min_label.text = str(b)
        self.slider.min = b
        self.slider.step = (self.slider.max - self.slider.min) / 500.0

    def on_slider_max(self, a, b):
        self.max_label.text = str(b)
        self.slider.max = b
        self.slider.step = (self.slider.max - self.slider.min) / 500.0

    def on_orientation(self, a, b):
        self.blayout.orientation = 'vertical'
        self.slider.orientation = b

    def on_show_controls(self,a,b):
        pass

# ### Local Variables: ###
# ### mode: python ###
# ### python-main-file: "main.py" ###
# ### python-working-dir: "../minimal_project/" ###
# ### End: ###
