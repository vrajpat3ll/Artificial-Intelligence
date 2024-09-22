from utils.graph import Graph
from utils.search import SimpleSearch


class TSPSolver (SimpleSearch):
    ''' Initialize the TSP problem
    '''

    def __init__(self, cities, rollNumber=20220100) -> None:
        '''Constructor for the problem solver
        '''
        super().__init__()

        self.number = rollNumber
        self.cities = cities
        self.graph = self._generateDistanceMatrix(str(rollNumber))

    def GoalTest(self, candidate) -> bool:
        """
        Checks whether `candidate` is a solution to our problem or not
        Returns True if it is.
        """
        return len(candidate[1]) == self.cities + 1 and \
            candidate[1][-1] == candidate[0]

    def MoveGen(self, state):
        """
        Generates all possible moves from the current state.
        """
        self.nodesExpanded += 1
        moves: list = []
        for city in range(1, self.cities + 1):
            if city not in state[1] or (len(state[1]) == self.cities and city == state[0]):

                newState = state.copy()

                newState[1] = state[1].copy()
                newState[2] = state[2] + self.graph.getEdgeWeight(
                    state[1][-1], city)
                newState[1].append(city)

                moves.append(newState)

        return moves

    def _generateDistanceMatrix(self, number: str):
        '''
        Generates the adjacency matrix for the cities, given a particular number,
        `Returns` a graph object.

        '''
        graph = Graph(self.cities)

        # hard coded for 4 cities
        # ---------------------------------------------------------------------------------------+
        # need to change this if we want to have more cities|
        number = number + number[-4:][::-1]
        # ---------------------------------------------------------------------------------------+
        weights = [int(number[i:i + 2]) for i in range(0, len(number), 2)]
        print(f"{weights=}")
        k = 0
        for i in range(1, self.cities + 1):
            for j in range(i + 1, self.cities + 1):
                graph.addUndirectedEdge(i, j, weights[k])
                k += 1

            graph.addEdge(i, i, 0)

        print("Distance Matrix:")
        print(graph)

        return graph

    def ConfigSearch(self,
                     startNode,
                     distanceThreshold: float = float('inf'),
                     traversal: str = 'bfs',
                     solution: str = 'one',
                     dbg: bool = True
                     ) -> list | str:
        self.OPEN = [startNode]
        self.CLOSED = []

        solutions = []

        while len(self.OPEN) > 0:

            candidate = self.OPEN[0]
            self.OPEN.pop(0)  # remove 1st element
            self.CLOSED.append(candidate)
            if dbg:
                print(f"{candidate=} ")
                print(f"{self.OPEN=}")
                print('-' * 90)

            if self.GoalTest(candidate):
                # if the solution is within the distance threshold, return it! We cannot minimise distance
                if candidate[2] <= distanceThreshold:
                    if solution.lower() == 'one':
                        return [candidate]
                    elif solution.lower() == 'all':
                        solutions.append(candidate)

            nodes = self.MoveGen(candidate)

            nodes = self.RemoveSeen(nodes)

            if traversal.lower() == 'bfs':
                self.OPEN = self.OPEN + nodes
            elif traversal.lower() == 'dfs':
                self.OPEN = nodes + self.OPEN

        if len(solutions) == 0:
            return "COULD NOT FIND SOLUTION!"

        return solutions

    # taken from file://utils/search.py only but had to modify it to suit TSP (epochs and distanceThreshold)
    def DFID(self,
             startNode,
             distanceThreshold: float = float('inf'),
             epochs: int = 1000,
             dbg: bool = True) -> list:
     
        depthBound = 0
        
        # while True: 
        for _ in range(epochs):

            solution = self._DB_DFS(
                startNode,
                distanceThreshold, depthBound, dbg)
            depthBound += 1
            if len(solution) != 0:
                break
        return solution

    # taken from file://utils/search.py only but had to modify it to suit TSP (distanceThreshold)
    def _DB_DFS(self,
                startNode,
                distanceThreshold: float,
                depthBound: int,
                dbg: bool = True) -> list:
        self.OPEN = [[startNode, None, 0]]
        self.CLOSED = []
        
        while len(self.OPEN) > 0:
            nodePair = self.OPEN[0]
            candidate, depth = nodePair[0], nodePair[2]
            self.nodesExpanded +=1
            if self.GoalTest(candidate) and candidate[2] <= distanceThreshold:
                return self.ReconstructPath(nodePair)

            self.CLOSED.append(nodePair)

            if depth < depthBound:
                children = self.MoveGen(candidate)

                newNodes = self.RemoveSeen(children)

                newPairs = self.MakePairs(newNodes, candidate, depth + 1)

                self.OPEN = newPairs + self.OPEN

            self.OPEN.remove(nodePair)

            if dbg:
                print(f"{depth=} | {len(self.OPEN)=}")
        return []
