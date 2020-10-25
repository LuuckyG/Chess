from setup.utils import opposite

class RuleBook:

    def __init__(self):
        self.is_game_end = False
        self.game_winner = 'Nobody'

    def end_of_game(self, position, king, color):
        """Check game ending situations"""
        if self.resignation or self.is_checkmate(king):
            self.is_game_end = True
            self.game_winner = opposite(color)
        elif self.is_draw or self.is_stalemate(king):
            self.is_game_end = True
            self.game_winner = 'Draw'

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

    def is_pinned(self, king):
        """King is pinned by enemy, meaning the piece cannot move"""
        return len(king.attacked_by['indirect']) >= 1

    def is_check(self, king):
        return len(king.attacked_by['direct']) >= 1

    def is_checkmate(self, king):
        if self.is_check(king):
            for square in king.valid_moves:
                if not square.attacked_by['direct']:
                    return False
            return True
        return False

    def is_stalemate(self, king):
        if not self.is_check(king):
            for square in king.valid_moves:
                if not square.attacked_by['direct']:
                    return False
            return True
        return False

    def is_draw(self):
        if self.is_stalemate:
            return True
        return False
    
    def resignation(self):
        return False
    
