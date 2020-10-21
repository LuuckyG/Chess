from setup.utils import opposite

from rules.rules import is_occupied, is_occupied_by

class Piece:
    """Base class for all pieces"""
    def __init__(self, symbol, color, chess_coord, square_width, square_height):

        self.symbol = symbol
        self.color = color
        
        self.x = chess_coord[0]
        self.y = chess_coord[1]
        self.chess_coord = chess_coord

        # Used to search in opposite directions around the pieces
        self.direction = [-1, 1]

        self.value_table = []

        # Determine row in image
        self.upper_y = 0 if self.color == 'w' else square_height
            
    def set_subsection(self, index, square_width, square_height):
        self.left_x = index * square_width
        self.subsection = (self.left_x, self.upper_y, square_width, square_height)
        self.pos = (-1, -1)

    def set_pos(self, pos):
        self.pos = pos

    def get_pos(self):
        return self.pos

    def set_coord(self, coord):
        self.chess_coord = coord
    
    def get_value_table(self):
        return self.value_table

    def set_piece_value(self, value_table):
        self.value = value_table[self.y][self.x]

    def get_piece_value(self):
        return self.value
    
    def horizontal_moves(self, board, max_range, enemy_color):
        """Check all horizontal squares the piece can move to, and
        possibly capture another piece."""

        for dx in self.direction:
            x_possible = self.x
            
            for _ in range(max_range): 
                
                x_possible += dx

                if 0 <= x_possible <= 7:
                    # Check if square is empty
                    if not is_occupied(board, x_possible, self.y):
                        self.valid_moves.append((x_possible, self.y))
                    else:
                        # Check for possible capture
                        if is_occupied_by(board, x_possible, self.y, enemy_color):
                            self.valid_moves.append((x_possible, self.y))

                else:
                    break

    def vertical_moves(self, board, max_range, enemy_color):
        """Check all vertical squares the piece can move to, and
        possibly capture another piece."""
        
        for dy in self.direction:
            y_possible = self.y

            for _ in range(max_range):
                
                y_possible += dy

                if 0 <= y_possible <= 7:
                    # Check if square is empty
                    if not is_occupied(board, self.x, y_possible):
                        self.valid_moves.append((self.x, y_possible))
                    else:
                        # Check for possible capture
                        if is_occupied_by(board, self.x, y_possible, enemy_color):
                            self.valid_moves.append((self.x, y_possible))

                else:
                    break

    def diagonal_moves(self, board, max_range, enemy_color):
        """Check all diagonal squares the piece can move to, and
        possibly capture another piece."""

        for d in self.direction:
            x_possible = self.x
            y_possible = self.y

            for _ in range(max_range):
                x_possible += d
                y_possible += d

                # Check first diagonal
                if 0 <= x_possible <= 7 and 0 <= y_possible <= 7:

                    # Check if square is empty
                    if not is_occupied(board, x_possible, y_possible):  
                        self.valid_moves.append((x_possible, y_possible))
                    else:
                        # Check for possible capture
                        if is_occupied_by(board, x_possible, y_possible, enemy_color):
                            self.valid_moves.append((x_possible, y_possible))

                else:
                    break

            # Reset search square
            x_possible = self.x
            y_opposite = self.y

            # Check second diagonal
            for _ in range(max_range):
                x_possible += d
                y_opposite -= d

                if 0 <= x_possible <= 7 and 0 <= y_opposite <= 7:
                    # Check if square is empty
                    if not is_occupied(board, x_possible, y_opposite):
                        self.valid_moves.append((x_possible, y_opposite))
                    else:
                        # Check for possible capture
                        if is_occupied_by(board, x_possible, y_opposite, enemy_color):
                            self.valid_moves.append((x_possible, y_opposite))

                else:
                    break       


class Pawn(Piece):
    """Class for pawns"""

    def __init__(self, symbol, color, chess_coord, square_width, square_height):
        
        super().__init__(symbol, color, chess_coord, square_width, square_height)
        
        self.index = 5
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
        board = position.get_board()
        enemy_color = opposite(self.color)
        previous_move = position.get_previous_move()
        self.valid_moves = []

        # Pawn Movement       
        if self.color == 'w':
            self.direction = [-1]
            max_range = 2 if self.y == 6 else 1
        else:
            self.direction = [1]
            max_range = 2 if self.y == 1 else 1
        
        self.vertical_moves(board=board, max_range=max_range, enemy_color=enemy_color)


        #### Pawn Captures ####
        # White pawns
        if self.x != 0 and is_occupied_by(board, self.x - 1, self.y - 1, enemy_color):
            self.valid_moves.append((self.x - 1, self.y - 1))
        if self.x != 7 and is_occupied_by(board, self.x + 1, self.y - 1, enemy_color):
            self.valid_moves.append((self.x + 1, self.y - 1))

        # Black pawns
        if self.x != 0 and is_occupied_by(board, self.x - 1, self.y + 1, enemy_color):
            self.valid_moves.append((self.x - 1, self.y + 1))
        if self.x != 7 and is_occupied_by(board, self.x + 1, self.y + 1, enemy_color):
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

    
class Knight(Piece):
    """Class for knights"""
    
    def __init__(self, name, color, chess_coord, square_width, square_height):
        super().__init__(name, color, chess_coord, square_width, square_height)
        self.index = 3
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
        
        board = position.get_board()
        enemy_color = opposite(self.color)
        self.valid_moves = []
        
        for dx in self.direction:
            # Possible squares that are +1/-1 in x, +2/-2 in y away from original square
           
            x_possible = self.x + dx
            if 0 <= x_possible <= 7:
                # Now check whether the knight can jump to any square d = |2y| away
                for dy in self.direction:
                    y_possible = self.y + 2 * dy
                    if 0 <= y_possible <= 7:
                        if not is_occupied(board, x_possible, y_possible):
                            self.valid_moves.append((x_possible, y_possible))
                        else:
                            if is_occupied_by(board, x_possible, y_possible, enemy_color):
                                self.valid_moves.append((x_possible, y_possible))

        for dy in self.direction:
            # Possible squares that are +2/-2 in x, +1/-1 in y away from original square
            
            y_possible = self.y + dy
            if 0 <= y_possible <= 7:
                # Now check whether the knight can jump to any square d = |2x| away
                for dx in self.direction:
                    x_possible = self.x + 2 * dx
                    if 0 <= x_possible <= 7:
                        if not is_occupied(board, x_possible, y_possible):
                            self.valid_moves.append((x_possible, y_possible))
                        else:
                            if is_occupied_by(board, x_possible, y_possible, enemy_color):
                                self.valid_moves.append((x_possible, y_possible))


class Bishop(Piece):
    """Class for pawn bishops"""

    def __init__(self, name, color, chess_coord, square_width, square_height):
        super().__init__(name, color, chess_coord, square_width, square_height)
        self.index = 2
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
        board = position.get_board()
        self.valid_moves = []
        self.diagonal_moves(board=board, max_range=7, enemy_color=opposite(self.color))


class Rook(Piece):
    """Class for rooks"""
    
    def __init__(self, name, color, chess_coord, square_width, square_height):
        super().__init__(name, color, chess_coord, square_width, square_height)
        self.index = 4
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
        board = position.get_board()
        self.valid_moves = []
        self.horizontal_moves(board=board, max_range=7, enemy_color=opposite(self.color))
        self.vertical_moves(board=board, max_range=7, enemy_color=opposite(self.color))


class Queen(Piece):
    """Class for the queen"""
    
    def __init__(self, name, color, chess_coord, square_width, square_height):
        super().__init__(name, color, chess_coord, square_width, square_height)
        self.index = 1
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
        board = position.get_board()
        self.valid_moves = []
        self.horizontal_moves(board=board, max_range=7, enemy_color=opposite(self.color))
        self.vertical_moves(board=board, max_range=7, enemy_color=opposite(self.color))
        self.diagonal_moves(board=board, max_range=7, enemy_color=opposite(self.color))
        

class King(Piece):
    """Class for the king"""
    
    def __init__(self, name, color, chess_coord, square_width, square_height):
        super().__init__(name, color, chess_coord, square_width, square_height)
        self.index = 0
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
        self.horizontal_moves(board=board, max_range=1, enemy_color=opposite(self.color))
        self.vertical_moves(board=board, max_range=1, enemy_color=opposite(self.color))
        self.diagonal_moves(board=board, max_range=1, enemy_color=opposite(self.color))

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
