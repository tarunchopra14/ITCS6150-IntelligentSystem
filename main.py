import random

# Define the 3D Tic Tac Toe board as a 4x4x4 array (64 slots)
board = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]
difficulty = input("Select difficulty (easy, difficult, insane): ")


# Function to print the current board
def print_board():
    for z in range(4):
        print(f"Layer {z + 1}:")
        for row in board[z]:
            print(" ".join(["X" if cell == 1 else "O" if cell == -1 else "." for cell in row]))
        print()

# Function to check if a player has won
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

# Function to make a move for the player
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
        if difficulty == "easy":
            max_depth = 2
        elif difficulty == "difficult":
            max_depth = 4
        elif difficulty == "insane":
            max_depth = 6
        best_value, best_move = alpha_beta(player, max_depth, alpha, beta)
        z, x, y = best_move
        board[z][x][y] = -1

# Function for the alpha-beta pruning algorithm
def alpha_beta(player, depth, alpha, beta):
    if depth == 0 or check_win(1) or check_win(-1):
        return evaluate(), None
    if player == -1:
        best_value = float('inf')
        best_move = None
        for z in range(4):
            for x in range(4):
                for y in range(4):
                    if board[z][x][y] == 0:
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
        for z in range(4):
            for x in range(4):
                for y in range(4):
                    if board[z][x][y] == 0:
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

# Evaluation function (customize based on your strategy)
def evaluate():
    # You can define your own evaluation strategy here
    return 0

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
        print("Computer wins!")
        break
