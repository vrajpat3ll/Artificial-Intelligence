class OthelloState:
    def __init__(self, board=None):
        if board is None:
            # Initialize standard 8x8 Othello board
            self.board = [[' ' for _ in range(8)] for _ in range(8)]
            # Set up initial pieces
            self.board[3][3] = self.board[4][4] = 'W'  # White pieces
            self.board[3][4] = self.board[4][3] = 'B'  # Black pieces
        else:
            self.board = [row[:] for row in board]
    
    def print_board(self):
        print('  0 1 2 3 4 5 6 7')
        for i, row in enumerate(self.board):
            print(f"{i} {'.'.join(row)}")
    
    def is_valid_move(self, move, player):
        if not self._is_on_board(move):
            return False
        
        if self.board[move[0]][move[1]] != ' ':
            return False
        
        opponent = 'W' if player == 'B' else 'B'
        
        for dx, dy in [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]:
            x, y = move[0] + dx, move[1] + dy
            if not self._is_on_board((x, y)) or self.board[x][y] != opponent:
                continue
                
            x, y = x + dx, y + dy
            while self._is_on_board((x, y)):
                if self.board[x][y] == ' ':
                    break
                if self.board[x][y] == player:
                    return True
                x, y = x + dx, y + dy
        
        return False
    
    def _is_on_board(self, pos):
        return 0 <= pos[0] < 8 and 0 <= pos[1] < 8
    
    def get_valid_moves(self, player):
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if self.is_valid_move((i, j), player):
                    valid_moves.append((i, j))
        return valid_moves
    
    def make_move(self, move, player):
        if not self.is_valid_move(move, player):
            return None
        
        new_state = OthelloState(self.board)
        new_state.board[move[0]][move[1]] = player
        opponent = 'W' if player == 'B' else 'B'
        
        for dx, dy in [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]:
            pieces_to_flip = []
            x, y = move[0] + dx, move[1] + dy
            
            while self._is_on_board((x, y)) and self.board[x][y] == opponent:
                pieces_to_flip.append((x, y))
                x, y = x + dx, y + dy
                
            if self._is_on_board((x, y)) and self.board[x][y] == player:
                for flip_x, flip_y in pieces_to_flip:
                    new_state.board[flip_x][flip_y] = player
                    
        return new_state
    
    def get_score(self):
        black_count = sum(row.count('B') for row in self.board)
        white_count = sum(row.count('W') for row in self.board)
        return black_count - white_count
    
    def is_game_over(self):
        return (not self.get_valid_moves('B') and 
                not self.get_valid_moves('W'))

def evaluate_position(state):
    # Position evaluation weights
    CORNER_WEIGHT = 25
    EDGE_WEIGHT = 5
    MOBILITY_WEIGHT = 2
    
    corners = [(0,0), (0,7), (7,0), (7,7)]
    edges = [(i,j) for i in range(8) for j in range(8) 
             if i in (0,7) or j in (0,7)]
    
    score = state.get_score()
    
    # Add corner bonus/penalty
    for corner in corners:
        if state.board[corner[0]][corner[1]] == 'B':
            score += CORNER_WEIGHT
        elif state.board[corner[0]][corner[1]] == 'W':
            score -= CORNER_WEIGHT
    
    # Add edge bonus/penalty
    for edge in edges:
        if state.board[edge[0]][edge[1]] == 'B':
            score += EDGE_WEIGHT
        elif state.board[edge[0]][edge[1]] == 'W':
            score -= EDGE_WEIGHT
    
    # Add mobility bonus/penalty
    black_mobility = len(state.get_valid_moves('B'))
    white_mobility = len(state.get_valid_moves('W'))
    score += MOBILITY_WEIGHT * (black_mobility - white_mobility)
    
    return score


# Alpha-Beta pruning
def minimax(state, depth, alpha, beta, maximizing_player):
    if depth == 0 or state.is_game_over():
        return evaluate_position(state), None
    
    player = 'B' if maximizing_player else 'W'
    valid_moves = state.get_valid_moves(player)
    
    if not valid_moves:
        # If no valid moves, pass turn
        score, _ = minimax(state, depth-1, alpha, beta, not maximizing_player)
        return score, None
    
    best_move = None
    if maximizing_player:
        max_eval = float('-inf')
        for move in valid_moves:
            new_state = state.make_move(move, player)
            eval_score, _ = minimax(new_state, depth-1, alpha, beta, False)
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in valid_moves:
            new_state = state.make_move(move, player)
            eval_score, _ = minimax(new_state, depth-1, alpha, beta, True)
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def play_game():
    state = OthelloState()
    current_player = 'B'  # Black moves first
    
    while not state.is_game_over():
        state.print_board()
        valid_moves = state.get_valid_moves(current_player)
        
        if not valid_moves:
            print(f"No valid moves for {current_player}. Passing turn.")
            current_player = 'W' if current_player == 'B' else 'B'
            continue
        
        if current_player == 'B':
            # AI move
            _, move = minimax(state, depth=4, alpha=float('-inf'), 
                            beta=float('inf'), maximizing_player=True)
            print(f"AI1 plays at: {move}")
        else:
            _, move = minimax(state, depth=4, alpha=float('-inf'), 
                            beta=float('inf'), maximizing_player=False)
            print(f"AI2 plays at: {move}")
            # Human move
            # while True:
            #     try:
            #         row = int(input("Enter row (0-7): "))
            #         col = int(input("Enter column (0-7): "))
            #         move = (row, col)
            #         if move in valid_moves:
            #             break
            #         print("Invalid move. Try again.")
            #     except ValueError:
            #         print("Please enter valid numbers.")
        
        state = state.make_move(move, current_player)
        current_player = 'W' if current_player == 'B' else 'B'
    
    # Game over
    state.print_board()
    score = state.get_score()
    if score > 0:
        print("Black wins!")
    elif score < 0:
        print("White wins!")
    else:
        print("It's a tie!")
    print(f"Final score - Black: {sum(row.count('B') for row in state.board)}, "
          f"White: {sum(row.count('W') for row in state.board)}")

if __name__ == "__main__":
    play_game()
