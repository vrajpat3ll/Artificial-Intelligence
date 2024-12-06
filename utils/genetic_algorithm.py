import random
from typing import List, Callable, Any


class GeneticAlgorithm:
    def __init__(self, populationSize: int, chromosome_length: int, genePool,
                 fitness_func, mutationRate: float = 0.01):
        self.populationSize = populationSize
        self.chromosome_length = chromosome_length
        self.genePool = genePool
        self.fitness_func = fitness_func
        self.mutationRate = mutationRate
        self.population = self.initializePopulation()

    def initializePopulation(self):
        # Return a list of chromosomes instead of Individuals
        return [[random.choice(self.genePool) for _ in range(self.chromosome_length)]
                for _ in range(self.populationSize)]

    def evaluateFitness(self):
        # Return a list of fitness values
        return [self.fitness_func(chromosome) for chromosome in self.population]

    def selectParents(self, fitnesses):
        # Tournament selection
        tournamentSize = 3
        selected = []
        for _ in range(2):
            tournament = random.sample(
                list(zip(self.population, fitnesses)), tournamentSize)
            selected.append(max(tournament, key=lambda x: x[1])[0])
        return selected

    def crossover(self, parent1, parent2):
        # Single-point crossover
        crossover_point = random.randint(1, self.chromosome_length - 1)
        return parent1[:crossover_point] + parent2[crossover_point:]

    def mutate(self, chromosome):
        for i in range(self.chromosome_length):
            if random.random() < self.mutationRate:
                chromosome[i] = random.choice(self.genePool)

    def evolve(self, generations: int, dbg: bool = True):

        if dbg:
            print('+' + '-' * 13 + '+' + '-' * 23 + '+')
            print(f"|{'Generation'.center(13)}|{'Best Fitness'.center(23)}|")
            print('+' + '-' * 13 + '+' + '-' * 23 + '+')

        for generation in range(1, generations + 1):
            fitnesses = self.evaluateFitness()

            # Elitism: keep the best chromosome
            eliteIndex = fitnesses.index(max(fitnesses))
            newPopulation = [self.population[eliteIndex].copy()]

            while len(newPopulation) < self.populationSize:
                parents = self.selectParents(fitnesses)
                child = self.crossover(parents[0], parents[1])
                self.mutate(child)
                newPopulation.append(child)

            self.population = newPopulation
            best_fitness = max(self.evaluateFitness())

            if dbg:
                print(f"|{generation:^13}|{best_fitness:^23}|")
        if dbg:
            print('+' + '-' * 13 + '+' + '-' * 23 + '+')

    def getBestChromosome(self) -> List[Any]:
        fitnesses = self.evaluateFitness()
        return self.population[fitnesses.index(max(fitnesses))]


if __name__ == "__main__":
    # Example usage:
    def example_fitness_function(chromosome: List[int]) -> float:
        return sum(chromosome)
    
    ga = GeneticAlgorithm(
        populationSize=100,
        chromosome_length=10,
        genePool=list(range(10)),
        fitness_func=example_fitness_function,
        mutationRate=0.01,
        dbg=True
    )

    ga.evolve(generations=50)
    best_chromosome = ga.get_best_chromosome()
    print(f"\nBest Chromosome: {best_chromosome}, Fitness: {
          example_fitness_function(best_chromosome)}")
