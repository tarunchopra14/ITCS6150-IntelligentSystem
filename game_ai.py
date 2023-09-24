"""
game_ai.py

This file implements the AI logic for a 3D Tic Tac Toe game. 
The AI uses the alpha-beta pruning algorithm to determine the best move.

Functions:
    - alpha_beta: Implements the alpha-beta pruning algorithm.
"""

import game_logic

GOOD_ENOUGH_THRESHOLD = 500  # Adjust as per requirements

def alpha_beta(player, depth, alpha, beta, board):
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
    if depth == 0 or game_logic.check_win(1, board) or game_logic.check_win(-1, board):  # Terminal state or depth limit reached
        return game_logic.evaluate(board, depth), None

    best_move = None

    # Logic for MAX player (i.e., our player)
    if player == 1:
        best_value = float('-inf')
        
        # Check all possible moves
        for z in range(4):
            for x in range(4):
                for y in range(4):
                    if board[z][x][y] == 0:  # if cell is empty
                        board[z][x][y] = player  # make a move
                        value, _ = alpha_beta(-1, depth - 1, alpha, beta, board)  # simulate opponent's turn
                        board[z][x][y] = 0  # undo the move

                        # Update best value and move if needed
                        if value > best_value:
                            best_value = value
                            best_move = (z, x, y)

                        # If a move is found that's "good enough", break out
                        print("CHECK MAX " + str(best_value >= GOOD_ENOUGH_THRESHOLD))
                        if best_value >= GOOD_ENOUGH_THRESHOLD:
                            return best_value, best_move

                        # Update alpha and prune if necessary
                        alpha = max(alpha, best_value)
                        if beta <= alpha:
                            break  # pruning

    # Logic for MIN player (i.e., the opponent)
    else:
        best_value = float('inf')
        
        # Check all possible moves
        for z in range(4):
            for x in range(4):
                for y in range(4):
                    if board[z][x][y] == 0:  # if cell is empty
                        board[z][x][y] = player  # make a move
                        value, _ = alpha_beta(1, depth - 1, alpha, beta, board)  # simulate our turn
                        board[z][x][y] = 0  # undo the move

                        # Update best value and move if needed
                        if value < best_value:
                            best_value = value
                            best_move = (z, x, y)

                        # If a move is found that's "bad enough", break out
                        print("CHECK MIN " + str(best_value <= -GOOD_ENOUGH_THRESHOLD))
                        if best_value <= -GOOD_ENOUGH_THRESHOLD:
                            return best_value, best_move

                        # Update beta and prune if necessary
                        beta = min(beta, best_value)
                        if beta <= alpha:
                            break  # pruning
    
    return best_value, best_move