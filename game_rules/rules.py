"""Functions to check if moves are legal"""


def opposite(color):
    """Returns opposite color"""
    if color == 'w':
        return 'b'
    elif color == 'b':
        return 'w'


def is_captured(board, target_x, target_y):
    return board[target_y][target_x] != 0


def get_piece_position(position, piece):
    board = position.get_board()
    for x in range(8):
        for y in range(8):
            if board[y][x] == piece:
                return x, y


def is_occupied(board, x, y):
    """Check if selected board tile is empty or not"""
    if board[y][x] == 0:
        return False
    return True


def is_occupied_by(board, x, y, color):
    """Check if selected board tile has a piece of the opponent"""
    if board[y][x] != 0:
        if board[y][x][1] == color:  # Space occupied by enemy piece
            return True
    return False



def is_attacked_by(position, target_x, target_y, color):
    board = position.get_board()
    piece = board[target_y][target_x][0]
    attacking_pieces = []
    attacked_squares = []
    for x in range(8):
        for y in range(8):
            if board[y][x] != 0:
                if board[y][x][1] == color:
                    attacking_piece = board[y][x]
                    pos_squares, _ = valid_piece_move(position, x, y, color, attack_search=True)
                    if (target_x, target_y) in pos_squares:
                        pass

    return attacked_squares


def attacked_squares(position, color):
    pass


def is_check(position, x, y, piece, color):
    pass


def is_checkmate(position, x, y, piece, color):
    pass


def is_stalemate(position, x, y, piece, color):
    pass
