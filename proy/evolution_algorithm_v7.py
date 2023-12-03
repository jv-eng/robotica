#This script implements the evolutionary algorithm

import random
from fuzzy_controller import FuzzyController
from population import Population
from deap import base, creator, tools
import numpy as np


class EvolutionaryAlgorithm:

    def __init__(self, n_population, vect_ranges, sim, robot, semilla):
        self.n_population = n_population
        self.vect_ranges = vect_ranges
        self.coppelia = sim
        self.robot = robot
        #configurar semilla
        self.semilla = semilla
        np.random.seed(semilla)

    """Ejecutar algoritmo"""
    def run(self, n_ej):
        #generar poblacion
        initial_population = Population(self.vect_ranges, self.semilla)
        initial_population.genPopulation(self.n_population)

        # Definir el problema y tipos de aptitud
        creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
        creator.create("Individuo", list, fitness=creator.FitnessMax)

        # Registrar operadores genéticos
        toolbox = base.Toolbox()
        toolbox.register("evaluate", self.fitness)
        toolbox.register("select", tools.selTournament, tournsize=3)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutUniformInt, low=0, up=10, indpb=0.2)
        toolbox.register("reemplazo", tools.selBest)


        #evaluar población inicial
        print("\nEvaluando población inicial")
        fitnesses = map(toolbox.evaluate, initial_population.getPopulation())
        for ind, fit in zip(initial_population.getPopulation(), fitnesses):
            ind.setFitness(fit[0])
        
        print("\nInicio del algoritmo")
        # Ejecución de 10 generaciones
        for gen in range(n_ej):
            print(f"\nEjecución número {gen}")
            initial_population.check_data()
            # Aplicar operadores genéticos para crear la siguiente generación
            offspring = toolbox.select(initial_population.getPopulation(), len(initial_population.getPopulation()))
            offspring = [toolbox.clone(ind) for ind in offspring]

            for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < 0.5:
                    toolbox.mate(ind1.getVector(), ind2.getVector())
                    ind1.setFitness(0)
                    ind2.setFitness(0)

            for ind in offspring:
                if random.random() < 0.2:
                    toolbox.mutate(ind.getVector())
                    ind.setFitness(0)

            # Evaluar la nueva población
            fitnesses = map(toolbox.evaluate, offspring)
            for ind, fit in zip(offspring, fitnesses):
                ind.setFitness(fit[0])

            #seleccionar mejores individuos
            poblacion_combinada = offspring + initial_population.getPopulation()

            mejores_descendencia = toolbox.reemplazo(poblacion_combinada, self.n_population)

            # Reemplazar la población actual con los mejores individuos de la descendencia
            initial_population.setPopulation(mejores_descendencia)

        #print(initial_population.best())
        #initial_population.best().getFuzzy().plot()
        return initial_population.best()


    """Calcular el fitness del individuo"""
    def fitness(self, ind):
        #creamos el modelo de lógica borrosa e inciamos parámetros
        fuzzy = FuzzyController(ind.getVector(), self.semilla)
        ind.setFuzzy(fuzzy)
        cont = 0
        num_tiempo = 20
        paso = 0.05

        #arrancamos la simulación
        self.coppelia.start_simulation()

        #gestionamos la simulación
        l = np.arange(0,num_tiempo,paso)
        while (t := self.coppelia.sim.getSimulationTime()) < num_tiempo:
            tmp = round(t, 2)
            if tmp in l:
                #ver si hemos llegado a la esfera
                if self.robot.detectar_colision_porcentaje_umbral(): break
                #obtenemos posición de la esfera
                res = self.robot.detectar_esfera_roja()

                #calcular error actual
                if res:
                    ind.setErrorPasado(ind.getErrorActual())
                    ind.setErrorActual(res[0])
                else:
                    ind.setErrorActual(255)
                    
                #pasar el resultado al modelo borroso
                res_fuzzy = fuzzy.sim(ind.getErrorActual(), ind.getErrorPasado())

                #penalizar
                if fuzzy.get_etiqueta() == 'correccion muy izq' or fuzzy.get_etiqueta() == 'correccion muy dcha':
                    cont += 1
                #revisar resultado
                if res_fuzzy:
                    self.robot.set_speed(res_fuzzy[0], res_fuzzy[1])
                else:
                    self.robot.set_speed(-0.5,+0.5)

        #terminamos la simulación
        self.coppelia.stop_simulation()

        #calculamos el fitness
        res = 0
        if cont > 0:
            res = t * (1 + 1 / cont)
        else:
            res = t
        return res,
