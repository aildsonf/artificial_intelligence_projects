from random import choices, randint, randrange, random
from typing import List, Tuple


# genetic representation of a solution, binary number, e.g. [1, 1, 1] = 7
Genome = List[int]
Population = List[Genome]


# generates one solution, given the length
def generate_genome(length: int) -> Genome:
    return choices([0, 1], k=length)


# given the size of the population, generates one
def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]


# def fitness_score(genome: Genome) -> int:
# TO-DO


# def natural_selection(population: Population, )


def crossover(gene_a: Genome, gene_b: Genome) -> Tuple[Genome, Genome]:
    if len(gene_a) != len(gene_b):
        raise ValueError("Genomes must have the same length")

    length = len(gene_a)
    if length < 2:
        return gene_a, gene_b

    partition = randint(1, length-1)
    return gene_a[0:partition] + gene_b[partition:], \
        gene_b[0:partition] + gene_a[partition:]


def mutation(genome: Genome, num: int = 1, p: float = 0.5) -> Genome:
    for _ in range(num):
        # gets a random position based on genome length
        index = randrange(len(genome))
        genome[index] = genome[index] if random(
        ) > p else abs(genome[index] - 1)
    return genome


# convert the genome (list of integers) to a decimal number
def convert_binary(genome: Genome) -> int:
    # [n, n, n] -> 'nnn'
    parse_genome = ''.join(map(str, genome))
    bin_prefix = '0b'
    decimal = bin_prefix + parse_genome
    return int(decimal, 2)


# tests
print(crossover([1, 0, 0, 1, 1], [0, 0, 1, 0, 0]))  # crossover test
print(convert_binary([1, 0, 0]))  # binary to decimal test (0b111 = 4)
print(generate_population(10, 2))  # population generation (size = 2) test
print(mutation([]))
