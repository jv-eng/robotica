#This script implements the evolutionary algorithm

import random
from fuzzy_controller import FuzzyController
from population import Population
from deap import base, creator, tools


class EvolutionaryAlgorithm:

    def __init__(self, n_population, vect_ranges, sim, robot):
        self.n_population = n_population
        self.vect_ranges = vect_ranges
        self.coppelia = sim
        self.robot = robot

    """Ejecutar algoritmo"""
    def run(self, n_ej):
        #generar poblacion
        initial_population = Population(self.vect_ranges)
        initial_population.genPopulation(self.n_population)
        #Mostrar primera población
        print("Población inicial:")
        print(initial_population)

        # Definir el problema y tipos de aptitud
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individuo", list, fitness=creator.FitnessMax)

        # Registrar operadores genéticos
        toolbox = base.Toolbox()
        toolbox.register("evaluate", self.fitness)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
        toolbox.register("select", tools.selTournament, tournsize=3)

        # Ejecución de 10 generaciones
        for gen in range(n_ej):
            # Aplicar operadores genéticos para crear la siguiente generación
            offspring = toolbox.select(initial_population, len(initial_population))
            offspring = [toolbox.clone(ind) for ind in offspring]

            for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < 0.5:
                    toolbox.mate(ind1, ind2)
                    del ind1.fitness.values
                    del ind2.fitness.values

            for ind in offspring:
                if random.random() < 0.2:
                    toolbox.mutate(ind)
                    del ind.fitness.values

            # Evaluar la nueva población
            aptitudes = [toolbox.evaluate(ind) for ind in offspring]

            # Mostrar los vectores y sus aptitudes en la nueva población
            """print(f"\nGeneración {gen + 1}:")
            for idx, (individuo, aptitud) in enumerate(zip(offspring, aptitudes)):
                print(f"Individuo {idx + 1}: {individuo} - Aptitud: {aptitud}")"""

            # Seleccionar los mejores individuos de la descendencia para el reemplazo
            n_mejores = self.n_population / 2  # Número de mejores individuos a seleccionar
            mejores_descendencia = tools.selBest(offspring, n_mejores)

            # Reemplazar la población actual con los mejores individuos de la descendencia
            initial_population[:] = mejores_descendencia + offspring[n_mejores:]


    """Calcular el fitness del individuo"""
    def fitness(self, ind):
        #creamos el modelo de lógica borrosa
        fuzzy = FuzzyController(ind.getVector())

        #arrancamos la simulación
        self.coppelia.start_simulation()

        cont_err = 0 #contador para penalizar que se desvíe mucho
        #gestionamos la simulación
        while (t := self.coppelia.sim.getSimulationTime()) < 15:
            #comprobar si hemos llegado a la esfera
            """"""
            #obtenemos posición de la esfera
            res = self.robot.detectar_esfera_roja()
            #calcular error actual
            ind.setErrorPasado(ind.getErrorActual())
            ind.setErrorActual(res[0] - ind.getErrorActual())
            #pasar el resultado al modelo borroso
            res_fuzzy = fuzzy.sim(ind.getErrorActual(), ind.getErrorPasado())
            if fuzzy.get_etiqueta() == 'correccion muy izq' or fuzzy.get_etiqueta() == 'correccion muy dcha':
                cont += 1
            #revisar resultado
            if res_fuzzy:
                self.coppelia.set_speed(res_fuzzy[0], res_fuzzy[1])

        #terminamos la simulación
        self.coppelia.stop_simulation()

        #calculamos el fitness
        if cont_err > 0:
            ind.setFitness(t * (1 + 1 / cont_err))
        else:
            ind.setFitness(t)
