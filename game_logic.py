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

    # Immediate win/loss
    if check_win(1, board):  # Player wins
        return 1000 / (depth + 1)
    elif check_win(-1, board):  # Opponent wins
        return -1000 / (depth + 1)

    score = 0

    # Check patterns function
    def check_pattern(target_sum, player):
        nonlocal score
        multiplier = 50 if target_sum == 2 else 150
        multiplier = multiplier if player == 1 else -multiplier
        local_score = 0
        for z in range(4):
            for i in range(4):
                if sum(board[z][i]) == target_sum * player or \
                   sum([board[z][j][i] for j in range(4)]) == target_sum * player:
                    local_score += multiplier
                if sum([board[z][i][i] for i in range(4)]) == target_sum * player or \
                   sum([board[z][i][3-i] for i in range(4)]) == target_sum * player:
                    local_score += multiplier

            for x in range(4):
                for y in range(4):
                    if sum([board[k][x][y] for k in range(4)]) == target_sum * player:
                        local_score += multiplier

            if sum([board[i][i][i] for i in range(4)]) == target_sum * player or \
               sum([board[i][3-i][i] for i in range(4)]) == target_sum * player or \
               sum([board[i][i][3-i] for i in range(4)]) == target_sum * player or \
               sum([board[i][3-i][3-i] for i in range(4)]) == target_sum * player:
                local_score += multiplier
        score += local_score

    # Check for two in a row
    for player in [1, -1]:
        check_pattern(2, player)

    # Check for almost wins (3 in a row)
    for player in [1, -1]:
        check_pattern(3, player)

    # Center control
    center_positions = [(1, 1, 1), (1, 1, 2), (1, 2, 1), (1, 2, 2), 
                        (2, 1, 1), (2, 1, 2), (2, 2, 1), (2, 2, 2)]
    for pos in center_positions:
        if board[pos[0]][pos[1]][pos[2]] == 1:
            score += 10  # Bonus for player control
        elif board[pos[0]][pos[1]][pos[2]] == -1:
            score -= 10  # Penalty for opponent control

    # Scale the score based on depth
    if depth != 0:
        score = score / depth

    return score
