import utils.heuristic_search as hs
from copy import deepcopy


class FifteenTilePuzzleSolver(hs.HeuristicSearch):
    # solver for the 15 Tile Puzzle
    def __init__(self, ) -> None:
        super().__init__()

    def GoalTest(self, node):
        for i in range(16):
            if node[i] != i + 1:
                return False

        return True

    def MoveGen(self, startNode: list):
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
                moves.append(newNode)
        return moves

    # hamming Distance
    def heuristicValue(self, node: list) -> int:
        value = 0
        for i in range(16):
            if node[i] != i + 1:
                value += 1
            # indexOfI = node.index(i+1)
            # X = indexOfI // 4
            # Y = indexOfI % 4
            # actualX = i // 4
            # actualY = i % 4
            # value += abs(X - actualX) + abs(Y - actualY)
        return value


# 16 in the state is blank space. BLANK SPACE HAS TO BE NAMED 16!
# please provide a valid input for the 15Tile problem!
startState = [5,  1, 2,  4,
              9,  6,  3,  8,
              10, 14, 7, 11,
              16, 13, 15, 12
              ]


solver = FifteenTilePuzzleSolver()
solution = solver.BestFirstSearch(startState)
print('+' + '-' * 72 + '+')
print(f"| Initial state: {startState} |")
print('+' + '-' * 72 + '+')

i = 0
for sol in solution:
    if i > 0:
        print(f"{i}: {sol}")
    i += 1
