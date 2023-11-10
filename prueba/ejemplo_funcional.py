import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definir los universos y conjuntos difusos
temperatura = ctrl.Antecedent(np.arange(0, 101, 1), 'temperatura')
humedad = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad')
velocidad = ctrl.Consequent(np.arange(0, 101, 1), 'velocidad')

# Definir funciones de membresía trapezoidales
temperatura['baja'] = fuzz.trapmf(temperatura.universe, [0, 0, 20, 40])
temperatura['media'] = fuzz.trapmf(temperatura.universe, [20, 40, 60, 80])
temperatura['alta'] = fuzz.trapmf(temperatura.universe, [60, 80, 100, 100])

humedad['baja'] = fuzz.trapmf(humedad.universe, [0, 0, 20, 40])
humedad['media'] = fuzz.trapmf(humedad.universe, [20, 40, 60, 80])
humedad['alta'] = fuzz.trapmf(humedad.universe, [60, 80, 100, 100])

velocidad['baja'] = fuzz.trapmf(velocidad.universe, [0, 0, 30, 45])
velocidad['media'] = fuzz.trapmf(velocidad.universe, [30, 45, 55, 80])
velocidad['alta'] = fuzz.trapmf(velocidad.universe, [55, 80, 100, 100])

# Definir reglas
regla1 = ctrl.Rule(temperatura['alta'] & humedad['baja'], velocidad['alta'])
regla2 = ctrl.Rule(temperatura['baja'] & humedad['alta'], velocidad['baja'])
regla3 = ctrl.Rule(temperatura['media'] & humedad['media'], velocidad['media'])

# Crear el sistema de control
sistema = ctrl.ControlSystem([regla1, regla2, regla3])
simulacion = ctrl.ControlSystemSimulation(sistema)

# Hacer una consulta
simulacion.input['temperatura'] = 70
simulacion.input['humedad'] = 30

# Computar el resultado
simulacion.compute()

# Obtener el resultado
print(f"La velocidad del ventilador es aproximadamente: {simulacion.output['velocidad']:.2f}")



# Graficar funciones de membresía
plt.figure(figsize=(8, 6))

# Temperatura
plt.subplot(3, 1, 1)
plt.plot(np.arange(0, 101, 1), fuzz.trapmf(temperatura.universe, [0, 0, 20, 40]), 'b', linewidth=1.5, label='Baja')
plt.plot(np.arange(0, 101, 1), fuzz.trapmf(temperatura.universe, [20, 40, 60, 80]), 'g', linewidth=1.5, label='Media')
plt.plot(np.arange(0, 101, 1), fuzz.trapmf(temperatura.universe, [60, 80, 100, 100]), 'r', linewidth=1.5, label='Alta')
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