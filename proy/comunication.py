'''
robotica.py

Provides the communication between CoppeliaSim robotics simulator and
external Python applications via the ZeroMQ remote API.

Copyright (C) 2023 Javier de Lope

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import numpy as np
import cv2
import time

from coppeliasim_zmqremoteapi_client import RemoteAPIClient


class Coppelia():

    def __init__(self):
        print('*** connecting to coppeliasim')
        client = RemoteAPIClient()
        self.sim = client.getObject('sim')

    def start_simulation(self):
        # print('*** saving environment')
        self.default_idle_fps = self.sim.getInt32Param(self.sim.intparam_idle_fps)
        self.sim.setInt32Param(self.sim.intparam_idle_fps, 0)
        self.sim.startSimulation()

    def stop_simulation(self):
        # print('*** stopping simulation')
        self.sim.stopSimulation()
        while self.sim.getSimulationState() != self.sim.simulation_stopped:
            time.sleep(0.1)
        # print('*** restoring environment')
        self.sim.setInt32Param(self.sim.intparam_idle_fps, self.default_idle_fps)
        print('*** done')

    def is_running(self):
        return self.sim.getSimulationState() != self.sim.simulation_stopped


class P3DX():

    num_sonar = 16
    sonar_max = 1.0
    left_speed = 0
    right_speed = 0

    def __init__(self, sim, robot_id, use_camera=False, use_lidar=False):
        self.sim = sim
        print('*** getting handles', robot_id)
        self.left_motor = self.sim.getObject(f'/{robot_id}/leftMotor')
        self.right_motor = self.sim.getObject(f'/{robot_id}/rightMotor')
        self.sonar = []
        for i in range(self.num_sonar):
            self.sonar.append(self.sim.getObject(f'/{robot_id}/ultrasonicSensor[{i}]'))
        if use_camera:
            self.camera = self.sim.getObject(f'/{robot_id}/camera')
        if use_lidar:
            self.lidar = self.sim.getObject(f'/{robot_id}/lidar')

    def get_sonar(self):
        readings = []
        for i in range(self.num_sonar):
            res,dist,_,_,_ = self.sim.readProximitySensor(self.sonar[i])
            readings.append(dist if res == 1 else self.sonar_max)
        return readings

    def get_image(self):
        img, resX, resY = self.sim.getVisionSensorCharImage(self.camera)
        img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)
        img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0)
        return img
    
    def get_lidar(self):
        data = self.sim.getStringSignal('PioneerP3dxLidarData')
        if data is None:
            return []
        else:
            return self.sim.unpackFloatTable(data)

    def set_speed(self, left_speed, right_speed):
        self.sim.setJointTargetVelocity(self.left_motor, left_speed)
        self.sim.setJointTargetVelocity(self.right_motor, right_speed)

    #obtener posicion de la esfera
    def detectar_esfera_roja(self):
        # Convertir la imagen de BGR a HSV
        hsv = cv2.cvtColor(self.get_image(), cv2.COLOR_BGR2HSV)

        # Definir el rango de colores rojos en HSV
        rango_bajo = np.array([0, 100, 100])
        rango_alto = np.array([10, 255, 255])

        # Crear una máscara utilizando el rango de colores rojos
        mascara = cv2.inRange(hsv, rango_bajo, rango_alto)

        # Encontrar contornos en la máscara
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filtrar contornos pequeños
        contornos = [c for c in contornos if cv2.contourArea(c) > 100]

        # Calcular el centro de masa de la esfera
        if contornos:
            mayor_contorno = max(contornos, key=cv2.contourArea)
            momentos = cv2.moments(mayor_contorno)
            centro_x = int(momentos['m10'] / momentos['m00'])
            centro_y = int(momentos['m01'] / momentos['m00'])
            return centro_x, centro_y
        else:
            #no hay imagen
            return None


def main(args=None):
    coppelia = Coppelia()
    robot = P3DX(coppelia.sim, 'PioneerP3DX', use_camera=True)
    robot.set_speed(+1.2, -1.2)
    coppelia.start_simulation()
    while (t := coppelia.sim.getSimulationTime()) < 15:
        print(f'Simulation time: {t:.3f} [s]')
        res = robot.detectar_esfera_roja()
        if res:
            centro_x, centro_y = res
            print("punto x: " + str(centro_x) + "\npunto y: " + str(centro_y))

    coppelia.stop_simulation()


if __name__ == '__main__':
    main()
