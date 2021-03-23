
import random, time, copy
import numpy as np
from statistics import mean
from genetic.generate_from_latent import create_random_vector

class DNA:
    def __init__(self, G):
        self.genes = create_random_vector(G)

    def crossover(self, partner):
        child = copy.deepcopy(self)
        for i in range(len(self.genes[0])):
            if random.random() >= 0.5:
                child.genes[0][i] = partner.genes[0][i]
            else:
                child.genes[0][i] = self.genes[0][i]
        return child

    def mutate(self, mutation_rate):
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                self.genes[0][i] = np.random.RandomState().randn()

def generate_initial_population(quant, G):
    return [DNA(G) for _ in range(quant)]

def _build_mating_pool(population, fitness):
    mating_pool = []
    for i in range(len(population)):
        mating_pool += [population[i]] * fitness[i]
    return mating_pool

def evolve(population, fitness, mutation_rate):
    mating_pool = _build_mating_pool(population, fitness)
    new_population = []
    for _ in range(len(population)):
        mother = random.choice(population)
        father = random.choice(population)
        child = mother.crossover(father)
        child.mutate(mutation_rate)
        new_population.append(child)
    return new_population
