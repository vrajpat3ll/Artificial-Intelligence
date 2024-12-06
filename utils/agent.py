class Agent:
    '''
    This is the base class that solves the problem given to it.
    The functions given below are domain-dependent.
    '''

    def __init__(self) -> None:
        self.OPEN = []
        self.CLOSED = []
        self.nodesExpanded = 0

    

    def PlanningSearch(self, startNode, goalNode, traversal, solution, dbg):
        # search-dependent
        pass

    def ConfigSearch(self, startNode, traversal, solution, dbg):
        # search-dependent
        pass

    def MoveGen(self, startNode):
        # domain-dependent
        pass

    def GoalTest(self, node):
        # domain-dependent
        pass