
from kivy.clock import Clock
import numpy as np
from kivy.config import Config
from kivy import platform

if platform == 'linux':
    ratio = 1.
    w = 1920
    Config.set('graphics', 'width', str(int(w)))
    Config.set('graphics', 'height', str(int(w)))
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
        self.x = 0.0
        self.y = 0.0
        self.z = 1.0

        ## iteratively update the positions of the particles
        def iterate(arg):
            ## random walk
            self.x += np.random.randn()*0.1
            self.y += np.random.randn()*0.1
            self.z += np.random.randn()*0.1

            if self.x > 1.0 :
                self.x -= 2.0
            if self.x < -1.0 :
                self.x += 2.0
            if self.y > 1.0 :
                self.y -= 2.0
            if self.y < -1.0 :
                self.y += 2.0
            if self.z > 1.0 :
                self.z -= 2.0
            if self.z < -1.0 :
                self.z += 2.0
                            
        ## start a thread to call the iterate fn as
        ## frequently as possible
        Clock.schedule_interval(iterate,0.0)
        
        init_rvit(self,rvit_file='rvit.kv') ## <-- Starts RVIT

if __name__ == '__main__':
    model = Model()
    ## An alternative, equivalent way to start rvit...
    # init_rvit(model ,rvit_file='rvit.kv') 

