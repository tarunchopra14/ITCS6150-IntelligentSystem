"""
main.py

The 3D Tic Tac Toe game script. This script manages the game flow,
incorporating player moves, AI moves, checking for wins, and UI elements.
"""

import game_play
import game_logic
import game_ui
import game_ai

def main():
    # Initialize the board and set game difficulty through the UI
    board = game_ui.initialize_board()
    difficulty = game_ui.set_difficulty()

    # Decide who plays first (player or AI) (Defaulted to player start)
    current_player = game_ui.choose_first_player()

    # Main game loop
    while True:
        # Display the current board
        game_ui.print_board(board)

        if current_player == 1:  # Player's turn
            move = game_play.get_player_move(board)
            board = game_play.make_move(board, move, current_player)
            
            # Check if player wins
            if game_logic.check_win(current_player, board):
                game_ui.print_board(board)
                game_ui.display_winner_message(current_player)
                return

        else:  # AI's turn
            move = game_play.computer_move(board, difficulty)
            board = game_play.make_move(board, move, current_player)

            # Check if AI wins
            if game_logic.check_win(current_player, board):
                game_ui.print_board(board)
                game_ui.display_winner_message(current_player)
                return

        # Check if the board is full, if so break the loop and display tie message
        if game_logic.is_board_full(board):
            game_ui.display_tie_message()
            return

        # Switch the current player
        current_player *= -1

if __name__ == "__main__":
    main()
