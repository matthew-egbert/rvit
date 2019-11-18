from rvit.core import init_rvit
from kivy.clock import Clock
import numpy as np

class DiffusionModel(object):
    def __init__(self, *args, **kwargs):
        N = 10**4
        self.pos = np.zeros((N, 2))

        ## iteratively update the positions of the particles
        def iterate(arg):
            self.pos[:] = self.pos+np.random.randn(N,2)*0.01
        ## start a thread to call the iterate fn as
        ## frequently as possible
        Clock.schedule_interval(iterate,0.0)

        init_rvit(self,rvit_file='rvit.kv') ## <-- Starts RVIT

if __name__ == '__main__':
    model = DiffusionModel()
    ## An alternative, equivalent way to start rvit...
    # init_rvit(model ,rvit_file='rvit.kv') 

