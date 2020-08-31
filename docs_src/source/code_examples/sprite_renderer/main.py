from rvit.core import init_rvit
from kivy.clock import Clock
import numpy as np

class Model(object):
    def __init__(self, *args, **kwargs):
        self.pos = np.zeros((3,1))

        ## iteratively update the positions of the particles
        def iterate(arg):
            self.pos[:2,0] = [self.pos[0]+np.random.randn()*0.01,
                              self.pos[1]+np.random.randn()*0.01]
            self.pos[2,0] += np.random.rand()*0.01

        ## start a thread to call the iterate fn as
        ## frequently as possible
        Clock.schedule_interval(iterate,0.0)

        init_rvit(self,rvit_file='rvit.kv') ## <-- Starts RVIT

if __name__ == '__main__':
    model = Model()

