from rvit.core import init_rvit
from kivy.clock import Clock
import numpy as np

class Model(object):
    def __init__(self, *args, **kwargs):
        self.track_me = 0.0

        ## iteratively update the positions of the particles
        def iterate(arg):
            self.track_me = np.random.rand() * 1.0
        ## start a thread to call the iterate fn as
        ## frequently as possible
        Clock.schedule_interval(iterate,0.0)

        init_rvit(self,rvit_file='rvit.kv',window_size=(1000,1000)) ## <-- Starts RVIT

if __name__ == '__main__':
    model = Model()

    
