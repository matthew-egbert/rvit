import sys
import os
import pickle
import shelve

import rvit
from kivy.logger import Logger
from kivy.core.text import LabelBase
from kivy.app import App
from kivy.lang import Builder

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
    # global path, pfile_path, pars, inspection_path
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

    rvit.core.pars = shelve.open(pfile_path)
    Logger.info('Parameter file: %s' % (pfile_path))

    loadFonts()
    kv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'rvit.kv')
    Builder.load_file(kv_file_path)

def disactivate():
    rvit.core.pars.close()

def init_rvit(model_object,rvit_string=None,rvit_file=None,window_size=(900,900)):
    """Initializes rvit. This must be run for RVIT to do
    anything. Generally run immediately after the simulation/artifact
    has been instantiated. See :ref:`Getting Started`!

    :param rvit_file: a string containing the filename of an rvit GUI specification file
    :param rvit_string: a string containing the rvit GUI specification

    :param window_size: the (width,height) of the RVIT window

    Either `rvit_file` or `rvit_string` must be provided. The former overrides the latter.

    """
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
            if rvit_file is not None:
                return Builder.load_file(rvit_file)
            elif rvit_string is not None:
                return Builder.load_string(rvit_kv_string, filename='rvit.kv')
            else:
                raise Error('Either rvit_file or rvit_string must be passed to init_rvit')


        def on_stop(self):
            disactivate()

    activate()
    app = RvitApp().run()
