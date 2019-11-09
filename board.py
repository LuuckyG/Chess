"""Script for saving board position and making moves"""
import copy


class GamePosition:
    """Class to store current position on the board"""

    def __init__(self, board, player, castling_rights, En_Passant_Target, half_move_clock, history={}):
        self.board = board
        self.player = player
        self.castling = castling_rights
        self.EPT = En_Passant_Target
        self.previous_move = [(-1, -1), (-1, -1)]
        self.HMC = half_move_clock  # Detect draw if there are 50 moves without any capture or pawn movement
        self.history = history  # Dict to check 3-fold repetition.

    def get_board(self):
        return self.board

    def set_board(self, board):
        self.board = board

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

    def set_EPT(self, EnP_Target):
        self.EPT = EnP_Target

    def get_previous_move(self):
        return self.previous_move

    def set_previous_move(self, previous_move):
        self.previous_move = previous_move

    def get_HMC(self):
        return self.HMC

    def set_HMC(self, HMC):
        self.HMC = HMC

    def clone(self):
        # This method returns another instance of the current object with exactly the same
        # parameters but independent of the current object.
        clone = GamePosition(copy.deepcopy(self.board),  # Independent copy
                             self.player,
                             copy.deepcopy(self.castling),  # Independent copy
                             self.EPT,
                             self.HMC)
        return clone


class BoardEvents:
    """
    Class to highlight events in the game, such as previous move, check, current selected piece and
    available moves for the selected piece.
    """

    def __init__(self, position, piece, possible_moves, previous_move):
        self.position = position
        self.piece = piece
        self.possible_moves = possible_moves
        self.previous_move = previous_move

    def highlight_selected_piece(self):
        pass

    def show_possible_moves(self):
        pass

    def show_previous_move(self):
        pass

    def show_check_move(self):
        pass

    def show_check_text(self):
        pass
