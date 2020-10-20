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
