class Empty:
    """Class for empty squares"""

    LETTERS = 'abcdefgh'
    
    def __init__(self, x, y):       
        self.x = x
        self.y = y
        self.attacked_by = {'direct': [], 'indirect': []}
        self.coordinate = self.LETTERS[self.x] + str(self.y + 1)
        

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
        self.is_pinned = False
        self.has_moved = False

        self.attacks = {'direct': [], 'indirect': []}
        self.attacked_by = {'direct': [], 'indirect': []}

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
    

    # def is_pinned(self):
    #     """King is pinned by enemy, meaning current piece cannot move"""
    #     return False
    

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

        attack_type = 'direct' if direct_attack else 'indirect'
        tile = board.get_tile_at_pos(x, y)
        
        if tile is not None:
            if not isinstance(tile.state, Empty):
                if tile.state.color != self.color and not self.is_blocked:
                    tile.state.attacked_by[attack_type].append(self)
                    self.attacks[attack_type].append(tile.state)
                    
                    if direct_attack:
                        self.valid_moves.append((tile.x, tile.y))
                        
                else:
                    self.is_blocked = True
                    
                return False
            else:
                tile.state.attacked_by[attack_type].append(self)
                
                if direct_attack:
                    self.valid_moves.append((tile.x, tile.y))
        
        return direct_attack
    

    def horizontal_moves(self, board, max_range):
        """Check all horizontal squares the piece can move to, and
        possibly capture another piece."""

        for dx in self.direction:
            x_possible = self.x
            direct_attack = True
            self.is_blocked = False

            for _ in range(max_range): 
                
                x_possible += dx

                if 0 <= x_possible <= 7:
                    direct_attack = self.check_square(board, x_possible, self.y, direct_attack)
                else:
                    break
                
                if self.is_blocked:
                    break


    def vertical_moves(self, board, max_range):
        """Check all vertical squares the piece can move to, and
        possibly capture another piece."""
        
        for dy in self.direction:
            y_possible = self.y
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
            y_possible = self.y
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
            y_opposite = self.y
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


class Pawn(Piece):
    """Class for pawns"""

    def __init__(self, id, symbol, color, x, y, square_width, square_height):
        
        super().__init__(id, symbol, color, x, y, square_width, square_height)
        
        # En Passant Target
        self.EPT = -1
        self.walk_direction = 1 if self.color == 'w' else -1
        
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
    

    def moves(self, board, previous_move):
        self.is_blocked = False
        self.valid_moves = []
        self.direction = [self.walk_direction]
        max_range = 2 if not self.has_moved else 1
        
        self.vertical_moves(board=board, max_range=max_range)
        self.captures(board=board)
        self.en_passant(board=board, previous_move=previous_move)
        self.promotion()
        return self.valid_moves
    
    
    def captures(self, board):
        if self.x != 0:
            tile = board.get_tile_at_pos(self.x - 1, self.y + self.walk_direction)
            if not isinstance(tile.state, Empty) and tile.state.color == self.enemy_color:
                self.valid_moves.append((self.x - 1, self.y + self.walk_direction)) 
                     
        if self.x != 7:
            tile = board.get_tile_at_pos(self.x + 1, self.y + self.walk_direction)  
            if not isinstance(tile.state, Empty) and tile.state.color == self.enemy_color:
                self.valid_moves.append((self.x + 1, self.y + self.walk_direction)) 
    
    
    def en_passant(self, board, previous_move):
        v = 0 if self.color == 'w' else 1
        w = 2 * self.walk_direction
        
        ept_y = 4 - v
                
        if self.y == ept_y:
            if self.x != 0:
                tile = board.get_tile_at_pos(self.x - 1, self.y)
                if previous_move == [(self.x - 1, self.y + w), (self.x - 1, self.y)] \
                    and isinstance(tile.state, Pawn):
                        self.valid_moves.append((self.x - 1, self.y + self.walk_direction))
                        self.EPT = (self.x - 1, self.y + self.walk_direction)
            
            if self.x != 7:
                tile = board.get_tile_at_pos(self.x + 1, self.y)
                if previous_move == [(self.x + 1, self.y + w), (self.x + 1, self.y)] \
                    and isinstance(tile.state, Pawn):
                        self.valid_moves.append((self.x + 1, self.y + self.walk_direction))
                        self.EPT = (self.x + 1, self.y + self.walk_direction)
                       
    
    def promotion(self):
        pass

    
class Knight(Piece):
    """Class for knights"""
    
    def __init__(self, id, name, color, x, y, square_width, square_height):
        super().__init__(id, name, color, x, y, square_width, square_height)
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


    def moves(self, board, previous_move):
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
                        tile = board.get_tile_at_pos(x_possible, y_possible)
                        if isinstance(tile.state, Empty):
                            self.valid_moves.append((x_possible, y_possible))
                        else: 
                            if tile.state.color == self.enemy_color:
                                self.valid_moves.append((x_possible, y_possible))

        for dy in self.direction:
            # Possible squares that are +2/-2 in x, +1/-1 in y away from original square
            
            y_possible = self.y + dy
            if 0 <= y_possible <= 7:
                # Now check whether the knight can jump to any square d = |2x| away
                for dx in self.direction:
                    x_possible = self.x + 2 * dx
                    if 0 <= x_possible <= 7:
                        tile = board.get_tile_at_pos(x_possible, y_possible)
                        if isinstance(tile.state, Empty):
                            self.valid_moves.append((x_possible, y_possible))
                        else: 
                            if tile.state.color == self.enemy_color:
                                self.valid_moves.append((x_possible, y_possible))
        
        return self.valid_moves


class Bishop(Piece):
    """Class for bishops"""

    def __init__(self, id, name, color, x, y, square_width, square_height):
        super().__init__(id, name, color, x, y, square_width, square_height)
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
    

    def moves(self, board, previous_move):
        self.valid_moves = []
        self.diagonal_moves(board=board, max_range=7)
        return self.valid_moves


class Rook(Piece):
    """Class for rooks"""
    
    def __init__(self, id, name, color, x, y, square_width, square_height):
        super().__init__(id, name, color, x, y, square_width, square_height)
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


    def moves(self, board, previous_move):
        self.valid_moves = []
        self.horizontal_moves(board=board, max_range=7)
        self.vertical_moves(board=board, max_range=7)
        return self.valid_moves


class Queen(Piece):
    """Class for the queen"""
    
    def __init__(self, id, name, color, x, y, square_width, square_height):
        super().__init__(id, name, color, x, y, square_width, square_height)
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


    def moves(self, board, previous_move):
        self.valid_moves = []
        self.horizontal_moves(board=board, max_range=7)
        self.vertical_moves(board=board, max_range=7)
        self.diagonal_moves(board=board, max_range=7)
        return self.valid_moves
        

class King(Piece):
    """Class for the king"""
    
    def __init__(self, id, name, color, x, y, square_width, square_height):
        super().__init__(id, name, color, x, y, square_width, square_height)
        self.index = 0
        self.points = 9999
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


    def moves(self, board, previous_move):
        """For the king, one need to checks the 8 surrounding squares, 
        for being in check, and castling options."""
        
        self.valid_moves = []
        self.horizontal_moves(board=board, max_range=1)
        self.vertical_moves(board=board, max_range=1)
        self.diagonal_moves(board=board, max_range=1)
        self.castling_rights(board=board)
        return self.valid_moves


    def castling_rights(self, board):
        position = board.position
        
        # Kingside castle
        if self.castling[0] and not self.has_moved:
            if (isinstance(position[7 * self.player][5], Empty) and 
                isinstance(position[7 * self.player][6], Empty)):
                self.valid_moves.append((6, 7 * self.player))
                
        # Queenside castle
        if self.castling[1] and not self.has_moved:
            if (isinstance(position[7 * self.player][1], Empty) and 
                isinstance(position[7 * self.player][2], Empty) and 
                isinstance(position[7 * self.player][3], Empty)):
                self.valid_moves.append((2, 7 * self.player))


    # def is_pinned(self):
    #     if len(king.attacked_by['indirect']) >= 1:
    #         return True


    def in_check(self):
        return len(self.attacked_by['direct']) >= 1


    def is_checkmate(self):
        if self.in_check():
            for square in self.valid_moves:
                if not square.attacked_by['direct']:
                    return False
            return True
        return False


    def is_stalemate(self):
        if not self.in_check():
            for square in self.valid_moves:
                if not square.attacked_by['direct']:
                    return False
            return True
        return False
