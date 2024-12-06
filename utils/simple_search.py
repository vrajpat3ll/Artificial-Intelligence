from utils.agent import Agent


class SimpleSearch(Agent):
    ''' can also be called blind_search
    '''

    # taken from notes
    def FindLink(self, node):
        for child, parent, _ in self.CLOSED:
            if node == child:
                return parent
        return None

    # taken from notes
    def ReconstructPath(self, nodePair: list):
        node, parent = nodePair[0], nodePair[1]
        path = [node]
        while parent != None:
            path = [parent] + path
            parent = self.FindLink(parent)

        return path

    # taken from notes
    def MakePairs(self, nodeList, parent, depth: int):
        return [[nodeList[i], parent, depth] for i in range(len(nodeList))]

    # taken from notes
    def PlanningSearch(self, startNode, goalNode, traversal: str = 'bfs', dbg: bool = True):
        self.OPEN = [[startNode, None, 0]]
        self.CLOSED = []

        while len(self.OPEN) > 0:

            nodePair = self.OPEN[0]
            candidate = nodePair[0]
            depth = nodePair[2]

            self.OPEN.pop(0)  # remove 1st element

            if dbg:
                print(f"{candidate=} ")
                print(f"{self.OPEN=}")
                print('-'*90)

            if candidate == goalNode:
                return self.ReconstructPath(nodePair)

            self.CLOSED.append(nodePair)

            children = self.MoveGen(candidate)

            newNodes = self.RemoveSeen(children)

            newPairs = self.MakePairs(newNodes, candidate, depth + 1)

            if traversal.lower() == 'bfs':
                self.OPEN = self.OPEN + newPairs
            elif traversal.lower() == 'dfs':
                self.OPEN = newPairs + self.OPEN

        return []

    # taken from notes
    def ConfigSearch(self, startNode, traversal: str = 'bfs', solution: str = 'one', dbg: bool = True):

        self.OPEN = [startNode]
        solutions = []

        while len(self.OPEN) > 0:

            candidate = self.OPEN[0]

            self.OPEN.pop(0)  # remove 1st element
            self.CLOSED.append(candidate)

            if dbg:
                print(f"{candidate=} ")
                print(f"{self.OPEN=}")
                print('-'*90)

            if self.GoalTest(candidate):
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

    # taken from notes
    def DFID(self, startNode, termination_criteria: function, dbg: bool = True):

        # taken from notes
        def _DB_DFS(startNode, depthBound: int, dbg: bool = True):
            self.OPEN = [[startNode, None, 0]]
            self.CLOSED = []
            while len(self.OPEN) > 0:
                nodePair = self.OPEN[0]
                candidate, depth = nodePair[0], nodePair[2]

                if self.GoalTest(candidate):
                    return candidate, self.ReconstructPath(nodePair)

                self.CLOSED.append(nodePair)

                if depth < depthBound:
                    children = self.MoveGen(candidate)

                    newNodes = self.RemoveSeen(children)

                    newPairs = self.MakePairs(newNodes, candidate, depth + 1)

                    self.OPEN = newPairs + self.OPEN  # DFS as we traverse through the newPairs first

                self.OPEN.remove(nodePair)

                if dbg:
                    print(f"{depth=} | {len(self.OPEN)=} ")
            return []

        depthBound = 0
        while termination_criteria():
            solution = _DB_DFS(startNode, depthBound=depthBound, dbg=dbg)

            depthBound += 1

            # if found 1 solution, exit the loop
            if len(solution) != 0:
                break
        return solution
