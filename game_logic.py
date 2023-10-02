"""
game_logic.py

This file contains the core logic functions for the 3D Tic Tac Toe game:
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
        # Rows and columns
        for i in range(4):
            if all(board[z][i][j] == player for j in range(4)) or all(board[z][j][i] == player for j in range(4)):
                return True
        # Diagonals
        if all(board[z][i][i] == player for i in range(4)) or all(board[z][i][3 - i] == player for i in range(4)):
            return True
    # Check vertical columns
    for x in range(4):
        for y in range(4):
            if all(board[z][x][y] == player for z in range(4)):
                return True
    # Check 3D diagonals
    if all(board[i][i][i] == player for i in range(4)) or all(board[i][i][3 - i] == player for i in range(4)):
        return True
    if all(board[i][3 - i][i] == player for i in range(4)) or all(board[i][3 - i][3 - i] == player for i in range(4)):
        return True
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

"""
    evaluate()
    Evaluates the current state of the board and returns a score.
    
    Returns:
    - int: The evaluation score of the board. 
           A positive score is good for "X", a negative score is good for "O", and 0 indicates a neutral board.
"""

def evaluate(board):
    if check_win(1,board):
        return 100
    elif check_win(-1,board):
        return -100
    else:
        return evaluate_lines(board)

"""
    evaluate_lines()
    Evaluates all lines (rows, columns, diagonals) on the board for their potential to lead to a win.
    
    Returns:
    - int: The evaluation score based on the board lines.
"""

def evaluate_lines(board):
    score = 0
    for z in range(4):
        for x in range(4):
            for y in range(4):
                if board[z][x][y] == 0:
                    score += evaluate_direction(z, x, y, 1, 0, 0,board)  # Forward
                    score += evaluate_direction(z, x, y, 0, 1, 0,board)  # Right
                    score += evaluate_direction(z, x, y, 0, 0, 1,board)  # Up
                    # Add other directions like diagonals, etc.
    return score


"""
    evaluate_direction(z, x, y, dz, dx, dy)
    Evaluates a specific direction from a given starting point on the board.
    
    Args:
    - z, x, y (int): The starting point's layer, row, and column respectively.
    - dz, dx, dy (int): The direction to move in the z, x, and y dimensions respectively.
    
    Returns:
    - int: The evaluation score based on the board's direction.
"""

def evaluate_direction(z, x, y, dz, dx, dy,board):
    player_count = 0
    opponent_count = 0
    for i in range(4):
        if 0 <= z + dz*i < 4 and 0 <= x + dx*i < 4 and 0 <= y + dy*i < 4:
            if board[z + dz*i][x + dx*i][y + dy*i] == 1:
                player_count += 1
            elif board[z + dz*i][x + dx*i][y + dy*i] == -1:
                opponent_count += 1

    if player_count == 3 and opponent_count == 0:
        return 10
    elif player_count == 2 and opponent_count == 0:
        return 3
    elif player_count == 1 and opponent_count == 0:
        return 1
    elif opponent_count == 3 and player_count == 0:
        return -10
    elif opponent_count == 2 and player_count == 0:
        return -3
    elif opponent_count == 1 and player_count == 0:
        return -1
    else:
        return 0
