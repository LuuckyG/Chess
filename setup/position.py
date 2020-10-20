import copy

from pieces.pieces import Pawn, Knight, Bishop, Rook, Queen, King
from setup.utils import position_to_key, pixel_coord_to_chess, chess_coord_to_pixels, opposite

class GamePosition:
    """Class to store current position on the board and 
    to keep track of all the pieces on the board."""

    BOARD = [['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb'],  # 8
            ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'],  # 7
            [0, 0, 0, 0, 0, 0, 0, 0],  # 6
            [0, 0, 0, 0, 0, 0, 0, 0],  # 5
            [0, 0, 0, 0, 0, 0, 0, 0],  # 4
            [0, 0, 0, 0, 0, 0, 0, 0],  # 3
            ['Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw'],  # 2
            ['Rw', 'Nw', 'Bw', 'Qw', 'Kw', 'Bw', 'Nw', 'Rw']]  # 1

    def __init__(self, board=BOARD, player=0, castling=[[True, True], [True, True]]):
        self.board = board

        # 0 is white, 1 is black
        self.player = player
        
        # Castling rights (King side, Queen side)
        self.castling = castling
        
        # This variable will store a coordinate if there is a square that can be en passant captured
        # on. Otherwise it stores -1, indicating lack of en passant targets
        self.EPT = -1  

        self.previous_move = [(-1, -1), (-1, -1)]
        self.play = True

        # Detect draw if there are 50 moves without any capture or pawn movement
        self.HMC = 0

        # Dictionary to check 3-fold repetition.
        self.history = {}

        self.pieces = {"white": [], "black": []}
    
    def create_pieces(self, square_width, square_height):
        """Create piece objects based on board position"""

        for x in range(8):
            for y in range(8):
                if self.board[x][y] != 0:

                    symbol = self.board[x][y][0]
                    color = self.board[x][y][1]

                    if symbol == 'K':
                        p = King(symbol, color, (y, x), square_width, square_height)
                    elif symbol == 'Q':
                        p = Queen(symbol, color, (y, x), square_width, square_height)
                    elif symbol == 'B':
                        p = Bishop(symbol, color, (y, x), square_width, square_height)
                    elif symbol == 'N':
                        p = Knight(symbol, color, (y, x), square_width, square_height)
                    elif symbol == 'R':
                        p = Rook(symbol, color, (y, x), square_width, square_height)
                    elif symbol == 'P':
                        p = Pawn(symbol, color, (y, x), square_width, square_height)

                    if color == 'w':
                        self.pieces["white"].append(p)
                    else:
                        self.pieces["black"].append(p)

    def get_piece(self, mouse_coord):
        """Get piece selected by mouse click"""

        self.white_pieces, self.black_pieces = self.pieces["white"], self.pieces["black"]
        self.pieces = self.white_pieces + self.black_pieces

        for piece in self.pieces:
            if piece.chess_coord == mouse_coord:
                return piece

    def get_board(self):
        return self.board

    def set_board(self, board):
        self.board = board

    def get_scale(self):
        return self.square_height, self.square_width
    
    def set_scale(self, height, width):
        self.square_height = height
        self.square_width = width
    
    def get_player(self):
        return self.player

    def set_player(self, player):
        self.player = player

    def get_castle_rights(self):
        return self.castling

    def set_castle_rights(self, castling_rights):
        self.castling = castling_rights

    def get_EPT(self):
        return self.EPT

    def set_EPT(self, en_passant_target):
        self.EPT = en_passant_target

    def get_previous_move(self):
        return self.previous_move

    def set_previous_move(self, previous_move):
        self.previous_move = previous_move

    def get_HMC(self):
        return self.HMC

    def set_HMC(self, HMC):
        self.HMC = HMC

    def get_history(self):
        return self.history

    def set_history(self, position):
        key = position_to_key(position)
        if key in self.history.keys():
            self.history[key] += 1
        else:
            self.history[key] = 1

    def get_play(self):
        return self.play

    def set_play(self, play):
        self.play = play

    def clone(self):
        """This method returns another instance of the current object with exactly the same
        parameters but independent of the current object."""

        # Independent copy
        clone = GamePosition(copy.deepcopy(self.board), 
                            self.player,
                            copy.deepcopy(self.castling))

        clone.set_EPT(self.EPT)
        clone.set_HMC(self.HMC)
        return clone
