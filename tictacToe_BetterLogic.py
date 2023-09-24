import random

# Define the Tic Tac Toe board as a 4x4x4 array (64 slots)
board = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]
difficulty = input("Select difficulty (easy, difficult, insane): ")

"""
    print_board():
    Displays the current state of the Tic Tac Toe board.
    Each layer of the board is printed separately.
"""

def print_board():
    for z in range(4):
        print(f"Layer {z + 1}:")
        for row in board[z]:
            print(" ".join(["X" if cell == 1 else "O" if cell == -1 else "." for cell in row]))
        print()

"""
    check_win(player)
    Checks if the given player has won the game.
    
    Args:
    - player (int): The player's marker (1 for "X", -1 for "O")
    
    Returns:
    - bool: True if the player has won, False otherwise.
"""

def check_win(player):
    # Check rows, columns, and diagonals
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

"""
    make_move(player)
    Executes a move for the given player. 
    If the player is human (1), it prompts them to input their move.
    If the player is the computer (-1), it calculates the best move using the alpha-beta pruning algorithm.
    
    Args:
    - player (int): The player's marker (1 for "X", -1 for "O")
"""

def make_move(player):
    if player == 1:
        print("Your turn (X)")
        while True:
            try:
                z = int(input("Enter layer (1-4): ")) - 1
                x = int(input("Enter row (1-4): ")) - 1
                y = int(input("Enter column (1-4): ")) - 1
                if 0 <= z < 4 and 0 <= x < 4 and 0 <= y < 4 and board[z][x][y] == 0:
                    board[z][x][y] = 1
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        print("Computer's turn (O)")
        alpha = float('-inf')
        beta = float('inf')
        empty_cells = sum(1 for z in range(4) for x in range(4) for y in range(4) if board[z][x][y] == 0)
        depth = get_max_depth(difficulty, empty_cells)
        # Use dynamic depth based on number of empty cells
        if empty_cells > 40:
            depth = 2
        elif 30 < empty_cells <= 40:
            depth = 3
        elif 20 < empty_cells <= 30:
            depth = 4
        else:
            depth = 5

        best_value, best_move = alpha_beta(player, depth, alpha, beta)
        z, x, y = best_move
        board[z][x][y] = -1

"""
    alpha_beta(player, depth, alpha, beta)
    Alpha-beta pruning algorithm to determine the best move for the computer.
    The function is recursive and evaluates potential moves using a depth-first search.
    
    Args:
    - player (int): The player's marker (1 for "X", -1 for "O")
    - depth (int): The current depth of the search.
    - alpha (float): The current best value achievable for the maximizing player.
    - beta (float): The current best value achievable for the minimizing player.
    
    Returns:
    - int: The evaluation value of the board after making the move.
    - tuple: The best move in the format (z, x, y) representing the layer, row, and column respectively.
"""


def alpha_beta(player, depth, alpha, beta):
    if depth == 0 or check_win(1) or check_win(-1):
        return evaluate(), None

    moves = order_moves(player)
    if player == -1:
        best_value = float('inf')
        best_move = None
        for move in moves:
            z, x, y = move
            board[z][x][y] = player
            value, _ = alpha_beta(1, depth - 1, alpha, beta)
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
            value, _ = alpha_beta(-1, depth - 1, alpha, beta)
            board[z][x][y] = 0
            if value > best_value:
                best_value = value
                best_move = (z, x, y)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value, best_move

"""
    evaluate()
    Evaluates the current state of the board and returns a score.
    
    Returns:
    - int: The evaluation score of the board. 
           A positive score is good for "X", a negative score is good for "O", and 0 indicates a neutral board.
"""

def evaluate():
    if check_win(1):
        return 100
    elif check_win(-1):
        return -100
    else:
        return evaluate_lines()

"""
    evaluate_lines()
    Evaluates all lines (rows, columns, diagonals) on the board for their potential to lead to a win.
    
    Returns:
    - int: The evaluation score based on the board lines.
"""

def evaluate_lines():
    score = 0
    for z in range(4):
        for x in range(4):
            for y in range(4):
                if board[z][x][y] == 0:
                    score += evaluate_direction(z, x, y, 1, 0, 0)  # Forward
                    score += evaluate_direction(z, x, y, 0, 1, 0)  # Right
                    score += evaluate_direction(z, x, y, 0, 0, 1)  # Up
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

def evaluate_direction(z, x, y, dz, dx, dy):
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



"""
    order_moves(player)
    Orders potential moves based on their heuristic score. 
    Central moves are prioritized as they have higher potential for winning or blocking.
    
    Args:
    - player (int): The player's marker (1 for "X", -1 for "O")
    
    Returns:
    - list: A list of potential moves ordered by their heuristic score.
"""

def order_moves(player):
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


"""
    get_max_depth(difficulty, empty_cells)
    Determines the maximum depth of the search based on the chosen difficulty level and the number of empty cells.
    
    Args:
    - difficulty (str): The chosen difficulty level ("easy", "difficult", "insane").
    - empty_cells (int): The number of unoccupied cells on the board
    Returns:
    - int: The maximum search depth.
 """

def get_max_depth(difficulty, empty_cells):
    """Returns the max depth based on the given difficulty level and the number of empty cells."""
    if difficulty == "easy":
        return 2
    elif difficulty == "difficult":
        if empty_cells > 40:
            return 2
        elif 30 < empty_cells <= 40:
            return 3
        elif 20 < empty_cells <= 30:
            return 4
        else:
            return 4
    elif difficulty == "insane":
        if empty_cells > 40:
            return 2
        elif 30 < empty_cells <= 40:
            return 4
        elif 20 < empty_cells <= 30:
            return 5
        else:
            return 6
    else:
        raise ValueError("Invalid difficulty level!")
    
    
# Main game loop
while True:
    print_board()
    make_move(1)
    if check_win(1):
        print("Congratulations! You win!")
        break
    if all(board[z][x][y] != 0 for z in range(4) for x in range(4) for y in range(4)):
        print("It's a tie!")
        break
    print_board()
    make_move(-1)
    if check_win(-1):
        print("Sorry, the computer wins!")
        break
