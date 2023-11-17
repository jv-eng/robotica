import random
from deap import base, creator, tools

# Definir el problema y tipos de aptitud
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individuo", list, fitness=creator.FitnessMax)

# Función de aptitud (Fitness function)
def evaluar_individuo(individuo):
    return sum(individuo),

# Inicializar la caja de herramientas (toolbox)
toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, -5.0, 5.0)
toolbox.register("individuo", tools.initRepeat, creator.Individuo, toolbox.attr_float, n=5)
toolbox.register("evaluate", evaluar_individuo)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# Crear una lista de 10 individuos
poblacion = [toolbox.individuo() for _ in range(10)]

aptitudes = [toolbox.evaluate(ind) for ind in poblacion]


# Mostrar la población creada
for idx, (individuo, aptitud) in enumerate(zip(poblacion, aptitudes)):
    print(f"Individuo {idx + 1}: {individuo} - Aptitud: {aptitud}")

