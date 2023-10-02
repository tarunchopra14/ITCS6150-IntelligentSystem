"""
game_ai.py

This file implements the AI logic for a 3D Tic Tac Toe game. 
The AI uses the alpha-beta pruning algorithm to determine the best move.

Functions:
    - alpha_beta: Implements the alpha-beta pruning algorithm.
"""

import game_logic

GOOD_ENOUGH_THRESHOLD = 500  # Adjust as per requirements

def alpha_beta(player, depth, alpha, beta,board):
    """
    Implement the alpha-beta pruning algorithm to find the best move.

    Args:
        player (int): 1 for the MAX player, -1 for the MIN player.
        depth (int): Depth to search for the alpha-beta pruning.
        alpha (float): Alpha value for the algorithm.
        beta (float): Beta value for the algorithm.
        board (list): The current state of the game board.

    Returns:
        tuple: Best value calculated by the algorithm and the best move as (z, x, y).
    """

    if depth == 0 or game_logic.check_win(1,board) or game_logic.check_win(-1,board):
        return game_logic.evaluate(board), None

    moves = order_moves(player,board)
    if player == -1:
        best_value = float('inf')
        best_move = None
        for move in moves:
            z, x, y = move
            board[z][x][y] = player
            value, _ = alpha_beta(1, depth - 1, alpha, beta, board)
            board[z][x][y] = 0
            if value < best_value:
                best_value = value
                best_move = (z, x, y)
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value, best_move
    else:
        best_value = float('-inf')
        best_move = None
        for move in moves:
            z, x, y = move
            board[z][x][y] = player
            value, _ = alpha_beta(-1, depth - 1, alpha, beta,board)
            board[z][x][y] = 0
            if value > best_value:
                best_value = value
                best_move = (z, x, y)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
    return best_value, best_move


def order_moves(player,board):
    moves = []
    for z in range(4):
        for x in range(4):
            for y in range(4):
                if board[z][x][y] == 0:
                    score = 0  # Default score
                    # Prioritize center cells
                    if z in [1, 2] and x in [1, 2] and y in [1, 2]:
                        score = 1 if player == 1 else -1
                    moves.append(((z, x, y), score))

    return [move for move, _ in sorted(moves, key=lambda item: item[1], reverse=(player == 1))]