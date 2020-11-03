import copy

from model.tile import Tile
from model.pieces import Pawn, Knight, Bishop, Rook, Queen, King, Empty


class Board:
    """Class to store current position on the board and 
    to keep track of all the pieces on the board."""

    START_POSITION = [['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb'],  # 8
                     ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'],  # 7
                     [0, 0, 0, 0, 0, 0, 0, 0],  # 6
                     [0, 0, 0, 0, 0, 0, 0, 0],  # 5
                     [0, 0, 0, 0, 0, 0, 0, 0],  # 4
                     [0, 0, 0, 0, 0, 0, 0, 0],  # 3
                     ['Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw'],  # 2
                     ['Rw', 'Nw', 'Bw', 'Qw', 'Kw', 'Bw', 'Nw', 'Rw']]  # 1

    def __init__(self, square_width, square_height):
        self.square_width = square_width
        self.square_height = square_height
        self.captured_pieces = []
        self.setup()
    

    def setup(self):
        """Create piece objects based on starting board position"""
        self.board = []

        for y in range(8):
            board_row = []
            for x in range(8):
                if self.START_POSITION[y][x] != 0:

                    symbol = self.START_POSITION[y][x][0]
                    color = self.START_POSITION[y][x][1]

                    if symbol == 'K':
                        piece = King(symbol, color, x, y, self.square_width, self.square_height)
                    elif symbol == 'Q':
                        piece = Queen(symbol, color, x, y, self.square_width, self.square_height)
                    elif symbol == 'B':
                        piece = Bishop(symbol, color, x, y, self.square_width, self.square_height)
                    elif symbol == 'N':
                        piece = Knight(symbol, color, x, y, self.square_width, self.square_height)
                    elif symbol == 'R':
                        piece = Rook(symbol, color, x, y, self.square_width, self.square_height)
                    elif symbol == 'P':
                        piece = Pawn(symbol, color, x, y, self.square_width, self.square_height)
                    
                    tile = Tile(x, y, self.square_width, piece)
                    
                else:
                    state = Empty(x, y)
                    tile = Tile(x, y, self.square_width, state)
            
                board_row.append(tile)
            self.board.append(board_row)
    
    def get_tile_at_pos(self, x, y):
        """"Get the tile at the mouse click location.
        
        Args:
        - x: x-coordinate of mouse at click
        - y: y-coordinate of mouse at click
        """
        for rows in self.board:
            for tile in rows:
                if tile.rect.collidepoint(x, y):
                    return tile
        return None


    def get_piece(self, x, y):
        """Get piece selected by mouse click"""
        tile = self.get_tile_at_pos(x, y)
        if tile is not None:
            if not isinstance(tile.state, Empty):
                return tile.state
        return None
