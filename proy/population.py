import numpy as np
from genome import Genome

class Population:

    """
    Stores the different solutons
    """

    def __init__(self):
        self.population = []

        
    def __str__(self):
        st = ""
        for i in self.population:
            st += f"Vector: {i.getVector()}\nFitness: {i.getFitness()}\n"
        return st

    #getter
    def getPopulation(self):
        return self.population

    #add a new solution
    def setPopulation(self,new_population):
        self.population = new_population

    #delete one individual of the solution
    def deleteIndividual(self,ind):
        self.population.remove(ind)

    #adds a new individual of tipe Genome
    def add_individual(self,ind):
        self.population.append(ind)

    #orders population
    def order(self,orden):
        orden = False
        if orden == 1: orden = True
        self.population = sorted(self.population, key=lambda ind: ind.getFitness(), reverse=orden)
        return self.population

    #get best solution
    def best(self):
        self.ordenar(1)
        return self.population[0]

    #generate popultion
    def genPopulation(self,population,psize):
        limit = population[0]
        for i in range(psize):
            v = range(len(population))
            v = [np.random.uniform(limit[0],limit[1]) for n in range(len(population))]
            g = Genome(v,0)
            self.population.append(g)
        return self.population