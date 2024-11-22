from rvit.core import init_rvit
from kivy.clock import Clock
import numpy as np

class Model(object):
    def __init__(self, *args, **kwargs):
        N = 100
        self.pos = np.zeros((3,N))

        ## iteratively update the positions of the particles
        def iterate(arg):
            ## random walk
            self.pos[0,:] += np.random.randn(N)*0.001
            self.pos[1,:] += np.random.randn(N)*0.001
            self.pos[2,:] += np.random.randn(N)*0.01

            ## with periodic boundary conditions
            self.pos[0,:] = np.mod(self.pos[0,:]+1,2.0)-1.0
            self.pos[1,:] = np.mod(self.pos[1,:]+1,2.0)-1.0
                            

        ## start a thread to call the iterate fn as
        ## frequently as possible
        Clock.schedule_interval(iterate,0.0)

        init_rvit(self,rvit_file='rvit.kv') ## <-- Starts RVIT

if __name__ == '__main__':
    model = Model()

