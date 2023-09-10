import random

# Define the Tic Tac Toe board as a 4x4x4 array (64 slots)
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
# It takes the player argument, which represents whether it's the player's turn (1) or the computer's turn (-1).

# If it's the player's turn (player == 1), the code does the following:

# It prints a message indicating that it's the player's turn with "Your turn (X)".
# It enters a while loop, which will keep running until the player makes a valid move.
# Inside the loop, it tries to get the player's input for the layer (z), row (x), and column (y) of their move.
# It subtracts 1 from each input to convert it from a 1-based index to a 0-based index.
# It checks if the entered coordinates (z, x, y) are within the valid range (0-3) and if the selected slot on the board is empty (board[z][x][y] == 0).
# If the move is valid, it updates the board with the player's mark (1 for X) and breaks out of the loop.
# If the move is invalid (outside the board or in an already occupied slot), it prints "Invalid move. Try again." and continues to prompt the player for input.
# If it's the computer's turn (player == -1), the code does the following:

# It prints a message indicating that it's the computer's turn with "Computer's turn (O)".
# It initializes alpha and beta values for alpha-beta pruning.
# It determines the depth of the alpha-beta pruning procedure based on the selected difficulty level ("easy," "difficult," or "insane").
# It calls the alpha_beta function to find the best move for the computer using alpha-beta pruning. The best move is represented as (z, x, y) and is assigned to best_move.
# It extracts the z, x, and y coordinates from best_move and updates the board with the computer's mark (-1 for O).
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
    # This is the base case.
    #If the depth is 0 or one of the two players win, then the function returns the evaluation
    # of the board and None.
    if depth == 0 or check_win(1) or check_win(-1):
        return evaluate(), None
    
#    This is the case for the max player.
#    We first initialize the best_value as positive infinity.
#    Then we iterate through all the possible spots on the board. If the spot is empty, then we place the piece for the max player.
#    Then we call the alpha_beta function recursively for the min player. After that, we return the board to its original state.
#    If the value returned from the min player is smaller than the current best_value, then we update the best_value and best_move.
#    After updating the best_value, we update beta as the minimum of beta and best_value, and if beta is smaller than or equal to alpha, then we break the loop.
#    Finally, we return the best_value and best_move.
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
#    This is the case for the min player.
#    We first initialize the best_value as negative infinity.
#    Then we iterate through all the possible spots on the board. If the spot is empty, 
# then we place the piece for the min player.
#    Then we call the alpha_beta function recursively for the max player. 
# After that, we return the board to its original state.
#    If the value returned from the max player is larger than the current best_value, then we update the best_value and 
# best_move.
#   After updating the best_value, we update alpha as the maximum of alpha and best_value, 
# and if beta is smaller than or equal to alpha, then we break the loop.
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

# Evaluation function (we can customize based on our strategy. I just added random numbers)
def evaluate():
    if check_win(1):
        return 100
    elif check_win(-1):
        return -100
    else:
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
