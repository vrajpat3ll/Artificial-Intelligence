import random
from typing import List, Any


class GeneticAlgorithm:
    def __init__(self, populationSize: int, chromosomeLength: int, genePool: List,
                 fitnessFunc, mutationRate: float = 0.01):
        self.populationSize = populationSize
        self.chromosomeLength = chromosomeLength
        self.genePool = genePool
        self.fitnessFunc = fitnessFunc
        self.mutationRate = mutationRate
        self.population = self.initializePopulation()

    def initializePopulation(self):
        # list of chromosomes (which are lists, themselves)
        return [[random.choice(self.genePool) for _ in range(self.chromosomeLength)]
                for _ in range(self.populationSize)]

    def evaluateFitness(self):
        # list of fitness values for each chromosome/creature in population
        return [self.fitnessFunc(chromosome) for chromosome in self.population]

    def selectParents(self, fitnesses):
        # Tournament selection
        tournamentSize = self.populationSize
        selected = []
        
        # just to select 2 parents for crossover
        for _ in range(2):
            tournament = random.sample(
                list(zip(self.population, fitnesses)), tournamentSize)
            selected.append(max(tournament, key=lambda x: x[1])[0])
        return selected

    def crossover(self, parent1, parent2):
        # Single-point crossover

        # excluding first and last index so that we get features from both parents
        crossoverPoint = random.randint(1, self.chromosomeLength - 2)
        return parent1[:crossoverPoint] + parent2[crossoverPoint:]

    def mutate(self, chromosome):
        for i in range(self.chromosomeLength):
            if random.random() < self.mutationRate:
                # randomly choose gene from gene pool with equal probability
                chromosome[i] = random.choice(self.genePool)

    def evolve(self, generations: int, dbg: bool = True):

        if dbg:
            print('+' + '-' * 13 + '+' + '-' * 23 + '+')
            print(f"|{'Generation'.center(13)}|{'Best Fitness'.center(23)}|")
            print('+' + '-' * 13 + '+' + '-' * 23 + '+')

        for generation in range(1, generations + 1):
            fitnesses = self.evaluateFitness()

            eliteIndex = fitnesses.index(max(fitnesses))
            newPopulation = [self.population[eliteIndex].copy()]

            while len(newPopulation) < self.populationSize:
                parents = self.selectParents(fitnesses)
                child = self.crossover(parents[0], parents[1])
                self.mutate(child)
                newPopulation.append(child)

            self.population = newPopulation
            bestFitness = max(self.evaluateFitness())

            if dbg:
                print(f"|{generation:^13}|{bestFitness:^23}|")
        if dbg:
            print('+' + '-' * 13 + '+' + '-' * 23 + '+')

    def getBestChromosome(self) -> List[Any]:
        fitnesses = self.evaluateFitness()
        return self.population[fitnesses.index(max(fitnesses))]
