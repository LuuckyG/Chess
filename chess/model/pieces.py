

class Empty:
    """Class for empty squares"""

    LETTERS = 'abcdefgh'
    
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.attacked_by = {'direct': dict(), 'indirect': dict()}
        self.coordinate = self.LETTERS[self.x] + str(self.y + 1)
    
    def reset(self):
        """Reset state of square each turn"""
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

        self.can_move = True
        self.has_moved = False
        self.is_blocked = False
        
        self.valid_moves = []
        self.attacks = {'direct': dict(), 'indirect': dict()}
        self.attacked_by = {'direct': dict(), 'indirect': dict()}
        self.defended_by = set()

        self.direction = [-1, 1]
        self.set_coordinate()

    def set_coordinate(self):
        """Get board notation of the position of the piece"""
        self.coordinate = self.LETTERS[self.x] + str(self.y + 1)

    def set_subsection(self, index, square_width, square_height):
        """Set piece image"""
        self.left_x = index * square_width
        self.subsection = (self.left_x, self.upper_y, square_width, square_height)
        self.pos = (-1, -1)

    def set_piece_value(self, value_table):
        """Set value of piece based on position"""
        self.value = value_table[self.y][self.x]
       
    def check_square(self, board, x, y, attack_line, direct_attack):
        """Check if piece can move to inspected square.
        If it can move to this square, check if it attacks the square or defends
        a friendly piece on this square.
        Also record if the attack, if attack, is direct or indirect. This is important
        for checking for check.
        """

        attack_type = 'direct' if direct_attack else 'indirect'
        square = board.position[y][x]
        
        try: index = attack_line.index([(self.x, self.y), (square.x, square.y)]) + 1
        except ValueError: index = len(attack_line) + 1
        
        
        if not isinstance(square, Empty):
            if square.color != self.color and not self.is_blocked:
                square.attacked_by[attack_type][str(self.id)] = attack_line[:index]
                self.attacks[attack_type][str(square.id)] = attack_line[:index]
                
                # Can't capture king
                if direct_attack and not isinstance(square, King):
                    self.valid_moves.append([(self.x, self.y), (square.x, square.y)])
                    
            else:
                square.defended_by.add(self.id)
                self.is_blocked = True
                
            return False

        else:
            square.attacked_by[attack_type][str(self.id)] = attack_line[:index]
            self.attacks[attack_type][str(square.id)] = attack_line[:index]

            if direct_attack:
                self.valid_moves.append([(self.x, self.y), (square.x, square.y)])
        
        return direct_attack

    def horizontal_moves(self, board, max_range):
        """Check all horizontal squares the piece can move to, and
        possibly capture another piece."""

        for dx in self.direction:
            x_possible = self.x
            y_possible = self.y
            attack_line = [(x_possible, y_possible)]
            
            direct_attack = True
            self.is_blocked = False

            for _ in range(max_range): 
                
                x_possible += dx
                if 0 <= x_possible <= 7:
                    attack_line.extend([(x_possible, y_possible)])
                    direct_attack = self.check_square(board, 
                                                      x_possible, 
                                                      y_possible,
                                                      attack_line,
                                                      direct_attack)
                else: break
                
                if self.is_blocked: break

    def vertical_moves(self, board, max_range):
        """Check all vertical squares the piece can move to, and
        possibly capture another piece."""
        
        for dy in self.direction:
            x_possible = self.x
            y_possible = self.y
            attack_line = [(x_possible, y_possible)]
            
            direct_attack = True
            self.is_blocked = False

            for _ in range(max_range):
                
                y_possible += dy
                if 0 <= y_possible <= 7:
                    attack_line.extend([(self.x, y_possible)])
                    direct_attack = self.check_square(board, 
                                                      self.x, 
                                                      y_possible, 
                                                      attack_line,
                                                      direct_attack)
                else: break
                
                if self.is_blocked: break

    def diagonal_moves(self, board, max_range):
        """Check all diagonal squares the piece can move to, and
        possibly capture another piece."""

        for d in self.direction:
            x_possible = self.x
            y_possible = self.y
            attack_line = [(x_possible, y_possible)]

            direct_attack = True
            self.is_blocked = False

            for _ in range(max_range):
                x_possible += d
                y_possible += d

                # Check first diagonal
                if 0 <= x_possible <= 7 and 0 <= y_possible <= 7:
                    attack_line.extend([(x_possible, y_possible)])
                    direct_attack = self.check_square(board, 
                                                      x_possible, 
                                                      y_possible, 
                                                      attack_line,
                                                      direct_attack)
                else: break
                    
                if self.is_blocked: break

            # Reset search square
            x_possible = self.x
            y_opposite = self.y
            attack_line = [(x_possible, y_opposite)]
            
            direct_attack = True
            self.is_blocked = False

            # Check second diagonal
            for _ in range(max_range):
                x_possible += d
                y_opposite -= d

                if 0 <= x_possible <= 7 and 0 <= y_opposite <= 7:
                    attack_line.extend([(x_possible, y_opposite)])
                    direct_attack = self.check_square(board, 
                                                      x_possible, 
                                                      y_opposite,
                                                      attack_line, 
                                                      direct_attack)
                else: break
            
                if self.is_blocked: break

    def add_attack(self, square):
        """Save how piece attacks square"""
        square.attacked_by['direct'][str(self.id)] = [(self.x, self.y), (square.x, square.y)]
        self.attacks['direct'][str(self.id)] = [(self.x, self.y), (square.x, square.y)]
        
        # Can't capture king
        if not isinstance(square, King): self.valid_moves.append([(self.x, self.y), (square.x, square.y)])

    def make_move(self, x, y):
        """Update piece variables to new position on the board"""
        self.x = x
        self.y = y
        self.has_moved = True
        self.set_piece_value(self.value_table)
        self.set_coordinate()
    
    def can_block_or_capture(self, attack_line):
        """If check, or pinned, the piece may be able to capture or block attacker"""
        moves = []
        for x1, y1 in attack_line:
            if [(self.x, self.y), (x1, y1)] in self.valid_moves: 
                moves.append([(self.x, self.y), (x1, y1)])
        return moves
    
    def reset(self):
        """Reset piece variables each turn"""
        self.can_move = True
        self.is_blocked = False
        self.attacks = {'direct': dict(), 'indirect': dict()}
        self.attacked_by = {'direct': dict(), 'indirect': dict()}
        self.defended_by = set()
        

class Pawn(Piece):
    """Class for pawns"""

    def __init__(self, id, symbol, color, x, y, square_width, square_height):
        super().__init__(id, symbol, color, x, y, square_width, square_height)
        self.EPT = -1
        self.index = 5
        self.points = 1
        self.promotion_target = 7 if color == 'w' else 0
        self.set_value_table()
        self.set_subsection(self.index, square_width, square_height)
        self.set_piece_value(self.value_table) 

    def set_value_table(self):
        """Get value table of pawn"""
        self.value_table = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [50, 50, 50, 50, 50, 50, 50, 50],
                            [10, 10, 20, 30, 30, 20, 10, 10],
                            [5, 5, 10, 25, 25, 10, 5, 5],
                            [0, 0, 0, 20, 20, 0, 0, 0],
                            [5, -5, -10, 0, 0, -10, -5, 5],
                            [5, 10, 10, -20, -20, 10, 10, 5],
                            [0, 0, 0, 0, 0, 0, 0, 0]]

    def moves(self, board):
        """All pawn moves"""
        self.is_blocked = False
        self.valid_moves = []
        
        max_range = 2 if not self.has_moved else 1
        self.walk_direction = 1 if self.color == 'w' else -1
        self.direction = [self.walk_direction]
        
        self.vertical(board, max_range)
        self.captures(board)
        self.en_passant(board)
        return self.valid_moves
    
    def vertical(self, board, max_range):
        """Vertical moves of pawn"""
        self.is_blocked = False
        for i in range(1, max_range + 1):
            if self.is_blocked: break
            
            y = self.y + i * self.walk_direction
            if 0 <= y <= 7:
                square = board.position[y][self.x]
                if not isinstance(square, Empty): self.is_blocked = True
                else: self.valid_moves.append([(self.x, self.y), (square.x, square.y)])

    def captures(self, board):
        """Pawn captures"""
        if self.x != 0:
            square = board.position[self.y + self.walk_direction][self.x - 1]
            if not isinstance(square, Empty) and square.color == self.enemy_color:
                self.add_attack(square)
            else:
                square.attacked_by['direct'][str(self.id)] = [(self.x, self.y), (square.x, square.y)]
                self.attacks['direct'][str(self.id)] = [(self.x, self.y), (square.x, square.y)]
                     
        if self.x != 7:
            square = board.position[self.y + self.walk_direction][self.x + 1]
            if not isinstance(square, Empty) and square.color == self.enemy_color:
                self.add_attack(square)
            else:
                square.attacked_by['direct'][str(self.id)] = [(self.x, self.y), (square.x, square.y)]
                self.attacks['direct'][str(self.id)] = [(self.x, self.y), (square.x, square.y)]
    
    def en_passant(self, board):
        """En Passant"""
        w = 2 * self.walk_direction
        ept_y = 4 if self.color == 'w' else 3
                
        if self.y == ept_y:
            if self.x != 0:
                square = board.position[self.y][self.x - 1]
                if board.previous_move == [(self.x - 1, self.y + w), (self.x - 1, self.y)] \
                   and isinstance(square, Pawn):
                        self.valid_moves.append([(self.x, self.y), 
                                                 (square.x, square.y + self.walk_direction)])
                        self.EPT = (square.x, square.y + self.walk_direction)
                                    
            if self.x != 7:
                square = board.position[self.y][self.x + 1]
                if board.previous_move == [(self.x + 1, self.y + w), (self.x + 1, self.y)] \
                   and isinstance(square, Pawn):
                        self.valid_moves.append([(self.x, self.y), 
                                                 (square.x, square.y + self.walk_direction)])
                        self.EPT = (square.x, square.y + self.walk_direction)

    
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
        """Get value table of knight"""
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
        self.valid_moves = []       
        for dx in self.direction:
            # Possible squares that are +1/-1 in x, +2/-2 in y away from original square
            x_possible = self.x + dx
            if 0 <= x_possible <= 7:
                # Now check whether the knight can jump to any square d = |2y| away
                for dy in self.direction:
                    y_possible = self.y + 2 * dy
                    if 0 <= y_possible <= 7:
                        square = board.position[y_possible][x_possible]
                        if isinstance(square, Empty): self.add_attack(square)
                        else: 
                            if square.color == self.enemy_color: self.add_attack(square)
                            else: square.defended_by.add(self)

        for dy in self.direction:
            # Possible squares that are +2/-2 in x, +1/-1 in y away from original square
            y_possible = self.y + dy
            if 0 <= y_possible <= 7:
                # Now check whether the knight can jump to any square d = |2x| away
                for dx in self.direction:
                    x_possible = self.x + 2 * dx
                    if 0 <= x_possible <= 7:
                        square = board.position[y_possible][x_possible]
                        if isinstance(square, Empty): self.add_attack(square)
                        else: 
                            if square.color == self.enemy_color: self.add_attack(square)
                            else: square.defended_by.add(self)
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
        """Get value table of bishop"""
        self.value_table = [[-20, -10, -10, -10, -10, -10, -10, -20],
                            [-10, 0, 0, 0, 0, 0, 0, -10],
                            [-10, 0, 5, 10, 10, 5, 0, -10],
                            [-10, 5, 5, 10, 10, 5, 5, -10],
                            [-10, 0, 10, 10, 10, 10, 0, -10],
                            [-10, 10, 10, 10, 10, 10, 10, -10],
                            [-10, 5, 0, 0, 0, 0, 5, -10],
                            [-20, -10, -90, -10, -10, -90, -10, -20]]
    
    def moves(self, board):
        """All moves of bishop are diagonal"""
        self.valid_moves = []
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
        """Get value table of rook"""
        self.value_table = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [5, 10, 10, 10, 10, 10, 10, 5],
                            [-5, 0, 0, 0, 0, 0, 0, -5],
                            [-5, 0, 0, 0, 0, 0, 0, -5],
                            [-5, 0, 0, 0, 0, 0, 0, -5],
                            [-5, 0, 0, 0, 0, 0, 0, -5],
                            [-5, 0, 0, 0, 0, 0, 0, -5],
                            [0, 0, 0, 5, 5, 0, 0, 0]]

    def moves(self, board):
        """All moves of rook go either horizontal or vertical"""
        self.valid_moves = []
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
        """Get value table of queen"""
        self.value_table = [[-20, -10, -10, -5, -5, -10, -10, -20],
                            [-10, 0, 0, 0, 0, 0, 0, -10],
                            [-10, 0, 5, 5, 5, 5, 0, -10],
                            [-5, 0, 5, 5, 5, 5, 0, -5],
                            [0, 0, 5, 5, 5, 5, 0, -5],
                            [-10, 5, 5, 5, 5, 5, 0, -10],
                            [-10, 0, 5, 0, 0, 0, 0, -10],
                            [-20, -10, -10, 70, -5, -10, -10, -20]]

    def moves(self, board):
        """Get all queen moves"""
        self.valid_moves = []       
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
        """Get value table of king"""
        self.value_table = [[-30, -40, -40, -50, -50, -40, -40, -30],
                            [-30, -40, -40, -50, -50, -40, -40, -30],
                            [-30, -40, -40, -50, -50, -40, -40, -30],
                            [-30, -40, -40, -50, -50, -40, -40, -30],
                            [-20, -30, -30, -40, -40, -30, -30, -20],
                            [-10, -20, -20, -20, -20, -20, -20, -10],
                            [20, 20, 0, 0, 0, 0, 20, 20],
                            [20, 30, 10, 0, 0, 10, 30, 20]]
    
    def is_endgame(self):
        """Get value table of king in the endgame"""
        self.value_table = [[-50, -40, -30, -20, -20, -30, -40, -50],
                            [-30, -20, -10, 0, 0, -10, -20, -30],
                            [-30, -10, 20, 30, 30, 20, -10, -30],
                            [-30, -10, 30, 40, 40, 30, -10, -30],
                            [-30, -10, 30, 40, 40, 30, -10, -30],
                            [-30, -10, 20, 30, 30, 20, -10, -30],
                            [-30, -30, 0, 0, 0, 0, -30, -30],
                            [-50, -30, -30, -30, -30, -30, -30, -50]]

    def get_neighboring_squares(self):
        """Get squares next to king, as possible
        squares to move to, capture or attack."""
        
        tiles = []
        coordinates = [set(), set()]
        coordinates[0].add(self.x)
        coordinates[1].add(self.y)
        
        if self.x > 0: coordinates[0].add(self.x - 1)
        if self.x < 7: coordinates[0].add(self.x + 1)
        if self.y > 0: coordinates[1].add(self.y - 1)
        if self.y < 7: coordinates[1].add(self.y + 1)

        for x in coordinates[0]:
            for y in coordinates[1]:
                if (x, y) != (self.x, self.y): tiles.append((x, y))               
        return tiles
    
    def moves(self, board):
        """For the king, one need to checks the 8 surrounding squares, 
        for being in check, and castling options."""
        self.in_check = self.is_check(board.pieces[self.enemy_color])
        self.normal_moves(board, self.in_check)
        if not self.in_check or self.has_moved: self.castling_rights(board)
                     
    def normal_moves(self, board, check):
        """Get all moves of king.
        Check whether the squares are blocked, or that they are not 
        attacked. If filled by enemy piece, check if king can capture
        the piece, when it is not defended.
        """
        self.valid_moves = []
        squares = self.get_neighboring_squares()
        
        for (x, y) in squares:
            square = board.position[y][x]
            
            # Filled squares
            if not isinstance(square, Empty):
                
                # Enemy pieces
                if square.color != self.color:
                    square.attacked_by['direct'][self.id] = [(self.x, self.y), (square.x, square.y)]
                    self.attacks['direct'][square.id] = [(self.x, self.y), (square.x, square.y)]
                    
                    # Enemy piece is not defended and can be captured
                    if len(square.defended_by) == 0: self.valid_moves.append([(self.x, self.y), (square.x, square.y)])
                
                # Friendly piece  
                else: square.defended_by.add(self.id)
                
            # Empty squares
            else:
                possible = True
                
                # Square not attacked directly
                if not square.attacked_by['direct'].keys(): 
                    square.attacked_by['direct'][self.id] = [(self.x, self.y), (square.x, square.y)]
                    self.attacks['direct'][square.id] = [(self.x, self.y), (square.x, square.y)]
                    self.valid_moves.append([(self.x, self.y), (square.x, square.y)])
                    break
                
                # Square is attacked
                if square.attacked_by['direct'].keys():
                    for enemy_piece in board.pieces[self.enemy_color]:
                        if enemy_piece.id in square.attacked_by['direct'].keys(): possible = False
                        
                        # X-ray attack - same line of attack - (only when in check)
                        if check and square.attacked_by['indirect'].keys():
                            if enemy_piece.id in square.attacked_by['indirect'].keys() and \
                                enemy_piece.id in self.attacked_by['direct']: 
                                    direct_attack_line = set(self.attacked_by['direct'][enemy_piece.id])
                                    indirect_attack_line = set(square.attacked_by['indirect'][enemy_piece.id])
                                    if direct_attack_line.issubset(indirect_attack_line): possible = False
                    
                    if possible: 
                        square.attacked_by['direct'][self.id] = [(self.x, self.y), (square.x, square.y)]
                        self.attacks['direct'][square.id] = [(self.x, self.y), (square.x, square.y)]
                        self.valid_moves.append([(self.x, self.y), (square.x, square.y)])

    def castling_rights(self, board):
        """Check for castling options"""        
        self.castling_loc = []
        y = 0 if self.color == 'w' else 7
        
        if self.has_moved: 
            self.castling = [False, False]
            return

        # Kingside castle
        rook = board.position[y][7]
        if (self.castling[0] 
            and not isinstance(rook, Empty) 
            and not rook.has_moved):
            square_5 = board.position[y][5]
            square_6 = board.position[y][6]

            if (isinstance(square_5, Empty) 
                and isinstance(square_6, Empty)):
                attackers_5 = square_5.attacked_by['direct']
                attackers_6 = square_6.attacked_by['direct']
                direct_attack = False
                
                for piece in board.pieces[self.enemy_color]:
                    if piece.id in attackers_5.keys(): 
                        direct_attack = True
                
                if not direct_attack:
                    for piece in board.pieces[self.enemy_color]:
                        if piece.id in attackers_6.keys(): 
                            direct_attack = True
                
                if not direct_attack:
                    self.valid_moves.append([(self.x, y), (6, y)])
                    self.castling_loc.append((6, y))
                               
        # Queenside castle
        rook = board.position[y][0]
            
        if (self.castling[1] 
            and not isinstance(rook, Empty) 
            and not rook.has_moved):
            square_1 = board.position[y][1]
            square_2 = board.position[y][2]
            square_3 = board.position[y][3]
            
            if (isinstance(square_1, Empty) 
                and isinstance(square_2, Empty) 
                and isinstance(square_3, Empty)):
                
                attackers_2 = square_2.attacked_by['direct']
                attackers_3 = square_3.attacked_by['direct']
                direct_attack = False
                
                for piece in board.pieces[self.enemy_color]:
                    if piece.id in attackers_2.keys(): 
                        direct_attack = True
                
                if not direct_attack:
                    for piece in board.pieces[self.enemy_color]:
                        if piece.id in attackers_3.keys(): 
                            direct_attack = True
                
                if not direct_attack:
                    self.valid_moves.append([(self.x, y), (2, y)])
                    self.castling_loc.append((2, y))

    def is_check(self, enemy_pieces):
        """Check if king is in check"""        
        if self.attacked_by['direct']:
            for enemy_piece in enemy_pieces:
                if enemy_piece.id in self.attacked_by['direct'].keys(): 
                    return True
        return False
