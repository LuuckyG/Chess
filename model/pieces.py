class Empty:
    """Class for empty squares"""

    LETTERS = 'abcdefgh'
    
    def __init__(self, x, y):       
        self.x = x
        self.y = y
        self.attacked_by = {'direct': dict(), 'indirect': dict()}
        self.coordinate = self.LETTERS[self.x] + str(self.y + 1)
    
    def reset(self):
        self.attacked_by = {'direct': dict(), 'indirect': dict()}
        

class Piece:
    """Base class for all pieces"""

    LETTERS = 'abcdefgh'

    def __init__(self, id, symbol, color, x, y, square_width, square_height):
        
        self.id = id
        self.symbol = symbol
        self.color = color
        self.enemy_color = 'b' if self.color == 'w' else 'w'
        self.player = 0 if self.color == 'w' else 1
        
        self.x = x
        self.y = y
        self.upper_y = 0 if self.color == 'w' else square_height

        self.is_blocked = False
        self.can_move = True
        self.has_moved = False

        self.valid_moves = set()
        self.attack_line = []
        self.attacks = {'direct': dict(), 'indirect': dict()}
        self.attacked_by = {'direct': dict(), 'indirect': dict()}
        self.defended_by = set()

        self.direction = [-1, 1]
        self.set_coordinate()


    def set_coordinate(self):
        self.coordinate = self.LETTERS[self.x] + str(self.y + 1)


    def set_subsection(self, index, square_width, square_height):
        self.left_x = index * square_width
        self.subsection = (self.left_x, self.upper_y, square_width, square_height)
        self.pos = (-1, -1)


    def set_piece_value(self, value_table):
        self.value = value_table[self.y][self.x]
       

    def check_square(self, board, x, y, direct_attack):
        """[summary]

        Args:
            board ([type]): [description]
            x ([type]): [description]
            y ([type]): [description]
            direct_attack ([type]): [description]

        Returns:
            [type]: [description]
        """
        self.attack_line.extend((x, y))
        attack_type = 'direct' if direct_attack else 'indirect'
        tile = board.get_tile_at_pos(x, y)
        
        if tile is not None:
            if not isinstance(tile.state, Empty):
                piece = board.get_piece(tile)
                if piece.color != self.color and not self.is_blocked:
                    piece.attacked_by[attack_type][str(self.id)] = self.attack_line
                    self.attacks[attack_type][str(self.id)] = self.attack_line
                    
                    if direct_attack and not isinstance(piece, King):
                        self.valid_moves.add((tile.x, tile.y))
                        
                else:
                    piece.defended_by.add(self.id)
                    self.is_blocked = True
                    
                return False
            else:
                tile.state.attacked_by[attack_type][str(self.id)] = self.attack_line
                
                # Can't capture king
                if direct_attack and not isinstance(tile.state, King):
                    self.valid_moves.add((tile.x, tile.y))
        
        return direct_attack
    

    def horizontal_moves(self, board, max_range):
        """Check all horizontal squares the piece can move to, and
        possibly capture another piece."""

        for dx in self.direction:
            x_possible = self.x
            y_possible = self.y if board.is_flipped else (7 - self.y)
            self.attack_line = [(x_possible, y_possible)]
            
            direct_attack = True
            self.is_blocked = False

            for _ in range(max_range): 
                
                x_possible += dx

                if 0 <= x_possible <= 7:
                    
                    direct_attack = self.check_square(board, x_possible, y_possible, direct_attack)
                else:
                    break
                
                if self.is_blocked:
                    break


    def vertical_moves(self, board, max_range):
        """Check all vertical squares the piece can move to, and
        possibly capture another piece."""
        
        for dy in self.direction:
            y_possible = self.y if board.is_flipped else (7 - self.y)
            self.attack_line = [(self.x, y_possible)]
            
            direct_attack = True
            self.is_blocked = False

            for _ in range(max_range):
                
                y_possible += dy

                if 0 <= y_possible <= 7:
                    direct_attack = self.check_square(board, self.x, y_possible, direct_attack)
                else:
                    break
                
                if self.is_blocked:
                    break


    def diagonal_moves(self, board, max_range):
        """Check all diagonal squares the piece can move to, and
        possibly capture another piece."""

        for d in self.direction:
            x_possible = self.x
            y_possible = self.y if board.is_flipped else (7 - self.y)

            self.attack_line = [(x_possible, y_possible)]

            direct_attack = True
            self.is_blocked = False

            for _ in range(max_range):
                x_possible += d
                y_possible += d

                # Check first diagonal
                if 0 <= x_possible <= 7 and 0 <= y_possible <= 7:
                    direct_attack = self.check_square(board, x_possible, y_possible, direct_attack)
                else:
                    break
                    
                if self.is_blocked:
                    break

            # Reset search square
            x_possible = self.x
            y_opposite = self.y if board.is_flipped else (7 - self.y)
            self.attack_line = [(x_possible, y_opposite)]
            
            direct_attack = True
            self.is_blocked = False

            # Check second diagonal
            for _ in range(max_range):
                x_possible += d
                y_opposite -= d

                if 0 <= x_possible <= 7 and 0 <= y_opposite <= 7:
                    direct_attack = self.check_square(board, x_possible, y_opposite, direct_attack)
                else:
                    break
            
                if self.is_blocked:
                    break


    def add_attack(self, x, y, tile):
        self.attack_line.extend((x, y))
        self.valid_moves.add((x, y))
        tile.state.attacked_by['direct'][str(self.id)] = self.attack_line
        self.attacks['direct'][str(self.id)] = self.attack_line


    def make_move(self, x, y):
        self.x = x
        self.y = y
        self.has_moved = True
        self.set_piece_value(self.value_table)
        self.set_coordinate()
    
    
    def can_block_or_capture(self, attack_line):
        for (x, y) in self.valid_moves:
            if (x, y) in attack_line:
                return (x, y)
        return None

    
    def reset(self):
        self.attacks = {'direct': dict(), 'indirect': dict()}
        self.attacked_by = {'direct': dict(), 'indirect': dict()}
        self.defended_by = set()
        

class Pawn(Piece):
    """Class for pawns"""

    def __init__(self, id, symbol, color, x, y, square_width, square_height):
        
        super().__init__(id, symbol, color, x, y, square_width, square_height)
        
        # En Passant Target
        self.EPT = -1
        self.index = 5
        self.points = 1
        self.set_value_table()
        self.set_subsection(self.index, square_width, square_height)
        self.set_piece_value(self.value_table)
    

    def set_value_table(self):
        self.value_table = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [50, 50, 50, 50, 50, 50, 50, 50],
                            [10, 10, 20, 30, 30, 20, 10, 10],
                            [5, 5, 10, 25, 25, 10, 5, 5],
                            [0, 0, 0, 20, 20, 0, 0, 0],
                            [5, -5, -10, 0, 0, -10, -5, 5],
                            [5, 10, 10, -20, -20, 10, 10, 5],
                            [0, 0, 0, 0, 0, 0, 0, 0]]
    

    def moves(self, board):
        self.is_blocked = False
        self.valid_moves = set()
        self.walk_direction = 1
        
        if not board.is_flipped and self.color == 'w': self.walk_direction = -1
        if board.is_flipped and self.color == 'b': self.walk_direction = -1

        self.direction = [self.walk_direction]
        max_range = 2 if not self.has_moved else 1
        
        tile_y = board.tile_coord_to_piece(self.y)
        self.attack_line = [(self.x, tile_y)]
        
        self.vertical_moves(board, max_range)
        self.captures(board)
        self.en_passant(board)
        self.promotion(board)
        return self.valid_moves

    
    def captures(self, board):
        tile_y = board.tile_coord_to_piece(self.y)
        
        if self.x != 0:
            self.attack_line = [(self.x, tile_y)]
            tile = board.get_tile_at_pos(self.x - 1, tile_y + self.walk_direction)
            if not isinstance(tile.state, Empty) and tile.state.color == self.enemy_color and \
                not isinstance(tile.state, King):
                self.add_attack(self.x - 1, tile_y + self.walk_direction, tile)

                     
        if self.x != 7:
            self.attack_line = [(self.x, tile_y)]
            tile = board.get_tile_at_pos(self.x + 1, tile_y + self.walk_direction)  
            if not isinstance(tile.state, Empty) and tile.state.color == self.enemy_color and \
                not isinstance(tile.state, King):
                self.add_attack(self.x + 1, tile_y + self.walk_direction, tile)
    
    
    def en_passant(self, board):
        """En Passant"""
        v = 0 if self.color == 'w' else 1
        w = 2 * self.walk_direction
        
        ept_y = 4 - v
                
        if self.y == ept_y:
            tile_y = board.tile_coord_to_piece(self.y)
            if self.x != 0:
                self.attack_line = [(self.x, tile_y)]
                tile = board.get_tile_at_pos(self.x - 1, tile_y)
                if board.previous_move == [(self.x - 1, tile_y + w), (self.x - 1, tile_y)] \
                    and isinstance(tile.state, Pawn):
                        self.add_attack(self.x - 1, tile_y + self.walk_direction, tile)
                        self.EPT = (self.x - 1, tile_y + self.walk_direction)
                        
            
            if self.x != 7:
                self.attack_line = [(self.x, tile_y)]
                tile = board.get_tile_at_pos(self.x + 1, tile_y)
                if board.previous_move == [(self.x + 1, tile_y + w), (self.x + 1, tile_y)] \
                    and isinstance(tile.state, Pawn):
                        self.add_attack((self.x + 1, tile_y + self.walk_direction))
                        self.EPT = (self.x + 1, tile_y + self.walk_direction)
                       
    
    def promotion(self, board):
        pass

    
class Knight(Piece):
    """Class for knights"""
    
    def __init__(self, id, symbol, color, x, y, square_width, square_height):
        super().__init__(id, symbol, color, x, y, square_width, square_height)
        self.index = 3
        self.points = 3
        self.set_value_table()
        self.set_subsection(self.index, square_width, square_height)
        self.set_piece_value(self.value_table)


    def set_value_table(self):
        self.value_table = [[-50, -40, -30, -30, -30, -30, -40, -50],
                            [-40, -20, 0, 0, 0, 0, -20, -40],
                            [-30, 0, 10, 15, 15, 10, 0, -30],
                            [-30, 5, 15, 20, 20, 15, 5, -30],
                            [-30, 0, 15, 20, 20, 15, 0, -30],
                            [-30, 5, 10, 15, 15, 10, 5, -30],
                            [-40, -20, 0, 5, 5, 0, -20, -40],
                            [-50, -90, -30, -30, -30, -30, -90, -50]]


    def moves(self, board):
        """A knight can either move +2/-2 in x direction and +1/-1 in y direction, or the other way around"""

        self.valid_moves = set()
        
        tile_orig_y = board.tile_coord_to_piece(self.y)
        self.attack_line = [(self.x, tile_orig_y)]
        
        for dx in self.direction:
            # Possible squares that are +1/-1 in x, +2/-2 in y away from original square
            x_possible = self.x + dx
            if 0 <= x_possible <= 7:
                # Now check whether the knight can jump to any square d = |2y| away
                for dy in self.direction:
                    y_possible = self.y + 2 * dy
                    if 0 <= y_possible <= 7:
                        tile_y = y_possible if board.is_flipped else 7 - y_possible
                        tile = board.get_tile_at_pos(x_possible, tile_y)
                        
                        if isinstance(tile.state, Empty):
                            self.add_attack(x_possible, tile_y, tile)
                            
                        else: 
                            if tile.state.color == self.enemy_color and not isinstance(tile.state, King):
                                self.add_attack(x_possible, tile_y, tile)

        self.attack_line = [(self.x, tile_orig_y)]
        for dy in self.direction:
            # Possible squares that are +2/-2 in x, +1/-1 in y away from original square
            y_possible = self.y + dy
           
            if 0 <= y_possible <= 7:
                # Now check whether the knight can jump to any square d = |2x| away
                for dx in self.direction:
                    x_possible = self.x + 2 * dx
                    if 0 <= x_possible <= 7:
                        tile_y = y_possible if board.is_flipped else 7 - y_possible
                        tile = board.get_tile_at_pos(x_possible, tile_y)
                        
                        if isinstance(tile.state, Empty):
                            self.add_attack(x_possible, tile_y, tile)
                        
                        else: 
                            if tile.state.color == self.enemy_color and not isinstance(tile.state, King):
                                self.add_attack(x_possible, tile_y, tile)
        
        return self.valid_moves


class Bishop(Piece):
    """Class for bishops"""

    def __init__(self, id, symbol, color, x, y, square_width, square_height):
        super().__init__(id, symbol, color, x, y, square_width, square_height)
        self.index = 2
        self.points = 3
        self.set_value_table()
        self.set_subsection(self.index, square_width, square_height)
        self.set_piece_value(self.value_table)


    def set_value_table(self):
        self.value_table = [[-20, -10, -10, -10, -10, -10, -10, -20],
                            [-10, 0, 0, 0, 0, 0, 0, -10],
                            [-10, 0, 5, 10, 10, 5, 0, -10],
                            [-10, 5, 5, 10, 10, 5, 5, -10],
                            [-10, 0, 10, 10, 10, 10, 0, -10],
                            [-10, 10, 10, 10, 10, 10, 10, -10],
                            [-10, 5, 0, 0, 0, 0, 5, -10],
                            [-20, -10, -90, -10, -10, -90, -10, -20]]
    

    def moves(self, board):
        tile_y = board.tile_coord_to_piece(self.y)
        self.attack_line = [(self.x, tile_y)]
        self.valid_moves = set()
        self.diagonal_moves(board=board, max_range=7)
        return self.valid_moves


class Rook(Piece):
    """Class for rooks"""
    
    def __init__(self, id, symbol, color, x, y, square_width, square_height):
        super().__init__(id, symbol, color, x, y, square_width, square_height)
        self.index = 4
        self.points = 5
        self.set_value_table()
        self.set_subsection(self.index, square_width, square_height)
        self.set_piece_value(self.value_table)


    def set_value_table(self):
        self.value_table = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [5, 10, 10, 10, 10, 10, 10, 5],
                            [-5, 0, 0, 0, 0, 0, 0, -5],
                            [-5, 0, 0, 0, 0, 0, 0, -5],
                            [-5, 0, 0, 0, 0, 0, 0, -5],
                            [-5, 0, 0, 0, 0, 0, 0, -5],
                            [-5, 0, 0, 0, 0, 0, 0, -5],
                            [0, 0, 0, 5, 5, 0, 0, 0]]


    def moves(self, board):
        self.valid_moves = set()
        
        tile_y = board.tile_coord_to_piece(self.y)
        self.attack_line = [(self.x, tile_y)]
        
        self.horizontal_moves(board=board, max_range=7)
        self.vertical_moves(board=board, max_range=7)
        return self.valid_moves


class Queen(Piece):
    """Class for the queen"""
    
    def __init__(self, id, symbol, color, x, y, square_width, square_height):
        super().__init__(id, symbol, color, x, y, square_width, square_height)
        self.index = 1
        self.points = 9
        self.set_value_table()
        self.set_subsection(self.index, square_width, square_height)
        self.set_piece_value(self.value_table)


    def set_value_table(self):
        self.value_table = [[-20, -10, -10, -5, -5, -10, -10, -20],
                            [-10, 0, 0, 0, 0, 0, 0, -10],
                            [-10, 0, 5, 5, 5, 5, 0, -10],
                            [-5, 0, 5, 5, 5, 5, 0, -5],
                            [0, 0, 5, 5, 5, 5, 0, -5],
                            [-10, 5, 5, 5, 5, 5, 0, -10],
                            [-10, 0, 5, 0, 0, 0, 0, -10],
                            [-20, -10, -10, 70, -5, -10, -10, -20]]


    def moves(self, board):
        
        self.valid_moves = set()
        
        tile_y = board.tile_coord_to_piece(self.y)
        self.attack_line = [(self.x, tile_y)]
        
        self.horizontal_moves(board=board, max_range=7)
        self.vertical_moves(board=board, max_range=7)
        self.diagonal_moves(board=board, max_range=7)
        return self.valid_moves
        

class King(Piece):
    """Class for the king"""
    
    def __init__(self, id, symbol, color, x, y, square_width, square_height):
        super().__init__(id, symbol, color, x, y, square_width, square_height)
        self.index = 0
        self.points = 9999
        self.in_check = False
        self.castling = [True, True]
        self.set_value_table()
        self.set_subsection(self.index, square_width, square_height)
        self.set_piece_value(self.value_table)


    def set_value_table(self):
        self.value_table = [[-30, -40, -40, -50, -50, -40, -40, -30],
                            [-30, -40, -40, -50, -50, -40, -40, -30],
                            [-30, -40, -40, -50, -50, -40, -40, -30],
                            [-30, -40, -40, -50, -50, -40, -40, -30],
                            [-20, -30, -30, -40, -40, -30, -30, -20],
                            [-10, -20, -20, -20, -20, -20, -20, -10],
                            [20, 20, 0, 0, 0, 0, 20, 20],
                            [20, 30, 10, 0, 0, 10, 30, 20]]
    

    def is_endgame(self):
        self.value_table = [[-50, -40, -30, -20, -20, -30, -40, -50],
                            [-30, -20, -10, 0, 0, -10, -20, -30],
                            [-30, -10, 20, 30, 30, 20, -10, -30],
                            [-30, -10, 30, 40, 40, 30, -10, -30],
                            [-30, -10, 30, 40, 40, 30, -10, -30],
                            [-30, -10, 20, 30, 30, 20, -10, -30],
                            [-30, -30, 0, 0, 0, 0, -30, -30],
                            [-50, -30, -30, -30, -30, -30, -30, -50]]


    def moves(self, board):
        """For the king, one need to checks the 8 surrounding squares, 
        for being in check, and castling options."""
        
        self.valid_moves = set()
        coordinates = [set(), 
                       set()]
        
        tile_y = board.tile_coord_to_piece(self.y)
        self.attack_line = [(self.x, tile_y)]
        
        coordinates[0].add(self.x)
        coordinates[1].add(tile_y)
        
        if self.x > 0: coordinates[0].add(self.x - 1)
        if self.x < 7: coordinates[0].add(self.x + 1)
        if tile_y > 0: coordinates[1].add(tile_y - 1)
        if tile_y < 7: coordinates[1].add(tile_y + 1)

        for x in coordinates[0]:
            for y in coordinates[1]:
                if (x, y) == (self.x, tile_y): continue

                tile = board.get_tile_at_pos(x, y)
                
                if tile is not None:
                    if not isinstance(tile.state, Empty):
                        piece = board.get_piece(tile)
                        if piece.color != self.color:
                            self.attack_line.extend((x, y))
                            piece.attacked_by['direct'][str(self.id)] = self.attack_line
                            self.attacks['direct'][str(piece.id)] = self.attack_line
                            
                            if len(piece.defended_by) == 0: self.valid_moves.add((tile.x, tile.y))
                        else: piece.defended_by.add(self.id)
                    else:
                        tile.state.attacked_by['direct'][str(self.id)] = self.attack_line
                        
                        if len(tile.state.attacked_by['direct'].keys()) == 0: 
                            self.valid_moves.add((tile.x, tile.y))
                        else:
                            for attacker in tile.state.attacked_by['direct']:
                                if attacker.color != self.color: break
                                self.valid_moves.add((tile.x, tile.y))
                            
        self.in_check = self.is_check()
        if not self.in_check: self.castling_rights(board=board)
        
        return self.valid_moves


    def castling_rights(self, board):
        self.castling_loc = []
        
        if self.has_moved: 
            self.castling = [False, False]
            return
        
        if board.is_flipped: y = 0 if self.color == 'w' else 7
        else: y = 7 if self.color == 'w' else 0
            
        
        # Kingside castle
        rook_tile = board.get_tile_at_pos(7, y)
        rook = board.get_piece(rook_tile)
            
        if self.castling[0] and rook and not rook.has_moved:
            tile_5 = board.get_tile_at_pos(5, y)
            tile_6 = board.get_tile_at_pos(6, y)

            if isinstance(tile_5.state, Empty) and isinstance(tile_6.state, Empty):
                attackers_5 = tile_5.state.attacked_by['direct']
                attackers_6 = tile_6.state.attacked_by['direct']
                
                direct_attack = False

                for attacker_id in attackers_5.keys():
                    if not direct_attack:
                        for piece in self.pieces[self.enemy_color]:
                            if piece.id == attacker_id:
                                direct_attack = True
                                break
                
                if not direct_attack:
                    for attacker_id in attackers_6.keys():
                        if not direct_attack:
                            for piece in self.pieces[self.enemy_color]:
                                if piece.id == attacker_id:
                                    direct_attack = True
                                    break
                
                if not direct_attack:
                    self.valid_moves.add((6, y))
                    self.castling_loc.append((6, y))
                
                
        # Queenside castle
        rook_tile = board.get_tile_at_pos(0, y)
        rook = board.get_piece(rook_tile)
            
        if self.castling[1] and rook and not rook.has_moved:
            tile_2 = board.get_tile_at_pos(2, y)
            tile_3 = board.get_tile_at_pos(3, y)
            
            if isinstance(board.get_tile_at_pos(1, y).state, Empty) and \
                isinstance(tile_2.state, Empty) and \
                isinstance(tile_3.state, Empty):
                
                attackers_2 = tile_2.state.attacked_by['direct']
                attackers_3 = tile_3.state.attacked_by['direct']
                
                direct_attack = True
                
                for attacker_id in attackers_2.keys():
                    if not direct_attack:
                        for piece in self.pieces[self.enemy_color]:
                            if piece.id == attacker_id:
                                direct_attack = True
                                break
                
                if not direct_attack:
                    for attacker_id in attackers_3.keys():
                        if not direct_attack:
                            for piece in self.pieces[self.enemy_color]:
                                if piece.id == attacker_id:
                                    direct_attack = True
                                    break
                
                if not direct_attack:
                    self.valid_moves.add((2, y))
                    self.castling_loc.append((2, y))


    def is_check(self):
        return len(self.attacked_by['direct']) >= 1
