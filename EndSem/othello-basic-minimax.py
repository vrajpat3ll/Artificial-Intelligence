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
        
        # Check all eight directions
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
        
        # Flip pieces in all eight directions
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
    
    def evaluate_position(self):
        # Simple evaluation function
        CORNER_WEIGHT = 25
        EDGE_WEIGHT = 5
        
        score = 0
        corners = [(0,0), (0,7), (7,0), (7,7)]
        edges = [(i,j) for i in range(8) for j in range(8) 
                if i in (0,7) or j in (0,7)]
        
        # Count pieces
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 'B':
                    score += 1
                elif self.board[i][j] == 'W':
                    score -= 1
        
        # Add corner bonuses/penalties
        for corner in corners:
            if self.board[corner[0]][corner[1]] == 'B':
                score += CORNER_WEIGHT
            elif self.board[corner[0]][corner[1]] == 'W':
                score -= CORNER_WEIGHT
        
        # Add edge bonuses/penalties
        for edge in edges:
            if self.board[edge[0]][edge[1]] == 'B':
                score += EDGE_WEIGHT
            elif self.board[edge[0]][edge[1]] == 'W':
                score -= EDGE_WEIGHT
                
        return score
    
    def is_game_over(self):
        return (not self.get_valid_moves('B') and 
                not self.get_valid_moves('W'))
    
    def get_winner(self):
        if not self.is_game_over():
            return None
            
        black_count = sum(row.count('B') for row in self.board)
        white_count = sum(row.count('W') for row in self.board)
        
        if black_count > white_count:
            return 'B'
        elif white_count > black_count:
            return 'W'
        else:
            return 'draw'

def minimax(state, depth, maximizing_player):
    """
    Basic minimax algorithm without alpha-beta pruning
    Returns (score, best_move)
    """
    if depth == 0 or state.is_game_over():
        return state.evaluate_position(), None
    
    player = 'B' if maximizing_player else 'W'
    valid_moves = state.get_valid_moves(player)
    
    if not valid_moves:
        # If no valid moves, pass turn
        score, _ = minimax(state, depth-1, not maximizing_player)
        return score, None
    
    best_move = None
    if maximizing_player:
        max_eval = float('-inf')
        for move in valid_moves:
            new_state = state.make_move(move, player)
            eval_score, _ = minimax(new_state, depth-1, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in valid_moves:
            new_state = state.make_move(move, player)
            eval_score, _ = minimax(new_state, depth-1, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move

def play_ai_vs_ai(delay_seconds=1):
    """Play a game between two AI players"""
    import time
    
    state = OthelloState()
    current_player = 'B'  # Black moves first
    move_count = 0
    passes = 0  # Count consecutive passes
    
    print("Starting AI vs AI Othello game...")
    print("B: AI Player 1 (Maximizer)")
    print("W: AI Player 2 (Minimizer)\n")
    
    while not state.is_game_over():
        state.print_board()
        move_count += 1
        print(f"\nMove #{move_count}")
        
        valid_moves = state.get_valid_moves(current_player)
        
        if not valid_moves:
            print(f"\nNo valid moves for {current_player}. Passing turn.")
            passes += 1
            if passes >= 2:  # Both players passed consecutively
                break
        else:
            passes = 0  # Reset consecutive passes counter
            
            # Get AI move
            print(f"AI Player ({'Black' if current_player == 'B' else 'White'}) thinking...")
            time.sleep(delay_seconds)
            
            # Use lower depth (3) for faster gameplay
            _, move = minimax(state, depth=3, maximizing_player=(current_player == 'B'))
            
            if move:
                state = state.make_move(move, current_player)
                print(f"AI plays at: {move}")
        
        current_player = 'W' if current_player == 'B' else 'B'
    
    # Game over
    print("\nGame Over!")
    state.print_board()
    
    black_count = sum(row.count('B') for row in state.board)
    white_count = sum(row.count('W') for row in state.board)
    
    print(f"\nFinal score:")
    print(f"Black: {black_count}")
    print(f"White: {white_count}")
    
    if black_count > white_count:
        print("\nBlack wins!")
    elif white_count > black_count:
        print("\nWhite wins!")
    else:
        print("\nIt's a tie!")

if __name__ == "__main__":
    play_ai_vs_ai()
