#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

const int INF = 1000000;  // A large value representing infinity
const int SIZE = 8;       // Othello board size

enum Player { EMPTY = 0,
              PLAYER1 = 1,
              PLAYER2 = 2 };

struct Move {
    int row, col;
};

// A function to evaluate the board
int evaluateBoard(const vector<vector<int>>& board) {
    int score = 0;
    for (int i = 0; i < SIZE; ++i) {
        for (int j = 0; j < SIZE; ++j) {
            if (board[i][j] == PLAYER1)
                score++;
            else if (board[i][j] == PLAYER2)
                score--;
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
            } else if (board[x][y] == player) {
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
            } else if (board[x][y] == player) {
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

// Minimax algorithm
int minimax(vector<vector<int>>& board, int depth, int player, bool isMaximizing) {
    if (depth == 0) return evaluateBoard(board);

    vector<Move> moves = generateMoves(board, player);
    if (moves.empty()) return evaluateBoard(board);  // No valid moves

    int bestValue = isMaximizing ? -INF : INF;

    for (const auto& move : moves) {
        vector<vector<int>> newBoard = board;
        applyMove(newBoard, move.row, move.col, player);

        int value = minimax(newBoard, depth - 1, 3 - player, !isMaximizing);
        if (isMaximizing)
            bestValue = max(bestValue, value);
        else
            bestValue = min(bestValue, value);
    }

    return bestValue;
}

// Find the best move for the current player
Move findBestMove(vector<vector<int>>& board, int player, int depth) {
    int bestValue = -INF;
    Move bestMove = {-1, -1};

    vector<Move> moves = generateMoves(board, player);
    for (const auto& move : moves) {
        vector<vector<int>> newBoard = board;
        applyMove(newBoard, move.row, move.col, player);

        int moveValue = minimax(newBoard, depth - 1, 3 - player, false);
        if (moveValue > bestValue) {
            bestValue = moveValue;
            bestMove = move;
        }
    }

    return bestMove;
}
void printBoard(vector<vector<int>>& board) {
    for (int i = 0; i < SIZE; ++i) {
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
    int depth = 7;  // Depth for Minimax

    while (true) {
        Move bestMove = findBestMove(board, player, depth);
        if (bestMove.row == -1) break;  // No more valid moves

        applyMove(board, bestMove.row, bestMove.col, player);
        printBoard(board);
        cout << "Player " << player << " played: (" << bestMove.row << ", " << bestMove.col << ")\n";
        player = 3 - player;  // Switch players
    }
    printBoard(board);
    if (evaluateBoard(board) > 0) {
        cout << "Player (X) wins!"<<endl;
    }else
        cout << "Player (O) wins!"<<endl;

    return 0;
}
