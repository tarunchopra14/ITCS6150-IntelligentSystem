"""
main.py

3D Tic Tac Toe. This script manages the game flow,
incorporating player moves, AI moves, checking for wins, and UI elements.
"""

import game_play
import game_logic
import game_ui

def main():
    # Initialize the 3D board
    board = game_ui.initialize_board()

    # Prompt the user to set the game difficulty
    difficulty = game_ui.set_difficulty()

    # Decide the starting player. By default, the player starts first.
    current_player = game_ui.choose_first_player()

    # Main game loop
    while True:
        # Present the current state of the board
        game_ui.print_board(board)

        if current_player == 1:  # Player's turn 
            # Get the player's chosen move
            move = game_play.get_player_move(board)
            
            # Update the board based on the player's move
            board = game_play.make_move(board, move, current_player)
            
            # Check if the player's move led to a win
            if game_logic.check_win(current_player, board):
                game_ui.print_board(board)
                game_ui.display_winner_message(current_player)
                return

        else:  # AI's turn
            # Determine the computer's move based on the chosen difficulty level
            move = game_play.computer_move(board, difficulty)

            # Update the board based on the AI's move
            board = game_play.make_move(board, move, current_player)

            # Check if the AI's move led to a win
            if game_logic.check_win(current_player, board):
                game_ui.print_board(board)
                game_ui.display_winner_message(current_player)
                return

        # If all the cells on the board are filled and no one has won, then it's a tie
        if game_logic.is_board_full(board):
            game_ui.display_tie_message()
            return

        # Switch the current player for the next turn
        # Note: Assuming 1 is for player and -1 for AI, multiplying by -1 toggles between them.
        current_player *= -1

# Ensure the script is being run as the main module
if __name__ == "__main__":
    main()
