import random

from model.tile import Tile
from model.pieces import Pawn, Knight, Bishop, Rook, Queen, King, Empty


class Board:
    """Class to store current position on the board and 
    to keep track of all the pieces on the board."""

    # START_POSITION = [['Rw', 'Nw', 'Bw', 'Qw', 'Kw', 'Bw', 'Nw', 'Rw'],  # 1
    #                  ['Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw'],  # 2
    #                  [0, 0, 0, 0, 0, 0, 0, 0],  # 3
    #                  [0, 0, 0, 0, 0, 0, 0, 0],  # 4
    #                  [0, 0, 0, 0, 0, 0, 0, 0],  # 5
    #                  [0, 0, 0, 0, 0, 0, 0, 0],  # 6
    #                  ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'],  # 7
    #                  ['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb']]  # 8
    
    
    START_POSITION = [['Rw', 'Nw', 'Bw', 'Qw', 'Kw', 'Bw', 'Nw', 'Rw'],  # 1
                     ['Pw', 'Pw', 'Pw', 'Pw', 0, 'Pw', 'Pw', 'Pw'],  # 2
                     [0, 0, 0, 0, 'Pw', 0, 0, 0],  # 3
                     [0, 0, 0, 0, 0, 0, 0, 0],  # 4
                     [0, 0, 0, 0, 0, 0, 0, 0],  # 5
                     [0, 0, 0, 'Pb', 0, 'Pb', 0, 0],  # 6
                     ['Pb', 'Pb', 'Pb', 0, 'Pb', 0, 'Pb', 'Pb'],  # 7
                     ['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb']]  # 8


    def __init__(self, square_width, square_height, is_flipped):
        self.square_width = square_width
        self.square_height = square_height
        
        # Piece and tile variables
        self.id = 0
        self.captured_pieces = {'w': [], 'b': []}
        self.pieces = {'w': set(), 'b': set()}
        
        # Board position variables
        self.position = []
        self.highlighted_tiles = []
        self.arrow_coordinates = []
        self.is_flipped = is_flipped        
        self.king_position = {'w': (), 'b': ()}
        
        # Win conditions
        self.winner = None
        self.end_conditions = {'resignation': False,
                               'checkmate': False, 
                               'stalemate': False, 
                               'HMC': False, 
                               '3_fold_rep': False}
        self.HMC = 0

        # Player variables
        self.player_list = []
        self.current_player = 0
        self.current_color = 'wb'[self.current_player]

        # Move variables
        self.moves = []
        self.move_nr = 1
        self.move_history = []
        self.position_history = []
        self.previous_move = []
        self.all_possible_moves = {'w': [], 'b': []}
        
        self.setup()
    

    def setup(self):
        """Create piece objects based on starting board position"""
        
        for y in range(8):
            board_row = []
            
            # Give white pieces low indices, but have
            # their tiles be at the bottom of the board
            tile_y = y if self.is_flipped else 7 - y
                        
            for x in range(8):
                self.id += 1

                if self.START_POSITION[y][x] != 0:
                    
                    symbol = self.START_POSITION[y][x][0]
                    color = self.START_POSITION[y][x][1]
         
                    if symbol == 'K':
                        piece = King(str(self.id), symbol, color, x, y, self.square_width, self.square_height)
                        self.king_position[color] = (x, tile_y)
                    elif symbol == 'Q':
                        piece = Queen(str(self.id), symbol, color, x, y, self.square_width, self.square_height)
                    elif symbol == 'B':
                        piece = Bishop(str(self.id), symbol, color, x, y, self.square_width, self.square_height)
                    elif symbol == 'N':
                        piece = Knight(str(self.id), symbol, color, x, y, self.square_width, self.square_height)
                    elif symbol == 'R':
                        piece = Rook(str(self.id), symbol, color, x, y, self.square_width, self.square_height)
                    elif symbol == 'P':
                        piece = Pawn(str(self.id), symbol, color, x, y, self.square_width, self.square_height)
                        if color == 'w': piece.promotion_target = 7 if self.is_flipped else 0
                        if color == 'b': piece.promotion_target = 0 if self.is_flipped else 7
                    else:
                        raise ValueError('Undefined piece type.')
                    
                    tile = Tile(x, tile_y, 1, piece)
                    self.pieces[color].add(piece)
                    
                else:
                    state = Empty(str(self.id), x, y)
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
        if not isinstance(tile.state, Empty):
            return tile.state
            
    
    def move_piece(self, color, moving_piece, move):
        self.current_color = color
        self.moving = moving_piece
        
        (x2, tile_y2) = move[1]
        
        if isinstance(self.moving, King): 
            self.king_position[self.current_color] = (x2, tile_y2)
        
        self.special_moves(x2, tile_y2)

        if self.en_passant: self.is_en_passant(move)
        elif self.promotion: self.is_promotion(move)
        elif self.castling: self.is_castle(move)
        else: self.make_move(move)


    def special_moves(self, tile_x, tile_y):
        """[summary]

        Args:
            tile_x ([type]): [description]
            tile_y ([type]): [description]
        """
        
        if isinstance(self.moving, Pawn) and (tile_x, tile_y) == self.moving.EPT: self.en_passant = True
        else: self.en_passant = False
        
        if isinstance(self.moving, Pawn) and tile_y == self.moving.promotion_target: self.promotion = True
        else: self.promotion = False
        
        if isinstance(self.moving, King) and (tile_x, tile_y) in self.moving.castling_loc: self.castling = True
        else: self.castling = False
    
    
    def is_en_passant(self, move):
        x2, tile_y2 = move[1]
        self.make_move(move)
        
        # Capture other pawn
        tile_ept_y = tile_y2 - 1 if self.is_flipped and self.current_color == 'w' else tile_y2 + 1
        tile_ept_y = tile_y2 + 1 if not self.is_flipped and self.current_color == 'w' else tile_y2 - 1
        piece_ept_y = self.tile_coord_to_piece(tile_ept_y)
        en_passant_target = self.get_tile_at_pos(x2, tile_ept_y)
        
        if not isinstance(en_passant_target.state, Empty): self.remove_piece(en_passant_target.state)
        
        self.id += 1
        en_passant_target.state = Empty(str(self.id), x2, piece_ept_y)


    def is_promotion(self, move):
        x2, tile_y2 = move[1]
        self.make_move(move)
        
        # Create different tile state
        piece_y2 = self.tile_coord_to_piece(tile_y2)
        next_tile = self.get_tile_at_pos(x2, tile_y2)
        
        # Random promotion
        self.id += 1
        piece_nr = random.choice([0, 1, 2, 3])
        piece_type = [Queen, Rook, Bishop, Knight][piece_nr]
        
        if piece_nr == 0: symbol = 'Q'
        elif piece_nr == 1: symbol = 'R'        
        elif piece_nr == 2: symbol = 'B'
        elif piece_nr == 3: symbol = 'N'
            
        promotion_piece = piece_type(str(self.id), symbol, self.moving.color, x2, piece_y2, self.square_width, self.square_height)
        promotion_piece.set_piece_value(promotion_piece.value_table)
        
        self.pieces[self.current_color].discard(self.moving)
        self.pieces[self.current_color].add(promotion_piece)
        next_tile.state = promotion_piece


    def is_castle(self, move):
        """First move the king following normal rules, then move the rook"""
        (x2, tile_y2) = move[1]
        
        # Move the king
        self.make_move(move)
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
        self.id += 1
        rook_tile.state = Empty(str(self.id), x2, piece_y2)


    def make_move(self, move):
        """Make the move and update board variables

        Args:
            x2 (int): [description]
            tile_y2 (int): [description]
        """
        self.capture = False
        (x1, tile_y1), (x2, tile_y2) = move
        piece_y1 = self.tile_coord_to_piece(tile_y1)
        piece_y2 = self.tile_coord_to_piece(tile_y2)
        
        self.moving.make_move(x2, piece_y2)
        
        previous_tile = self.get_tile_at_pos(x1, tile_y1)
        previous_tile.state = Empty(str(self.id + 1), x1, piece_y1)
        
        next_tile = self.get_tile_at_pos(x2, tile_y2)
        if not isinstance(next_tile.state, Empty): 
            self.remove_piece(next_tile.state)
            self.capture = True
            
        next_tile.state = self.moving

        self.previous_move = move
        
    
    def remove_piece(self, piece):
        color = 'w' if self.current_color == 'b' else 'b'
        self.captured_pieces[color].append(piece)
        self.pieces[color].discard(piece)

    
    def check_for_block_or_pin(self, king, piece):
        """Check if piece is pinned and can block or capture attacker

        Args:
            king ():
            piece ([type]): [description]

        Returns:
            Piece: the piece that pins the current piece
        """

        # Double check
        if len(king.attacked_by['direct'].keys()) > 1:
            piece.can_move = False
            piece.valid_moves = []
        
        # Check: look for block or capture of attacking piece
        elif king.in_check:
            king_attacker_ids = king.attacked_by['direct'].keys()
            
            for attacker_id in king_attacker_ids:
                moves = piece.can_block_or_capture(self, king.attacked_by['direct'][attacker_id])
            
                if moves:
                    piece.can_move = True
                    piece.valid_moves = moves
                    return

            piece.can_move = False
            piece.valid_moves = []

        # Pin: check for capture of attacking piece
        elif king.attacked_by['indirect']:         
            king_attacker_ids = king.attacked_by['indirect'].keys()
            piece_attacker_ids = piece.attacked_by['direct'].keys()
            
            for attacker_id in piece_attacker_ids:
                if attacker_id in king_attacker_ids:
                    moves = piece.can_block_or_capture(self, king.attacked_by['indirect'][attacker_id])
            
                    if moves: piece.can_move = True
                    else: piece.can_move = False
                
                    piece.valid_moves = moves
       
        else: piece.can_move = True
    
    
    def update_possible_moves(self):
        """Check possible moves after last move"""
        
        # Reset tiles
        self.all_possible_moves = {'w': [], 'b': []}
        
        for rows in self.position:
            for tile in rows:
                tile.state.reset()
                if isinstance(tile.state, King): tile.state.in_check = False
        
        # Get attackers and defenders
        for color in self.pieces.keys():
            for piece in self.pieces[color]:
                piece.moves(self)
        
        # Get kings and look for check and update 
        # possible moves accordingly
        enemy_color = 'w' if self.current_color == 'b' else 'b'
        order = [enemy_color, self.current_color]
        
        for color in order:
            king_x, king_y = self.king_position[color]
            king = self.get_piece(self.get_tile_at_pos(king_x, king_y))
            king.moves(self)
            
            self.all_possible_moves[king.color].extend(king.valid_moves)
            
            if king.in_check or king.attacked_by['indirect']:
                for piece in self.pieces[color]:
                    if not isinstance(piece, King):
                        self.check_for_block_or_pin(king, piece)
                        self.all_possible_moves[piece.color].extend(piece.valid_moves)
                        
            else:
                for piece in self.pieces[color]: 
                    if not isinstance(piece, King): 
                        self.all_possible_moves[piece.color].extend(piece.valid_moves)
            
            # Check for game winning states
            if not king.in_check and not self.all_possible_moves[color] \
            and color == self.current_color:
                print('stalemate')
                self.end_conditions['stalemate'] = True
                self.winner = 'Draw'
                
            if king.in_check and not self.all_possible_moves[color]: 
                print('checkmate')
                self.end_conditions['checkmate'] = True
                self.winner = 'b' if color == 'w' else 'w'
    
    
    def next_turn(self, piece, move):
        """Update game state variables"""
        self.save_position(piece, move)
        self.current_player = 0 if self.current_player == 1 else 1
        self.current_color = 'wb'[self.current_player]
        
        # Only update move nr is white is back in turn
        if self.current_color == 'w': self.move_nr += 1
    
    
    def get_notation(self, piece, move):
        """"""
        notation = ''
        (x1, y1), (x2, y2) = move
        
        if piece.symbol != 'P': notation = piece.symbol
        
        if self.promotion: 
            promoted_piece = self.get_piece(self.get_tile_at_pos(x2, y2))
            notation = piece.coordinate + '=' + promoted_piece.symbol
        
        elif self.en_passant:
            y = self.tile_coord_to_piece(y1)
            notation = 'abcdefgh'[x1] + str(y)
            ept = self.get_piece(self.get_tile_at_pos(piece.EPT[0], piece.EPT[1]))
            notation += 'x'
            notation += ept.coordinate
        
        elif self.castling: 
            if x2 == 6: notation = 'O-O'
            if x2 == 2: notation = 'O-O-O'
            
        else:
            if self.capture: 
                if piece.symbol == 'P': notation += 'abcdefgh'[x1]
                notation += 'x'
            notation += piece.coordinate
            
        enemy_color = 'b' if self.current_color == 'w' else 'w'
        king_pos_x, king_pos_y = self.king_position[enemy_color]
        enemy_king = self.get_piece(self.get_tile_at_pos(king_pos_x, king_pos_y))
        
        if self.end_conditions['checkmate']: notation += '#' 
        elif enemy_king.in_check: notation += '+'
        
        return notation
    
    
    def save_position(self, piece, move):
        """"""
        notation = self.get_notation(piece, move)
        
        if self.current_color == 'w': 
            self.move_history.append(str(self.move_nr) + '. ' + notation + ' ')
            self.position_history.append([self.position])
        else:
            self.move_history[-1] += ' ' + notation
            self.position_history.extend([self.position])
        
    
    def tile_coord_to_piece(self, y):
        """"""
        return y if self.is_flipped else (7 - y)
