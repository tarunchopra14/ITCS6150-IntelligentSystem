"""
game_logic.py

This module contains the core logic functions for the 3D Tic Tac Toe game:
    1. Function to check for a winning condition.
    2. Function to evaluate the game state (for AI).
"""

def check_win(player, board):
    """
    Check if the specified player has won in the 4x4x4 3D tic-tac-toe board.

    Parameters:
    - player (int/str): The player's mark (usually an integer or string indicating the player).
    - board (3D list): A 4x4x4 list representing the game board. E.g., board[z][x][y] 
                       gives the mark at layer z, row x, and column y.

    Returns:
    - bool: True if the player has won, otherwise False.
    """

    # 2D Check:
    for z in range(4):
        # Check rows and columns for each layer (z)
        for i in range(4):
            if all(board[z][i][j] == player for j in range(4)) or \
               all(board[z][j][i] == player for j in range(4)):
                return True

        # Check two 2D diagonals for each layer (z)
        if all(board[z][i][i] == player for i in range(4)) or \
           all(board[z][i][3 - i] == player for i in range(4)):
            return True

    # 3D Check:
    # Check vertical stack across the layers
    for x in range(4):
        for y in range(4):
            if all(board[k][x][y] == player for k in range(4)):
                return True

    # Check 3D main diagonals
    # Top-left of top layer to bottom-right of bottom layer
    if all(board[i][i][i] == player for i in range(4)):
        return True

    # Top-right of top layer to bottom-left of bottom layer
    if all(board[i][3-i][i] == player for i in range(4)):
        return True

    # Bottom-left of top layer to top-right of bottom layer
    if all(board[i][i][3-i] == player for i in range(4)):
        return True

    # Bottom-right of top layer to top-left of bottom layer
    if all(board[i][3-i][3-i] == player for i in range(4)):
        return True

    # Check 3D diagonals across rows and columns
    # Diagonal top to bottom layer through each column
    for y in range(4):
        if all(board[i][3-i][y] == player for i in range(4)):
            return True
        
    # Diagonal bottom to top layer through each column
    for y in range(4):
        if all(board[i][i][y] == player for i in range(4)):
            return True

    # Diagonal top to bottom layer through each row
    for x in range(4):
        if all(board[i][x][3-i] == player for i in range(4)):
            return True

    # Diagonal bottom to top layer through each row
    for x in range(4):
        if all(board[i][x][i] == player for i in range(4)):
            return True

    # If none of the above conditions were met, the player hasn't won
    return False


def is_board_full(board):
    """
    Check if the game board is full.

    Args:
    - board (list): 3D list representing the game board.

    Returns:
    - bool: True if the board is full, False otherwise.
    """
    for layer in board:
        for row in layer:
            for cell in row:
                if cell == 0:  # Assuming 0 represents an empty cell
                    return False
    return True


def evaluate(board):
    """
    Evaluate the game state.

    Returns:
        int: 
            100 if the player wins,
            -100 if the opponent wins,
            0 otherwise.
    """
    if check_win(1, board):  # Player wins
        return 100
    elif check_win(-1, board):  # Opponent wins
        return -100
    else:
        return 0
