from pylab import *
import dill as pickle
import numpy as np
import os,sys


class TrackedValue(object):
    def __init__(self, name:str, getfn:str, should_sample):
        """
        ARGS:
            name : a machine readable name of the data being sampled
                   used as the filename of the data being stored

            getfn : a str that will be evaluated to gather the sample
                    it will use `m` to refer to a base class from which
                    the data can be gathered, e.g. m.idsm.all_nodes

            should_sample : a function fn(m) that takes the iteration
                            number and model and returns True iff it is
                            a good time to eval getfn.
        """
        self.name = name
        self.getfn = getfn
        self.should_sample = should_sample
        self.data = []

    def iterate(self,m):
        from copy import deepcopy
        if self.should_sample(m) :
            self.data.append( deepcopy(eval('m.'+self.getfn)) )

class TrackingManager(object):
    def __init__(self,name) :
        self.name = s = ''.join(filter(str.isalnum, name)) ## strips to alphanumeric
        self.trackers = []
        self.pickle_objs = {}

    def track(self,name,getfn,should_sample=lambda m:True) :
        self.trackers.append( TrackedValue(name,getfn,should_sample) )

    def add_pickle_obj(self,name,obj):
        self.pickle_objs[name] = obj

    def iterate(self,m):
        for t in self.trackers:
            t.iterate(m)

    def save(self,folder_path=None):
        if folder_path is None :
            folder_path = self.name
            
        path = folder_path
        try:
            os.makedirs(path)
        except FileExistsError:
            print("The data save dir already exists. "+
                  "You are overwriting any previous data!\n")
        try:
            os.remove('latest_output')
        except FileNotFoundError:
            print('no latest_output file to remove')
        os.symlink(path,'latest_output')

        for t in self.trackers:
            np.save(os.path.join(folder_path,f'{t.name}.npy'),t.data,allow_pickle=True)

        with open(os.path.join(folder_path,f'pickle_objs.pkl'), 'wb') as file:
            pickle.dump(self.pickle_objs, file)
        self.data_saved_at = path

    def data(self,name) :
        return [t for t in self.trackers if t.name == name][0].data

    def plot_x_against_y(self,x,y) :
        x = [t for t in self.trackers if t.name == x][0]
        y = [t for t in self.trackers if t.name == y][0]
        figure()
        plot(x.data,y.data)
        xlabel(x.name)
        ylabel(y.name)
        savefig(f'{self.data_saved_at}/{x.name}_vs_{y.name}.png',dpi=300)

    def save_additional_figure(self,name) :
        savefig(f'{self.data_saved_at}/{name}.png',dpi=300)
        
            
