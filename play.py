import pygame
from pygame.locals import *

from controller.chess import Chess


class Game:
    """game Main entry point. handles intialization of game and graphics, 
    as well as game loop"""    

    def __init__(self):
        """Initialize PyGame window."""
        
        self.chess = Chess()
        self.view = self.chess.view
        

    def play(self):
        """Game() main loop.

            1. player input
            2. move stuff
            3. draw stuff
        """
        self.chess.start_game()
        self.board = self.chess.board
        
        while self.chess.play:
            
            # get input            
            self.handle_events()

            # move stuff            
            self.update()

            # draw stuff
            self.draw()

            # cap FPS if: limit_fps == True
            if self.view.limit_fps: self.view.clock.tick(self.view.fps_max)
            else: self.view.clock.tick()


    def draw(self):
        """draw screen"""
        
        # draw code
        if self.chess.status != 'game': self.view.draw_screens(self.chess.status)
        else: self.view.draw_position(self.board, self.chess.is_dragged)
        
        # update / flip screen.
        pygame.display.flip()


    def update(self):
        """move guys."""
        
        # if self.chess.player_list[self.chess.current_player] == 'AI': self.chess.ai_move()
        
        self.chess.update()
        pass


    def handle_events(self):
        """handle events: keyboard, mouse, etc."""
        events = pygame.event.get()

        for event in events:
            # event: quit
            if event.type == pygame.QUIT: self.chess.play = False
            
            # event: keydown
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE: self.chess.play = False
                if event.key == K_q: self.chess.play = False
            
            # event: mousedown
            elif event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if event.button == 1: self.chess.process_click(x, y, is_up=False)
                if event.button == 3: self.chess.process_right_click(x, y, is_up=False)
            
            # event: mouseup
            elif event.type == MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if event.button == 1: self.chess.process_click(x, y, is_up=True)
                if event.button == 3: self.chess.process_right_click(x, y, is_up=True)


if __name__ == "__main__": 
    chess = Game()
    chess.play()    
