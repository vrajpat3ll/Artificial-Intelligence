class Agent:
    '''
    This is the base class that solves the problem given to it.
    The functions given below are domain-dependent.
    '''

    def __init__(self) -> None:
        self.OPEN: list = []
        self.CLOSED: list = []
        self.nodesExpanded = 0

    def RemoveSeen(self, moves):
        if len(moves) == 0:
            return []

        newMoves = []
        for move in moves:
            if move not in self.OPEN and move not in self.CLOSED:
                newMoves.append(move)
        return newMoves

    def PlanningSearch(self, startNode, goalNode, traversal, solution, dbg):
        # domain-dependent
        pass

    def ConfigSearch(self, startNode, traversal, solution, dbg):
        # domain-dependent
        pass

    def MoveGen(self, startNode):
        # domain-dependent
        pass

    def GoalTest(self, node) -> bool:
        # domain-dependent
        return False
