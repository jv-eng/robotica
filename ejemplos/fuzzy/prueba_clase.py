import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class Fuzzy:
    def __init__(self, tmp, h, v):
        self.temperatura = ctrl.Antecedent(np.arange(0, 101, 1), 'temperatura')
        self.humedad = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad')
        self.velocidad = ctrl.Consequent(np.arange(0, 101, 1), 'velocidad')

        self.temperatura['baja'] = fuzz.trapmf(self.temperatura.universe, tmp[0])
        self.temperatura['media'] = fuzz.trapmf(self.temperatura.universe, tmp[1])
        self.temperatura['alta'] = fuzz.trapmf(self.temperatura.universe, tmp[2])

        self.humedad['baja'] = fuzz.trapmf(self.humedad.universe, h[0])
        self.humedad['media'] = fuzz.trapmf(self.humedad.universe, h[1])
        self.humedad['alta'] = fuzz.trapmf(self.humedad.universe, h[2])

        self.velocidad['baja'] = fuzz.trapmf(self.velocidad.universe, v[0])
        self.velocidad['media'] = fuzz.trapmf(self.velocidad.universe, v[1])
        self.velocidad['alta'] = fuzz.trapmf(self.velocidad.universe, v[2])

        regla1 = ctrl.Rule(self.temperatura['alta'] & self.humedad['baja'], self.velocidad['alta'])
        regla11 = ctrl.Rule(self.temperatura['alta'] & self.humedad['media'], self.velocidad['alta'])
        regla12 = ctrl.Rule(self.temperatura['alta'] & self.humedad['alta'], self.velocidad['media'])
        regla2 = ctrl.Rule(self.temperatura['baja'] & self.humedad['alta'], self.velocidad['baja'])
        regla22 = ctrl.Rule(self.temperatura['baja'] & self.humedad['media'], self.velocidad['media'])
        regla23 = ctrl.Rule(self.temperatura['baja'] & self.humedad['baja'], self.velocidad['media'])
        regla3 = ctrl.Rule(self.temperatura['media'] & self.humedad['media'], self.velocidad['media'])
        regla32 = ctrl.Rule(self.temperatura['media'] & self.humedad['baja'], self.velocidad['alta'])
        regla33 = ctrl.Rule(self.temperatura['media'] & self.humedad['alta'], self.velocidad['baja'])

        sistema = ctrl.ControlSystem([regla1,regla11,regla12, regla2,regla22,regla23, regla3,regla32,regla33])
        self.simulacion = ctrl.ControlSystemSimulation(sistema)

    def sim(self, tmp, h):
        self.simulacion.input['temperatura'] = tmp
        self.simulacion.input['humedad'] = h
        self.simulacion.compute()
        resultado_velocidad = self.simulacion.output['velocidad']

        etiqueta_velocidad = None
        if resultado_velocidad <= 50:
            etiqueta_velocidad = 'Baja'
        elif resultado_velocidad <= 80:
            etiqueta_velocidad = 'Media'
        else:
            etiqueta_velocidad = 'Alta'
        return [resultado_velocidad, etiqueta_velocidad]

    def plot(self):
        plt.figure(figsize=(8, 6))

        # Temperatura
        plt.subplot(3, 1, 1)
        plt.plot(np.arange(0, 101, 1), fuzz.trapmf(self.temperatura.universe, [0, 0, 20, 40]), 'b', linewidth=1.5, label='Baja')
        plt.plot(np.arange(0, 101, 1), fuzz.trapmf(self.temperatura.universe, [20, 40, 60, 80]), 'g', linewidth=1.5, label='Media')
        plt.plot(np.arange(0, 101, 1), fuzz.trapmf(self.temperatura.universe, [60, 80, 100, 100]), 'r', linewidth=1.5, label='Alta')
        plt.title('Temperatura')
        plt.xlabel('Valor')
        plt.ylabel('Membresía')
        plt.legend()

        # Humedad
        plt.subplot(3, 1, 2)
        plt.plot(np.arange(0, 101, 1), fuzz.trapmf(np.arange(0, 101, 1), [0, 0, 20, 40]), 'b', linewidth=1.5, label='Baja')
        plt.plot(np.arange(0, 101, 1), fuzz.trapmf(np.arange(0, 101, 1), [20, 40, 60, 80]), 'g', linewidth=1.5, label='Media')
        plt.plot(np.arange(0, 101, 1), fuzz.trapmf(np.arange(0, 101, 1), [60, 80, 100, 100]), 'r', linewidth=1.5, label='Alta')
        plt.title('Humedad')
        plt.xlabel('Valor')
        plt.ylabel('Membresía')
        plt.legend()

        # Velocidad
        plt.subplot(3, 1, 3)
        plt.plot(np.arange(0, 101, 1), fuzz.trapmf(np.arange(0, 101, 1), [0, 0, 30, 45]), 'b', linewidth=1.5, label='Baja')
        plt.plot(np.arange(0, 101, 1), fuzz.trapmf(np.arange(0, 101, 1), [30, 45, 55, 80]), 'g', linewidth=1.5, label='Media')
        plt.plot(np.arange(0, 101, 1), fuzz.trapmf(np.arange(0, 101, 1), [55, 80, 100, 100]), 'r', linewidth=1.5, label='Alta')
        plt.title('Velocidad')
        plt.xlabel('Valor')
        plt.ylabel('Membresía')
        plt.legend()

        plt.tight_layout()
        plt.show()


#programa
f = Fuzzy([[0, 0, 20, 40],[20, 40, 60, 80],[60, 80, 100, 100]],
          [[0, 0, 20, 40],[20, 40, 60, 80],[60, 80, 100, 100]],
          [[0, 0, 30, 45],[30, 45, 55, 80],[55, 80, 100, 100]])

res = f.sim(70,30)
print(f"simulacion: {res[0]:.2f}")
print(f"etiqueta: {res[1]}")

f.plot()