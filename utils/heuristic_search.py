from typing import Callable
from queue import PriorityQueue
from utils.simple_search import SimpleSearch


class HeuristicSearch(SimpleSearch):

    def __init__(self) -> None:
        super().__init__()

    def heuristic(self, node) -> int | float:
        # domain-dependent
        pass

    def MakePairs(self, nodeList, parent) -> list:
        return [[nodeList[i], parent, self.heuristic(nodeList[i])] for i in range(len(nodeList))]

    def BestFirstSearch(self, startNode, dbg: bool = True) -> list:
        '''
        <h2>Completeness:</h2>

        - Complete for finite graphs. Cannot claim completeness for infinite graphs!

        <h2>Quality of Solution:</h2>

        - Path found may not be optimal.

        - When edge or move costs are equal, it can still find non-optimal paths.

        <h2>Space Complexity:</h2>

        - With a good heuristic function, BestFS has characteristics similar to DFS.

        - So, we might hope that the space complexity might be linear. But it is possible 
        that the algorithm may change its mind and
        sprout new branches in the search tree.

        - This goes against the grain of linear space, and it has been
        empirically observed that the space required is often
        exponential.

        <h2>Time Complexity:</h2>

        - If the heuristic function were to be perfect, it would drive the
        search directly towards the goal. Then the time complexity
        would be linear.

        - However, in practice, this is not seen to be the case and, more
        often than not, the time complexity is exponential.
        '''

        self.OPEN: PriorityQueue = PriorityQueue()
        self.OPEN.put((self.heuristic(startNode), [startNode, None]))

        if dbg:
            print("+" + "-" * 11 + "-" + "-" * 11 + "-" +
                  "-" * (len(str(startNode)) + 2) + "+")
            print("|"+"Best First Search".center(81)+"|")
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" +
                  "-" * (len(str(startNode)) + 2) + "+")
            print(f"|" + "Heuristic".center(11) + "|" +
                  "len(OPEN)".center(11) + "|"+"Node".center(len(str(startNode)) + 2)+"|")
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" +
                  "-" * (len(str(startNode)) + 2) + "+")
        while self.OPEN._qsize() > 0:
            heur, nodePair = self.OPEN.get()
            N, _ = nodePair

            if dbg:
                print(f"|{str(heur).center(11)}|{str(self.OPEN._qsize()).center(11)}|{
                      str(N).center(len(str(startNode)) + 2)}|")

            if self.GoalTest(N):
                if dbg:
                    print("+" + "-" * 11 + "+" + "-" * 11 + "+" +
                          "-" * (len(str(startNode)) + 2) + "+")
                return self.ReconstructPath(nodePair)

            self.CLOSED.append(nodePair)

            children = self.MoveGen(N)
            newNodes = self.RemoveSeen(children)

            for child in newNodes:
                if child not in self.CLOSED:
                    self.OPEN.put((self.heuristic(child), [child, N]))

        if dbg:
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" +
                  "-" * (len(str(startNode)) + 2) + "+")

        return []

    def FindLink(self, node):
        for child, parent in self.CLOSED:
            if node == child:
                return parent
        return None

    def HillClimbing(self, startNode):
        '''
        <h2>Completeness:</h2>
        - Terminates on all finite graphs.
        - If heuristic values are bounded, then it may terminate on infinite graphs as well.
        - May get stuck in local optimum.
        - Not complete.

        <h2>Quality of Solution:</h2>
        - Solution may not be found.

        <h2>Space Complexity:</h2>
        - O(b) where b is the branching factor, as we store the neighbors in the priority queue.
        - Because MoveGen's branching factor is bounded, the space complexity is bounded/constant.

        <h2>Time Complexity:</h2>
        - O(d * b * log(b)) where d is the depth of the search and b is the branching factor.
        - The log(b) factor comes from priority queue operations.
        '''

        self.OPEN: PriorityQueue = PriorityQueue()
        self.OPEN.put((self.heuristic(startNode), [startNode, None]))

        while not self.OPEN.empty():
            _, currentNode = self.OPEN.get()

            if self.GoalTest(currentNode[0]):
                return self.ReconstructPath(currentNode)

            neighbours = self.MoveGen(currentNode[0])
            for neighbour in neighbours:
                if self.isBetterNode(neighbour, currentNode[0]):
                    self.OPEN.put((self.heuristic(neighbour), [neighbour, currentNode[0]]))

        return [currentNode]

    def isBetterNode(self, node1, node2, comp=lambda x, y: x > y):
        '''
        - Compares two nodes based on their heuristic values.
        - Assumed: If the heuristic value of node1 is more than the heuristic value of node2, then node1 is better than node2.
        - Returns True if node1 is better than node2, False otherwise.
        '''
        return comp(self.heuristic(node1), self.heuristic(node2))

    def bestNode(self, nodeList, bestCriterion=lambda x: min(x, key=lambda x: x[2])):
        '''
        - Returns the best node in the list based on the given comparison function.
        '''
        return bestCriterion(nodeList)

    def VariableNeighborhoodSearch(self, startNode, MoveGens: list):
        '''
        - Variable Neighborhood Search (VNS) is a metaheuristic optimization algorithm used to solve combinatorial optimization problems.
        - It is an iterative search algorithm that explores different neighborhoods of the solution space to find better solutions.
        - VNS combines the idea of exploring different neighborhoods with the concept of shaking the current solution to escape from local optima.
        - The algorithm starts with an initial solution and iteratively improves it by exploring different neighborhoods of the solution space.
        - If a better solution is found in a neighborhood, the algorithm moves to that solution and continues the search.
        - If no better solution is found, the algorithm shakes the current solution to escape from local optima and continues the search.
        '''
        node = startNode

        for i in range(1, len(MoveGens)):
            node = self.HillClimbing(node, MoveGens[i])

        return node

    def BeamSearch(self, startNode, numEpochs=100, beamWidth=2, dbg=True):
        '''
        - Beam Search is a search algorithm that explores a search space by maintaining a beam of promising nodes.
        - It explores the search space by expanding the most promising nodes and selecting the best candidates for further exploration.
        - The algorithm iteratively refines the beam by expanding the most promising nodes and selecting the best candidates for further exploration.
        - The algorithm terminates when a satisfactory solution is found or when the search space has been fully explored.
        '''

        self.OPEN: list = [[startNode, None, self.heuristic(startNode)]]
        self.CLOSED: list = []

        if dbg:
            print("+" + "-" * 11 + "-" + "-" * 11 + "-" +
                  "-" * (len(str(startNode)) + 2) + "+")
            print("|"+"Beam Search".center(81)+"|")
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" +
                  "-" * (len(str(startNode)) + 2) + "+")
            print(f"|" + "Epoch".center(11) + "|" +
                  " len(OPEN)".center(11) + "|"+" Node".center(len(str(startNode)) + 2)+"|")
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" +
                  "-" * (len(str(startNode)) + 2) + "+")

        for i in range(1, numEpochs + 1):

            self.OPEN.sort(key=lambda x: self.heuristic(x[0]))
            self.OPEN = self.OPEN[:beamWidth]

            if dbg:
                print(f"|{str(i).center(11)}|{str(len(self.OPEN)).center(11)}|{
                      str(self.OPEN[0]).center(len(str(startNode)) + 2)}|")
                # print('-'*81)
                # print(self.OPEN)
            newPairs = []
            for node in self.OPEN:

                if self.GoalTest(node[0]):
                    return self.ReconstructPath(node)

                self.CLOSED.append(node)

                children = self.MoveGen(node[0])

                newNodes = self.RemoveSeen(children)

                newPairs += self.MakePairs(newNodes, node[0])

            self.OPEN = sorted(newPairs + self.OPEN,
                               key=lambda x: self.heuristic(x[0]))
        if dbg:
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" +
                  "-" * (len(str(startNode)) + 2) + "+")
        return []

    def TabuSearch(self, startNode, Allowed: Callable, numEpochs: int, dbg: bool = True):

        N = startNode
        bestSeen = startNode
        for _ in range(numEpochs):
            N = self.bestNode(Allowed(self.MoveGen(N)))
            if self.isBetterNode(N, bestSeen):
                bestSeen = N

        return bestSeen
