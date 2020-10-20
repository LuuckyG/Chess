def is_promotion(position, y):
    return y == position.get_player() * 7

def en_passant_rights(position, x, y):
    """If en passant captured, update board by removing captured pawn."""
    player = position.get_player()
    board = position.get_board()
    en_passant_target = position.get_EPT()

    if (x, y) == en_passant_target and 'wb'[player] == 'w':
        board[y + 1][x] = 0
    elif (x, y) == en_passant_target and 'wb'[player] == 'b':
        board[y - 1][x] = 0
    position.set_board(board)
    return position

def castle_rights(position, x, y):
    player = position.get_player()
    board = position.get_board()
    castle_right = position.get_castle_rights()

    if (x, y) == (2, (1 - player) * 7):
        # Queenside
        board[(1 - player) * 7][3] = board[(1 - player) * 7][0]
        board[(1 - player) * 7][0] = 0
        castle_right[player][0] = castle_right[player][1] = False
    elif (x, y) == (6, (1 - player) * 7):
        # Kingside
        board[(1 - player) * 7][5] = board[(1 - player) * 7][7]
        board[(1 - player) * 7][7] = 0
        castle_right[player][0] = castle_right[player][1] = False

    position.set_castle_rights(castle_right)
    position.set_board(board)
    return position