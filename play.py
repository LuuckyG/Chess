import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, K_q

from controller.chess import Chess


def play():
    """The main game loop"""
    chess = Chess()
    view = chess.view

    while getattr(chess, 'play'):
        pygame.display.update()
        status = getattr(chess, 'status')

        for event in pygame.event.get():
            if event.type == QUIT or pygame.key.get_pressed()[K_q]:
                chess.play = False
                pygame.quit()
                break
            
            chess.start_game()

            # if status != 'game':
            #     if event.type == MOUSEMOTION:
            #         x, y = event.pos
            #         view.follow_mouse(x, y, status)

            # else:
            #     player = chess.current_player

            #     if getattr(player, 'player_type') == 'AI':
            #         chess.ai_move()

            #     else:
                    
            #         if event.button == 1:
            #             if event.type == MOUSEBUTTONDOWN:
            #                 pass
            #             elif event.type == MOUSEBUTTONUP:
            #                 pass

            #         if event.button == 3:
            #             if event.type == MOUSEBUTTONDOWN:
            #                 pass
            #             elif event.type == MOUSEBUTTONUP:
            #                 pass

            #         left_click, _, right_click = pygame.mouse.get_pressed()

            #         if left_click:

            #             if getattr(chess, 'left_click'):
            #                 pass

            #             else:
            #                 setattr(chess, 'is_clicked', True)
            #                 setattr(chess, 'left_click', True)

            #         elif right_click:
            #             setattr(chess, 'right_click', True)
                        
            #             x, y = event.pos
            #             chess.process_click(x, y)
                    
            #         if event.type == MOUSEBUTTONUP:
            #             x, y = event.pos
            #             chess.process_click(x, y)

            view.draw_screens('game')

if __name__ == "__main__": play()
