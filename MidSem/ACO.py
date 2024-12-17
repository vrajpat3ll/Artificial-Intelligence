import random
import math


class VRPSolver:
    def __init__(self, numCustomers, maxVehicles, alpha, beta, evaporationRate, iterations, capacity, demand, timeMatrix):
        self.numCustomers = numCustomers
        self.maxVehicles = maxVehicles
        self.alpha = alpha
        self.beta = beta
        self.evaporationRate = evaporationRate
        self.iterations = iterations
        self.capacity = capacity
        self.timeMatrix = timeMatrix
        self.demand = demand

        self.pheromoneMatrix = [
            [1.0 for _ in range(numCustomers)] for _ in range(numCustomers)]

    def selectNextCity(self, currentCity, visited, currentDemand):
        probabilities = [0.0] * self.numCustomers
        total = 0.0

        for i in range(self.numCustomers):
            if not visited[i] and i != currentCity and self.demand[i] + currentDemand <= self.capacity:
                probabilities[i] = (self.pheromoneMatrix[currentCity][i] ** self.alpha) * \
                                   ((1.0 /
                                    self.timeMatrix[currentCity][i]) ** self.beta)
                total += probabilities[i]

        if total == 0:
            return -1

        probabilities = [p / total for p in probabilities]

        r = random.random()
        cumulative = 0.0
        for i in range(self.numCustomers):
            cumulative += probabilities[i]
            if r <= cumulative:
                return i

        return -1

    def calculateTourTime(self, tour):
        length = sum(self.timeMatrix[tour[i]][tour[i + 1]]
                     for i in range(len(tour) - 1))
        length += self.timeMatrix[tour[-1]][0]  # return to depot
        return length

    def updatePheromones(self, allTours, tourLengths):
        # evaporate pheromones
        for i in range(self.numCustomers):
            for j in range(self.numCustomers):
                self.pheromoneMatrix[i][j] *= (1 - self.evaporationRate)

        # deposit pheromones based on the ants' tours
        for ant, tour in enumerate(allTours):
            if tourLengths[ant] == 0:
                continue  # skip unused vehicles

            for i in range(len(tour) - 1):
                u, v = tour[i], tour[i + 1]
                deposit = 1.0 / tourLengths[ant]
                self.pheromoneMatrix[u][v] += deposit
                self.pheromoneMatrix[v][u] += deposit

            # return to depot
            u = tour[-1]
            deposit = 1.0 / tourLengths[ant]
            self.pheromoneMatrix[u][0] += deposit
            self.pheromoneMatrix[0][u] += deposit

    def solve(self, dbg=True):
        bestTours = [[] for _ in range(self.maxVehicles)]
        bestTourLengths = [float('inf')] * self.maxVehicles
        bestVehicleCount = self.maxVehicles

        if dbg:
            print('+' + '-' * 13 + '+' + '-' * 23 + '+' + '-'*19+'+')
            print(f"|{'Iteration'.center(13)}|{'Best Tour Length'.center(23)}|{
                  'Vehicles Used'.center(19)}|")
            print('+' + '-' * 13 + '+' + '-' * 23 + '+' + '-'*19+'+')

        for iter in range(self.iterations):
            allTours = [[] for _ in range(self.maxVehicles)]
            tourLengths = [0.0] * self.maxVehicles
            visited = [False] * self.numCustomers
            visited[0] = True  # depot is visited at the start

            for ant in range(self.maxVehicles):
                currentCity = 0  # start from the depot
                currentDemand = 0

                allTours[ant].append(currentCity)

                while True:
                    nextCity = self.selectNextCity(
                        currentCity, visited, currentDemand)
                    if nextCity == -1:
                        break  # no valid city to visit, go back to depot

                    allTours[ant].append(nextCity)
                    visited[nextCity] = True
                    currentDemand += self.demand[nextCity]
                    currentCity = nextCity

                    if all(visited[1:]):
                        break

                # complete tour by returning to depot
                allTours[ant].append(0)
                tourLengths[ant] = self.calculateTourTime(allTours[ant])

            vehicleCount = sum(1 for tour in allTours if len(tour) > 2)
            totalTourLength = sum(tourLengths)

            if vehicleCount < bestVehicleCount or \
               (vehicleCount == bestVehicleCount and totalTourLength < sum(bestTourLengths)):
                bestVehicleCount = vehicleCount
                bestTours = allTours
                bestTourLengths = tourLengths

            self.updatePheromones(allTours, tourLengths)
            if dbg:
                print("|"+str(iter + 1).center(13)+"|" +
                      str(totalTourLength).center(23)+"|" + str(vehicleCount).center(19)+"|")
        if dbg:
            print('+' + '-' * 13 + '+' + '-' * 23 + '+' + '-'*19+'+')
        return bestTours, bestTourLengths


# ---------------------------------------------------------------------------------------------------
numCustomers=5
maxVehicles=3
alpha = 1
beta = 1
evaporationRate = 0.1
numIterations = 20
capacity = 15

# demand: 0 for depot, some non-negative value of same mercahndise
demand = [0, 8, 12, 5, 10]

timeMatrix = [
    # first row converts distances from depot to customers to time quantities
    [0, 6, 7, 3, 4],
    [6, 0, 2, 5, 8],
    [7, 2, 0, 6, 3],
    [3, 5, 6, 0, 7],
    [4, 8, 3, 7, 0]
]


solver = VRPSolver(
    numCustomers=numCustomers,
    maxVehicles=maxVehicles,
    alpha=alpha,
    beta=beta,
    evaporationRate=evaporationRate,
    iterations=numIterations,
    capacity=capacity,
    demand=demand,
    timeMatrix=timeMatrix
)

bestTours, bestTourLengths = solver.solve()

print('+' + '-' * 13 + '+' + '-' * 23 + '+' + '-' * 19 + '+')
print(f"|{'Vehicle'.center(13)}|{'Path'.center(23)}|{
    'Total Travel Time'.center(19)}|")
print('+' + '-' * 13 + '+' + '-' * 23 + '+' + '-' * 19 + '+')

for ant, tour in enumerate(bestTours):
    if len(tour) > 2:  # Only print vehicles that have non-trivial tours
        print("|" + str(ant + 1).center(13) + "|" + ' '.join(map(str, tour)
                                                             ).center(23) + "|" + str(bestTourLengths
                                                                                      [ant]).center(19)
              + "|")
print('+' + '-' * 13 + '+' + '-' * 23 + '+' + '-' * 19 + '+')
print("|" + 'Total Time'.center(13) + " " + ' '.center(23) + "|" + str(sum([bestTourLength for bestTourLength in bestTourLengths])).center(19)
              + "|")

print('+' + '-' * 13 + '+' + '-' * 23 + '+' + '-' * 19 + '+')