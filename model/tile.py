import pygame

class Tile:
    """Class to create the seperate tiles of the chess board."""

    def __init__(self, x, y, size, state):
        """Initialization of the tile.
        
        Args:
        - x: the horizontal coordinate (in px) of the tile (top left)
        - y: the vertical coordinate (in px) of the tile (top left)
        - size: size of the tile (in px)
        - state: the state of the tile. This is either 'empty' (default), or a Piece
        """
        self.x = x
        self.y = y
        self.size = size
        self.state = state
        self.rect = pygame.Rect(x, y, size, size)
