import copy

from model.tile import Tile
from model.pieces import Pawn, Knight, Bishop, Rook, Queen, King, Empty


class Board:
    """Class to store current position on the board and 
    to keep track of all the pieces on the board."""

    START_POSITION = [['Rw', 'Nw', 'Bw', 'Qw', 'Kw', 'Bw', 'Nw', 'Rw'],  # 1
                     ['Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw'],  # 2
                     [0, 0, 0, 0, 0, 0, 0, 0],  # 3
                     [0, 0, 0, 0, 0, 0, 0, 0],  # 4
                     [0, 0, 0, 0, 0, 0, 0, 0],  # 5
                     [0, 0, 0, 0, 0, 0, 0, 0],  # 6
                     ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'],  # 7
                     ['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb']]  # 8


    def __init__(self, square_width, square_height, is_flipped):
        self.square_width = square_width
        self.square_height = square_height
        
        self.id = 0
        self.position = []
        self.captured_pieces = []
        self.highlighted_tiles = []
        self.arrow_coordinates = []
        self.pieces = {'w': [], 'b': []}
        self.king_position = {'w': (), 'b': ()}
        self.is_flipped = is_flipped
        
        self.setup()
    

    def setup(self):
        """Create piece objects based on starting board position"""
        
        for y in range(8):
            board_row = []
            
            # Give white pieces low indices, but have
            # their tiles be at the bottom of the board
            tile_y = y if self.is_flipped else 7 - y
                        
            for x in range(8):
                if self.START_POSITION[y][x] != 0:
                    self.id += 1
                    symbol = self.START_POSITION[y][x][0]
                    color = self.START_POSITION[y][x][1]
         
                    if symbol == 'K':
                        piece = King(self.id, symbol, color, x, y, self.square_width, self.square_height)
                        self.king_position[color] = (x, tile_y)
                    elif symbol == 'Q':
                        piece = Queen(self.id, symbol, color, x, y, self.square_width, self.square_height)
                    elif symbol == 'B':
                        piece = Bishop(self.id, symbol, color, x, y, self.square_width, self.square_height)
                    elif symbol == 'N':
                        piece = Knight(self.id, symbol, color, x, y, self.square_width, self.square_height)
                    elif symbol == 'R':
                        piece = Rook(self.id, symbol, color, x, y, self.square_width, self.square_height)
                    elif symbol == 'P':
                        piece = Pawn(self.id, symbol, color, x, y, self.square_width, self.square_height)
                    else:
                        raise ValueError('Undefined piece type.')
                    
                    tile = Tile(x, tile_y, 1, piece)
                    self.pieces[color].append(piece)
                    
                else:
                    state = Empty(x, y)
                    tile = Tile(x, tile_y, 1, state)
            
                board_row.append(tile)
            self.position.append(board_row)
            
    
    def get_tile_at_pos(self, x, y):
        """"Get the tile at the mouse click location.
        
        Args:
        - x: x-coordinate of mouse at click
        - y: y-coordinate of mouse at click
        """       
        for rows in self.position:
            for tile in rows:
                if tile.rect.collidepoint(x, y):
                    return tile
        return None


    def get_piece(self, tile):
        """Get piece at selected tile"""
        if tile is not None:
            if not isinstance(tile.state, Empty):
                return tile.state
            
    
    def check_for_pin(self, color, moving_piece):
        king_x, king_y = self.king_position[color]
        king_tile = self.get_tile_at_pos(king_x, king_y)
        king = self.get_piece(king_tile)
        
        if len(king.attacked_by['indirect']) > 0:
            king_attackers = king.attacked_by['indirect']
            if len(moving_piece.is_attacked_by['direct']) > 0:
                for attacker in moving_piece.is_attacked_by['direct']:
                    if attacker in king_attackers:
                        moving_piece.is_pinned = True
                        return
        else: moving_piece.is_pinned = False
            
