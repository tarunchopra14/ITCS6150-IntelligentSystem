"""
Main entry point for the 3D Tic Tac Toe game.

This module integrates the game's UI, logic, play, and AI functionalities. 
It initializes the board, sets the game's difficulty, and manages the turns 
of the player and the computer opponent using a loop until a win condition 
is met or the game ends in a tie.
"""

import game_ai

def get_player_move(board):
    """
    Prompt the player to make a move on the 3D Tic Tac Toe board.
    
    Args:
        board (list): The current 3D game board.
    
    Returns:
        tuple: A tuple containing the chosen coordinates (z, x, y) for the move.
    """
    while True:
        try:
            # Prompt the user for layer, row, and column.
            z = int(input("Enter layer (1-4): ")) - 1
            x = int(input("Enter row (1-4): ")) - 1
            y = int(input("Enter column (1-4): ")) - 1
            
            # Validate the move.
            if 0 <= z < 4 and 0 <= x < 4 and 0 <= y < 4 and board[z][x][y] == 0:
                return z, x, y  # Return the chosen coordinates.
            else:
                print("Invalid move. Try again.")
        except ValueError:
            # Handle non-integer inputs.
            print("Invalid input. Please enter a number between 1 and 4.")

def make_move(board, move, player):
    """
    Apply the player's move on the board.
    
    Args:
        board (list): The current 3D game board.
        move (tuple): A tuple containing the chosen coordinates (z, x, y) for the move.
        player (int): Represents whether it's the player's move (1) or the computer's (-1).
    
    Returns:
        list: Updated game board after the move.
    """
    z, x, y = move
    board[z][x][y] = player
    return board

def computer_move(board, difficulty):
    """
    Get the computer's move using the alpha-beta pruning algorithm.
    
    Args:
        board (list): The current 3D game board.
        difficulty (int): Depth for the alpha-beta pruning.
    
    Returns:
        tuple: A tuple containing the chosen coordinates (z, x, y) for the move.
    """
    _, move = game_ai.alpha_beta(-1, difficulty, float('-inf'), float('inf'), board)
    return move
