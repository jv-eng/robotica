import skfuzzy as fuzz
import numpy as np

# Funciones de membresía para la posición del objetivo
posicion = np.arange(0, 101, 1)
izquierda = fuzz.trapmf(posicion, [0, 0, 20, 40])
muy_izquierda = fuzz.trimf(posicion, [0, 20, 40])
centro = fuzz.trimf(posicion, [20, 50, 80])
derecha = fuzz.trapmf(posicion, [60, 80, 100, 100])
muy_derecha = fuzz.trapmf(posicion, [80, 100, 120, 120])

# Funciones de membresía para la medida de centrado
centrado = np.arange(0, 101, 1)
poco_centrado = fuzz.trapmf(centrado, [0, 0, 25, 50])
muy_poco_centrado = fuzz.trimf(centrado, [0, 25, 50])
centrado_en = fuzz.trimf(centrado, [25, 50, 75])
muy_centrado = fuzz.trapmf(centrado, [50, 75, 100, 100])

# Simulación de la posición del objetivo (para propósitos de prueba)
posicion_objetivo = 60

# Calcula el grado de membresía para la posición del objetivo
membership_izquierda = fuzz.interp_membership(posicion, izquierda, posicion_objetivo)
membership_muy_izquierda = fuzz.interp_membership(posicion, muy_izquierda, posicion_objetivo)
membership_centro = fuzz.interp_membership(posicion, centro, posicion_objetivo)
membership_derecha = fuzz.interp_membership(posicion, derecha, posicion_objetivo)
membership_muy_derecha = fuzz.interp_membership(posicion, muy_derecha, posicion_objetivo)

# Aplica reglas borrosas
rule1_activation = np.fmin(membership_izquierda, poco_centrado)
rule2_activation = np.fmin(membership_muy_izquierda, muy_poco_centrado)
rule3_activation = np.fmin(membership_centro, centrado_en)
rule4_activation = np.fmin(membership_derecha, muy_centrado)
rule5_activation = np.fmin(membership_muy_derecha, muy_centrado)

# Agrega las reglas
aggregated = np.fmax.reduce([rule1_activation, rule2_activation, rule3_activation, rule4_activation, rule5_activation])

# Defuzzifica para obtener la medida de centrado
medida_centrado = fuzz.defuzz(centrado, aggregated, 'centroid')

# Visualiza el resultado
print(f"Posición del objetivo: {posicion_objetivo}")
print(f"Medida de Centrado - Poco: {rule1_activation.max():.2f}")
print(f"Medida de Centrado - Muy Poco: {rule2_activation.max():.2f}")
print(f"Medida de Centrado - En: {rule3_activation.max():.2f}")
print(f"Medida de Centrado - Muy: {rule4_activation.max():.2f}")
print(f"Medida de Centrado - Muy: {rule5_activation.max():.2f}")
print(f"Resultado de la Defuzzificación (Medida de Centrado): {medida_centrado:.2f}")
