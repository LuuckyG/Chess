import pygame

from setup import setup_screen
from board.setup_board import initialize_board
from board.setup_board import draw_board


def play():
    pygame.init()

    setup_game()

    screen, position = setup_screen()


    # Game variables
    is_down = False
    is_clicked = False
    is_transition = False
    is_right_clicked = []

    font = pygame.font.SysFont("comicsans", 30, True)

    while position.get_play():
        pygame.time.Clock().tick(60)  # 60 fps

        # Update board position
        player = position.get_player()
        board = position.get_board()


        # Update display and show last move
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    play()
