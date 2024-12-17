import random
import numpy as np
import threading as T

class AntColonyOptimization:
    def __init__(self, numAnts, numEpochs, alpha, beta, rho, q):
        self.numAnts = numAnts
        self.numEpochs = numEpochs
        self.alpha = alpha  # pheromone importance
        self.beta = beta    # visibility importance
        self.rho = rho      # pheromone evaporation rate
        self.q = q          # pheromone deposit factor

    def initializePheromones(self, numCustomers):
        ans = np.ones((numCustomers, numCustomers))
        for i in range(numCustomers):
            ans[i][i] = 0
        return ans

    def run(self, distances, capacityOfEachVehicle, dbg=True):
        numCustomers = len(distances)
        pheromones = self.initializePheromones(numCustomers)
        bestPath = None
        bestCost = float('inf')

        if dbg:
            print('+' + '-' * 11 + '+' + '-' * 11 + '+')
            print(f"|{'Epoch'.center(11)}|{'Best Cost'.center(11)}|")
            print('+' + '-' * 11 + '+' + '-' * 11 + '+')

        for iteration in range(1, self.numEpochs + 1):

            if dbg:
                print(f"|{iteration:^11}|{bestCost:^11}|")

            paths = self.constructSolutions(distances, capacityOfEachVehicle, pheromones)
            self.updatePheromones(pheromones, paths, distances)
            for path in paths:
                cost = self.calculatePathCost(path, distances)
                if cost < bestCost:
                    bestCost = cost
                    bestPath = path

        if dbg:
            print('+' + '-' * 11 + '+' + '-' * 11 + '+')

        return bestPath, bestCost

    def constructSolutions(self, distances, capacityOfEachVehicle, pheromones):
        numCustomers = len(distances)
        paths = []

        unvisited = set(range(numCustomers))
        # for each ant
        for _ in range(self.numAnts):
            path = self.constructPath(
                distances, pheromones, numCustomers, capacityOfEachVehicle, unvisited)
            paths.append(path)
            self.updatePheromones(pheromones, paths, distances)

        return paths

    def constructPath(self, distances, pheromones, numCustomers, capacityOfEachVehicle, unvisited: set):
        start = 0
        path = [start]
        unvisited.remove(start)
        while unvisited:
            current = path[-1]
            nextCity = self.selectNextCity(
                current, unvisited, distances, pheromones)
            path.append(nextCity)
            unvisited.remove(nextCity)

            if self.calculatePathCost(path, distances) > capacityOfEachVehicle:
                # if demand greater than capacity, re-instantiate the path 
                path = [start]
                unvisited.remove(start)
        
        return path

    def selectNextCity(self, current, unvisited, distances, pheromones):
        probabilities = []

        for city in unvisited:
            pheromone = pheromones[current][city]
            distance = distances[current][city]
            probability = (pheromone ** self.alpha) * \
                ((1.0 / distance) ** self.beta)
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
