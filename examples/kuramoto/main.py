from kivy import platform
from kivy.config import Config
Config.set('kivy', 'log_level', 'debug')  # Set the log level to 'debug'

if platform == 'linux':    
    ratio = 2.0
    # w = 1920/2
    w = 1200
    Config.set('graphics', 'width', str(int(w)))
    Config.set('graphics', 'height', str(int(w / 2)))
    #Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'fullscreen', 'false')

# from kivy.logger import Logger
# Logger.setLevel(LOG_LEVELS["debug"])
# Logger.info('title: This is a info message.')
# Logger.debug('title: This is a debug message.')


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

# from kivy.uix.floatlayout import FloatLayout
# from kivy.lang import Builder

from itertools import combinations
import cmath
import numpy as np

import networkx as nx

from rvit.core import init_rvit

class KOsc(object):
    def __init__(self, model, x, y):
        self.model = model
        self.x = x
        self.y = y
        self.state = np.random.rand() * 2.0 * np.pi

        self.N = model.N
        self.base_omega = 0.5
        self.omega_variation = np.random.randn()
        self.connections = {}

    def addConnectionTo(self, other_node, weight):
        self.connections[other_node] = weight

    def prepareToIterate(self):
        summation = 0.0
        for other_node, weight in self.connections.items():
            # summation += weight*np.sin(other_node.state-self.state) ## disabling weight
            summation += np.sin(other_node.state - self.state)
        N_CONNECTIONS = max(1, len(self.connections))
        self.dstate = (self.base_omega +
                       self.omega_variation * self.model.omega_variation_scale +
                       (self.model.weight_scale / N_CONNECTIONS) * summation)

    def iterate(self):
        DT = 0.05
        self.state += DT * self.dstate
        self.state = np.fmod(self.state, np.pi * 2.0)


class Model(object):
    def __init__(self, *args, **kwargs):
        self.it = 0
        self.G = nx.balanced_tree(4, 4)
        # #self.G = nx.erdos_renyi_graph(200,0.02)
        # #self.G = nx.scale_free_graph(200)
        self.draw_frequency = 1.0

        self.N = self.G.number_of_nodes()
        self.weight_scale = 1.0
        self.omega_variation_scale = 0.5
        self.max_dstate = 1.0

        # self.degrees = np.array([float(self.G.degree(x)) for x in xrange(self.N)])
        # self.degrees /= self.degrees.max()

        pos = nx.drawing.nx_pydot.graphviz_layout(self.G, prog='neato')
        xs = np.array([x-1 for x, y in pos.values()])
        ys = np.array([y for x, y in pos.values()])
        for key in pos.keys():
            x, y = pos[key]
            x = x / abs(xs).max()
            y = y / abs(ys).max()
            x = (x*2-1.0)*0.9
            y = (y*2-1.0)*0.9
            pos[key] = x, y
            x, y = pos[key]
            
        self.oscs = [KOsc(self, pos[index][0], pos[index][1]) for index in range(self.N)]


        self.node_edges = []
        c = 0
        for vertex_a, vertex_b in self.G.edges():
            c += 1
            a = self.oscs[vertex_a]
            b = self.oscs[vertex_b]
            a.addConnectionTo(b, 1.0)
            b.addConnectionTo(a, 1.0)
            self.node_edges += [[a.x, a.y], ]
            self.node_edges += [[b.x, b.y], ]
        self.node_edges = np.array(self.node_edges, dtype=float)

        self.node_positions = np.zeros((self.N, 2), dtype=float)
        self.node_positions[:, 0] = [o.x for o in self.oscs]
        self.node_positions[:, 1] = [o.y for o in self.oscs]

        self.node_phases = np.zeros((self.N), dtype=float)
        self.node_phases[:] = [o.state for o in self.oscs]  # used to color nodes by their phase

        self.phase_plot_positions = np.zeros_like(self.node_positions, dtype=float)

        self.N_SYNCHRONY_MEASURES = 1024
        self.synchrony = 0.0
        # self.synchrony = np.zeros((self.N_SYNCHRONY_MEASURES, 2), dtype=float32)
        # self.synchrony[:, 0] = np.linspace(0, 1, self.N_SYNCHRONY_MEASURES)
        self.synchrony_vector = np.array([0.0, 0.0,
                                          0.0, 1.0], dtype=float).reshape([2, 2])

        #super(Model, self).__init__(**kwargs)

        self.leaf_nodes = self.get_leaf_nodes(self.G)
        def iterate(arg):
            self.iterate()

        Clock.schedule_interval(iterate, 1.0 / 500.0)
        print('constructor done')

    def get_leaf_nodes(self, network):
        return [x for x in network.nodes() if network.degree(x) == 1]

    def calculateKuramotoOrderParameter(self):
        """ calculate Kuramoto order parameter r, the degree of synchrony """
        return sum([np.exp(1j * complex(osc.state)) for osc in self.oscs]) / self.N

    def iterate(self):
        pass
        for _ in range(int(self.draw_frequency)):
            for o in self.oscs:
                o.prepareToIterate()
            for o in self.oscs:
                o.iterate()

        # print(self.leaf_nodes)         
        # for node in self.leaf_nodes:
        #     self.oscs[node].state = 0.0

        current_max_dstate = max([o.dstate for o in self.oscs])
        if self.max_dstate > 3.0 * current_max_dstate:
            self.max_dstate /= 2.0
        elif self.max_dstate < current_max_dstate:
            self.max_dstate *= 1.25

        self.updateDrawnArrays()
        self.it += 1

    def updateDrawnArrays(self):
        # radius is node index
        node_indices = np.linspace(0.1, 1.0, self.N)
        self.phase_plot_positions[:, 0] = [
            0.9 * np.cos(o.state) * d for o, d in zip(self.oscs, node_indices)]
        self.phase_plot_positions[:, 1] = [
            0.9 * np.sin(o.state) * d for o, d in zip(self.oscs, node_indices)]

        self.node_phases[:] = [o.state / (2.0 * np.pi) for o in self.oscs]  # node color

        kop = self.calculateKuramotoOrderParameter()
        self.synchrony =cmath.polar(kop)[0]
        # self.synchrony[self.it % self.N_SYNCHRONY_MEASURES, 1] = cmath.polar(kop)[0]
        self.synchrony_vector[1, :] = [kop.real, kop.imag]




if __name__ == '__main__':
    pass
    m = Model()
    init_rvit(m,rvit_file='rvit.kv',window_size=(500,250))
    # skivy.activate()
    # ModelApp().run()
