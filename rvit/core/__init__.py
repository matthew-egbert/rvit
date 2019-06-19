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




from .init_rvit import init_rvit
