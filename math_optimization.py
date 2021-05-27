from random import choices, randint, randrange, random
from typing import List, Tuple


# chromosome: genetic representation of a solution
# binary number, e.g. [1, 1, 1] = 7
Population = List[str]
Polynomial = List[int]


# generates one solution, given the length
def generate_chromosome(length: int) -> str:
    chromosome = ''
    gene = ''
    for _ in range(length):
        temp = str(randint(0, 1))
        gene += temp

    if(random() < 0.5):
        chromosome = '+0b' + gene
    else:
        chromosome = '-0b' + gene

    return chromosome


# given the size of the population, generates one
def generate_population(size: int, chromosome_length: int) -> Population:
    return [generate_chromosome(chromosome_length) for _ in range(size)]


###############################################################


# calculates the distance between the number (chromosome_number) and
# the expected number (perfect_number), and returns it as a score
# (fitness_score, e.g. chromosome_number = 7, perfect_number = 7 ->
#   distance = 0, fitness_score = 100 -> 100%)
def fitness(chromosome: str, expected_number: int) -> int:
    chromosome_number = convert_binary(chromosome)
    score = (
        int(100 - ((expected_number - chromosome_number) * 100) / (expected_number)))

    if score >= 85 and score <= 100:
        return score
    else:
        return 1


###############################################################


# selection occurs as a roulette based on the fitness score
def natural_selection(population: Population, expected_number: int):
    return choices(
        population,
        weights=[fitness(chromosome, expected_number)
                 for chromosome in population],
        k=2
    )


###############################################################


def crossover(gene_a: str, gene_b: str) -> Tuple[str, str]:
    if len(gene_a) != len(gene_b):
        raise ValueError("Chromosomes must have the same length")

    length = len(gene_a)
    if length < 4:
        return gene_a, gene_b

    partition = randint(3, length - 1)
    return gene_a[0: partition] + gene_b[partition:], gene_b[0: partition] + gene_a[partition:]


###############################################################


def mutation(chromosome: str, num: int = 1, probability: float = 0.5) -> str:
    for _ in range(num):
        # gets a random position based on chromosome length
        index = randrange(3, len(chromosome))
        mutated = list(chromosome)

        if(random() <= probability):
            if(mutated[index] == '1'):
                mutated[index] = '0'
            else:
                mutated[index] = '1'

        chromosome = "".join(mutated)
    return chromosome


###############################################################


# convert the chromosome (str) to a decimal number
def convert_binary(chromosome: str) -> int:
    return int(chromosome, 2)


###############################################################


def evolution_proccess(
        population_size: int,
        chromosome_length: int,
        expected_number: int,
        generation_limit: int = 100) -> Tuple[Population, str, int, int]:
    population = generate_population(population_size, chromosome_length)
    generation = 0
    iterator = 0

    result_unknown = True
    result_number = 0
    result_fitness = 0

    while(iterator < generation_limit and result_unknown):
        for x in (population):
            if(fitness(x, expected_number) == 100):
                result_number = convert_binary(x)
                result_fitness = 100
                result_unknown = False
                break
            elif(fitness(x, expected_number) > result_fitness):
                result_fitness = fitness(x, expected_number)
                result_number = convert_binary(x)

        population = sorted(
            population,
            key=lambda chromosome: fitness(chromosome, expected_number),
            reverse=True
        )

        # gets the best pair of the current population
        new_population = population[0:2]

        for _ in range(int(len(population) / 2) - 1):
            parents = natural_selection(population, expected_number)

            offspring_a, offspring_b = crossover(
                parents[0], parents[1])
            offspring_a = mutation(offspring_a)
            offspring_b = mutation(offspring_b)

            new_population += [offspring_a, offspring_b]

        population = new_population
        iterator += 1
        generation += 1

    return generation, population, result_number, result_fitness


def main():
    expected_result = 31
    test = evolution_proccess(10, 5, expected_result)
    print(
        f"Population: {test[1]}\n\nGeneration: {test[0]}\n")
    print(
        f"Best Result: {test[2]}\n")
    if(test[3] < 85 or test[3] > 100):
        print("Fitness is out of boundaries due to elitism.")
    else:
        print(f"Fitness Score: {test[3]}")


if __name__ == "__main__":
    main()
