from kivy.properties import ObjectProperty, StringProperty, NumericProperty,\
    OptionProperty, ListProperty
from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

class RVIToggleButton(ToggleButton):
    """
    Specifies a button that when clicked calls a method of the simulation object.
    """

    boolean = StringProperty('') # 
    """A string that specifies the boolean variable that is toggled when
    this button is pressed.

    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
    
    def on_boolean(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()
            if eval('self.simulation.%s' % (self.boolean)) :
                self.state = 'down'

    def on_press(self):
        s = 'self.simulation.%s = not(self.simulation.%s)' % (self.boolean,self.boolean)
        print(f'TOGGLEING {self.boolean}')
        exec(s)
