#executes the simulation

import comunication
from fuzzy_controller import FuzzyController
from evolution_algorithm import EvolutionaryAlgorithm


def main():
    #configure the simulation, robot and simulation 
    coppelia = comunication.Coppelia()
    robot = comunication.P3DX(coppelia.sim, 'PioneerP3DX', True)    
    robot.set_speed(+1.0, +1.0)

    #rangos
    rangos = []

    #start the simulation (max 20 seconds)
    coppelia.start_simulation()
    while (t := coppelia.sim.getSimulationTime()) < 20:
        print(f'Simulation time: {t:.3f} [s]')
    coppelia.stop_simulation()

if __name__ == '__main__':
    for i in range(2):
        print(f"{i}")
        main()