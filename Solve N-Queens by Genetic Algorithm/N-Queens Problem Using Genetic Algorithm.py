from operator import indexOf
import random
from PIL import Image, ImageDraw
import imageio
import os

# Making random chromosomes
def random_chromosome(size):
    return [random.randint(0, size - 1) for _ in range(size)]

# Calculating fitness
def fitness(chromosome, maxFitness):
    horizontal_collisions = (
        sum([chromosome.count(queen) - 1 for queen in chromosome]) / 2
    )
    diagonal_collisions = 0

    n = len(chromosome)
    left_diagonal = [0] * (2 * n - 1)
    right_diagonal = [0] * (2 * n - 1)
    for i in range(n):
        left_diagonal[i + chromosome[i] - 1] += 1
        right_diagonal[len(chromosome) - i + chromosome[i] - 2] += 1

    diagonal_collisions = 0
    for i in range(2 * n - 1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i] - 1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i] - 1
        diagonal_collisions += counter

    return int(maxFitness - (horizontal_collisions + diagonal_collisions))

# Doing cross_over between two chromosomes
def crossover(x, y):
    n = len(x)
    child = [0] * n
    for i in range(n):
        c = random.randint(0, 1)
        if c < 0.5:
            child[i] = x[i]
        else:
            child[i] = y[i]
    return child

# Randomly changing the value of a random index of a chromosome
def mutate(x):
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(0, n - 1)
    x[c] = m
    return x

# Calculating probability
def probability(chromosome, maxFitness):
    return fitness(chromosome, maxFitness) / maxFitness

# Roulette-wheel selection
def random_pick(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"

# Genetic algorithm
def genetic_queen(population, maxFitness):
    mutation_probability = 0.1
    new_population = []
    sorted_population = []
    probabilities = []
    for n in population:
        f = fitness(n, maxFitness)
        probabilities.append(f / maxFitness)
        sorted_population.append([f, n])

    sorted_population.sort(reverse=True)

    new_population.append(sorted_population[0][1])  # the best gen
    new_population.append(sorted_population[-1][1])  # the worst gen

    for i in range(len(population) - 2):
        chromosome_1 = random_pick(population, probabilities)
        chromosome_2 = random_pick(population, probabilities)
        child = crossover(chromosome_1, chromosome_2)

        if random.random() < mutation_probability:
            child = mutate(child)

        new_population.append(child)
        if fitness(child, maxFitness) == maxFitness:
            break

    # Print chromosomes and fitness for each generation
    print("=== Generation {} ===".format(generation))
    for chromosome in new_population:
        print("Chromosome: {}, Fitness: {}".format(chromosome, fitness(chromosome, maxFitness)))

    return new_population

# prints given chromosome
def print_chromosome(chrom, maxFitness):
    print(
        "Chromosome = {},  Fitness = {}".format(str(chrom), fitness(chrom, maxFitness))
    )

# prints given chromosome board
def print_board(chrom):
    board = []

    for x in range(nq):
        board.append(["x"] * nq)

    for i in range(nq):
        board[chrom[i]][i] = "Q"

    def print_board(board):
        for row in board:
            print(" ".join(row))

    print()
    print_board(board)

# Save board as image in a specific folder
def save_board_image(chrom, generation, nq, folder="queen_images"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    square_size = 50
    img_size = nq * square_size
    img = Image.new("RGB", (img_size, img_size), "white")
    draw = ImageDraw.Draw(img)

    for i in range(nq):
        for j in range(nq):
            top_left = (j * square_size, i * square_size)
            bottom_right = ((j + 1) * square_size, (i + 1) * square_size)
            if (i + j) % 2 == 0:
                draw.rectangle([top_left, bottom_right], fill="gray")
            else:
                draw.rectangle([top_left, bottom_right], fill="white")

    for i in range(nq):
        q_top_left = (i * square_size, chrom[i] * square_size)
        q_bottom_right = ((i + 1) * square_size, (chrom[i] + 1) * square_size)
        draw.ellipse([q_top_left, q_bottom_right], fill="red")

    img_path = os.path.join(folder, f"generation_{generation}.png")
    img.save(img_path)

if __name__ == "__main__":
    POPULATION_SIZE = 500
    images = []

    while True:
        nq = int(input("Please enter your desired number of queens (0 for exit): "))
        if nq == 0:
            break

        maxFitness = (nq * (nq - 1)) / 2
        population = [random_chromosome(nq) for _ in range(POPULATION_SIZE)]

        generation = 1
        while (
            not maxFitness in [fitness(chrom, maxFitness) for chrom in population]
            and generation < 200
        ):
            population = genetic_queen(population, maxFitness)
            if generation % 10 == 0:
                print("=== Generation {} ===".format(generation))
                print(
                    "Maximum Fitness = {}".format(
                        max([fitness(n, maxFitness) for n in population])
                    )
                )
            bestChromosome = max(population, key=lambda chrom: fitness(chrom, maxFitness))
            save_board_image(bestChromosome, generation, nq)
            images.append(imageio.imread(f"queen_images/generation_{generation}.png"))
            generation += 1

        fitnessOfChromosomes = [fitness(chrom, maxFitness) for chrom in population]

        bestChromosome = population[
            indexOf(fitnessOfChromosomes, max(fitnessOfChromosomes))
        ]

        if maxFitness in fitnessOfChromosomes:
            print("\nSolved in Generation {}!".format(generation - 1))
            print_chromosome(bestChromosome, maxFitness)
            print_board(bestChromosome)
        else:
            print(
                "\nUnfortunately, we couldn't find the answer until generation {}. The best answer that the algorithm found was:".format(
                    generation - 1
                )
            )
            print_board(bestChromosome)

        # Create GIF from saved images
        imageio.mimsave('queen_images/nqueens_evolution.gif', images, duration=0.5)