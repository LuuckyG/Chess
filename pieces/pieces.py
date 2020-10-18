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
    
    def get_value_table(self):
        return self.value_table

    def is_endgame(self):
        self.value_table = [-50, -40, -30, -20, -20, -30, -40, -50,
                            -30, -20, -10, 0, 0, -10, -20, -30,
                            -30, -10, 20, 30, 30, 20, -10, -30,
                            -30, -10, 30, 40, 40, 30, -10, -30,
                            -30, -10, 30, 40, 40, 30, -10, -30,
                            -30, -10, 20, 30, 30, 20, -10, -30,
                            -30, -30, 0, 0, 0, 0, -30, -30,
                            -50, -30, -30, -30, -30, -30, -30, -50]
