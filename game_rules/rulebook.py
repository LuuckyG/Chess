class RuleBook:

    def __init__(self):
        pass

    def valid_moves(self, position, color):
        """Get all possible moves of all pieces of a player"""
        board = position.get_board()
        player_pieces = []
        player_moves = []

        for x in range(8):
            for y in range(8):
                if board[y][x] != 0:
                    if board[y][x][1] == color:
                        player_pieces.append(board[y][x])
                        player_moves.append(valid_piece_move(position, x, y, color)[0])
        return player_moves

    def show_moves(self):
        pass

    def resignation(self):
        pass

    def is_checkmate(self):
        pass

    def is_check(self):
        pass

    def is_stalemate(self):
        pass
