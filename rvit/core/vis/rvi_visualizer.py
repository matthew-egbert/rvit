import numpy as np
from collections import defaultdict
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
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
from rvit.core.rvi_widget import RVIWidget, DataTargettingProperty
from kivy.graphics.stencil_instructions import *


class RVIVisualizer(RVIWidget):
    """All Visualizers have the following properties. """

    
    self_update = BooleanProperty(True)
    """Boolean flag indicating whether this widget should be responsible
    for autonomously updating its own data (i.e. pulling the data from
    the simulation at a regular interval). Defaults to True.
    """ 

    fps = NumericProperty(30.0)
    """Frames per second. A numeric value indicating how many times this
    RVI element should update its data per second. Only relevant when
    self_update is True. Defaults to 30.

    """
    
    background_color = ListProperty([0.0] * 4)
    
    def __init__(self, *args, **kwargs):
        self.render_context = RenderContext()
        super().__init__(**kwargs)
        self.configurable_properties = {}

        self.render_context['modelview_mat'] = Matrix().identity()
        self.render_context['projection_mat'] = Matrix().identity()
        self.render_context['window_size'] = [float(Window.width), float(Window.height)]
        self.canvas.before.add(self.render_context)

        self.update_event = None

        self.shader_substitutions = defaultdict(list)
        self.fmt = []
        self.n_data_sources = 0
        self.vertices_per_datum = 1
        self.format_has_changed = True
        
        prop = self.property('fps')
        prop.dispatch(self)
        with self.canvas:
            StencilPush()
            Color(0,1,1,mode='hsv')
            self.stencil = Rectangle(pos=(10,10),size=(self.size))
            StencilUse()
            self.stencil_color = Color(*self.background_color)
            Rectangle(pos=(-100,-100),size=(10000,1000000))
            self.render_context = RenderContext()
            StencilPop()
        self.addControlBar()


    def addControlBar(self):
        """ Adds bar to top of widget with various controls for that widget. """
        self.top_buttons = BoxLayout(orientation='horizontal',
                                     size_hint=(1.0, None),
                                     size=(0, 20),
                                     pos_hint={'right': 1.0,
                                               'top': 1.0},)

        ## create title label
        self.title_label = Label()
        self.top_buttons.add_widget(self.title_label)


        ## create inspection button
        if 'inspect' in dir(self):
            self.inspect_button = Button(text='inspect',
                                         on_press=lambda x: self.inspect(),
                                         background_color=rvit.core.WHITE,
                                         pos_hint={'x': 0.0, 'top': 1.0})

            self.top_buttons.add_widget(self.inspect_button)

        ## create disable button 
        self.disable_button = ToggleButton(size_hint=(None, None),
                                           background_color=rvit.core.RED,
                                           size=(20, 20),
                                           state='down',
                                           )

        def enabled_state_changed(inst, value):
            self.enabled = value == 'down'
        self.enabled = True
        self.disable_button.bind(state=enabled_state_changed)
        self.top_buttons.add_widget(self.disable_button)

        ## add all created buttons to layout (i.e. display them all)
        self.add_widget(self.top_buttons)
        
    def update(self):
        pass

    def on_background_color(self,obj,value):
        self.stencil_color.rgba = value

    def on_fps(self, obj, value):
        if self.update_event is not None:
            self.update_event.cancel()

        if self.self_update:
            def iterate(a):
                self.update()
            self.update_event = Clock.schedule_interval(iterate, 1.0/self.fps)
        
