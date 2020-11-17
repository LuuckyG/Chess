import random
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
        self.HMC = 0
        self.end_conditions = {'resignation': False,
                               'checkmate': False, 
                               'stalemate': False, 
                               'draw_agreed': False,
                               'HMC': False, 
                               '3_fold_rep': False}
        
        # Player variables
        self.player_list = []
        self.current_player = 0
        self.current_color = 'w'

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
                        
            for x in range(8):
                self.id += 1

                if self.START_POSITION[y][x] != 0:
                    
                    symbol = self.START_POSITION[y][x][0]
                    color = self.START_POSITION[y][x][1]
         
                    if symbol == 'K':
                        square = King(str(self.id), symbol, color, x, y, self.square_width, self.square_height)
                        self.king_position[color] = (x, y)
                    elif symbol == 'Q':
                        square = Queen(str(self.id), symbol, color, x, y, self.square_width, self.square_height)
                    elif symbol == 'B':
                        square = Bishop(str(self.id), symbol, color, x, y, self.square_width, self.square_height)
                    elif symbol == 'N':
                        square = Knight(str(self.id), symbol, color, x, y, self.square_width, self.square_height)
                    elif symbol == 'R':
                        square = Rook(str(self.id), symbol, color, x, y, self.square_width, self.square_height)
                    elif symbol == 'P':
                        square = Pawn(str(self.id), symbol, color, x, y, self.square_width, self.square_height)
                        
                    else:
                        raise ValueError('Undefined piece type.')
                    
                    self.pieces[color].add(square)
                    
                else:
                    square = Empty(str(self.id), x, y)
            
                board_row.append(square)
            self.position.append(board_row)
                
    def flipped_board(self, y):
        return y if self.is_flipped else 7 - y
            
    def show(self):
        for rows in self.position:
            row = []
            for square in rows:
                if not isinstance(square, Empty): row.append(square.symbol + square.color)
                else: row.append(0)
            print(row)

    def get_square(self, x, y):
        """"""
        if (0 <= x <= 7) and (0 <= y <= 7):
            y = self.flipped_board(y)
            return self.position[y][x]
            
    def move_piece(self, color, moving_piece, move):
        """Make move"""
        self.current_color = color
        self.moving = moving_piece
        
        (x2, y2) = move[1]
        
        if isinstance(self.moving, King): 
            self.king_position[self.current_color] = (x2, y2)
        
        self.special_moves(x2, y2)

        if self.en_passant: self.is_en_passant(move)
        elif self.promotion: self.is_promotion(move)
        elif self.castling: self.is_castle(move)
        else: self.make_move(move)

    def special_moves(self, x, y):
        """[summary]

        Args:
            x ([type]): [description]
            y ([type]): [description]
        """
        
        if isinstance(self.moving, Pawn) and (x, y) == self.moving.EPT: 
            self.en_passant = True
        else: self.en_passant = False
        
        if isinstance(self.moving, Pawn) and y == self.moving.promotion_target: 
            self.promotion = True
        else: self.promotion = False
        
        if isinstance(self.moving, King) and (x, y) in self.moving.castling_loc: 
            self.castling = True
        else: self.castling = False
        
    def is_en_passant(self, move):
        x2, y2 = move[1]
        self.make_move(move)
        
        # Capture other pawn
        ept_y = y2 - self.moving.walk_direction
        en_passant_target = self.position[ept_y][x2]
        
        if not isinstance(en_passant_target, Empty): self.remove_piece(en_passant_target)
        
        self.id += 1
        self.position[ept_y][x2] = Empty(str(self.id), x2, ept_y)

    def is_promotion(self, move):
        x2, y2 = move[1]
        self.make_move(move)
                
        # Random promotion
        self.id += 1
        piece_nr = random.choice([0, 1, 2, 3])
        piece_type = [Queen, Rook, Bishop, Knight][piece_nr]
        
        symbol = 'Q'
        
        if piece_nr == 0: symbol = 'Q'
        elif piece_nr == 1: symbol = 'R'        
        elif piece_nr == 2: symbol = 'B'
        elif piece_nr == 3: symbol = 'N'
            
        promotion_piece = piece_type(str(self.id), symbol, self.moving.color, x2, y2, self.square_width, self.square_height)
        promotion_piece.points = 1
        promotion_piece.set_piece_value(promotion_piece.value_table)
        
        self.pieces[self.current_color].discard(self.moving)
        self.pieces[self.current_color].add(promotion_piece)
        self.position[y2][x2] = promotion_piece

    def is_castle(self, move):
        """First move the king following normal rules, then move the rook"""
        _, (x2, y2) = move
        
        # Move the king
        self.make_move(move)
        
        # Queenside castle
        if x2 == 2: 
            rook = self.position[y2][0]
            new_square = self.position[y2][3]
        
        # Kingside castle
        else: 
            rook = self.position[y2][7]
            new_square = self.position[y2][5]
        
        # Move the rook
        x1 = rook.x
        rook.x = new_square.x
        rook.y = y2
        rook.set_piece_value(rook.value_table)
        
        self.position[new_square.y][new_square.x] = rook
        self.id += 1
        self.position[y2][x1] = Empty(str(self.id), x1, y2)

    def make_move(self, move):
        """Make the move and update board variables

        Args:
            x2 (int): [description]
            tile_y2 (int): [description]
        """
        self.capture = False
        (x1, y1), (x2, y2) = move
        self.moving.make_move(x2, y2)
        
        self.position[y1][x1] = Empty(str(self.id + 1), x1, y1)

        if not isinstance(self.position[y2][x2], Empty): 
            self.remove_piece(self.position[y2][x2])
            self.capture = True
            
        self.position[y2][x2]= self.moving
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
                moves = piece.can_block_or_capture(king.attacked_by['direct'][attacker_id])
            
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
                    moves = piece.can_block_or_capture(king.attacked_by['indirect'][attacker_id])
            
                    if moves: piece.can_move = True
                    else: piece.can_move = False
                
                    piece.valid_moves = moves
       
        else: piece.can_move = True
     
    def update_possible_moves(self):
        """Check possible moves after last move"""
        
        # Reset tiles
        self.all_possible_moves = {'w': [], 'b': []}
        
        for rows in self.position:
            for square in rows:
                square.reset()
                if isinstance(square, King): square.in_check = False
        
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
            king = self.position[king_y][king_x]
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
            if (not king.in_check 
                and not self.all_possible_moves[color] 
                and color == self.current_color):
                print('stalemate')
                self.end_conditions['stalemate'] = True
                self.winner = 'Draw'
                
            if king.in_check and not self.all_possible_moves[color]: 
                print('checkmate')
                self.end_conditions['checkmate'] = True
                self.winner = 'Black' if color == 'w' else 'White'
    
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
            promoted_piece = self.position[y2][x2]
            notation = piece.coordinate + '=' + promoted_piece.symbol
        
        elif self.en_passant:
            notation = 'abcdefgh'[x1] + str(y1)
            ept = self.position[piece.EPT[1]][piece.EPT[0]]
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
        king_x, king_y = self.king_position[enemy_color]
        enemy_king = self.position[king_y][king_x]
        
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

    # def position_to_key(self, position):
    #     """Create tuple of information about current position"""
    #     board = position.get_board()
    #     castle_rights = position.get_castle_rights()

    #     save_board = []
    #     for ranks in board:
    #         save_board.append(tuple(ranks))
    #     save_board = tuple(save_board)

    #     save_rights = []
    #     for right in castle_rights:
    #         save_rights.append(tuple(right))
    #     save_rights = tuple(save_rights)

    #     key = (save_board, position.get_player(), save_rights)
    #     return key

    def tile_coord_to_piece(self, y):
        """"""
        return y if self.is_flipped else (7 - y)
