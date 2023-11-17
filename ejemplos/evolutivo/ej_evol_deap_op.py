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

# Crear una lista de 10 individuos
poblacion = [toolbox.individuo() for _ in range(10)]

# Evaluación de la población
aptitudes = [toolbox.evaluate(ind) for ind in poblacion]

# Registrar la población y mostrar los vectores y sus aptitudes
pop = list(zip(poblacion, aptitudes))
for idx, (individuo, aptitud) in enumerate(pop):
    print(f"Individuo {idx + 1}: {individuo} - Aptitud: {aptitud}")
