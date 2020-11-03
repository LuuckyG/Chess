from setup.utils import opposite


class Empty:
    """Class for empty squares"""
    def __init__(self, x, y):       
        self.x = x
        self.y = y
        self.attacked_by = {'direct': [], 'indirect': []}
        

class Piece:
    """Base class for all pieces"""
    def __init__(self, symbol, color, x, y, square_width, square_height):

        self.symbol = symbol
        self.color = color
        self.enemy_color = opposite(self.color)
        
        self.x = x
        self.y = y

        self.is_pinned = False
        self.attacks = {'direct': [], 'indirect': []}
        self.attacked_by = {'direct': [], 'indirect': []}

        # Used to search in opposite directions around the pieces
        self.direction = [-1, 1]

        self.value_table = []

        # Determine row in image
        self.upper_y = 0 if self.color == 'w' else square_height
            
    def set_subsection(self, index, square_width, square_height):
        self.left_x = index * square_width
        self.subsection = (self.left_x, self.upper_y, square_width, square_height)
        self.pos = (-1, -1)

    def set_piece_value(self, value_table):
        self.value = value_table[self.y][self.x]
    
    # def is_pinned(self):
    #     """King is pinned by enemy, meaning current piece cannot move"""
    #     return False
    
    def check_square(self, position, x, y, direct_attack):

        attack_type = 'direct' if direct_attack else 'indirect'

        # Check if square is empty
        if not position.is_occupied(x, y):
            self.valid_moves.append((x, y))
            empty_square = position.get_piece((x, y), empty=True)
            empty_square.attacked_by[attack_type].append(self)
        else:
            # Check for possible capture
            if position.is_occupied_by_enemy(x, y, self.enemy_color):
                attacked_piece = position.get_piece((x, y))
                attacked_piece.attacked_by[attack_type].append(self)
                
                self.valid_moves.append((x, y))
                self.attacks[attack_type].append(attacked_piece)
                return False
        return True
    
    def horizontal_moves(self, position, max_range):
        """Check all horizontal squares the piece can move to, and
        possibly capture another piece."""

        for dx in self.direction:
            x_possible = self.x
            direct_attack = True

            for _ in range(max_range): 
                
                x_possible += dx

                if 0 <= x_possible <= 7:
                    direct_attack = self.check_square(position, x_possible, self.y, direct_attack)
                else:
                    break

    def vertical_moves(self, position, max_range):
        """Check all vertical squares the piece can move to, and
        possibly capture another piece."""
        
        for dy in self.direction:
            y_possible = self.y
            direct_attack = True

            for _ in range(max_range):
                
                y_possible += dy

                if 0 <= y_possible <= 7:
                    direct_attack = self.check_square(position, self.x, y_possible, direct_attack)
                else:
                    break

    def diagonal_moves(self, position, max_range):
        """Check all diagonal squares the piece can move to, and
        possibly capture another piece."""

        for d in self.direction:
            x_possible = self.x
            y_possible = self.y
            direct_attack = True

            for _ in range(max_range):
                x_possible += d
                y_possible += d

                # Check first diagonal
                if 0 <= x_possible <= 7 and 0 <= y_possible <= 7:
                    direct_attack = self.check_square(position, x_possible, y_possible, direct_attack)
                else:
                    break

            # Reset search square
            x_possible = self.x
            y_opposite = self.y
            direct_attack = True

            # Check second diagonal
            for _ in range(max_range):
                x_possible += d
                y_opposite -= d

                if 0 <= x_possible <= 7 and 0 <= y_opposite <= 7:
                    direct_attack = self.check_square(position, x_possible, y_opposite, direct_attack)
                else:
                    break


class Pawn(Piece):
    """Class for pawns"""

    def __init__(self, symbol, color, x, y, square_width, square_height):
        
        super().__init__(symbol, color, x, y, square_width, square_height)
        
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
    
    def moves(self, position):
        board = position.board
        previous_move = position.get_previous_move()
        
        self.valid_moves = []

        # Pawn Movement       
        if self.color == 'w':
            self.direction = [-1]
            max_range = 2 if self.y == 6 else 1
        else:
            self.direction = [1]
            max_range = 2 if self.y == 1 else 1
        
        self.vertical_moves(position=position, max_range=max_range)


        #### Pawn Captures ####
        # White pawns
        if self.x != 0 and position.is_occupied_by_enemy(self.x - 1, self.y - 1, self.enemy_color):
            self.valid_moves.append((self.x - 1, self.y - 1))
        if self.x != 7 and position.is_occupied_by_enemy(self.x + 1, self.y - 1, self.enemy_color):
            self.valid_moves.append((self.x + 1, self.y - 1))

        # Black pawns
        if self.x != 0 and position.is_occupied_by_enemy(self.x - 1, self.y + 1, self.enemy_color):
            self.valid_moves.append((self.x - 1, self.y + 1))
        if self.x != 7 and position.is_occupied_by_enemy(self.x + 1, self.y + 1, self.enemy_color):
            self.valid_moves.append((self.x + 1, self.y + 1))


        #### EN PASSANT ####
        # Check for en passant possibilities (white)
        if self.y == 3:
            if previous_move == [(self.x - 1, 1), (self.x - 1, self.y)]:
                if board[self.y][self.x - 1][0] == 'P':
                    self.valid_moves.append((self.x - 1, self.y - 1))
                    position.set_EPT((self.x - 1, self.y - 1))
            elif previous_move == [(self.x + 1, 1), (self.x + 1, self.y)]:
                if board[self.y][self.x + 1][0] == 'P':
                    self.valid_moves.append((self.x + 1, self.y - 1))
                    position.set_EPT((self.x + 1, self.y - 1))

        # Check for en passant possibilities (black)
        if self.y == 4:
            if previous_move == [(self.x - 1, 6), (self.x - 1, self.y)]:
                if board[self.y][self.x - 1][0] == 'P':
                    self.valid_moves.append((self.x - 1, self.y + 1))
                    position.set_EPT((self.x - 1, self.y + 1))
            elif previous_move == [(self.x + 1, 6), (self.x + 1, self.y)]:
                if board[self.y][self.x + 1][0] == 'P':
                    self.valid_moves.append((self.x + 1, self.y + 1))
                    position.set_EPT((self.x + 1, self.y + 1))

        #### PROMOTION ####
        # TO DO!
        # def is_promotion(position, y):
        #     return y == position.get_player() * 7

        # def en_passant_rights(position, x, y):
        #     """If en passant captured, update board by removing captured pawn."""
        #     player = position.get_player()
        #     board = position.get_board()
        #     en_passant_target = position.get_EPT()

        #     if (x, y) == en_passant_target and 'wb'[player] == 'w':
        #         board[y + 1][x] = 0
        #     elif (x, y) == en_passant_target and 'wb'[player] == 'b':
        #         board[y - 1][x] = 0
        #     position.set_board(board)
        #     return position

    
class Knight(Piece):
    """Class for knights"""
    
    def __init__(self, name, color, x, y, square_width, square_height):
        super().__init__(name, color, x, y, square_width, square_height)
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

    def moves(self, position):
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
                        if not position.is_occupied(x_possible, y_possible):
                            self.valid_moves.append((x_possible, y_possible))
                        else:
                            if position.is_occupied_by_enemy(x_possible, y_possible, self.enemy_color):
                                self.valid_moves.append((x_possible, y_possible))

        for dy in self.direction:
            # Possible squares that are +2/-2 in x, +1/-1 in y away from original square
            
            y_possible = self.y + dy
            if 0 <= y_possible <= 7:
                # Now check whether the knight can jump to any square d = |2x| away
                for dx in self.direction:
                    x_possible = self.x + 2 * dx
                    if 0 <= x_possible <= 7:
                        if not position.is_occupied(x_possible, y_possible):
                            self.valid_moves.append((x_possible, y_possible))
                        else:
                            if position.is_occupied_by_enemy(x_possible, y_possible, self.enemy_color):
                                self.valid_moves.append((x_possible, y_possible))


class Bishop(Piece):
    """Class for pawn bishops"""

    def __init__(self, name, color, x, y, square_width, square_height):
        super().__init__(name, color, x, y, square_width, square_height)
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
    
    def moves(self, position):
        self.valid_moves = []
        self.diagonal_moves(position=position, max_range=7)


class Rook(Piece):
    """Class for rooks"""
    
    def __init__(self, name, color, x, y, square_width, square_height):
        super().__init__(name, color, x, y, square_width, square_height)
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

    def moves(self, position):
        self.valid_moves = []
        self.horizontal_moves(position=position, max_range=7)
        self.vertical_moves(position=position, max_range=7)


class Queen(Piece):
    """Class for the queen"""
    
    def __init__(self, name, color, x, y, square_width, square_height):
        super().__init__(name, color, x, y, square_width, square_height)
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

    def moves(self, position):
        self.valid_moves = []
        self.horizontal_moves(position=position, max_range=7)
        self.vertical_moves(position=position, max_range=7)
        self.diagonal_moves(position=position, max_range=7)
        

class King(Piece):
    """Class for the king"""
    
    def __init__(self, name, color, x, y, square_width, square_height):
        super().__init__(name, color, x, y, square_width, square_height)
        self.index = 0
        self.points = 9999
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

    def moves(self, position):
        """For the king, one need to checks the 8 surrounding squares, for being in check, and castling options."""
        board = position.get_board()
        self.valid_moves = []
        self.horizontal_moves(position=position, max_range=1)
        self.vertical_moves(position=position, max_range=1)
        self.diagonal_moves(position=position, max_range=1)

        # Castling options
        castle_right = position.get_castle_rights()

        if self.color == 'w':
            # Kingside castle
            if castle_right[0][0]:
                if board[7][5] == 0 and board[7][6] == 0:
                    self.valid_moves.append((6, 7))
            # Queenside castle
            if castle_right[0][1]:
                if board[7][1] == 0 and board[7][2] == 0 and board[7][3] == 0:
                    self.valid_moves.append((2, 7))
        elif self.color == 'b':
            # Kingside castle
            if castle_right[1][0]:
                if board[0][5] == 0 and board[0][6] == 0:
                    self.valid_moves.append((6, 0))
            # Queenside castle
            if castle_right[1][1]:
                if board[0][1] == 0 and board[0][2] == 0 and board[0][3] == 0:
                    self.valid_moves.append((2, 0))

    # def castle_rights(position, x, y):
    #     player = position.get_player()
    #     board = position.get_board()
    #     castle_right = position.get_castle_rights()

    #     if (x, y) == (2, (1 - player) * 7):
    #         # Queenside
    #         board[(1 - player) * 7][3] = board[(1 - player) * 7][0]
    #         board[(1 - player) * 7][0] = 0
    #         castle_right[player][0] = castle_right[player][1] = False
    #     elif (x, y) == (6, (1 - player) * 7):
    #         # Kingside
    #         board[(1 - player) * 7][5] = board[(1 - player) * 7][7]
    #         board[(1 - player) * 7][7] = 0
    #         castle_right[player][0] = castle_right[player][1] = False

    #     position.set_castle_rights(castle_right)
    #     position.set_board(board)
    #     return position

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
