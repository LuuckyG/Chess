import copy

from pieces.pieces import Pawn, Knight, Bishop, Rook, Queen, King, Empty
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
        self.winner = 'Nobody'

        # Detect draw if there are 50 moves without any capture or pawn movement
        self.HMC = 0

        # Dictionary to check 3-fold repetition.
        self.history = {}

        self.pieces = {"white": [], "black": []}
        self.empty_squares = []
    
    def end_of_game(self, king, color):
        """Check game ending situations"""
        if self.resignation or king.is_checkmate():
            self.set_play(False)
            self.winner = opposite(color)
        elif self.is_draw or king.is_stalemate():
            self.game_winner = 'Draw'
            self.set_play(False)
            
    def is_draw(self):
        """Check if players agreed to a draw"""
        return False

    def resignation(self, color):
        """Check if current player resigned"""
        return False
    
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

                    self.pieces["white"].append(p) if color == 'w' else self.pieces["black"].append(p)
                    
                else:
                    empty_square = Empty((y,x))
                    self.empty_squares.append(empty_square)

        return self.pieces

    def get_piece(self, mouse_coord, empty=False):
        """Get piece selected by mouse click"""

        self.white_pieces, self.black_pieces = self.pieces["white"], self.pieces["black"]

        if not empty:
            for color in self.pieces:
                for piece in self.pieces[color]:
                    if piece.chess_coord == mouse_coord:
                        return piece
        else:
            for square in self.empty_squares:
                if square.chess_coord == mouse_coord:
                    return square
    
    def get_piece_position(self, piece):
        for x in range(8):
            for y in range(8):
                if self.board[y][x] == piece:
                    return x, y
    
    def reset_attacking_squares(self):
        for color in self.pieces:
            for piece in self.pieces[color]:
                piece.attacks['direct'] = []
                piece.attacks['indirect'] = []

                piece.attacked_by['direct'] = []
                piece.attacked_by['indirect'] = []
        
        for square in self.empty_squares:
            square.attacked_by['direct'] = []
            square.attacked_by['indirect'] = []

    def is_occupied(self, x, y):
        """Check if selected board tile is empty or not"""
        return self.board[y][x] != 0

    def is_occupied_by_enemy(self, x, y, color):
        """Check if selected board tile has a piece of the opponent"""
        if self.board[y][x] != 0:
            if self.board[y][x][1] == color:  # Space occupied by enemy piece
                return True
        return False

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
