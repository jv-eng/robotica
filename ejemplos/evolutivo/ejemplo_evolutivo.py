import random

# Función de evaluación (Fitness)
def evaluar_individuo(vector):
    # Suma de los componentes del vector como función de aptitud
    aptitud = sum(vector)
    return aptitud

# Función para crear un individuo aleatorio
def crear_individuo(longitud):
    return [random.uniform(-5.0, 5.0) for _ in range(longitud)]

# Función para crear una población inicial
def crear_poblacion(tamano_poblacion, longitud_individuo):
    return [crear_individuo(longitud_individuo) for _ in range(tamano_poblacion)]

# Algoritmo evolutivo
def algoritmo_evolutivo(tamano_poblacion, longitud_individuo, num_generaciones):
    poblacion = crear_poblacion(tamano_poblacion, longitud_individuo)
    
    for gen in range(num_generaciones):
        # Evaluación de la población actual
        aptitudes = [evaluar_individuo(individuo) for individuo in poblacion]
        
        # Selección de padres (selecciona dos padres aleatorios)
        padres = random.choices(poblacion, weights=aptitudes, k=2)
        
        # Cruzar los padres para crear descendencia
        punto_cruce = random.randint(1, longitud_individuo - 1)
        descendencia = padres[0][:punto_cruce] + padres[1][punto_cruce:]
        
        # Aplicar mutación a la descendencia
        prob_mutacion = 0.1
        for i in range(longitud_individuo):
            if random.random() < prob_mutacion:
                descendencia[i] += random.uniform(-0.5, 0.5)
        
        # Reemplazar al peor individuo con la descendencia
        peor_indice = aptitudes.index(min(aptitudes))
        poblacion[peor_indice] = descendencia
    
    # Retornar la mejor solución
    aptitudes = [evaluar_individuo(individuo) for individuo in poblacion]
    mejor_indice = aptitudes.index(max(aptitudes))
    return poblacion[mejor_indice], max(aptitudes)

# Parámetros del algoritmo
tamano_poblacion = 50
longitud_individuo = 10
num_generaciones = 100

# Ejecutar el algoritmo evolutivo
mejor_solucion, mejor_aptitud = algoritmo_evolutivo(tamano_poblacion, longitud_individuo, num_generaciones)

# Mostrar la mejor solución y su aptitud
print("Mejor solución encontrada:", mejor_solucion)
print("Mejor aptitud encontrada:", mejor_aptitud)
