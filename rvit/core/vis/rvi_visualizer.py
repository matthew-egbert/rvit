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

class CustomLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            # Create a Color instruction to set the background color
            self.bg_color = Color(0, 1, 0, 1)  # RGBA for green background
            # Create a Rectangle instruction to draw the background
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

    def _update_bg(self, instance, value):
        # Update the background rectangle size and position
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

class RVIVisualizer(RVIWidget):
    """All Visualizers have the following properties. """

    self_update = BooleanProperty(True)
    """Boolean flag indicating whether this widget should be responsible
    for autonomously updating its own data (i.e. pulling the data from
    the simulation at a regular interval). Defaults to True.
    """

    fps = NumericProperty(60.0)
    """Frames per second. A numeric value indicating how many times this
    RVI element should update its data per second. Only relevant when
    self_update is True. Defaults to 60.

    """

    background_color = ListProperty([0.0] * 4)

    def __init__(self, *args, **kwargs):
        self.render_context = RenderContext(use_parent_projection=True,
                                            use_parent_modelview=True,
                                            use_parent_frag_modelview=True)
        super().__init__(**kwargs)
        self.configurable_properties = {}

        #self.render_context['modelview_mat'] = Matrix().identity()
        #self.render_context['projection_mat'] = Matrix().identity()
        #self.render_context['window_size'] = [float(Window.width), float(Window.height)]
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
                                     pos_hint={'x': 0.0,
                                               'top': 1.0},)

        # self.top_buttons = FloatLayout(size_hint=(1.0, None),
        #                                size=(0, 20),
        #                                pos_hint={'right': 1.0,
        #                                          'top': 1.0},)

        ## create title label
        self.title_label = Label(bold=True, size_hint=(None, None),padding=(0,0,10,0))
        self.title_label.bind(texture_size=lambda instance, 
                              value: instance.setter('size')(instance, (value[0], 20)))
        self.top_buttons.add_widget(self.title_label)

        ## create inspection button
        if 'inspect' in dir(self):
            self.inspect_button = Button(bold=True,
                                         text='[Insp.]',
                                         on_press=lambda x: self.inspect(),
                                         background_color=rvit.core.colors.BLACK,
                                         color=rvit.core.colors.LIGHTBLUE,
                                         pos_hint={'right': 1.0, 'top': 1.0},
                                         size_hint=(None,None),
                                         size=(50, 20))

            self.top_buttons.add_widget(self.inspect_button)

        ## create disable button
        self.disable_button = ToggleButton(size_hint=(None, None),
                                           background_color=rvit.core.colors.RED,
                                           size=(20, 20),
                                           pos_hint={'right': 1.0, 'top': 1.0},
                                           state='down',
                                           )
        
        self.filler = Widget(size_hint=(1.0, 1.0))
        self.top_buttons.add_widget(self.filler)

        def enabled_state_changed(inst, value):
            self.enabled = value == 'down'
        self.enabled = True
        self.disable_button.bind(state=enabled_state_changed)
        #self.top_buttons.add_widget(self.disable_button)

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

