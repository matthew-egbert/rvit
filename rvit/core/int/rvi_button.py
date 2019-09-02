from kivy.properties import ObjectProperty, StringProperty, NumericProperty,\
    OptionProperty, ListProperty
from kivy.app import App

from kivy.uix.button import Button

class RVIButton(Button):
    """
    Specifies a button that when clicked calls a method of the simulation object.
    """

    function = StringProperty('') # 
    """A string that specifies a function (or method) that is called when
    this button is pressed.

    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
    
    def on_function(self, obj, value):
        if not hasattr(self,'simulation'):
            self.simulation = App.get_running_app().get_simulation()


    def on_press(self):
        s = 'self.simulation.%s' % (self.function)
        print(s)
        exec(s)
