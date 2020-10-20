"""Script to create piece class"""


class Piece:
    """Base class for all pieces"""
    def __init__(self, name, color, chess_coord, square_width, square_height):

        self.name = name
        self.color = color
        self.chess_coord = chess_coord

        self.piece = self.name[0]
        self.color = self.name[1]

        self.x = self.chess_coord[0]
        self.y = self.chess_coord[1]

        # Used to search in opposite directions around the pieces
        self.direction = [-1, 1]

        # Give index to pieces on sprite:
        if self.piece == 'K':
            self.index = 0
        elif self.piece == 'Q':
            self.index = 1
        elif self.piece == 'B':
            self.index = 2
        elif self.piece == 'N':
            self.index = 3
        elif self.piece == 'R':
            self.index = 4
        elif self.piece == 'P':
            self.index = 5
        else:
            raise ValueError("Unknown piece!")

        # Determine row in image
        if self.color == 'w':
            upper_y = 0
        else:
            upper_y = square_height

        left_x = self.index * square_width

        self.subsection = (left_x, upper_y, square_width, square_height)
        self.pos = (-1, -1)

    def get_info(self):
        return self.chess_coord, self.color, self.subsection, self.pos

    def set_pos(self, pos):
        self.pos = pos

    def get_pos(self):
        return self.pos

    def set_coord(self, coord):
        self.chess_coord = coord

    def __repr__(self):
        return self.name + '(' + str(self.chess_coord[0]) + ',' + str(self.chess_coord[1]) + ')'


class Pawn(Piece):

    def __init__(self):
        super().__init__(self)
        self.set_value_table()
    
    def set_value_table(self):
        self.value_table = [0, 0, 0, 0, 0, 0, 0, 0,
                            50, 50, 50, 50, 50, 50, 50, 50,
                            10, 10, 20, 30, 30, 20, 10, 10,
                            5, 5, 10, 25, 25, 10, 5, 5,
                            0, 0, 0, 20, 20, 0, 0, 0,
                            5, -5, -10, 0, 0, -10, -5, 5,
                            5, 10, 10, -20, -20, 10, 10, 5,
                            0, 0, 0, 0, 0, 0, 0, 0]
    
    def get_value_table(self):
        return self.value_table
    
    def moves(self, position, x, y):
        board = position.get_board()
        piece = board[y][x][0]
        enemy_color = opposite(self.color)
        previous_move = position.get_previous_move()
        
        valid_moves = []

        if self.color == 'w':
            # Check if pawn is blocked or not
            if board[y - 1][x] == 0:
                valid_moves.append((x, y - 1))  # Pawn can move one up
                if y == 6 and board[y - 2][x] == 0:
                    valid_moves.append((x, y - 2))  # Pawn can also move two up (only first move)

            # Check if pawn can capture
            if x != 0 and is_occupied_by(board, x - 1, y - 1, enemy_color):
                valid_moves.append((x - 1, y - 1))  # Capture right
            if x != 7 and is_occupied_by(board, x + 1, y - 1, enemy_color):
                valid_moves.append((x + 1, y - 1))  # Capture left

            # Check for en passant possibilities
            if y == 3:
                if previous_move == [(x - 1, 1), (x - 1, y)]:
                    if board[y][x - 1][0] == 'P':
                        valid_moves.append((x - 1, y - 1))
                        position.set_EPT((x - 1, y - 1))
                elif previous_move == [(x + 1, 1), (x + 1, y)]:
                    if board[y][x + 1][0] == 'P':
                        valid_moves.append((x + 1, y - 1))
                        position.set_EPT((x + 1, y - 1))

        # For black the movement are in the positive y direction
        elif self.color == 'b':  
            # Check if pawn is blocked or not
            if board[y + 1][x] == 0:
                valid_moves.append((x, y + 1))  # Pawn can move one up
                if y == 1 and board[y + 2][x] == 0:
                    valid_moves.append((x, y + 2))  # Pawn can also move two up (only first move)

            # Check if pawn can capture
            if x != 0 and is_occupied_by(board, x - 1, y + 1, enemy_color):
                valid_moves.append((x - 1, y + 1))  # Capture right
            if x != 7 and is_occupied_by(board, x + 1, y + 1, enemy_color):
                valid_moves.append((x + 1, y + 1))  # Capture left

            # Check for en passant possibilities
            if y == 4:
                if previous_move == [(x - 1, 6), (x - 1, y)]:
                    if board[y][x - 1][0] == 'P':
                        valid_moves.append((x - 1, y + 1))
                        position.set_EPT((x - 1, y + 1))
                elif previous_move == [(x + 1, 6), (x + 1, y)]:
                    if board[y][x + 1][0] == 'P':
                        valid_moves.append((x + 1, y + 1))
                        position.set_EPT((x + 1, y + 1))

    
class Knight(Piece):
    
    def __init__(self):
        super().__init__(self)
        self.set_value_table()

    def set_value_table(self):
        self.value_table = [-50, -40, -30, -30, -30, -30, -40, -50,
                            -40, -20, 0, 0, 0, 0, -20, -40,
                            -30, 0, 10, 15, 15, 10, 0, -30,
                            -30, 5, 15, 20, 20, 15, 5, -30,
                            -30, 0, 15, 20, 20, 15, 0, -30,
                            -30, 5, 10, 15, 15, 10, 5, -30,
                            -40, -20, 0, 5, 5, 0, -20, -40,
                            -50, -90, -30, -30, -30, -30, -90, -50]
    
    def get_value_table(self):
        return self.value_table

    def moves(self):
        # A knight can either move +2/-2 in x direction and +1/-1 in y direction, or the other way around
        for dx in direction:
            # Possible squares that are +1/-1 in x, +2/-2 in y away from original square
            x_possible = x + dx
            if 0 <= x_possible <= 7:
                # Now check whether the knight can jump to any square d = |2y| away
                for dy in direction:
                    y_possible = y + 2 * dy
                    if 0 <= y_possible <= 7:
                        if not is_occupied(board, x_possible, y_possible):
                            valid_moves.append((x_possible, y_possible))
                        else:
                            if is_occupied_by(board, x_possible, y_possible, enemy_color):
                                valid_moves.append((x_possible, y_possible))

        for dy in direction:
            # Possible squares that are +2/-2 in x, +1/-1 in y away from original square
            y_possible = y + dy
            if 0 <= y_possible <= 7:
                # Now check whether the knight can jump to any square d = |2x| away
                for dx in direction:
                    x_possible = x + 2 * dx
                    if 0 <= x_possible <= 7:
                        if not is_occupied(board, x_possible, y_possible):
                            valid_moves.append((x_possible, y_possible))
                        else:
                            if is_occupied_by(board, x_possible, y_possible, enemy_color):
                                valid_moves.append((x_possible, y_possible))


class Bishop(Piece):
    
    def __init__(self):
        super().__init__(self)
        self.set_value_table()

    def set_value_table(self):
        self.value_table = [-20, -10, -10, -10, -10, -10, -10, -20,
                            -10, 0, 0, 0, 0, 0, 0, -10,
                            -10, 0, 5, 10, 10, 5, 0, -10,
                            -10, 5, 5, 10, 10, 5, 5, -10,
                            -10, 0, 10, 10, 10, 10, 0, -10,
                            -10, 10, 10, 10, 10, 10, 10, -10,
                            -10, 5, 0, 0, 0, 0, 5, -10,
                            -20, -10, -90, -10, -10, -90, -10, -20]
    
    def get_value_table(self):
        return self.value_table
    
    def moves(self):
        for d in direction:
            x_possible = x + d
            y_possible = y + d

            while True:
                # Check first diagonal
                if 0 <= x_possible <= 7 and 0 <= y_possible <= 7:
                    if not is_occupied(board, x_possible, y_possible):  # Square is empty
                        valid_moves.append((x_possible, y_possible))
                    else:
                        if is_occupied_by(board, x_possible, y_possible, enemy_color):
                            valid_moves.append((x_possible, y_possible))
                        if not attack_search:
                            break

                    # Update square that is checked
                    x_possible += d
                    y_possible += d

                else:
                    break

            # Reset search square
            x_possible = x + d
            y_opposite = y - d

            while True:
                # Check second diagonal
                if 0 <= x_possible <= 7 and 0 <= y_opposite <= 7:
                    if not is_occupied(board, x_possible, y_opposite):  # Square is empty
                        valid_moves.append((x_possible, y_opposite))
                    else:
                        if is_occupied_by(board, x_possible, y_opposite, enemy_color):
                            valid_moves.append((x_possible, y_opposite))
                        if not attack_search:
                            break  # Bishop cannot jump over other pieces, no need to search further

                    # Update square that is checked
                    x_possible += d
                    y_opposite -= d

                else:
                    break


class Rook(Piece):
    
    def __init__(self):
        super().__init__(self)
        self.set_value_table()

    def set_value_table(self):
        self.value_table = [0, 0, 0, 0, 0, 0, 0, 0,
                            5, 10, 10, 10, 10, 10, 10, 5,
                            -5, 0, 0, 0, 0, 0, 0, -5,
                            -5, 0, 0, 0, 0, 0, 0, -5,
                            -5, 0, 0, 0, 0, 0, 0, -5,
                            -5, 0, 0, 0, 0, 0, 0, -5,
                            -5, 0, 0, 0, 0, 0, 0, -5,
                            0, 0, 0, 5, 5, 0, 0, 0]
    
    def get_value_table(self):
        return self.value_table

    def moves(self):
        # Horizontal squares
        for dx in direction:
            x_possible = x + dx
            while True:
                if 0 <= x_possible <= 7:
                    if not is_occupied(board, x_possible, y):  # Square is empty
                        valid_moves.append((x_possible, y))
                    else:
                        if is_occupied_by(board, x_possible, y, enemy_color):
                            valid_moves.append((x_possible, y))
                        if not attack_search:
                            break  # Rook cannot jump over other pieces, no need to search further

                    x_possible += dx  # Update square that is checked

                else:
                    break

        # Vertical squares
        for dy in direction:
            y_possible = y + dy
            while True:
                if 0 <= y_possible <= 7:
                    if not is_occupied(board, x, y_possible):  # Square is empty
                        valid_moves.append((x, y_possible))
                    else:
                        if is_occupied_by(board, x, y_possible, enemy_color):
                            valid_moves.append((x, y_possible))
                        if not attack_search:
                            break  # Rook cannot jump over other pieces, no need to search further

                    y_possible += dy  # Update square that is checked

                else:
                    break


class Queen(Piece):
    
    def __init__(self):
        super().__init__(self)
        self.set_value_table()

    def set_value_table(self):
        self.value_table = [-20, -10, -10, -5, -5, -10, -10, -20,
                            -10, 0, 0, 0, 0, 0, 0, -10,
                            -10, 0, 5, 5, 5, 5, 0, -10,
                            -5, 0, 5, 5, 5, 5, 0, -5,
                            0, 0, 5, 5, 5, 5, 0, -5,
                            -10, 5, 5, 5, 5, 5, 0, -10,
                            -10, 0, 5, 0, 0, 0, 0, -10,
                            -20, -10, -10, 70, -5, -10, -10, -20]
    
    def get_value_table(self):
        return self.value_table

    def moves(self):
        # Horizontal squares
        for dx in direction:
            x_possible = x + dx
            while True:
                if 0 <= x_possible <= 7:
                    if not is_occupied(board, x_possible, y):  # Square is empty
                        valid_moves.append((x_possible, y))
                    else:
                        if is_occupied_by(board, x_possible, y, enemy_color):
                            valid_moves.append((x_possible, y))
                        if not attack_search:
                            break  # Queen cannot jump over other pieces, no need to search further

                    x_possible += dx  # Update square that is checked

                else:
                    break

        # Vertical squares
        for dy in direction:
            y_possible = y + dy
            while True:
                if 0 <= y_possible <= 7:
                    if not is_occupied(board, x, y_possible):  # Square is empty
                        valid_moves.append((x, y_possible))
                    else:
                        if is_occupied_by(board, x, y_possible, enemy_color):
                            valid_moves.append((x, y_possible))
                        if not attack_search:
                            break  # Queen cannot jump over other pieces, no need to search further

                    y_possible += dy  # Update square that is checked

                else:
                    break

        # Diagonal squares
        for d in direction:
            x_possible = x + d
            y_possible = y + d

            while True:
                # Check first diagonal
                if 0 <= x_possible <= 7 and 0 <= y_possible <= 7:
                    if not is_occupied(board, x_possible, y_possible):  # Square is empty
                        valid_moves.append((x_possible, y_possible))
                    else:
                        if is_occupied_by(board, x_possible, y_possible, enemy_color):
                            valid_moves.append((x_possible, y_possible))
                        if not attack_search:
                            break

                    # Update square that is checked
                    x_possible += d
                    y_possible += d

                else:
                    break

            # Reset search square
            x_possible = x + d
            y_opposite = y - d

            while True:
                # Check second diagonal
                if 0 <= x_possible <= 7 and 0 <= y_opposite <= 7:
                    if not is_occupied(board, x_possible, y_opposite):  # Square is empty
                        valid_moves.append((x_possible, y_opposite))
                    else:
                        if is_occupied_by(board, x_possible, y_opposite, enemy_color):
                            valid_moves.append((x_possible, y_opposite))
                        if not attack_search:
                            break # Queen cannot jump over other pieces, no need to search further

                    # Update square that is checked
                    x_possible += d
                    y_opposite -= d

                else:
                    break


class King(Piece):
    
    def __init__(self):
        super().__init__(self)
        self.set_value_table()

    def set_value_table(self):
        self.value_table = [-30, -40, -40, -50, -50, -40, -40, -30,
                            -30, -40, -40, -50, -50, -40, -40, -30,
                            -30, -40, -40, -50, -50, -40, -40, -30,
                            -30, -40, -40, -50, -50, -40, -40, -30,
                            -20, -30, -30, -40, -40, -30, -30, -20,
                            -10, -20, -20, -20, -20, -20, -20, -10,
                            20, 20, 0, 0, 0, 0, 20, 20,
                            20, 30, 10, 0, 0, 10, 30, 20]
    
    def is_endgame(self):
        self.value_table = [-50, -40, -30, -20, -20, -30, -40, -50,
                            -30, -20, -10, 0, 0, -10, -20, -30,
                            -30, -10, 20, 30, 30, 20, -10, -30,
                            -30, -10, 30, 40, 40, 30, -10, -30,
                            -30, -10, 30, 40, 40, 30, -10, -30,
                            -30, -10, 20, 30, 30, 20, -10, -30,
                            -30, -30, 0, 0, 0, 0, -30, -30,
                            -50, -30, -30, -30, -30, -30, -30, -50]
    
    def get_value_table(self):
        return self.value_table

    def moves(self):
        # For the king, one need to checks the 8 surrounding squares, for being in check, and castling options.
        for d in direction:

            x_possible = x + d
            y_possible = y + d
            y_opposite = y - d

            if 0 <= x_possible <= 7:
                # Horizontal squares
                if not is_occupied(board, x_possible, y):  # Square is empty
                    valid_moves.append((x_possible, y))
                else:
                    if is_occupied_by(board, x_possible, y, enemy_color):
                        valid_moves.append((x_possible, y))

            if 0 <= y_possible <= 7:
                # Vertical squares
                if not is_occupied(board, x, y_possible):  # Square is empty
                    valid_moves.append((x, y_possible))
                else:
                    if is_occupied_by(board, x, y_possible, enemy_color):
                        valid_moves.append((x, y_possible))

            if 0 <= x_possible <= 7 and 0 <= y_possible <= 7:
                # Diagonal squares
                if not is_occupied(board, x_possible, y_possible):  # Square is empty
                    valid_moves.append((x_possible, y_possible))
                else:
                    if is_occupied_by(board, x_possible, y_possible, enemy_color):
                        valid_moves.append((x_possible, y_possible))

            if 0 <= x_possible <= 7 and 0 <= y_opposite <= 7:
                if not is_occupied(board, x_possible, y_opposite):  # Square is empty
                    valid_moves.append((x_possible, y_opposite))
                else:
                    if is_occupied_by(board, x_possible, y_opposite, enemy_color):
                        valid_moves.append((x_possible, y_opposite))

        # Castling options
        castle_right = position.get_castle_rights()

        if color == 'w':
            # Kingside castle
            if castle_right[0][0]:
                if board[7][5] == 0 and board[7][6] == 0:
                    valid_moves.append((6, 7))
            # Queenside castle
            if castle_right[0][1]:
                if board[7][1] == 0 and board[7][2] == 0 and board[7][3] == 0:
                    valid_moves.append((2, 7))
        elif color == 'b':
            # Kingside castle
            if castle_right[1][0]:
                if board[0][5] == 0 and board[0][6] == 0:
                    valid_moves.append((6, 0))
            # Queenside castle
            if castle_right[1][1]:
                if board[0][1] == 0 and board[0][2] == 0 and board[0][3] == 0:
                    valid_moves.append((2, 0))
