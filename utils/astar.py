from typing import Any, Optional, Callable
import utils.heuristic_search as hs
from dataclasses import dataclass


@dataclass
class State:
    state: Any
    parent: Optional['State'] = None
    g_value: int | float = 0
    f_value: int | float = 0

    def __hash__(self):
        return hash(self.state)

    def __str__(self):
        return str(self.state)+', ' + str(self.f_value)


class AStar(hs.HeuristicSearch):
    def __init__(self, alpha=1, beta=1):
        super().__init__()
        self.alpha = alpha
        self.beta = beta

    def ReconstructPath(self, node: State):
        path = [node]
        while node.parent != None:
            path = [node.parent] + path
            node = node.parent
        return path

    def PropagateImprovement(self, node: State, cost: Callable[[Any, Any], int | float]):
        neighbours = self.MoveGen(node.state)
        neighbours = [State(x) for x in neighbours]
        for neighbour in neighbours:
            if node.g_value + cost(node, neighbour) < neighbour.g_value:
                neighbour.parent = node
                neighbour.g_value = node.g_value + cost(node, neighbour)
                neighbour.f_value = self.alpha * neighbour.g_value + \
                    self.beta * self.heuristic(neighbour)
                if neighbour in self.CLOSED:
                    self.PropagateImprovement(neighbour)
        return

    def AStarSearch(self, src: State, cost: Callable[[Any, Any], int | float]):
        """ Search using A* algorithm

        `src`: source node of type state
        """
        src.parent = None
        src.g_value = 0
        src.f_value = self.alpha*src.g_value + \
            self.beta * self.heuristic(src.state)
        self.OPEN = [src]
        self.CLOSED: set = set()

        while len(self.OPEN) > 0:

            N: State = self.bestNode(
                self.OPEN, bestCriterion=lambda nodeList: min(
                    nodeList, key=lambda node: node.f_value)
            )
            self.CLOSED.add(N)
            print(f"Checking {N=}")
            print(f"h_value={self.heuristic(N.state)}")
            print(f"f_value={N.f_value}")

            if self.GoalTest(N.state):
                return self.ReconstructPath(N)

            neighbours = self.MoveGen(N.state)
            neighbours = [State(x) for x in neighbours]
            for neighbour in neighbours:
                if neighbour not in self.OPEN and neighbour not in self.CLOSED:
                    neighbour.parent = N
                    neighbour.g_value = N.g_value + cost(N, neighbour)
                    neighbour.f_value = self.alpha * neighbour.g_value + \
                        self.beta*self.heuristic(neighbour.state)
                    self.OPEN.append(neighbour)
                else:
                    if N.g_value + cost(N, neighbour) < neighbour.g_value:
                        neighbour.parent = N
                        neighbour.g_value = N.g_value + cost(N, neighbour)
                        neighbour.f_value = self.alpha * neighbour.g_value + \
                            self.beta * self.heuristic(neighbour.state)
                        if neighbour in self.CLOSED:
                            self.PropagateImprovement(neighbour, cost)
        return []
