#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const int INF = 1000000; // A large value representing infinity
const int SIZE = 8;      // Othello board size

enum Player { EMPTY = 0, PLAYER1 = 1, PLAYER2 = 2 };

struct Move {
    int row, col;
};

// A function to evaluate the board
int evaluateBoard(const vector<vector<int>>& board) {
    int score = 0;
    for (int i = 0; i < SIZE; ++i) {
        for (int j = 0; j < SIZE; ++j) {
            if (board[i][j] == PLAYER1) score++;
            else if (board[i][j] == PLAYER2) score--;
        }
    }
    return score;
}

// Check if a move is valid for the given player
bool isValidMove(const vector<vector<int>>& board, int row, int col, int player) {
    if (board[row][col] != EMPTY) return false;
    // Directions: right, left, down, up, and diagonal
    int directions[8][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}, {1, 1}, {1, -1}, {-1, 1}, {-1, -1}};
    bool isValid = false;
    
    for (auto& dir : directions) {
        int x = row + dir[0], y = col + dir[1];
        bool foundOpponent = false;
        
        while (x >= 0 && x < SIZE && y >= 0 && y < SIZE && board[x][y] != EMPTY) {
            if (board[x][y] == 3 - player) {
                foundOpponent = true;
            }
            else if (board[x][y] == player) {
                if (foundOpponent) isValid = true;
                break;
            }
            x += dir[0];
            y += dir[1];
        }
    }
    return isValid;
}

// Apply a move on the board
void applyMove(vector<vector<int>>& board, int row, int col, int player) {
    board[row][col] = player;
    int directions[8][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}, {1, 1}, {1, -1}, {-1, 1}, {-1, -1}};
    
    for (auto& dir : directions) {
        int x = row + dir[0], y = col + dir[1];
        vector<pair<int, int>> toFlip;
        
        while (x >= 0 && x < SIZE && y >= 0 && y < SIZE && board[x][y] != EMPTY) {
            if (board[x][y] == 3 - player) {
                toFlip.push_back({x, y});
            }
            else if (board[x][y] == player) {
                for (auto& flip : toFlip) {
                    board[flip.first][flip.second] = player;
                }
                break;
            }
            x += dir[0];
            y += dir[1];
        }
    }
}

// Generate all valid moves for the current player
vector<Move> generateMoves(const vector<vector<int>>& board, int player) {
    vector<Move> moves;
    for (int i = 0; i < SIZE; ++i) {
        for (int j = 0; j < SIZE; ++j) {
            if (isValidMove(board, i, j, player)) {
                moves.push_back({i, j});
            }
        }
    }
    return moves;
}

// Alpha-Beta Pruning algorithm
int alphaBeta(vector<vector<int>>& board, int depth, int player, int alpha, int beta, bool isMaximizing) {
    if (depth == 0) return evaluateBoard(board);

    vector<Move> moves = generateMoves(board, player);
    if (moves.empty()) return evaluateBoard(board); // No valid moves

    if (isMaximizing) {
        int maxValue = -INF;
        for (const auto& move : moves) {
            vector<vector<int>> newBoard = board;
            applyMove(newBoard, move.row, move.col, player);
            
            int value = alphaBeta(newBoard, depth - 1, 3 - player, alpha, beta, false);
            maxValue = max(maxValue, value);
            alpha = max(alpha, maxValue);
            if (alpha >= beta) break; // Beta cut-off
        }
        return maxValue;
    } else {
        int minValue = INF;
        for (const auto& move : moves) {
            vector<vector<int>> newBoard = board;
            applyMove(newBoard, move.row, move.col, player);
            
            int value = alphaBeta(newBoard, depth - 1, 3 - player, alpha, beta, true);
            minValue = min(minValue, value);
            beta = min(beta, minValue);
            if (alpha >= beta) break; // Alpha cut-off
        }
        return minValue;
    }
}

// Find the best move for the current player using Alpha-Beta Pruning
Move findBestMove(vector<vector<int>>& board, int player, int depth) {
    int bestValue = -INF;
    Move bestMove = {-1, -1};
    
    vector<Move> moves = generateMoves(board, player);
    int alpha = -INF, beta = INF;

    for (const auto& move : moves) {
        vector<vector<int>> newBoard = board;
        applyMove(newBoard, move.row, move.col, player);

        int moveValue = alphaBeta(newBoard, depth - 1, 3 - player, alpha, beta, false);
        if (moveValue > bestValue) {
            bestValue = moveValue;
            bestMove = move;
        }
    }
    
    return bestMove;
}

// Get user input for their move
Move getUserMove(const vector<vector<int>>& board) {
    int row, col;
    while (true) {
        cout << "Enter your move (row and column): ";
        cin >> row >> col;

        if (row >= 0 && row < SIZE && col >= 0 && col < SIZE && isValidMove(board, row, col, PLAYER1)) {
            return {row, col};
        } else {
            cout << "Invalid move. Please try again." << endl;
        }
    }
}

void printBoard(const vector<vector<int>>& board) {
    cout << "  ";
    for (int j = 0; j < SIZE; ++j) {
        cout << j << " ";
    }
    cout << "\n";

    for (int i = 0; i < SIZE; ++i) {
        cout << i << " "; // Print the row number
        for (int j = 0; j < SIZE; ++j) {
            cout << (board[i][j] == PLAYER1 ? "X" : (board[i][j] == PLAYER2 ? "O" : ".")) << " ";
        }
        cout << "\n";
    }
}

int main() {
    vector<vector<int>> board(SIZE, vector<int>(SIZE, EMPTY));
    
    // Initializing the board
    board[3][3] = board[4][4] = PLAYER1;
    board[3][4] = board[4][3] = PLAYER2;

    int player = PLAYER1;
    int depth = 3; // Depth for Alpha-Beta

    while (true) {
        printBoard(board);

        if (player == PLAYER1) {
            // User's move
            Move userMove = getUserMove(board);
            applyMove(board, userMove.row, userMove.col, PLAYER1);
        } else {
            // AI's move using Alpha-Beta
            Move bestMove = findBestMove(board, PLAYER2, depth);
            cout << "AI (Player 2) plays: (" << bestMove.row << ", " << bestMove.col << ")\n";
            applyMove(board, bestMove.row, bestMove.col, PLAYER2);
        }

        // Switch player
        player = 3 - player;

        // Check for game over (no valid moves left for both players)
        vector<Move> userMoves = generateMoves(board, PLAYER1);
        vector<Move> aiMoves = generateMoves(board, PLAYER2);
        if (userMoves.empty() && aiMoves.empty()) {
            cout << "Game Over!" << endl;
            break;
        }
    }

    printBoard(board);
    return 0;
}
