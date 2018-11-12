"""
Attach to a MIDI device and send the contents of a MIDI file to it.
"""
import sys
import time
import midi
import midi.sequencer as sequencer
import numpy as np
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, OptionProperty, BooleanProperty
from kivy.clock import Clock
from skivy_controller import SkivySlider


class XTouch(object):
    def __init__(self):
        self.client = 28
        self.port = 0

        self.writer = sequencer.SequencerWrite()
        self.writer.subscribe_port(self.client, self.port)
        self.writer.start_sequencer()

        self.reader = sequencer.SequencerRead(sequencer_resolution=120)
        self.reader.subscribe_port(self.client, self.port)
        self.reader.start_sequencer()

        self.sliders = {}

        def listen_callback(dt):
            event = self.reader.event_read()
            while not(event is None):
                # print(event)
                self.process_event(event)
                event = self.reader.event_read()

        Clock.schedule_interval(listen_callback, 1.0 / 20.0)

    def process_event(self, event):
        if isinstance(event, midi.ControlChangeEvent):
            # assumming a slider motion
            slider_id = event.data[0]
            position = event.data[1]
            # print(self.sliders.keys())
            if slider_id in self.sliders.keys():
                self.sliders[slider_id].slider.value_normalized = float(position) / 128
                # print(self.sliders[slider_id].slider.value_normalized)

    def bind_slider(self, slider_index, xtouch_slider):
        self.sliders[slider_index + 1] = xtouch_slider


xtouch = XTouch()


class XTouchSlider(SkivySlider):
    slider_index = NumericProperty(-1)

    def __init__(self, *args, **kwargs):
        super(XTouchSlider, self).__init__(**kwargs)
        self.slider.bind(value_normalized=self.on_value_normalized)
        # print(':::::::::',self.slider_index)

        for p in ['slider_min', 'slider_max']:
            prop = self.property(p)
            # dispatch this property on the button instance
            prop.dispatch(self)

    def setPos(self, pos):
        """ takes between 0 and 1 """
        if self.slider_index is not None:
            event = midi.ControlChangeEvent(
                tick=0,
                control=self.slider_index + 1,
                value=int(
                    pos * 127))
            xtouch.writer.event_write(event, False, False, True)

    def on_value_normalized(self, x, y):
        self.setPos(self.slider.value_normalized)

    def on_slider_index(self, x, y):
        xtouch.bind_slider(self.slider_index, self)
