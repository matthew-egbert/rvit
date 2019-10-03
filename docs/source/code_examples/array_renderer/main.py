from rvit.core import init_rvit
from kivy.clock import Clock
import numpy as np


class Model(object):
    def __init__(self, *args, **kwargs):
        l,h = -0.5,0.5
        r = 101
        depth = 1
        self.y = np.random.rand(r,r,depth)

        ## iteratively update the positions of the particles
        def iterate(arg):
            self.y[:,:,:] = np.random.randn(r,r,depth)
        ## start a thread to call the iterate fn as
        ## frequently as possible
        Clock.schedule_interval(iterate,0.0)

        init_rvit(self,rvit_file='rvit.kv') ## <-- Starts RVIT
        

if __name__ == '__main__':
    model = Model()

