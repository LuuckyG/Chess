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