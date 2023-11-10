#each individual solution
class Genome:
    def __init__(self,vector,valor):
        self.vector = vector #different parameters
        self.fitness = valor #fitness
        
    def __str__(self):
        return f"Vector: {self.vector}\t\nFitness: {self.valor}\n"

    def getFitness(self):
        return self.valor

    def getVector(self):
        return self.vector

    def setFitness(self,new_value):
        self.valor = new_value

    def setVector(self,new_vector):
        self.vector = new_vector