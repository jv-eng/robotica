import skfuzzy as fuzz
import numpy as np
import matplotlib.pyplot as plt

# Definir los límites del universo y los parámetros de los trapecios
x = np.linspace(0, 10, 1000)

# Definir parámetros para los trapecios
trapecio1 = [1, 2, 3, 4]  # Parámetros del primer trapecio
trapecio2 = [3, 4, 5, 6]  # Parámetros del segundo trapecio
trapecio3 = [5, 6, 7, 8]  # Parámetros del tercer trapecio

# Crear funciones de membresía trapezoidales
membresia1 = fuzz.trapmf(x, trapecio1)
membresia2 = fuzz.trapmf(x, trapecio2)
membresia3 = fuzz.trapmf(x, trapecio3)

# Graficar las funciones de membresía
plt.figure()
plt.plot(x, membresia1, 'b', linewidth=1.5, label='Trapecio 1')
plt.plot(x, membresia2, 'g', linewidth=1.5, label='Trapecio 2')
plt.plot(x, membresia3, 'r', linewidth=1.5, label='Trapecio 3')
plt.title('Conjuntos Difusos Trapezoidales')
plt.xlabel('Valor')
plt.ylabel('Membresía')
plt.legend()
plt.show()
