"""
This file contains the main game loop for our project. 
The game comprises a 3D board represented by 4 levels of 2D boards stacked on top of each other.
Users can choose a difficulty level and play against an AI opponent.
"""

import pygame
import numpy as np
import game_play
import game_logic
import game_ui 

def main():
    """
    The main function that initializes and runs the game loop.
    """
    
    # Initialize the 3D board.
    board = game_ui.initialize_board()

    # Decide the starting player. By default, the player starts first.
    current_player = 1 

    # Flags for managing UI states
    running = True
    show_play_button = True
    show_difficulty_screen = False
    winner = 0
    show_winner_screen = False
    difficulty = None

    # Main game loop
    while running:
        # Clear screen and redraw the background
        game_ui.screen.fill(game_ui.BACKGROUND)
        
        # Draw the game title
        game_ui.draw_title()

        # AI's move logic (moved outside of the event loop)
        if current_player == -1 and not show_play_button and not show_difficulty_screen and not show_winner_screen:
            move = game_play.computer_move(board, difficulty)
            if game_play.is_valid_move(board, move):
                level, row, col = move
                board = game_play.make_move(board, move, current_player)
                game_ui.draw_circle_in_cell(level, row, col, current_player)
                if game_logic.check_win(current_player, board):
                    # Handle AI win
                    winner = -1
                    show_winner_screen = True
                current_player *= -1

        for event in pygame.event.get():
            # Quit the game if the close button is clicked
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle reset button click
                if game_ui.reset_button["rect"].collidepoint(event.pos):
                    board = game_ui.initialize_board()
                    show_play_button = True
                    show_difficulty_screen = False
                    show_winner_screen = False
                    current_player = 1
                    continue  # Skip other checks if Reset was clicked

                # When winner screen is displayed, don't process other actions
                if show_winner_screen:
                    continue
                
                # Handle play button click
                if show_play_button:
                    if game_ui.play_button["rect"].collidepoint(event.pos):
                        show_play_button = False
                        show_difficulty_screen = True
                # Handle difficulty selection click
                elif show_difficulty_screen:
                    difficulty = game_ui.get_clicked_difficulty(event.pos)
                    if difficulty:
                        show_difficulty_screen = False
                else:
                    # Player's move logic
                    if current_player == 1:
                        cell = game_ui.get_clicked_cell(event.pos)
                        if cell:
                            level, row, col = cell
                            move = (level, row, col)
                            if game_play.is_valid_move(board, move):
                                board = game_play.make_move(board, move, current_player)
                                game_ui.draw_circle_in_cell(level, row, col, current_player)
                                if game_logic.check_win(current_player, board):
                                    # Handle player win
                                    winner = 1
                                    show_winner_screen = True
                                current_player *= -1

        # Drawing logic based on game's state
        if show_play_button:
            game_ui.draw_play_button()
        elif show_difficulty_screen:
            game_ui.draw_buttons()
        else:
            game_ui.draw_board(board)
            game_ui.draw_reset_button()
            game_ui.draw_title()
            if show_winner_screen:
                game_ui.draw_winner_screen(winner)

        pygame.display.flip()  # Update the display with the new drawings

    pygame.quit()  # Clean up and close the game

if __name__ == "__main__":
    # If this file is run directly, start the game
    main()
