"""
User Interface for the 3D Tic Tac Toe game.

This module manages:
- Initialization of the game board.
- Displaying the board to the user.
- User prompts for game difficulty, choosing the starting player, and selecting moves.
- Displaying game results including winner or tie messages.

The game board is a 4x4x4 3D list where:
    0  -> Empty cell
    1  -> Cell occupied by X (User)
   -1  -> Cell occupied by O (Computer)
"""

def initialize_board():
    """
    Initialize a 4x4x4 3D Tic Tac Toe board.
    
    Returns:
        list: A 3D list filled with zeros, signifying an empty board.
    """
    return [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]


def set_difficulty():
    """
    Prompt the user to select the AI opponent's difficulty level.
    
    Returns:
        int: Depth of search for the AI. Higher values equate to increased difficulty.
    """
    print("Choose the difficulty level:")
    print("1. Easy")
    print("2. Difficult")
    print("3. Insane")

    while True:
        try:
            choice = int(input("Enter your choice (1/2/3): "))
            if choice in [1, 2, 3]:
                break
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
        except ValueError:
            print("Please enter a valid number.")

    difficulty_map = {1: 2, 2: 4, 3: 6}
    return difficulty_map[choice]


def choose_first_player():
    """
    Default the game so the human player always plays first.

    Returns:
        int: 1, indicating the user plays first.
    """
    print("You go first!")
    return 1


def print_board(board):
    """
    Display the current state of the 3D Tic Tac Toe board.
    
    Args:
        board (list): Current game board represented as a 3D list.
    
    Returns:
        None
    """
    for z in range(4):
        print(f"Layer {z + 1}:")
        for row in board[z]:
            print(" ".join(["X" if cell == 1 else "O" if cell == -1 else "." for cell in row]))
        print()


def display_winner_message(player):
    """
    Display a message indicating the winner of the game.
    
    Args:
        player (int): The player who won. 1 for the human player, -1 for the AI.
    
    Returns:
        None
    """
    if player == 1:
        print("\nCongratulations! You have won!")
    elif player == -1:
        print("\nToo bad! The computer wins this round!")
    else:
        print("\nError determining the winner.")


def display_tie_message():
    """
    Display a message indicating that the game has ended in a tie.
    
    Returns:
        None
    """
    print("\nIt's a tie! Well played!")
