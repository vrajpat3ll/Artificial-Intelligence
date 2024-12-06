from utils.graph import Graph
import utils.genetic_algorithm as ga
import random
from typing import List


def distance(graph: Graph, city1, city2) -> float:
    return graph.getEdgeWeight(city1, city2)


def totalDistance(route: List[int], graph: Graph) -> float:
    return sum(distance(graph, route[i], route[(i+1) % len(route)]) for i in range(len(route)))


def tspFitness(route: List[int], cities) -> float:
    # Add small value to avoid division by zero
    return 1 / (totalDistance(route, cities) + 1e-10)


def solve(cities:Graph, populationSize: int = 100, generations: int = 10) -> List[int]:
    numCities = len(cities.graph)

    def fitness_func(route): return tspFitness(route, cities)

    # Initialize the genetic algorithm
    tsp_ga = ga.GeneticAlgorithm(
        populationSize=populationSize,
        chromosome_length=numCities,
        genePool=list(range(numCities)),
        fitness_func=fitness_func,
        mutationRate=0.02
    )

    # Modify the initial population to ensure valid routes (no repeated cities)
    tsp_ga.population = [random.sample(
        range(numCities), numCities) for _ in range(populationSize)]

    # Override crossover method to use Ordered Crossover (OX)
    def orderedCrossover(parent1: List[int], parent2: List[int]) -> List[int]:
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))
        child = [-1] * size
        child[start:end] = parent1[start:end]
        remaining = [gene for gene in parent2 if gene not in child]
        for i in range(size):
            if child[i] == -1:
                child[i] = remaining.pop(0)
        return child

    tsp_ga.crossover = orderedCrossover

    # Override mutation method to use Swap Mutation
    def swapMutation(route: List[int]):
        if random.random() < tsp_ga.mutation_rate:
            i, j = random.sample(range(len(route)), 2)
            route[i], route[j] = route[j], route[i]

    tsp_ga.mutate = swapMutation

    # Evolve the population
    tsp_ga.evolve(generations)

    # Return the best route found
    return tsp_ga.getBestChromosome()



numCities = 7
# cities = generate_cities(numCities)
cities = Graph(numCities)
cities.graph = [
[float('inf'), 50, 36, 28, 30, 72, 50],
[50, float('inf'), 82, 36, 58, 41, 71],
[36, 82, float('inf'), 50, 32, 92, 42],
[28, 36, 50, float('inf'), 22, 45, 36],
[30, 58, 32, 22, float('inf'), 61, 20],
[72, 41, 92, 45, 61, float('inf'), 61],
[50, 71, 42, 36, 20, 61, float('inf')]
]

best_route = solve(cities)

print(f"Best route found: {best_route}")
print(f"Total distance: {totalDistance(best_route, cities):.2f}")

# Optionally, you can plot the route here using matplotlib
