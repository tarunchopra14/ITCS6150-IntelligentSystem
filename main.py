import pygame
import numpy as np
import game_play
import game_logic
import game_ui 

def main():
    # Initialize the 3D board
    board = game_ui.initialize_board()

    # Decide the starting player. By default, the player starts first.
    current_player = 1  # Player starts first by default

    running = True
    show_play_button = True
    show_difficulty_screen = False
    difficulty = None

    while running:
        game_ui.screen.fill(game_ui.BACKGROUND)
        game_ui.draw_title()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_play_button:
                    if game_ui.play_button["rect"].collidepoint(event.pos):
                        show_play_button = False
                        show_difficulty_screen = True
                elif show_difficulty_screen:
                    difficulty = game_ui.get_clicked_difficulty(event.pos)
                    if difficulty:
                        show_difficulty_screen = False
                else:
                    if game_ui.reset_button["rect"].collidepoint(event.pos):  # Check if reset button was clicked
                        board = game_ui.initialize_board()
                        show_play_button = True
                        show_difficulty_screen = False
                        current_player = 1
                        continue  # Skip other checks if Reset was clicked

                    cell = game_ui.get_clicked_cell(event.pos)
                    if cell:
                        level, row, col = cell
                        move = (level, row, col)

                    # Player's turn
                    if current_player == 1 and not show_play_button and not show_difficulty_screen:
                        cell = game_ui.get_clicked_cell(event.pos)
                        if cell:
                            level, row, col = cell
                            move = (level, row, col)
                            if game_play.is_valid_move(board, move):
                                board = game_play.make_move(board, move, current_player)
                                game_ui.draw_circle_in_cell(level, row, col, current_player)  # Draw the move on the board
                                if game_logic.check_win(current_player, board):
                                    # game_ui.display_winner_message(current_player)
                                    return
                                current_player *= -1

                    # AI's turn
                    if current_player == -1 and not show_play_button and not show_difficulty_screen:
                        attempts = 0
                        while attempts < 100:  # Limit the attempts to 100 (or any other upper limit)
                            move = game_play.computer_move(board, difficulty)
                            if game_play.is_valid_move(board, move):
                                level, row, col = move
                                board = game_play.make_move(board, move, current_player)
                                game_ui.draw_circle_in_cell(level, row, col, current_player) # Draw the move on the board
                                if game_logic.check_win(current_player, board):
                                    # game_ui.display_winner_message(current_player)
                                    return
                                current_player *= -1
                                break
                            attempts += 1

        # if game_ui.is_board_full(board):
        #     game_ui.display_tie_message()
        #     return

        if show_play_button:
            game_ui.draw_play_button()
        elif show_difficulty_screen:
            game_ui.draw_buttons()
        else:
            game_ui.draw_board(board)
            game_ui.draw_reset_button()
            game_ui.draw_title()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
