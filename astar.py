from typing import Any, Optional, Callable, List
from dataclasses import dataclass
from abc import ABC, abstractmethod
import heapq


@dataclass
class State:
    state: Any
    parent: Optional['State'] = None
    g_value: float = 0.0
    f_value: float = 0.0

    def __hash__(self):
        return hash((self.state, self.parent))

    def __str__(self):
        return f"{self.state}, f={self.f_value}"


class SimpleSearch(ABC):
    def __init__(self):
        self.CLOSED: set = set()
        self.OPEN: List

    @abstractmethod
    def MoveGen(self, node: Any) -> List[Any]:
        """Generates possible moves from the current state."""
        pass

    @abstractmethod
    def GoalTest(self, node: Any) -> bool:
        """Tests if the current state is the goal."""
        pass

    @abstractmethod
    def ReconstructPath(self, node: State) -> List[State]:
        """Reconstructs the path from the goal to the start."""
        pass

    @abstractmethod
    def RemoveSeen(self, children: List[Any]) -> List[Any]:
        """Removes already seen nodes."""
        pass


class HeuristicSearch(SimpleSearch, ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def heuristic(self, node: State) -> float:
        """Heuristic function to be defined in derived classes."""
        pass

    def MakePairs(self, nodeList: List[Any], parent: State) -> List[tuple]:
        """Creates a list of tuples containing (node, parent, heuristic)."""
        return [(node, parent, self.heuristic(State(state=node))) for node in nodeList]

    def BestFirstSearch(self, startNode: Any, dbg: bool = True) -> List[State]:
        '''
        Best-First Search algorithm.
        Completeness: Complete for finite graphs. Not complete for infinite graphs.
        Quality: Path found may not be optimal.
        Space Complexity: Often exponential.
        Time Complexity: Often exponential.
        '''
        start_state = State(state=startNode, parent=None, f_value=self.heuristic(State(state=startNode)))
        open_queue = []
        heapq.heappush(open_queue, (start_state.f_value, start_state))
        self.CLOSED = set()

        if dbg:
            header = f"|{'Heuristic':^11}|{'len(OPEN)':^11}|{'Node':^20}|"
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")
            print("| Best First Search".center(44) + "|")
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")
            print(header)
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")

        while open_queue:
            heur, current = heapq.heappop(open_queue)

            if dbg:
                print(f"|{current.f_value:^11.2f}|{len(open_queue):^11}|{str(current):^20}|")

            if self.GoalTest(current.state):
                if dbg:
                    print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")
                return self.ReconstructPath(current)

            if current in self.CLOSED:
                continue

            self.CLOSED.add(current)

            children_states = self.MoveGen(current.state)
            new_children = self.RemoveSeen(children_states)

            for child in new_children:
                child_state = State(state=child, parent=current)
                child_state.f_value = self.heuristic(child_state)
                if child_state not in self.CLOSED:
                    heapq.heappush(open_queue, (child_state.f_value, child_state))

        if dbg:
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")

        return []

    def FindLink(self, node: Any) -> Optional[State]:
        """Finds the parent of a node in CLOSED."""
        for child in self.CLOSED:
            if child.state == node:
                return child.parent
        return None

    def HillClimbing(self, startNode: Any, dbg: bool = True) -> List[State]:
        '''
        Hill Climbing search algorithm.
        Completeness: May get stuck in local optimum. Not complete.
        Quality: Solution may not be found.
        Space Complexity: O(b), where b is branching factor.
        Time Complexity: O(d * b * log(b)), where d is depth, b is branching factor.
        '''
        current = State(state=startNode, parent=None, f_value=self.heuristic(State(state=startNode)))
        open_heap = []
        heapq.heappush(open_heap, (current.f_value, current))
        self.CLOSED = set()

        if dbg:
            header = f"|{'Heuristic':^11}|{'len(OPEN)':^11}|{'Node':^20}|"
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")
            print("| Hill Climbing".center(44) + "|")
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")
            print(header)
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")

        while open_heap:
            current_f, current = heapq.heappop(open_heap)

            if dbg:
                print(f"|{current.f_value:^11.2f}|{len(open_heap):^11}|{str(current):^20}|")

            if self.GoalTest(current.state):
                if dbg:
                    print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")
                return self.ReconstructPath(current)

            if current in self.CLOSED:
                continue

            self.CLOSED.add(current)

            neighbours = self.MoveGen(current.state)
            new_nodes = self.RemoveSeen(neighbours)

            for neighbour in new_nodes:
                if neighbour not in self.CLOSED:
                    neighbour_state = State(state=neighbour, parent=current)
                    neighbour_state.f_value = self.heuristic(neighbour_state)
                    heapq.heappush(open_heap, (neighbour_state.f_value, neighbour_state))

        if dbg:
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")

        return []

    def bestNode(self, nodeList: List[State], bestCriterion: Callable[[List[State]], State] = min) -> State:
        '''
        Returns the best node in the list based on the given comparison function.
        Default is node with minimum f_value.
        '''
        return bestCriterion(nodeList, key=lambda x: x.f_value)

    def VariableNeighborhoodSearch(self, startNode: Any, MoveGens: List[Callable[[Any], List[Any]]], dbg: bool = True) -> Any:
        '''
        Variable Neighborhood Search (VNS) is a metaheuristic optimization algorithm.
        '''
        node = startNode

        for move_gen in MoveGens:
            neighbours = move_gen(node)
            if not neighbours:
                continue
            # Find the best neighbor
            best_neighbor = self.bestNode([State(state=n, parent=None, f_value=self.heuristic(State(state=n))) for n in neighbours])
            if self.isBetterNode(best_neighbor, State(state=node)):
                node = best_neighbor.state
            else:
                # Shaking: select a random neighbor to escape local optimum
                node = neighbours[0]  # Simplified for example

        return node

    def BeamSearch(self, startNode: Any, numEpochs: int = 100, beamWidth: int = 2, dbg: bool = True) -> List[State]:
        '''
        Beam Search algorithm.
        '''
        start_state = State(state=startNode, parent=None, f_value=self.heuristic(State(state=startNode)))
        OPEN = [start_state]
        self.CLOSED = set()

        if dbg:
            header = f"|{'Epoch':^11}|{'len(OPEN)':^11}|{'Node':^20}|"
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")
            print("| Beam Search".center(44) + "|")
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")
            print(header)
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")

        for epoch in range(1, numEpochs + 1):
            # Sort OPEN based on heuristic and keep beamWidth
            OPEN.sort(key=lambda x: self.heuristic(x))
            OPEN = OPEN[:beamWidth]

            if dbg:
                print(f"|{str(epoch):^11}|{str(len(OPEN)):^11}|{str(OPEN[0]):^20}|")

            new_pairs = []
            for node in OPEN:
                if self.GoalTest(node.state):
                    if dbg:
                        print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")
                    return self.ReconstructPath(node)

                self.CLOSED.add(node)

                children = self.MoveGen(node.state)
                new_nodes = self.RemoveSeen(children)

                for child in new_nodes:
                    if child not in self.CLOSED:
                        child_state = State(state=child, parent=node)
                        child_state.f_value = self.heuristic(child_state)
                        new_pairs.append(child_state)

            # Update OPEN with new pairs, sorted by heuristic
            OPEN = sorted(new_pairs, key=lambda x: x.f_value)[:beamWidth]

        if dbg:
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")

        return []

    def TabuSearch(self, startNode: Any, Allowed: Callable[[List[Any]], List[Any]], numEpochs: int, dbg: bool = True) -> Any:
        '''
        Tabu Search algorithm.
        '''
        current = startNode
        best_seen = startNode
        tabu_list = set()

        for epoch in range(numEpochs):
            neighbours = self.MoveGen(current)
            allowed = Allowed(neighbours)
            best_neighbor = self.bestNode([State(state=n, parent=None, f_value=self.heuristic(State(state=n))) for n in allowed])
            if self.isBetterNode(best_neighbor, State(state=best_seen)):
                best_seen = best_neighbor.state
                current = best_seen
                tabu_list.add(current)
            else:
                # Shaking: choose a neighbor not in tabu list
                non_tabu = [n for n in neighbours if n not in tabu_list]
                if non_tabu:
                    current = non_tabu[0]
            # Manage the size of tabu_list
            if len(tabu_list) > 10:  # example size
                tabu_list.pop()

        return best_seen

    def isBetterNode(self, node1: State, node2: State, comp: Callable[[float, float], bool] = lambda x, y: x < y) -> bool:
        '''
        Compares two nodes based on their heuristic values.
        Returns True if node1 is better than node2.
        '''
        return comp(self.heuristic(node1), self.heuristic(node2))


class AStar(HeuristicSearch):
    def __init__(self, alpha: float = 1.0, beta: float = 1.0):
        super().__init__()
        self.alpha = alpha
        self.beta = beta

    def ReconstructPath(self, node: State) -> List[State]:
        path = []
        current = node
        while current is not None:
            path.insert(0, current)
            current = current.parent
        return path

    def PropagateImprovement(self, node: State, cost: Callable[[Any, Any], float]):
        neighbours_states = self.MoveGen(node.state)
        for neighbor_state in neighbours_states:
            tentative_g = node.g_value + cost(node.state, neighbor_state)
            # Find the neighbor in CLOSED
            neighbor = next((n for n in self.CLOSED if n.state == neighbor_state), None)
            if neighbor and tentative_g < neighbor.g_value:
                neighbor.parent = node
                neighbor.g_value = tentative_g
                neighbor.f_value = self.alpha * neighbor.g_value + self.beta * self.heuristic(neighbor)
                self.PropagateImprovement(neighbor, cost)

    @abstractmethod
    def heuristic(self, node: State) -> float:
        """Define the heuristic function in derived class."""
        pass

    def AStarSearch(self, src: Any, cost: Callable[[Any, Any], float], dbg: bool = True) -> List[State]:
        """Search using A* algorithm.

        Args:
            src (Any): Source node state.
            cost (Callable[[Any, Any], float]): Function to compute cost between two states.
            dbg (bool, optional): Whether to print debug information. Defaults to True.

        Returns:
            List[State]: The path from source to goal.
        """
        start = State(state=src, parent=None, g_value=0.0, f_value=self.alpha * 0.0 + self.beta * self.heuristic(State(state=src)))
        open_heap = []
        heapq.heappush(open_heap, (start.f_value, start))
        self.CLOSED = set()

        if dbg:
            header = f"|{'f_value':^11}|{'len(OPEN)':^11}|{'Node':^20}|"
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")
            print("| A* Search".center(44) + "|")
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")
            print(header)
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")

        while open_heap:
            current_f, current = heapq.heappop(open_heap)
            if current in self.CLOSED:
                continue

            if dbg:
                print(f"|{current.f_value:^11.2f}|{len(open_heap):^11}|{str(current):^20}|")

            if self.GoalTest(current.state):
                if dbg:
                    print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")
                return self.ReconstructPath(current)

            self.CLOSED.add(current)

            children_states = self.MoveGen(current.state)
            new_children = self.RemoveSeen(children_states)

            for child in new_children:
                tentative_g = current.g_value + cost(current.state, child)
                child_state = State(state=child, parent=current, g_value=tentative_g)
                child_state.f_value = self.alpha * child_state.g_value + self.beta * self.heuristic(child_state)

                if child_state in self.CLOSED and tentative_g >= child_state.g_value:
                    continue

                heapq.heappush(open_heap, (child_state.f_value, child_state))

        if dbg:
            print("+" + "-" * 11 + "+" + "-" * 11 + "+" + "-" * 20 + "+")

        return []


# Example implementation of a concrete search class
class MySearch(AStar):
    def __init__(self, alpha=1.0, beta=1.0):
        super().__init__(alpha, beta)

    def MoveGen(self, node: Any) -> List[Any]:
        # Implement move generation based on your specific problem
        # Example: for integer states, generate n+1 and n-1
        return [node + 1, node - 1]

    def GoalTest(self, node: Any) -> bool:
        # Define your goal condition
        return node == 10  # Example goal

    def ReconstructPath(self, node: State) -> List[State]:
        path = []
        current = node
        while current is not None:
            path.insert(0, current)
            current = current.parent
        return path

    def RemoveSeen(self, children: List[Any]) -> List[Any]:
        # Remove children that have been seen (in CLOSED)
        return [child for child in children if not any(c.state == child for c in self.CLOSED)]

    def heuristic(self, node: State) -> float:
        # Example heuristic: absolute difference from goal
        return abs(10 - node.state)


def main():
    search = MySearch()
    start = 0

    # Define the cost function
    def cost(a: Any, b: Any) -> float:
        return 1.0  # Uniform cost

    # Perform A* Search
    path = search.AStarSearch(start, cost, dbg=True)

    if path:
        print("Path found:")
        for state in path:
            print(state.state, end=" -> ")
        print("Goal")
    else:
        print("No path found.")


if __name__ == "__main__":
    main()
