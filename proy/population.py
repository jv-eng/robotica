import numpy as np
from genome import Genome

class Population:

    """
    Stores the different solutons
    """

    def __init__(self, rangos):
        self.population = []
        self.rangos = rangos

        
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
        self.order(1)
        return self.population[0]
    
    def check_data(self):
        for ind in self.population:
            ind.setVector(sorted(ind.getVector()))
    
    
    #generate popultion
    def genPopulation(self,psize):
        for _ in range(psize):
            v = [
                np.random.uniform(self.rangos[0], self.rangos[1]),
                np.random.uniform(self.rangos[2], self.rangos[3]),
                np.random.uniform(self.rangos[4], self.rangos[5]),
                np.random.uniform(self.rangos[6], self.rangos[7]),
                np.random.uniform(self.rangos[8], self.rangos[9]),
                np.random.uniform(self.rangos[10], self.rangos[11]),
                np.random.uniform(self.rangos[12], self.rangos[13]),
                np.random.uniform(self.rangos[14], self.rangos[15]),
            ]
            g = Genome(v,0)
            self.population.append(g)
        #self.population = sorted(self.population) #que sean rangos normales
        return self.population