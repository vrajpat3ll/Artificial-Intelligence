class GameState:
    def __init__(self, board=None):
        self.board = board if board else [0 for _ in range(16)]

    def get_available_moves(self):
        moves = []
        for i in range(4):
            for j in range(4):
                if self.board[4 * i + j] == 0:
                    moves.append((i, j))
        return moves

    def make_move(self, move, player):
        new_state = GameState(self.board)
        new_state.board[4 * move[0] + move[1]] = player
        return new_state

    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != 0 or row[1] == row[2] == row[3] != 0:
                return row[0]

        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]

        # Check for draw
        if not any(' ' in row for row in self.board):
            return 'draw'

        return None


def minimax(state: GameState, depth, is_maximizing_player, alpha=-float('inf'), beta=float('inf')):
    """
    Minimax algorithm with alpha-beta pruning
    Returns tuple of (best_score, best_move)
    """
    winner = state.check_winner()

    # Base cases
    if winner == 'X':
        return 1, None
    elif winner == 'O':
        return -1, None
    elif winner == 'draw':
        return 0, None
    elif depth == 0:
        return 0, None

    available_moves = state.get_available_moves()

    if is_maximizing_player:
        best_score = -float('inf')
        best_move = None

        for move in available_moves:
            new_state = state.make_move(move, 'X')
            score, _ = minimax(new_state, depth - 1, False, alpha, beta)

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        return best_score, best_move

    else:
        best_score = float('inf')
        best_move = None

        for move in available_moves:
            new_state = state.make_move(move, 'O')
            score, _ = minimax(new_state, depth - 1, True, alpha, beta)

            if score < best_score:
                best_score = score
                best_move = move

            beta = min(beta, best_score)
            if beta <= alpha:
                break

        return best_score, best_move


def print_board(state: GameState):
    """Utility function to print the game board"""
    for row in state.board:
        print('|'.join(row))
        print('-' * 5)

# Example usage


def play_game(input_board):
    state = GameState(input_board)
    current_player = 'X'

    while True:
        print_board(state)

        if current_player == 'X':
            # AI move
            _, best_move = minimax(state, depth=9, is_maximizing_player=True)
            if best_move:
                state = state.make_move(best_move, 'X')
                print(f"AI plays at position: {best_move}")
        else:
            # _, best_move = minimax(state, depth=9, is_maximizing_player=False)
            # if best_move:
            #     state = state.make_move(best_move, 'O')
            #     print(f"AI plays at position: {best_move}")
            # Human move
            valid_moves = state.get_available_moves()
            while True:
                try:
                    row = int(input("Enter row (0-2): "))
                    col = int(input("Enter column (0-2): "))
                    if (row, col) in valid_moves:
                        state = state.make_move((row, col), 'O')
                        break
                    else:
                        print("Invalid move, try again.")
                except ValueError:
                    print("Please enter valid numbers.")

        winner = state.check_winner()
        if winner:
            print_board(state)
            if winner == 'draw':
                print("Game is a draw!")
            else:
                print(f"Player {winner} wins!")
            break

        current_player = 'O' if current_player == 'X' else 'X'


if __name__ == "__main__":
    
    input_board = []
    try:
        input_board = list(map(int, input().strip().split()))
    except Exception:
        if len(input_board) != 16:
            print("Enter valid board! (length != 16)")

    play_game(input_board)
