import pygame
from pygame.locals import QUIT, MOUSEBUTTONUP, MOUSEMOTION, K_q

from controller.chess import Chess


def play():
    """The main game loop"""
    chess = Chess()
    view = chess.view

    while getattr(chess, 'play'):
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT or pygame.key.get_pressed()[K_q]:
                chess.play = False
                pygame.quit()
                break
            
            # Start and settings screens
            if getattr(chess, 'status') != 'game':
                if event.type == MOUSEMOTION:
                    x, y = event.pos
                    view.follow_mouse(x, y)
                
                elif event.type == MOUSEBUTTONUP:
                    x, y = event.pos
                    chess.process_click(x, y)

            # During the game
            if getattr(chess, 'status') == 'game':
                player = chess.current_player

                if getattr(player, 'player_type') == 'AI':
                    chess.ai_move()

                elif event.type == MOUSEBUTTONUP:
                    x, y = event.pos
                    chess.process_click(x, y)

            view.draw_screens(getattr(chess, 'status'))

if __name__ == "__main__": play()
