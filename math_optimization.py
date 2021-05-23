from random import choices, randint, randrange, random
from typing import List, Tuple


# chromosome: genetic representation of a solution
# binary number, e.g. [1, 1, 1] = 7
Chromosome = List[int]
Population = List[Chromosome]


# generates one solution, given the length
def generate_chromosome(length: int) -> Chromosome:
    return choices([0, 1], k=length)


# given the size of the population, generates one
def generate_population(size: int, chromosome_length: int) -> Population:
    return [generate_chromosome(chromosome_length) for _ in range(size)]


# calculates the distance between the number (chromosome_number) and
# the expected number (perfect_number), and returns it as a score
# (fitness_score, e.g. chromosome_number = 7, perfect_number = 7 ->
#   distance = 0, fitness_score = 100 -> 100%)
def fitness(chromosome: Chromosome, num: int) -> int:
    chromosome_number = convert_binary(chromosome)
    perfect_number = num
    distance = (perfect_number - chromosome_number)
    fitness_score = int(100 - (distance * 100) / (perfect_number))
    return fitness_score


# selection occurs as a roulette based on the fitness score
def natural_selection(population: Population, num: int):
    return choices(
        population,
        weights=[fitness(chromosome, num)
                 for chromosome in population],
        k=2
    )


def crossover(gene_a: Chromosome, gene_b: Chromosome) -> Tuple[Chromosome, Chromosome]:
    if len(gene_a) != len(gene_b):
        raise ValueError("Chromosomes must have the same length")

    length = len(gene_a)
    if length < 2:
        return gene_a, gene_b

    partition = randint(1, length - 1)
    return gene_a[0:partition] + gene_b[partition:], gene_b[0:partition] + gene_a[partition:]


def mutation(chromosome: Chromosome, num: int = 1, probability: float = 0.5) -> Chromosome:
    for _ in range(num):
        # gets a random position based on chromosome length
        index = randrange(len(chromosome))
        chromosome[index] = chromosome[index] if random(
        ) > probability else abs(chromosome[index] - 1)
    return chromosome


# convert the chromosome (list of integers) to a decimal number
def convert_binary(chromosome: Chromosome) -> int:
    # [n, n, n] -> 'nnn'
    parse_chromosome = ''.join(map(str, chromosome))
    bin_prefix = '0b'
    decimal = bin_prefix + parse_chromosome
    return int(decimal, 2)


def evolution_proccess(
        population_size: int,
        chromosome_length: int,
        expected_result: int,
        fitness_limit: int = 100,
        generation_limit: int = 100) -> Tuple[Population, int]:
    population = generate_population(population_size, chromosome_length)

    for i in range(generation_limit):
        population = sorted(
            population,
            key=lambda chromosome: fitness(chromosome, expected_result),
            reverse=True
        )
        # prevents numbers out of the expected range
        if fitness(population[0], expected_result) >= fitness_limit:
            break

        # gets the best pair of the current population
        new_population = population[0:2]

        for p in range(int(len(population) / 2) - 1):
            parents = natural_selection(population)

            offspring_a, offspring_b = crossover(parents[0], parents[1])
            offspring_a = mutation(offspring_a)
            offspring_b = mutation(offspring_b)

            new_population += [offspring_a, offspring_b]

        population = new_population

    return population, i
