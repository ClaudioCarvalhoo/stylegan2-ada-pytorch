
import random, time, copy
import numpy as np
from statistics import mean
from genetic.generate_from_latent import create_random_vector

class DNA:
    def __init__(self, G):
        self.genes = create_random_vector(G)

    def crossover(self, partner, G):
        child = DNA(G)
        for i in range(len(self.genes[0])):
            if random.random() >= 0.5:
                child.genes[0][i] = partner.genes[0][i]
            else:
                child.genes[0][i] = self.genes[0][i]
        return child

    def mutate(self, mutation_rate):
        for i in range(len(self.genes[0])):
            mutation = random.random()
            if mutation < mutation_rate:
                self.genes[0][i] = np.random.RandomState().randn()

class Population:
    def __init__(self, G, population_size):
        self.G = G
        self.individuals = [DNA(G) for _ in range(population_size)]

    def _build_mating_pool(self, fitness):
        mating_pool = []
        for i in range(len(self.individuals)):
            mating_pool += [self.individuals[i]] * fitness[i]
        if len(mating_pool) <= 0:
            mating_pool = [DNA(self.G) for _ in range(len(self.individuals))]
        return mating_pool

    def evolve(self, fitness, mutation_rate):
        mating_pool = self._build_mating_pool(fitness)
        new_individuals = []
        for _ in range(len(self.individuals)):
            mother = random.choice(mating_pool)
            father = random.choice(mating_pool)
            child = mother.crossover(father, self.G)
            child.mutate(mutation_rate)
            new_individuals.append(child)
        self.individuals = new_individuals
