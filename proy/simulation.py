#executes the simulation

import comunication
from fuzzy_controller import FuzzyController
from evolution_algorithm_v1 import EvolutionaryAlgorithm as ea1
from evolution_algorithm_v2 import EvolutionaryAlgorithm as ea2
from evolution_algorithm_v3 import EvolutionaryAlgorithm as ea3
from evolution_algorithm_v4 import EvolutionaryAlgorithm as ea4
from evolution_algorithm_v5 import EvolutionaryAlgorithm as ea5
from evolution_algorithm_v6 import EvolutionaryAlgorithm as ea6
from evolution_algorithm_v7 import EvolutionaryAlgorithm as ea7
from evolution_algorithm_v8 import EvolutionaryAlgorithm as ea8
import random
import numpy as np


def execution(ea,semilla, ind, gen):
    #configure the simulation, robot and simulation 
    coppelia = comunication.Coppelia()
    robot = comunication.P3DX(coppelia.sim, 'PioneerP3DX', True)  
    robot.set_speed(1.0, 1.0)

    #rangos
    rangos_funciones = set()

    while len(rangos_funciones) < 16:
        rango = [random.randint(15, 240), random.randint(15, 240)]
        rango.sort()  # Ordenar los valores del rango
        rangos_funciones.add(rango[0])
        rangos_funciones.add(rango[1])

    rangos_funciones = sorted(list(rangos_funciones))

    algorithm = ea(int(ind), rangos_funciones, coppelia, robot, semilla)
    res = algorithm.run(int(gen))

    return res

    #parámetros de la simulación
    """num_ind = input("Number of individuals: ")
    num_ej = input("Number of executions: ")
    read = input(f"Start simulation with {num_ind} individuals and {num_ej} generations? (y/n): ")

    #iniciar o no simulación
    if read == 'y' or not read:
        algorithm = ea(int(num_ind), rangos_funciones, coppelia, robot, semilla)
        return algorithm.run(int(num_ej))
    else:
        print("no simulation is started")"""

def main():
    list_ea = [ea1, ea2, ea3, ea4, ea5, ea6, ea7, ea8]
    list_op = [
        "Torneo, 1 punto, uniforme, generacional", "Torneo, 1 punto, gaussiana, generacional", "Torneo, 2 puntos, uniforme, generacional",
        "Torneo, 2 puntos, gaussiana, generacional", "Torneo, 1 punto, uniforme, elitista", "Torneo, 1 punto, gaussiana, elitista",
        "Torneo, 2 puntos, uniforme, elitista", "Torneo, 2 puntos, uniforme, elitista"
        ]
    list_semillas = [0, 45, 90]
    list_gen = [10, 15]
    list_ind = [5, 8]
    best = (execution(ea1, 0, 2, 1), list_op[1], f"semilla: {0}\tnº ind: {2}\t nº gen: {1}\top: {list_op[0]}")
    list_semillas = [90]
    list_gen = [12]
    list_ind = [8]
    #ejecucion
    with open('resultados_izq.txt', 'a') as fichero:
        fichero.write("\n\n")
        for semilla in list_semillas:
            for ind in list_ind:
                for gen in list_gen:
                    for ea, op in zip(list_ea, list_op):
                        print("\n\nNUEVA EJECUCIÓN")
                        #configurar semilla
                        np.random.seed(semilla)
                        #ejecucion
                        best_ind = execution(ea, semilla, ind, gen)
                        #mostrar datos
                        tmp = f"semilla: {semilla}\tnº ind: {ind}\t nº gen: {gen}\top: {op}\n"
                        print(tmp)
                        #print(best_ind.getVector())
                        #print(best_ind.getFitness())
                        print(best_ind)
                        print("\n")
                        fichero.write(tmp)
                        fichero.write(str(best_ind))
                        #fichero.write(str(best_ind.getFitness()))
                        fichero.write("\n")
                        del best_ind


if __name__ == '__main__':
    main()
