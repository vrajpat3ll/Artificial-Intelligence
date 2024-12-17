PLAYER_MAX = 1
PLAYER_MIN = -1
DRAW = 0

# State for board
class GameState:
    def __init__(self, board=None):
        self.board = board if board else [
            [0 for _ in range(4)] for _ in range(4)]

    def get_available_moves(self):
        moves = []
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    moves.append((i, j))
        return moves

    def make_move(self, move, player):
        new_state = GameState([row[:] for row in self.board])
        new_state.board[move[0]][move[1]] = player
        return new_state

    def check_winner(self):
        # Check rows
        for row in self.board:
            if sum([1 for x in row if x == PLAYER_MAX]) == 3:
                return PLAYER_MAX
            if sum([1 for x in row if x == PLAYER_MIN]) == 3:
                return PLAYER_MIN

        # Check columns
        for col in range(4):
            column = [self.board[i][col] for i in range(4)]

            if sum([1 for x in column if x == PLAYER_MAX]) == 3:
                return PLAYER_MAX
            if sum([1 for x in column if x == PLAYER_MIN]) == 3:
                return PLAYER_MIN

        # Check diagonals
        diagonals = [
            [self.board[i][i] for i in range(4)],
            [self.board[i+1][i] for i in range(3)],
            [self.board[i][i+1] for i in range(3)],
            [self.board[2 - i][i] for i in range(3)],
            [self.board[3 - i][i] for i in range(4)],
            [self.board[i][2 - i] for i in range(3)],
            [self.board[i][3 - i] for i in range(4)],
        ]

        for diagonal in diagonals:
            Max = [1 for x in diagonal if x == PLAYER_MAX]
            Min = [1 for x in diagonal if x == PLAYER_MIN]
            if sum(Max) == 3:
                return PLAYER_MAX
            if sum(Min) == 3:
                return PLAYER_MIN
        
        # Check for draw
        if not any(0 in row for row in self.board):
            return DRAW

        return None

def evaluate(state: GameState, is_Max):
    c1 = 0
    c2 = 0
    for row in state.board:
        if 0 in row:
            if 1 in row:
                c1 += 1
            if -1 in row:
                c2 += 1
    for col in range(4):
        column = [state.board[i][col] for i in range(4)]
        if 1 in column:
            c1 += 1
        if -1 in column:
            c2 += 1

    diagonals = [
            [state.board[i][i] for i in range(4)],
            [state.board[i+1][i] for i in range(3)],
            [state.board[i][i+1] for i in range(3)],
            [state.board[2 - i][i] for i in range(3)],
            [state.board[3 - i][i] for i in range(4)],
            [state.board[i][2 - i] for i in range(3)],
            [state.board[i][3 - i] for i in range(4)],
        ]

    for diagonal in diagonals:
        if 0 in diagonal:
            if 1 in diagonal:
                c1 += 1
            if -1 in diagonal:
                c2 += 1

    return c1-c2 # as given in question


def minimax(state: GameState, depth, is_Max, alpha=-float('inf'), beta=float('inf')):
    """
    Minimax algorithm with alpha-beta pruning
    Returns tuple of (best_score, best_move)
    depth is ply
    """
    winner = state.check_winner()

    # Base cases
    if winner == PLAYER_MAX:
        return 100, None
    elif winner == PLAYER_MIN:
        return -100, None
    elif winner == DRAW:
        return evaluate(state, is_Max), None
    elif depth == 0:
        return evaluate(state, is_Max), None

    available_moves = state.get_available_moves()

    if is_Max:
        best_score = -float('inf')
        best_move = None

        for move in available_moves:
            new_state = state.make_move(move, PLAYER_MAX)
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
            new_state = state.make_move(move, PLAYER_MIN)
            score, _ = minimax(new_state, depth - 1, True, alpha, beta)

            if score < best_score:
                best_score = score
                best_move = move

            beta = min(beta, best_score)
            if beta <= alpha:
                break

        return best_score, best_move


def print_board(state: GameState):
    print("\nCurrent board:")
    for row in state.board:
        p = []
        for x in row:
            if x==1:
                p.append('  1  ')
            elif x==-1:
                p.append(' -1  ')
            else:
                p.append('  0  ')
        print('|'.join(p))
        print('-' * len(p) * 5 + '--')


def play_ai_vs_ai(input_board, current_player, k, takeUserInput, delay_seconds=1):
    """Play a game between one AI and yourself/two AI players with a delay between moves"""

    import time
    state = GameState(input_board)
    move_count = 0

    print("Starting AI vs AI game...")
    print("X: AI Player 1 (Maximizer)")
    print("O: AI Player 2 (Minimizer)\n")

    while True:
        print_board(state)
        move_count += 1
        print(f"\nMove #{move_count}")

        # Get AI move
        if current_player == PLAYER_MAX:
            _, best_move = minimax(state, depth=k, is_Max=True)
            print("AI Player 1 (X) thinking...")
        else:
            if takeUserInput:
                flag = True
                r=4
                c=4

                while flag:
                    try:
                        r, c = map(int, input("Enter row and column: ").strip().split())
                        print(r,c)
                    except Exception as e:
                        print(e)

                    if (r < 0 or r >= 4) or (c < 0 or c>=4):
                        print("Invalid entry (Try again)!")
                        continue
                    flag = False
                    best_move = (r, c)
            else:
                _, best_move = minimax(state, depth=k, is_Max=False)
                print("AI Player 2 (O) thinking...")

        time.sleep(delay_seconds)  # Add delay to make the game visible

        if best_move:
            state = state.make_move(best_move, current_player)
            print(f"AI plays at position: {best_move}")

        winner = state.check_winner()
        if winner:
            print_board(state)
            if winner == 'draw':
                print("\nGame is a draw!")
            else:
                print(f"\nAI Player {'X' if winner == PLAYER_MAX else 'O'} ({winner}) wins!")
            break

        current_player = PLAYER_MAX if current_player == PLAYER_MIN else PLAYER_MIN


if __name__ == "__main__":

    input_board = []
    flag = True
    while flag:
        try:
            k = int(input("Enter k: "))
            input_board = list(map(int, input("Enter board as a list of 16 numbers in a single line:\n(-1 for Min, +1 for Max and 0 for blank)\n").strip().split()))
            current_player = int(input("1 for Max's turn, -1 for Min's turn: "))
            takeUserInput = input("Play yourself instead of Min? [yes/no]: ").lower().strip()
        except Exception as e:
            print("error occured while taking input: ", e)

        if len(input_board) != 16:
            print("Enter valid board! (length != 16)")
            continue
        flag = False
    input_board = [input_board[4 * i:4*i+4] for i in range(4)]
    print(input_board)
    play_ai_vs_ai(input_board, current_player, k, True if takeUserInput=='yes' else False)
