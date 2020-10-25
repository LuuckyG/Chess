def is_occupied(board, x, y):
    """Check if selected board tile is empty or not"""
    return board[y][x] != 0


def is_occupied_by_enemy(board, x, y, color):
    """Check if selected board tile has a piece of the opponent"""
    if board[y][x] != 0:
        if board[y][x][1] == color:  # Space occupied by enemy piece
            return True
    return False









