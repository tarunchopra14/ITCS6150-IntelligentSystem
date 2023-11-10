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


def evaluate(board, depth):
    """
    Evaluate the game state.
    
    Args:
        board: The current state of the game board.
        depth: Current depth in the search tree.

    Returns:
        int: 
            Scaled score based on the depth.
    """

    # Check for immediate win/loss FIRST
    if check_win(1, board):  # Player wins
        return 10000
    elif check_win(-1, board):  # Opponent (AI) wins
        return -10000

    score = 0

    # Check patterns function
    def check_pattern(target_sum, player):
        nonlocal score
        multiplier = 50 if target_sum == 2 else 100
        multiplier = multiplier if player == 1 else -multiplier 
        local_score = 0
        
        def add_to_score():
            nonlocal local_score
            local_score += multiplier

        # 2D Check:
        for z in range(4):
            for i in range(4):
                if sum(board[z][i]) == target_sum * player or \
                sum([board[z][j][i] for j in range(4)]) == target_sum * player:
                    add_to_score()

                if sum([board[z][i][i] for i in range(4)]) == target_sum * player or \
                sum([board[z][i][3-i] for i in range(4)]) == target_sum * player:
                    add_to_score()

        # 3D Check:
        for x in range(4):
            for y in range(4):
                if sum([board[k][x][y] for k in range(4)]) == target_sum * player:
                    add_to_score()

        for pattern in [[(i, i, i) for i in range(4)],
                        [(i, 3-i, i) for i in range(4)],
                        [(i, i, 3-i) for i in range(4)],
                        [(i, 3-i, 3-i) for i in range(4)],
                        [(i, 3-i, y) for i in range(4) for y in range(4)],
                        [(i, i, y) for i in range(4) for y in range(4)],
                        [(i, x, 3-i) for i in range(4) for x in range(4)],
                        [(i, x, i) for i in range(4) for x in range(4)]]:
            if all(board[i][j][k] == player for i, j, k in pattern):
                add_to_score()

        # Accumulate the local score
        score += local_score

    # Check for almost wins (3 in a row)
    for player in [1, -1]:
        check_pattern(3, player)

    print("Score after checking 3 in a row: " + str(score))

    # Check for two in a row
    for player in [1, -1]:
        check_pattern(2, player)

    print("Score after checking 2 in a row: " + str(score))

    # Center control
    center_value = 20  # Adjust this value as per importance
    for z in [1, 2]:
        for x in [1, 2]:
            for y in [1, 2]:
                if board[z][x][y] == 1:  # Player
                    score -= center_value
                elif board[z][x][y] == -1:  # AI
                    score += center_value
    print("Score after center control: " + str(score))

    # Scale the score based on depth
    if depth != 0:
        score = score

    print("final " + str(score))
    return score