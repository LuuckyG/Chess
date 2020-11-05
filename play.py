import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, K_q, K_c

from controller.chess import Chess


def play():
    """The main game loop"""
    chess = Chess()
    view = chess.view
    chess.start_game()

    while getattr(chess, 'play'):
        pygame.display.update()
        status = getattr(chess, 'status')

        for event in pygame.event.get():
            if event.type == QUIT or pygame.key.get_pressed()[K_q]:
                chess.play = False
                pygame.quit()
                break

            # if status != 'game':
            #     if event.type == MOUSEMOTION:
            #         x, y = event.pos
            #         view.follow_mouse(x, y, status)
            #     
            #     view.draw_screens(status)

            # else:
            #     player = chess.current_player

            #     if getattr(player, 'player_type') == 'AI':
            #         chess.ai_move()

            #     else:
            
            # if event.type == MOUSEMOTION and chess.is_dragged is not None:
            #     chess.view.draw_dragged_piece()
            
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                
                # Left click
                if event.button == 1:
                    chess.process_click(x, y, is_up=False)

                # Right click
                if event.button == 3:
                    x, y = pygame.mouse.get_pos()
                    chess.process_right_click(x, y, is_up=False)

            if event.type == MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()

                # Left click
                if event.button == 1:
                    chess.process_click(x, y, is_up=True)

                # Right click
                if event.button == 3:                   
                    chess.process_right_click(x, y, is_up=True)

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
            
            # if chess.is_clicked is not None:
            #     print(chess.is_clicked.moves(chess.board))


if __name__ == "__main__": play()
