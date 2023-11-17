#This script implements the evolutionary algorithm

import deap
import comunication
from fuzzy_controller import FuzzyController
from population import Population


class EvolutionaryAlgorithm:

    def __init__(self, n_population, vect_ranges, sim, robot):
        self.n_population = n_population
        self.vect_ranges = vect_ranges
        self.sim = sim
        self.robot = robot

    """Ejecutar algoritmo"""
    def run(self, n_ej):
        #generar poblacion
        initial_population = Population(self.vect_ranges)
        initial_population.genPopulation(self.n_population)

        #ejecutar algoritmo
        for i in range(0, n_ej):
            pass

    def fitness(self):
        pass


"""if __name__ == '__main__':
    algorithm = EvolutionaryAlgorithm()
    read = input("Start simulation? (y/n): ")
    print(read)
    if read == 'y' or not read:
        algorithm.run()
    else:
        print("no simulation is started")"""