
from kivy.clock import Clock
import numpy as np
from kivy.config import Config
from kivy import platform

if platform == 'linux':
    ratio = 1.
    w = 1920
    Config.set('graphics', 'width', str(int(w)))
    Config.set('graphics', 'height', str(int(w/2)))
    Config.set('graphics', 'fullscreen', 'false')
    Config.set('graphics', 'maxfps', '60')
    Config.set('postproc', 'maxfps', '60')
    # Disable pause on minimize
    Config.set('kivy', 'pause_on_minimize', '0')
    # Disable pause when window is out of focus
    Config.set('kivy', 'pause_on_focus', '0')

from rvit.core import init_rvit

class Model(object):
    def __init__(self, *args, **kwargs):
        l,h = -1.0,1.0        
        self.dots = np.random.rand(1000,3)*2-1
        self.colors_1d = self.dots[:,1]
        
        init_rvit(self,rvit_file='rvit.kv') ## <-- Starts RVIT

if __name__ == '__main__':
    model = Model()
    ## An alternative, equivalent way to start rvit...
    # init_rvit(model ,rvit_file='rvit.kv') 

