import numpy as np

# Establecer la semilla aleatoria en 42
np.random.seed(42)

# Generar números aleatorios usando la semilla establecida
random_array = np.random.rand(5)
print("Números aleatorios generados con la semilla 42:", random_array)

# Cambiar la semilla a otro número
np.random.seed(100)

# Generar nuevos números aleatorios usando la nueva semilla
new_random_array = np.random.rand(5)
print("Números aleatorios generados con la semilla 100:", new_random_array)
