"""
rvit.core docstring
"""

import sys
import os
from kivy.logger import Logger
import pickle
import shelve
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.app import App

# expose things to importers of this module
#import widgets
from .configurable_property import ConfigurableProperty

# colors
from kivy.utils import get_color_from_hex
WHITE = get_color_from_hex('ffffffff')
GREY = get_color_from_hex('888a85ff')
RED = get_color_from_hex('cc0000ff')
BLUE = get_color_from_hex('3465a4ff')
PURPLE = get_color_from_hex('75507bff')
GREEN = get_color_from_hex('73d216ff')
YELLOW = get_color_from_hex('edd400ff')
ORANGE = get_color_from_hex('f57900ff')

BUTTON_BORDER_HEIGHT = 20

# Instead of 'globals', we make these module attributes
path, pfile_path, pars, inspection_path = (None, None, None, None,)

def loadFonts():
    font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             'fonts/')

    KIVY_FONTS = [
        {
            "name": "uasquare",
            "fn_regular": os.path.join(font_path, "uasquare.ttf"),
            "fn_bold": os.path.join(font_path, "uasquare.ttf"),
            "fn_italic": os.path.join(font_path, "uasquare.ttf"),
            "fn_bolditalic": os.path.join(font_path, "uasquare.ttf"),
        }]

    for font in KIVY_FONTS:
        LabelBase.register(**font)


def activate(rvit_path=None):
    global path, pfile_path, pars, inspection_path
    Logger.info('==== Activating Rvit ====')

    if rvit_path is None:
        rvit_path = os.path.dirname(sys.argv[0])
        rvit_path = os.path.join(rvit_path, '.rvit')
        rvit_path = os.path.abspath(rvit_path)

    # if no rvit dir exists, create it
    try:
        Logger.info('Creating directory (%s) for Rvit.' % (rvit_path))
        os.makedirs(rvit_path)
    except os.error:
        pass

    path = rvit_path
    inspection_path = os.path.join(path, 'inspections')

    # if no parameter file exists, create it
    pfile_path = os.path.join(rvit_path, 'parameters.p')
    pars = shelve.open(pfile_path)
    Logger.info('Parameter file: %s' % (pfile_path))

    loadFonts()
    kv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'rvit.kv')
    Builder.load_file(kv_file_path)

def disactivate():
    global pars
    pars.close()

def init_rvit(model_object,rvit_kv_string,window_size=(900,900)):
    import pkg_resources
    from kivy import platform
    from kivy.config import Config
    if platform == 'linux':
        Config.set('graphics', 'width', str(int(window_size[0])))
        Config.set('graphics', 'height', str(int(window_size[0])))
    
    class RvitApp(App):
        def __init__(self, *args, **kwargs):
            super().__init__(*args,**kwargs)
            self.model = model_object

        def get_simulation(self):
            return self.model

        def build(self):
                return Builder.load_string(rvit_kv_string, filename='rvit.kv')

        def on_stop(self):
            disactivate()

    activate()
    app = RvitApp().run()

