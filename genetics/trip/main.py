import random
from helpers import domain, build_schedule, cost_function

# Universidade Federal Rural de Pernambuco
# DC - Departamento de Computacao
# Inteligencia Artificial - 2021.1
# Aildson Ferreira, Thiago Ferreira

# Otimizacao de Parametros de um Classificador

# O problema gira em torno de 6 amigos que pretendem
# viajar ao mesmo destino; elas irao dividir o custo
# total da viagem (total das passagens/ passagem adi-
# cional por atraso)


def mutation(domain, reference, solution):
    i = random.randint(0, len(domain) - 1)  # position to change the value
    mutant = solution

    if random.random() < 0.5:  # probability to suffer mutation (sum or sub)
        if solution[i] != domain[i][0]:
            mutant = solution[0:i] + [solution[i] - reference] + solution[i + 1:]
        else:
            if solution[i] != domain[i][1]:
                mutant = solution[0:i] + [solution[i] + reference] + solution[i + 1:]

    return mutant


def crossover(domain, parent_1, parent_2):
    i = random.randint(1, len(domain) - 2)  # position to trim
    offspring = parent_1[0:i] + parent_2[i:]

    return offspring


def evolution(domain, cost_function, population_size=10, reference=1,
              mutation_rate=0.1, elitism=0.2, generations=100):
    population = []

    # build first population
    for i in range(population_size):
        solution = [random.randint(domain[i][0], domain[i][1])
                    for i in range(len(domain))]
        population.append(solution)

    # calculates how many individuals to be chosen for the next gen
    elitism_size = int(elitism * population_size)

    # evolutionary proccess
    for i in range(generations):
        solution_cost = [(cost_function(individual), individual)
                         for individual in population]
        solution_cost.sort()

        fittest_individuals = [individual for (_, individual) in solution_cost]

        # guarantee elitism of n%
        population = fittest_individuals[0:elitism_size]

        while len(population) < population_size:
            # here we assume a possibility to either happen a mutation or
            # a crossover
            if random.random() < mutation_rate:
                m = random.randint(0, elitism_size)
                mutant = mutation(domain, reference, fittest_individuals[m])
                population.append(mutant)
            else:
                chosen_parents = random.choices(
                    # roulette to select parents for crossover
                    fittest_individuals,
                    weights=[cost for (cost, _) in solution_cost],
                    k=2
                )
                offspring = crossover(
                    domain, chosen_parents[0],
                    chosen_parents[1])
                population.append(offspring)

    return solution_cost[0][1]


best_solution = evolution(domain, cost_function)
best_solution_cost = cost_function(best_solution)

build_schedule(best_solution)
print(f'\nTotal ${best_solution_cost}')
