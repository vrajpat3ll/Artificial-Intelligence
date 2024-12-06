import utils.astar as A
from copy import deepcopy


class FifteenTilePuzzleSolver(A.AStar):
    # solver for the 15 Tile Puzzle
    def __init__(self) -> None:
        super().__init__()

    def GoalTest(self, node):
        for i in range(16):
            if node[i] != i + 1:
                return False

        return True

    def MoveGen(self, startNode):
        startNode = list(startNode)
        indexOfBlankSpace = startNode.index(16)
        X = indexOfBlankSpace // 4
        Y = indexOfBlankSpace % 4
        moves = []
        dirs = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        for x, y in dirs:
            newX = X + x
            newY = Y + y
            if newX >= 0 and newX < 4 and newY >= 0 and newY < 4:
                newNode = deepcopy(startNode)
                newNode[4 * X + Y], newNode[4*newX+newY] = startNode[4 *
                                                                     newX + newY], startNode[4 * X + Y]
                moves.append(tuple(newNode))
        startNode = tuple(startNode)
        return moves

    # hamming Distance
    def heuristic(self, node: list) -> int:
        value = 0
        for i in range(16):
            # if node[i] != i + 1:
            #     value += 1
            indexOfI = node.index(i+1)
            X = indexOfI // 4
            Y = indexOfI % 4
            actualX = i // 4
            actualY = i % 4
            value += (abs(X - actualX) + abs(Y - actualY))
        return value


# 16 in the state is blank space. BLANK SPACE HAS TO BE NAMED 16!
# please provide a valid input for the 15Tile problem!
startState = A.State(tuple([
    1, 2, 3,4,
    5, 6, 7, 8,
    9, 10, 11, 12,
    13, 14, 15, 16
]))
goalState = A.State(
    tuple([1,2, 3, 4, 
           16, 6, 7, 8, 
           5, 10, 11, 12, 
           9, 13, 14, 15]))


def cost(src, dest): return 1#FifteenTilePuzzleSolver().heuristic(src.state)


solver = FifteenTilePuzzleSolver()
solution = solver.AStarSearch(startState, cost=cost
                              )
print('+' + '-' * 78 + '+')
print(f"| Initial state: {startState}".ljust(79)+"|")
print('+' + '-' * 78 + '+')

i = 0
for sol in solution:
    if i > 0:
        print(f"{i}: {sol}")
    i += 1
if i == 1:
    print("Already solved!")
