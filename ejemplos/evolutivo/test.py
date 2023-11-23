import random
from deap import base, creator, tools

# Definir la función de evaluación (minimizar la función cuadrática)
def evaluate(individual):
    return sum(x**2 for x in individual),  # Devuelve una coma al final para mantener el tipo de retorno como tupla

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimizar la función
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, -5.0, 5.0)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=2)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxBlend, alpha=0.5)  # Operador de cruce (crossover)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)  # Operador de mutación
toolbox.register("select", tools.selBest)  # Operador de selección

def main():
    pop = toolbox.population(n=50)
    CXPB, MUTPB, NGEN = 0.5, 0.2, 40

    print("Iniciando la evolución...")

    fitnesses = [toolbox.evaluate(ind) for ind in pop]
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("  Evaluación de la población inicial")

    for g in range(NGEN):
        print(f"Generación {g+1}/{NGEN}")

        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = [toolbox.evaluate(ind) for ind in invalid_ind]
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        combined_pop = pop + offspring  # Combinar la población actual y la generada
        pop[:] = toolbox.select(combined_pop, len(pop))  # Seleccionar los mejores individuos para la siguiente generación

        fits = [ind.fitness.values[0] for ind in pop]

        print(f"  Min fitness: {min(fits)}")

    print("Evolution completa")

    best_ind = tools.selBest(pop, 1)[0]
    print(f"Mejor individuo encontrado: {best_ind}, Fitness: {best_ind.fitness.values[0]}")

if __name__ == "__main__":
    main()
