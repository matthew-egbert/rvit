from kivy import platform
from kivy.config import Config

if platform == 'linux':
    ratio = 2.0
    # w = 1920/2
    w = 1500
    Config.set('graphics', 'width', str(int(w)))
    Config.set('graphics', 'height', str(int(w / 2)))
    #Config.set('graphics', 'fullscreen', 'auto')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.lang import Builder
from math import sin, cos

import numpy as np
import random

from rvit.core import init_rvit

def weighted_choice(weights):
    totals = []
    running_total = 0

    for w in weights:
        running_total += w
        totals.append(running_total)

    rnd = random.random() * running_total
    for i, total in enumerate(totals):
        if rnd < total:
            return i

class Model(object):
    def __init__(self, *args, **kwargs):
        self.w = 64
        self.fitness_landscape = np.array(np.linspace(0.5, 0.0, self.w * self.w * 4),
                                          dtype=np.float32).reshape(self.w, self.w, 4)
        self.noise_scale = 0.0
        self.lump_scale = 0.0
        self.gradient_scale = 0.1
        self.mutation_rate = 0.01
        self.POP_SIZE = 50
        self.deme_size = int(self.POP_SIZE / 2)
        self.its_per_frame = 1
        self.n_steps = 512

        self.randomize_landscape = False

        self.genomes = np.zeros((self.POP_SIZE, 2))
        self.fitnesses = np.zeros(self.POP_SIZE)
        self.mean_fitness = 0.0
        self.peak_fitness = 0.0
        self.reset()

        self.animate = False

        super(Model, self).__init__(**kwargs)

        def iterate(arg):
            self.iterate()

        Clock.schedule_interval(iterate, 1.0 / 500.0)
        self.iterate()

    def setAnimate(self, value):
        self.animate = value

    def reset(self):
        self.genomes[:] = np.random.rand(self.POP_SIZE, 2) * 0.1
        self.fitnesses[:] = np.zeros(self.POP_SIZE)

        self.it = 0

    def f(self, x, y):
        if x > 1.0 or x < 0.0 or y > 1.0 or y < 0.0:
            return - 5.0

        if self.randomize_landscape:
            if x > 0.0 and x < 0.1:
                x += 0.5
            elif x > 0.5 and x < 0.6:
                x -= 0.5
            if x > 0.1 and x < 0.2:
                x += 0.6
            elif x > 0.7 and x < 0.8:
                x -= 0.6

            if y > 0.0 and y < 0.1:
                y += 0.5
            elif y > 0.5 and y < 0.6:
                y -= 0.4
            if y > 0.1 and y < 0.2:
                y += 0.5
            elif y > 0.6 and y < 0.7:
                y -= 0.6

        v = self.lump_scale * (cos((5.0 * x)**2) - sin((5.0 * y)**2)) + \
            self.gradient_scale * (x + y) + np.random.randn() * self.noise_scale

        v = np.floor(v * self.n_steps) / self.n_steps
        return v

    def setItsPerFrame(self, ipf):
        self.its_per_frame = ipf

    def toggleRandomizeLandscape(self):
        self.randomize_landscape = not self.randomize_landscape

    def recombine(self, a_genes, b_genes):
        return [np.random.choice([a_genes[g_i], b_genes[g_i]]) for g_i in [0, 1]]

    def ga_iterate(self):
        # evaluate all fitnesses
        for i in range(self.POP_SIZE):
            self.fitnesses[i] = self.f(self.genomes[i, 0],
                                       self.genomes[i, 1])# / (0.0001 + self.max_fitness)

            
            
        # #### truncation selection
        # ## sorted_indices
        # s_i = np.argsort(self.fitnesses)
        # s_i = s_i[-1::-1]
        # N_TO_KEEP = int(self.POP_SIZE * 0.1) ## keep top 10% 
        # for i in range(N_TO_KEEP,self.POP_SIZE) :
        #     ## replace all the others as offspring of that top 10%...
        #     ## parents
        #     a_i = s_i[np.random.randint(N_TO_KEEP)]
        #     b_i = s_i[np.random.randint(N_TO_KEEP)]
        #     a_genes = self.genomes[a_i,:]
        #     b_genes = self.genomes[b_i,:]
        #     ## Q: Does this algorithm have 'elitism'?
        #     self.genomes[s_i[i]] = self.recombine(a_genes,b_genes)+np.random.randn(2)*self.mutation_rate

        # pairwise-tournament selection
        a_i = np.random.randint(self.POP_SIZE)
        deme_delta = np.random.randint(-self.deme_size, self.deme_size + 1)
        b_i = (a_i + deme_delta) % self.POP_SIZE
        a_genes = self.genomes[a_i, :]
        b_genes = self.genomes[b_i, :]
        new_genotype = np.clip(self.recombine(a_genes, b_genes) + np.random.randn(2) * self.mutation_rate,0,1)
        ## Q: Is this a 'generational' genetic algorithm?
        if self.fitnesses[a_i] > self.fitnesses[b_i]:
            self.genomes[b_i] = new_genotype
        else:
            self.genomes[a_i] = new_genotype



            
        ###############################
            
        self.mean_fitness = self.fitnesses.mean()
        self.peak_fitness = self.fitnesses.max()

    def iterate(self):
        self.min_fitness = 0.0
        self.max_fitness = 0.0

        min_value = 1000000.0
        for i in range(self.w):
            for j in range(self.w):
                y = float(i) / self.w
                x = float(j) / self.w
                value = self.f(x, y)
                self.fitness_landscape[i, j, :] = value
                if value < min_value:
                    min_value = value
                if value > self.max_fitness:
                    self.max_fitness = value

        self.fitness_landscape -= min_value
        self.fitness_landscape /= 0.001 + self.max_fitness - min_value

        for _ in range(self.its_per_frame):
            if self.animate:
                self.ga_iterate()
        self.it += 1


class ModelApp(App):
    def build(self):
        return Builder.load_file('sk.kv')

    def on_stop(self):
        skivy.disactivate()


if __name__ == '__main__':
    m = Model()
    init_rvit(m,rvit_file='rvit.kv',window_size=(300,300)) ## <-- Starts RVIT
