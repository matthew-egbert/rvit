from rvit.core import init_rvit
from kivy.clock import Clock
import numpy as np


class DiffusionModel(object):
    def __init__(self, *args, **kwargs):
        l,h = -0.5,0.5
        self.pos = np.array([[l,l],
                             [l,h],
                             [l,h],
                             [h,l],
                             [h,h]])

        self.inds = [0,1,3,4]
        init_rvit(self,rvit_file='rvit.kv') ## <-- Starts RVIT

if __name__ == '__main__':
    model = DiffusionModel()
    ## An alternative, equivalent way to start rvit...
    # init_rvit(model ,rvit_file='rvit.kv') 

