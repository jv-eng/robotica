#This script implements the evolutionary algorithm

import deap
import simulation
from fuzzy_controller import FuzzyController
from population import Population

#different solutions
class Population:
    pass

class EvolutionaryAlgorithm:
    #launches the algorithm
    def run(self):
        pass


if __name__ == '__main__':
    algorithm = EvolutionaryAlgorithm()
    read = input("Start simulation? (y/n): ")
    print(read)
    if read == 'y' or not read:
        algorithm.run()
    else:
        print("no simulation is started")