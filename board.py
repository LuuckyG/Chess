"""Script for saving board position and making moves"""
import copy


class GamePosition:
    """Class to store current position on the board"""

    def __init__(self, board, player, castling_rights):
        self.board = board
        self.player = player
        self.castling = castling_rights
        self.EPT = -1  # This variable will store a coordinate if there is a square that can be en passant captured
        # on. Otherwise it stores -1, indicating lack of en passant targets
        self.previous_move = [(-1, -1), (-1, -1)]
        self.play = True
        self.HMC = 0  # Detect draw if there are 50 moves without any capture or pawn movement
        self.history = {}  # Dictionary to check 3-fold repetition.

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
        # This method returns another instance of the current object with exactly the same
        # parameters but independent of the current object.
        clone = GamePosition(copy.deepcopy(self.board),  # Independent copy
                             self.player,
                             copy.deepcopy(self.castling))  # Independent copy
        clone.set_EPT(self.EPT)
        clone.set_HMC(self.HMC)
        return clone


def position_to_key(position):
    """Create tuple of information about current position"""
    board = position.get_board()
    castle_rights = position.get_castle_rights()

    save_board = []
    for ranks in board:
        save_board.append(tuple(ranks))
    save_board = tuple(save_board)

    save_rights = []
    for right in castle_rights:
        save_rights.append(tuple(right))
    save_rights = tuple(save_rights)

    key = (save_board, position.get_player(), save_rights)
    return key
