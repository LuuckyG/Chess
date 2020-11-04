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


def chess_coord_to_pixels(self, chess_coord, square_width, square_height):
    """Get pixel coordinates from chess board coordinates"""
    x, y = chess_coord
    return x * square_width, y * square_height


def pixel_coord_to_chess(self, pixel_coord, square_width, square_height):
    """Get board coordinates from pixel board coordinates"""
    x, y = pixel_coord
    return x // square_width, y // square_height


def opposite(color):
    """Returns opposite color"""
    return 'b' if color == 'w' else 'w'
