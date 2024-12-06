from utils.simple_search import SimpleSearch


class State:
    def __init__(self, rollNumber, N=8) -> None:
        self.grid = [['.' for _ in range(N)] for __ in range(N)]
        self.queenPosCols = [int(x) for x in str(rollNumber).zfill(N)][:N]
        j = 0
        for i in range(N):
            self.grid[i][self.queenPosCols[j]] = 'Q'
            j += 1

    def __str__(self) -> str:
        ret = ""
        for row in self.grid:
            for char in row:
                ret += str(char).center(3)
            ret += '\n'
        return ret


class NQueensSolver(SimpleSearch):

    def __init__(self, rollNumber=20220100, N=8) -> None:
        super().__init__()

        self.state = State(rollNumber, N)
        self.N = N

    def GoalTest(self, node: State) -> bool:
        # Check if all queens are placed and none are under attack
        for row in range(self.N):
            col = node.queenPosCols[row]
            if not self.isSafe(node, row, col):
                return False
        return True

    def MoveGen(self, state: State):
        moves = []
        N = self.N
        self.nodesExpanded += 1
        for row in range(N):
            currentCol = state.queenPosCols[row]
            # Check if the current queen is under attack
            if not self.isSafe(state, row, currentCol):
                # This queen is under attack, try to move it within its row
                for newCol in range(N):
                    if newCol != currentCol and self.isSafe(state, row, newCol):
                        # Create a new state with the moved queen
                        move = State(0, N)
                        move.queenPosCols = state.queenPosCols.copy()
                        move.queenPosCols[row] = newCol
                        # Reconstruct the grid based on new queen positions
                        move.grid = [
                            ['.' for _ in range(N)] for __ in range(N)]
                        for i, queen_col in enumerate(move.queenPosCols):
                            move.grid[i][queen_col - 1] = 'Q'

                        moves.append(move)

                # We've generated moves for this queen, so we can stop
                # This ensures we only move one queen at a time
                break

            # If the current queen is safe, we move to the next row
            # The loop will continue to the next iteration

        return moves

    def isSafe(self, state: State, row, col):
        # Check if a queen at (row, col) is safe from queens in previous rows
        for prev_row in range(row):
            prev_col = state.queenPosCols[prev_row]
            # Check if queens are in the same column
            if col == prev_col:
                return False

            # Check if queens are on the same diagonal
            if abs(row - prev_row) == abs(col - prev_col):
                return False

        return True
