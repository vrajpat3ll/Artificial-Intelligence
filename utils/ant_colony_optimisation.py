import random
import numpy as np


class AntColonyOptimization:
    def __init__(self, numAnts, numEpochs, alpha, beta, rho, q):
        self.numAnts = numAnts
        self.numEpochs = numEpochs
        self.alpha = alpha  # pheromone importance
        self.beta = beta    # visibility importance
        self.rho = rho      # pheromone evaporation rate
        self.q = q          # pheromone deposit factor

    def initializePheromones(self, numCities):
        ans = np.ones((numCities, numCities))
        for i in range(numCities):
            ans[i][i] = 0
        return ans

    def run(self, distances, dbg=True):
        numCities = len(distances)
        pheromones = self.initializePheromones(numCities)
        bestPath = None
        bestCost = float('inf')
        
        if dbg:
            print('+' + '-' * 11 + '+' + '-' * 11 + '+')
            print(f"|{'Epoch'.center(11)}|{'Best Cost'.center(11)}|")
            print('+' + '-' * 11 + '+' + '-' * 11 + '+')
        
        for iteration in range(1, self.numEpochs + 1):
        
            if dbg:
                print(f"|{iteration:^11}|{bestCost:^11}|")
        
            paths = self.constructSolutions(distances, pheromones)
            self.updatePheromones(pheromones, paths, distances)
            for path in paths:
                cost = self.calculatePathCost(path, distances)
                if cost < bestCost:
                    bestCost = cost
                    bestPath = path

        if dbg:
            print('+' + '-' * 11 + '+' + '-' * 11 + '+')
        
        return bestPath, bestCost

    def constructSolutions(self, distances, pheromones):
        numCities = len(distances)
        paths = []

        for _ in range(self.numAnts):
            path = self.constructPath(distances, pheromones, numCities)
            paths.append(path)

        return paths

    def constructPath(self, distances, pheromones, numCities):
        unvisited = set(range(numCities))
        start = random.randint(0, numCities - 1)
        path = [start]
        unvisited.remove(start)

        while unvisited:
            current = path[-1]
            nextCity = self.selectNextCity(
                current, unvisited, distances, pheromones)
            path.append(nextCity)
            unvisited.remove(nextCity)

        return path

    def selectNextCity(self, current, unvisited, distances, pheromones):
        probabilities = []

        for city in unvisited:
            pheromone = pheromones[current][city]
            distance = distances[current][city]
            probability = (pheromone ** self.alpha) * ((1.0 / distance) ** self.beta)
            probabilities.append((city, probability))

        total = sum(prob for _, prob in probabilities)
        normalizedProbabilities = [(city, prob / total)
                                   for city, prob in probabilities]

        return self.rouletteWheelSelection(normalizedProbabilities)

    def rouletteWheelSelection(self, probabilities):
        r = random.random()
        for city, prob in probabilities:
            r -= prob
            if r <= 0:
                return city

    def updatePheromones(self, pheromones, paths, distances):
        pheromones *= (1 - self.rho)

        for path in paths:
            cost = self.calculatePathCost(path, distances)
            for i in range(len(path)):
                j = (i + 1) % len(path)
                pheromones[path[i]][path[j]] += self.q / cost

    def calculatePathCost(self, path, distances):
        return sum(distances[path[i]][path[(i + 1) % len(path)]] for i in range(len(path)))


if __name__ == "__main__":
    distances = np.array([
        [0, 50, 36, 28, 30, 72, 50],
        [50, 0, 82, 36, 58, 41, 71],
        [36, 82, 0, 50, 32, 92, 42],
        [28, 36, 50, 0, 22, 45, 36],
        [30, 58, 32, 22, 0, 61, 20],
        [72, 41, 92, 45, 61, 0, 61],
        [50, 71, 42, 36, 20, 61, 0]
    ])

    aco = AntColonyOptimization(
        numAnts=7, numEpochs=20, alpha=1, beta=3, rho=0.1, q=10)
    bestPath, bestCost = aco.run(distances)
    print(f"Best Path: {bestPath}")
    print(f"Best Cost: {bestCost}")
