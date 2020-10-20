import pygame

from setup.chessgame import ChessGame


def play():
    pygame.init()

    chess_game = ChessGame()
    
    chess_game.draw_board()
    pygame.display.update()

    # Game variables
    is_down = False
    is_clicked = False
    is_transition = False
    is_right_clicked = []

    font = pygame.font.SysFont("comicsans", 30, True)

    # while position.get_play():
    #     pygame.time.Clock().tick(60)  # 60 fps

    #     # Update board position
    #     player = position.get_player()
    #     board = position.get_board()


    #     # Update display and show last move
    #     pygame.display.update()

    # pygame.quit()


if __name__ == '__main__':
    play()
