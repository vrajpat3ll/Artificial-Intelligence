from utils.genetic_algorithm import GeneticAlgorithm
from typing import List


def fitness_function(chromosome: List, clauses: List[List]) -> int:
    # fitness value = number of satisfied clauses by a chromosome/creature
    satisfiedClauses = 0
    for clause in clauses:
        if any((var > 0 and chromosome[abs(var) - 1] == True) or
               (var < 0 and chromosome[abs(var) - 1] == False) for var in clause):
            satisfiedClauses += 1
    return satisfiedClauses


def solveSAT(clauses: List[List[int]], numVariables: int, populationSize: int = 100, generations: int = 10, mutationRate: float = 0.01) -> List[int]:
    def fitness(chromosome):
        # fitness defined here so that we can know what are the clauses and use it as a paramter
        return fitness_function(chromosome, clauses)

    ga = GeneticAlgorithm(
        populationSize=populationSize,
        chromosomeLength=numVariables,
        genePool=[False, True],
        fitnessFunc=fitness,
        mutationRate=mutationRate
    )

    # run the evolution for `generations` generations
    ga.evolve(generations)
    bestSolution = ga.getBestChromosome()

    return bestSolution


# Q3. example
clauses = [
    [1, -2,-3,-4],
]

numVariables = 4
populationSize = 4
generations = 50
mutationRate = 0.02

solution = solveSAT(clauses, numVariables, populationSize,
                    generations, mutationRate)

print("Best Solution found:")
for i, value in enumerate(solution):
    print(f"x{i+1} = {value}")

print(f"Satisfied clauses: {fitness_function(
    solution, clauses)} out of {len(clauses)}")
