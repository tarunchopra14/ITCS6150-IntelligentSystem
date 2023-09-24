"""
Main entry point for the 3D Tic Tac Toe game.

This module integrates the game's UI, logic, play, and AI functionalities. 
It initializes the board, sets the game's difficulty, and manages the turns 
of the player and the computer opponent using a loop until a win condition 
is met or the game ends in a tie.
"""

import game_ai

def is_valid_move(board, move):
    """
    Checks if a move at the given level, row, and column is valid.
    
    Args:
        board (list): The 3D game board.
        move (tuple): A tuple representing a move (level, row, col).

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    level, row, col = move

    return board[level][row][col] == 0

def make_move(board, move, player):
    """
    Place a move on the board.
    
    Args:
        board (list): The 3D game board.
        move (tuple): A tuple representing a move (level, row, col).
        player (int): The player making the move (1 or -1).

    Returns:
        list: The updated game board.
    """
    level, row, col = move
    board[level][row][col] = player
    return board

def computer_move(board, difficulty):
    """
    Determine the computer's move based on the current board state and difficulty.
    This implementation uses the Minimax algorithm with alpha-beta pruning.
    
    Args:
        board (list): The 3D game board.
        difficulty (int): The depth for the alpha-beta pruning.

    Returns:
        tuple: The chosen move for the computer as (level, row, col).
    """
    _, move = game_ai.alpha_beta(-1, difficulty, float('-inf'), float('inf'), board)
    return move
