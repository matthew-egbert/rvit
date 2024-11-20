from rvit.core import init_rvit
from kivy.clock import Clock
import numpy as np


class DiffusionModel(object):
    def __init__(self, *args, **kwargs):
        l,h = -1.0,1.0
        self.pos = np.array([[l,l,l],                             
                             [l,l,h],
                             [l,h,h],
                             [l,h,l],
                             [h,l,l],
                             [h,l,h],
                             [h,h,h],
                             [h,h,l],
                             ])

        self.inds = [0,1,1,2,2,3,3,0,
                     4,5,5,6,6,7,7,4,
                     0,4,1,5,2,6,3,7]
        
        self.dots = np.random.rand(100,3)*2-1

        init_rvit(self,rvit_file='rvit.kv') ## <-- Starts RVIT

if __name__ == '__main__':
    model = DiffusionModel()
    ## An alternative, equivalent way to start rvit...
    # init_rvit(model ,rvit_file='rvit.kv') 

