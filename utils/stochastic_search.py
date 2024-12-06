import utils.heuristic_search as hs
import random
import math


class StochasticSearch(hs.HeuristicSearch):
    def __init__(self) -> None:
        super().__init__()

    # cost function same as heuristic value
    def Cost(self, node):
        return self.heuristicValue(node)

    def RandomWalk(self, startNode, numEpochs: int = 100):
        bestSeen = startNode
        node = startNode
        for i in range(numEpochs):
            moves = self.MoveGen(node)
            idx = random.randint(0, len(moves) - 1)
            node = moves[idx]
            if self.isBetterNode(node, bestSeen):
                bestSeen = node

        return bestSeen

    def SimulatedAnnealing(self, startNode, numEpochs: int = 100, T: float = 3, alpha: float = 0.99, comp=lambda x, y: x < y, dbg=True):
        bestSeen = startNode
        node = startNode
        T_initial = T

        if dbg:
            print("+" + "-" * 11 + "-" + "-" * 11 + "-" +
                  "-" * (len(str(bestSeen)) + 2) + "+")
            print("|"+"Simulated Annealing".center(81)+"|")
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" +
                  "-" * (len(str(bestSeen)) + 2) + "+")
            print(f"|" + "Epoch".center(11) + "|" +
                  " Cost".center(11) + "|"+" Node".center(len(str(bestSeen)) + 2)+"|")
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" +
                  "-" * (len(str(bestSeen)) + 2) + "+")

        for i in range(1, numEpochs+1):
            moves = self.MoveGen(node)
            idx = random.randint(0, len(moves) - 1)
            neighbour = moves[idx]

            if random.random() < math.exp(-(self.Cost(neighbour) - self.Cost(node)) / T):
                node = neighbour

                if dbg:
                    print(f"|{str(i).center(11)}|{
                          str(self.Cost(node)).center(11)}|{str(node).center(len(str(bestSeen)) + 2)}|")

                if self.isBetterNode(node, bestSeen, comp):
                    bestSeen = node

            T = max(T_initial * math.exp(-alpha * i), 0.01)

        if dbg:
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" +
                  "-" * (len(str(bestSeen)) + 2) + "+")
            print(f"\nBest Seen: {bestSeen}")
            print(f"Cost: {self.Cost(bestSeen)}\n")

        return bestSeen

    def StochasticHillClimbing(self, startNode, numEpochs: int = 100, T: float = 1, comp=lambda x, y: x < y, dbg=True):
        bestSeen = startNode
        node = startNode

        if dbg:
            print("+" + "-" * 11 + "-" + "-" * 11 + "-" +
                  "-" * (len(str(bestSeen)) + 2) + "+")
            print("|"+"Stochastic Hill Climbing".center(81)+"|")
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" +
                  "-" * (len(str(bestSeen)) + 2) + "+")
            print(f"|" + "Epoch".center(11) + "|" +
                  " Cost".center(11) + "|"+" Node".center(len(str(bestSeen)) + 2)+"|")
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" +
                  "-" * (len(str(bestSeen)) + 2) + "+")

        # termination criteria: Epochs
        for i in range(1, numEpochs+1):
            moves = self.MoveGen(node)
            idx = random.randint(0, len(moves) - 1)
            neighbour = moves[idx]

            deltaE = self.Cost(neighbour) - self.Cost(node)
            if random.random() < math.exp(-deltaE / T):
                node = neighbour

            if dbg:
                print(f"|{str(i).center(11)}|{
                      str(self.Cost(node)).center(11)}|{str(node).center(len(str(bestSeen)) + 2)}|")

            if self.isBetterNode(node, bestSeen, comp=comp):
                bestSeen = node

        if dbg:
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" +
                  "-" * (len(str(bestSeen)) + 2) + "+")
            print(f"\nBest Seen: {bestSeen}")
            print(f"Cost: {self.Cost(bestSeen)}\n")

        return bestSeen
