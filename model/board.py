import random

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
        self.moves = []
        self.all_possible_moves = {'w': [], 'b': []}
        self.position = []
        self.previous_move = []
        self.captured_pieces = []
        self.highlighted_tiles = []
        self.arrow_coordinates = []
        self.pieces = {'w': set(), 'b': set()}
        self.king_position = {'w': (), 'b': ()}
        self.current_color = 'w'
        self.is_flipped = is_flipped
        
        self.winner = None
        self.stalemate = False
        self.checkmate = False
        
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
                        if color == 'w': piece.promotion_target = 7 if self.is_flipped else 0
                        if color == 'b': piece.promotion_target = 0 if self.is_flipped else 7
                    else:
                        raise ValueError('Undefined piece type.')
                    
                    tile = Tile(x, tile_y, 1, piece)
                    self.pieces[color].add(piece)
                    
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
            
    
    def update_board(self, color, moving_piece, x1, tile_y1, x2, tile_y2):
        self.current_color = color
        self.moving = moving_piece
        
        if isinstance(self.moving, King): self.king_position[self.current_color] = (x2, tile_y2)
        
        en_passant, promotion, castling = self.special_moves(x2, tile_y2)

        if en_passant: self.is_en_passant(x1, tile_y1, x2, tile_y2)
        elif promotion: self.is_promotion(x1, tile_y1, x2, tile_y2)
        elif castling: self.is_castle(x1, tile_y1, x2, tile_y2)
        else: self.make_move(x1, tile_y1, x2, tile_y2)


    def special_moves(self, tile_x, tile_y):
        """[summary]

        Args:
            tile_x ([type]): [description]
            tile_y ([type]): [description]

        Returns:
            [type]: [description]
        """
        
        if isinstance(self.moving, Pawn) and (tile_x, tile_y) == self.moving.EPT: en_passant = True
        else: en_passant = False
        
        if isinstance(self.moving, Pawn) and tile_y == self.moving.promotion_target: promotion = True
        else: promotion = False
        
        if isinstance(self.moving, King) and (tile_x, tile_y) in self.moving.castling_loc: castling = True
        else: castling = False
        
        return en_passant, promotion, castling
    
    
    def is_en_passant(self, x1, tile_y1, x2, tile_y2):
        self.make_move(x1, tile_y1, x2, tile_y2)
        
        # Capture other pawn
        tile_ept_y = tile_y2 - 1 if self.is_flipped and self.current_color == 'w' else tile_y2 + 1
        tile_ept_y = tile_y2 + 1 if not self.is_flipped and self.current_color == 'w' else tile_y2 - 1
        piece_ept_y = self.tile_coord_to_piece(tile_ept_y)
        en_passant_target = self.get_tile_at_pos(x2, tile_ept_y)
        if not isinstance(en_passant_target.state, Empty): self.remove_piece(en_passant_target.state)
        en_passant_target.state = Empty(x2, piece_ept_y)


    def is_promotion(self, x1, tile_y1, x2, tile_y2):
        self.make_move(x1, tile_y1, x2, tile_y2)
        
        # Create different tile state
        piece_y2 = self.tile_coord_to_piece(tile_y2)
        next_tile = self.get_tile_at_pos(x2, tile_y2)
        
        # Random promotion
        piece_type = random.choice([Queen, Rook, Bishop, Knight])
        promotion_piece = piece_type(self.id + 1, 'Q', self.moving.color, x2, piece_y2, self.square_width, self.square_height)
        promotion_piece.set_piece_value(promotion_piece.value_table)
        
        self.pieces[self.current_color].discard(self.moving)
        self.pieces[self.current_color].add(promotion_piece)
        next_tile.state = promotion_piece


    def is_castle(self, x1, tile_y1, x2, tile_y2):
        """First move the king following normal rules, then move the rook"""
        
        # Move the king
        self.make_move(x1, tile_y1, x2, tile_y2)
        piece_y2 = self.tile_coord_to_piece(tile_y2)
        
        # Queenside castle
        if x2 == 2: 
            rook_tile = self.get_tile_at_pos(0, tile_y2)
            new_tile = self.get_tile_at_pos(3, tile_y2)
        
        # Kingside castle
        else: 
            rook_tile = self.get_tile_at_pos(7, tile_y2)
            new_tile = self.get_tile_at_pos(5, tile_y2)
        
        # Move the rook
        rook = self.get_piece(rook_tile)
        rook.x = new_tile.x
        rook.y = piece_y2
        rook.set_piece_value(rook.value_table)
        
        new_tile.state = rook
        rook_tile.state = Empty(x2, piece_y2)


    def make_move(self, x1, tile_y1, x2, tile_y2):
        """Make the move and update board variables

        Args:
            x2 (int): [description]
            tile_y2 (int): [description]
        """
        piece_y1 = self.tile_coord_to_piece(tile_y1)
        piece_y2 = self.tile_coord_to_piece(tile_y2)
        
        self.moving.make_move(x2, piece_y2)
        self.moving.set_piece_value(self.moving.value_table)
        
        previous_tile = self.get_tile_at_pos(x1, tile_y1)
        previous_tile.state = Empty(x1, piece_y1)
        
        next_tile = self.get_tile_at_pos(x2, tile_y2)
        if not isinstance(next_tile.state, Empty): self.remove_piece(next_tile.state)
        next_tile.state = self.moving

        self.previous_move = [(x1, tile_y1), (x2, tile_y2)]
        
    
    def remove_piece(self, piece):
        color = 'w' if self.current_color == 'b' else 'w'
        self.pieces[color].discard(piece)

    
    def check_for_block_or_pin(self, king, piece):
        """Check if piece is pinned and can block or capture attacker

        Args:
            king ():
            piece ([type]): [description]

        Returns:
            Piece: the piece that pins the current piece
        """
       
        if len(king.attacked_by['indirect'].keys()) > 0:
            king_attacker_ids = king.attacked_by['indirect'].keys()
            if len(piece.attacked_by['direct'].keys()) > 0:
                for attacker_id in piece.attacked_by['direct'].keys():
                    if attacker_id in king_attacker_ids:
                        loc = piece.can_block_or_capture(piece.attacked_by['direct'][attacker_id])
                        if loc is not None:
                            piece.can_move = True
                            piece.valid_moves = [(loc[0], loc[1])]
                        else:
                            piece.can_move = False
                            piece.valid_moves = []
                        return
       
        piece.can_move = True
    
    
    def update_possible_moves(self):
        """Check possible moves after last move"""
        
        for rows in self.position:
            for tile in rows:
                tile.state.reset()
                
                if not isinstance(tile.state, Empty):
                    piece = self.get_piece(tile)
                    piece.moves(self)
        
        for color, (king_x, king_y) in self.king_position.items():
            king = self.get_piece(self.get_tile_at_pos(king_x, king_y))
            king.in_check = king.is_check()
        
            if king.in_check or king.attacked_by['indirect']:
                for piece in self.pieces[color]:
                    self.check_for_block_or_pin(king, piece)
                    self.all_possible_moves[piece.color].extend(piece.valid_moves)
            
            # Check for game winning states
            if not king.in_check and self.all_possible_moves[color]: 
                self.stalemate = True
                self.winner = 'Draw'
                
            if king.in_check and self.all_possible_moves[color]: 
                self.checkmate = True
                self.winner = 'b' if color == 'w' else 'w'
    
    
    def tile_coord_to_piece(self, y):
        return y if self.is_flipped else (7 - y)
