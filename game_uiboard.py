import pygame
import sys
import numpy as np

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE
LINE_WIDTH = 5
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
PLAYER_X_COLOR = (255, 0, 0)
PLAYER_O_COLOR = (0, 0, 255)
WINNING_LINE_COLOR = (0, 255, 0)

# Initialize the game board
board = np.full((GRID_SIZE, GRID_SIZE, GRID_SIZE), ' ')

# Initialize Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Tic Tac Toe")

def draw_board():
    screen.fill(WHITE)

    for z in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if board[z, y, x] == 'X':
                    pygame.draw.line(screen, PLAYER_X_COLOR, (x * CELL_SIZE, y * CELL_SIZE), ((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE), LINE_WIDTH)
                    pygame.draw.line(screen, PLAYER_X_COLOR, ((x + 1) * CELL_SIZE, y * CELL_SIZE), (x * CELL_SIZE, (y + 1) * CELL_SIZE), LINE_WIDTH)
                elif board[z, y, x] == 'O':
                    pygame.draw.circle(screen, PLAYER_O_COLOR, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - LINE_WIDTH // 2, LINE_WIDTH)

    for i in range(GRID_SIZE + 1):
        pos = i * CELL_SIZE
        pygame.draw.line(screen, LINE_COLOR, (0, pos), (WIDTH, pos), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (pos, 0), (pos, HEIGHT), LINE_WIDTH)

def check_win(player):
    for z in range(GRID_SIZE):
        # Check rows
        for y in range(GRID_SIZE):
            if np.all(board[z, y, :] == player) or np.all(board[z, :, y] == player) or np.all(board[:, y, z] == player):
                return True

        # Check diagonals
        if np.all(np.diag(board[z, :, :]) == player) or np.all(np.diag(np.fliplr(board[z, :, :])) == player):
            return True

    # Check vertical and depth diagonals
    if np.all(np.diag(board[:, :, :]) == player) or np.all(np.diag(np.fliplr(board[:, :, :])) == player):
        return True

    return False

def main():
    current_player = 'X'
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y, z = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE, 0
                while z < GRID_SIZE and board[z, y, x] != ' ':
                    z += 1

                if z < GRID_SIZE:
                    board[z, y, x] = current_player

                    if check_win(current_player):
                        game_over = True
                    elif np.all(board != ' '):
                        game_over = True
                    else:
                        current_player = 'O' if current_player == 'X' else 'X'

        draw_board()
        pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
