from rvit.core import init_rvit
from kivy.clock import Clock
import numpy as np

class Model(object):
    def __init__(self, *args, **kwargs):
        N = 51
        self.t = 0.0
        self.track_me = np.zeros(N)

        ## iteratively update the positions of the particles
        def iterate(arg):
            self.track_me[:] = [np.sin(x*self.t) for x in np.linspace(0,1,N)]
            self.t+=0.05
        ## start a thread to call the iterate fn as
        ## frequently as possible
        Clock.schedule_interval(iterate,0.0)

        init_rvit(self,rvit_file='rvit.kv',window_size=(300,300)) ## <-- Starts RVIT

if __name__ == '__main__':
    model = Model()

    
