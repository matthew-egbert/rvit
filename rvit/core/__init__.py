"""
rvit.core docstring
"""

import sys
import os
import pickle
import shelve
from kivy.logger import Logger
from kivy.core.text import LabelBase
from kivy.app import App
from kivy.lang import Builder

# expose things to importers of this module
#import widgets
from .configurable_property import ConfigurableProperty

# colors
from kivy.utils import get_color_from_hex
WHITE = get_color_from_hex('ffffffff')
BLACK = get_color_from_hex('000000ff')
GREY = get_color_from_hex('888a85ff')
RED = get_color_from_hex('ff1900ff')
BLUE = get_color_from_hex('057dffff')
LIGHTBLUE = get_color_from_hex('00ddffff')
PURPLE = get_color_from_hex('9800ff')
GREEN = get_color_from_hex('00ff2eff')
YELLOW = get_color_from_hex('fffa00ff')
ORANGE = get_color_from_hex('ffcc00ff')
PINK = get_color_from_hex('ff008cff')
CYAN = get_color_from_hex('00ffe1ff')
LIME = get_color_from_hex('d8ff00ff')

CONFIG_BUTTON_COLOR = LIME

BUTTON_BORDER_HEIGHT = 20

# Instead of 'globals', we make these module attributes
path, pfile_path, pars, inspection_path = (None, None, None, None,)




from .init_rvit import init_rvit
from .init_rvit import rvit_reconnect
