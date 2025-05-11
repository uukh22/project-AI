## Solve N-Queens by Genetic Algorithm

### Overview
The N-Queens problem is a classic problem in combinatorial optimization, where the goal is to place N chess queens on an N×N chessboard so that no two queens threaten each other.

### How the genetic algorithm solves the n-queen problem?
- Step 1: A random chromosome is generated
- Step 2: Fitness value of the chromosome is calculated
- Step 3: If fitness is not equal to Fmax
- Step 4: Reproduce (crossover) new chromosome from 2 randomly selected best chromosomes
- Step 5: Mutation may take place
- Step 6: New chromosome added to population
- Repeat Step 2 to 6 until a chromosome (solution) with Fitness value = Fmax is found

### Features

1. **Genetic Algorithm :**
   - Utilizes a genetic algorithm to search for solutions to the N-Queens problem.

2. **Fitness Function :**
   - Calculates the fitness of each chromosome (solution candidate) based on the number of conflicts (horizontal and diagonal) between queens.

3. **Mutation and Crossover :**
   -Implements mutation and crossover operations to evolve the population of solutions over generations.
   
5. **Visualization :**
   - Generates images of the chessboard with queens placed for each generation and combines them into an animated GIF.

6. **Customizable :**
   - Allows users to specify the number of queens and population size.
