import random
from deap import base, creator, tools

# Definir el problema y tipos de aptitud
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individuo", list, fitness=creator.FitnessMax)

# Función de aptitud (Fitness function)
def evaluar_individuo(individuo):
    return sum(individuo),

# Registrar operadores genéticos
toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, -5.0, 5.0)
toolbox.register("individuo", tools.initRepeat, creator.Individuo, toolbox.attr_float, n=5)
toolbox.register("evaluate", evaluar_individuo)
toolbox.register("mate", tools.cxUniform, indpb=0.5)
toolbox.register("mutate", tools.mutUniformInt, low=-10, up=10, indpb=0.2)
toolbox.register("select", tools.selBest)

# Crear una lista de 10 individuos (población inicial)
poblacion = [toolbox.individuo() for _ in range(10)]

# Evaluación de la población inicial
aptitudes = [toolbox.evaluate(ind) for ind in poblacion]

# Mostrar los vectores y sus aptitudes en la población inicial
print("Población inicial:")
for idx, (individuo, aptitud) in enumerate(zip(poblacion, aptitudes)):
    print(f"Individuo {idx + 1}: {individuo} - Aptitud: {aptitud}")

# Aplicar operadores genéticos para crear la siguiente generación
offspring = toolbox.select(poblacion, len(poblacion))
offspring = [toolbox.clone(ind) for ind in offspring]

for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
    if random.random() < 0.5:
        toolbox.mate(ind1, ind2)
        del ind1.fitness.values
        del ind2.fitness.values

for ind in offspring:
    if random.random() < 0.2:
        toolbox.mutate(ind)
        del ind.fitness.values

# Evaluación de la nueva población
aptitudes = [toolbox.evaluate(ind) for ind in offspring]

# Mostrar los vectores y sus aptitudes en la nueva población
print("\nNueva población después de una generación:")
for idx, (individuo, aptitud) in enumerate(zip(offspring, aptitudes)):
    print(f"Individuo {idx + 1}: {individuo} - Aptitud: {aptitud}")
