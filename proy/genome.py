#each individual solution
class Genome:
    def __init__(self,vector,valor):
        self.vector = vector #different parameters
        self.fitness = valor #fitness
        self.err_actual = 0
        self.err_pasado = 0
        
    def __str__(self):
        return f"Vector: {self.vector}\t\nFitness: {self.valor}\n"
    
    def getErrorActual(self):
        return self.err_actual
    
    def getErrorPasado(self):
        return self.err_pasado

    def getFitness(self):
        return self.fitness

    def getVector(self):
        return self.vector
    
    def getFuzzy(self):
        return self.fuzzy
    
    def setErrorActual(self, new_value):
        self.err_actual = new_value

    def setErrorPasado(self, new_value):
        self.err_pasado = new_value

    def setFitness(self,new_value):
        self.valor = new_value

    def setVector(self,new_vector):
        self.vector = new_vector

    def setFuzzy(self, fuzzy):
        self.fuzzy = fuzzy