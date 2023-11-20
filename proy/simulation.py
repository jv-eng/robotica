#executes the simulation

import comunication
from fuzzy_controller import FuzzyController
from evolution_algorithm import EvolutionaryAlgorithm
import random


def main():
    #configure the simulation, robot and simulation 
    coppelia = comunication.Coppelia()
    robot = comunication.P3DX(coppelia.sim, 'PioneerP3DX', True)    
    robot.set_speed(-1.0, -1.0)

    #rangos
    rangos_funciones = []
    for _ in range(8):
        rango = [random.randint(0, 255), random.randint(0, 255)]
        rango.sort()  # Ordenar los valores del rango
        rangos_funciones.append(rango[0])
        rangos_funciones.append(rango[1])
    rangos_funciones.sort()
    print(rangos_funciones)

    #parámetros de la simulación
    read = input("Start simulation? (y/n): ")
    num_ind = input("Number of individuals: ")
    num_ej = input("Number of executions: ")

    #iniciar o no simulación
    if read == 'y' or not read:
        algorithm = EvolutionaryAlgorithm(int(num_ind), rangos_funciones, coppelia, robot)
        algorithm.run(int(num_ej))
    else:
        print("no simulation is started")


    """#start the simulation (max 20 seconds)
    coppelia.start_simulation()
    while (t := coppelia.sim.getSimulationTime()) < 20:
        print(f'Simulation time: {t:.3f} [s]')
    coppelia.stop_simulation()"""

if __name__ == '__main__':
    main()

"""if __name__ == '__main__':
    algorithm = EvolutionaryAlgorithm()
    read = input("Start simulation? (y/n): ")
    print(read)
    if read == 'y' or not read:
        algorithm.run()
    else:
        print("no simulation is started")"""