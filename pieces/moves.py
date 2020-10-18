def moves(piece, position, x, y, color):

    

    return valid_moves


def valid_piece_move(position, x, y, color, attack_search=False):
    """Check if the piece makes legal move"""
    board = position.get_board()
    piece = board[y][x][0]
    enemy_color = opposite(color)
    previous_move = position.get_previous_move()
    direction = [-1, 1]  # Used to search in opposite directions around the pieces
    valid_moves = []

    if piece == 'P':  # Pawn
        if color == 'w':
            # Check if pawn is blocked or not
            if board[y - 1][x] == 0:
                valid_moves.append((x, y - 1))  # Pawn can move one up
                if y == 6 and board[y - 2][x] == 0:
                    valid_moves.append((x, y - 2))  # Pawn can also move two up (only first move)

            # Check if pawn can capture
            if x != 0 and is_occupied_by(board, x - 1, y - 1, enemy_color):
                valid_moves.append((x - 1, y - 1))  # Capture right
            if x != 7 and is_occupied_by(board, x + 1, y - 1, enemy_color):
                valid_moves.append((x + 1, y - 1))  # Capture left

            # Check for en passant possibilities
            if y == 3:
                if previous_move == [(x - 1, 1), (x - 1, y)]:
                    if board[y][x - 1][0] == 'P':
                        valid_moves.append((x - 1, y - 1))
                        position.set_EPT((x - 1, y - 1))
                elif previous_move == [(x + 1, 1), (x + 1, y)]:
                    if board[y][x + 1][0] == 'P':
                        valid_moves.append((x + 1, y - 1))
                        position.set_EPT((x + 1, y - 1))

        elif color == 'b':  # For black the movement are in the positive y direction
            # Check if pawn is blocked or not
            if board[y + 1][x] == 0:
                valid_moves.append((x, y + 1))  # Pawn can move one up
                if y == 1 and board[y + 2][x] == 0:
                    valid_moves.append((x, y + 2))  # Pawn can also move two up (only first move)

            # Check if pawn can capture
            if x != 0 and is_occupied_by(board, x - 1, y + 1, enemy_color):
                valid_moves.append((x - 1, y + 1))  # Capture right
            if x != 7 and is_occupied_by(board, x + 1, y + 1, enemy_color):
                valid_moves.append((x + 1, y + 1))  # Capture left

            # Check for en passant possibilities
            if y == 4:
                if previous_move == [(x - 1, 6), (x - 1, y)]:
                    if board[y][x - 1][0] == 'P':
                        valid_moves.append((x - 1, y + 1))
                        position.set_EPT((x - 1, y + 1))
                elif previous_move == [(x + 1, 6), (x + 1, y)]:
                    if board[y][x + 1][0] == 'P':
                        valid_moves.append((x + 1, y + 1))
                        position.set_EPT((x + 1, y + 1))

    elif piece == 'R':  # Rook
        # Horizontal squares
        for dx in direction:
            x_possible = x + dx
            while True:
                if 0 <= x_possible <= 7:
                    if not is_occupied(board, x_possible, y):  # Square is empty
                        valid_moves.append((x_possible, y))
                    else:
                        if is_occupied_by(board, x_possible, y, enemy_color):
                            valid_moves.append((x_possible, y))
                        if not attack_search:
                            break  # Rook cannot jump over other pieces, no need to search further

                    x_possible += dx  # Update square that is checked

                else:
                    break

        # Vertical squares
        for dy in direction:
            y_possible = y + dy
            while True:
                if 0 <= y_possible <= 7:
                    if not is_occupied(board, x, y_possible):  # Square is empty
                        valid_moves.append((x, y_possible))
                    else:
                        if is_occupied_by(board, x, y_possible, enemy_color):
                            valid_moves.append((x, y_possible))
                        if not attack_search:
                            break  # Rook cannot jump over other pieces, no need to search further

                    y_possible += dy  # Update square that is checked

                else:
                    break

    elif piece == 'N':  # Knight
        # A knight can either move +2/-2 in x direction and +1/-1 in y direction, or the other way around
        for dx in direction:
            # Possible squares that are +1/-1 in x, +2/-2 in y away from original square
            x_possible = x + dx
            if 0 <= x_possible <= 7:
                # Now check whether the knight can jump to any square d = |2y| away
                for dy in direction:
                    y_possible = y + 2 * dy
                    if 0 <= y_possible <= 7:
                        if not is_occupied(board, x_possible, y_possible):
                            valid_moves.append((x_possible, y_possible))
                        else:
                            if is_occupied_by(board, x_possible, y_possible, enemy_color):
                                valid_moves.append((x_possible, y_possible))

        for dy in direction:
            # Possible squares that are +2/-2 in x, +1/-1 in y away from original square
            y_possible = y + dy
            if 0 <= y_possible <= 7:
                # Now check whether the knight can jump to any square d = |2x| away
                for dx in direction:
                    x_possible = x + 2 * dx
                    if 0 <= x_possible <= 7:
                        if not is_occupied(board, x_possible, y_possible):
                            valid_moves.append((x_possible, y_possible))
                        else:
                            if is_occupied_by(board, x_possible, y_possible, enemy_color):
                                valid_moves.append((x_possible, y_possible))

    elif piece == 'B':  # Bishop
        for d in direction:
            x_possible = x + d
            y_possible = y + d

            while True:
                # Check first diagonal
                if 0 <= x_possible <= 7 and 0 <= y_possible <= 7:
                    if not is_occupied(board, x_possible, y_possible):  # Square is empty
                        valid_moves.append((x_possible, y_possible))
                    else:
                        if is_occupied_by(board, x_possible, y_possible, enemy_color):
                            valid_moves.append((x_possible, y_possible))
                        if not attack_search:
                            break

                    # Update square that is checked
                    x_possible += d
                    y_possible += d

                else:
                    break

            # Reset search square
            x_possible = x + d
            y_opposite = y - d

            while True:
                # Check second diagonal
                if 0 <= x_possible <= 7 and 0 <= y_opposite <= 7:
                    if not is_occupied(board, x_possible, y_opposite):  # Square is empty
                        valid_moves.append((x_possible, y_opposite))
                    else:
                        if is_occupied_by(board, x_possible, y_opposite, enemy_color):
                            valid_moves.append((x_possible, y_opposite))
                        if not attack_search:
                            break  # Bishop cannot jump over other pieces, no need to search further

                    # Update square that is checked
                    x_possible += d
                    y_opposite -= d

                else:
                    break

    elif piece == 'Q':  # Queen
        # Horizontal squares
        for dx in direction:
            x_possible = x + dx
            while True:
                if 0 <= x_possible <= 7:
                    if not is_occupied(board, x_possible, y):  # Square is empty
                        valid_moves.append((x_possible, y))
                    else:
                        if is_occupied_by(board, x_possible, y, enemy_color):
                            valid_moves.append((x_possible, y))
                        if not attack_search:
                            break  # Queen cannot jump over other pieces, no need to search further

                    x_possible += dx  # Update square that is checked

                else:
                    break

        # Vertical squares
        for dy in direction:
            y_possible = y + dy
            while True:
                if 0 <= y_possible <= 7:
                    if not is_occupied(board, x, y_possible):  # Square is empty
                        valid_moves.append((x, y_possible))
                    else:
                        if is_occupied_by(board, x, y_possible, enemy_color):
                            valid_moves.append((x, y_possible))
                        if not attack_search:
                            break  # Queen cannot jump over other pieces, no need to search further

                    y_possible += dy  # Update square that is checked

                else:
                    break

        # Diagonal squares
        for d in direction:
            x_possible = x + d
            y_possible = y + d

            while True:
                # Check first diagonal
                if 0 <= x_possible <= 7 and 0 <= y_possible <= 7:
                    if not is_occupied(board, x_possible, y_possible):  # Square is empty
                        valid_moves.append((x_possible, y_possible))
                    else:
                        if is_occupied_by(board, x_possible, y_possible, enemy_color):
                            valid_moves.append((x_possible, y_possible))
                        if not attack_search:
                            break

                    # Update square that is checked
                    x_possible += d
                    y_possible += d

                else:
                    break

            # Reset search square
            x_possible = x + d
            y_opposite = y - d

            while True:
                # Check second diagonal
                if 0 <= x_possible <= 7 and 0 <= y_opposite <= 7:
                    if not is_occupied(board, x_possible, y_opposite):  # Square is empty
                        valid_moves.append((x_possible, y_opposite))
                    else:
                        if is_occupied_by(board, x_possible, y_opposite, enemy_color):
                            valid_moves.append((x_possible, y_opposite))
                        if not attack_search:
                            break # Queen cannot jump over other pieces, no need to search further

                    # Update square that is checked
                    x_possible += d
                    y_opposite -= d

                else:
                    break

    elif piece == 'K':  # King
        # For the king, one need to checks the 8 surrounding squares, for being in check, and castling options.
        for d in direction:

            x_possible = x + d
            y_possible = y + d
            y_opposite = y - d

            if 0 <= x_possible <= 7:
                # Horizontal squares
                if not is_occupied(board, x_possible, y):  # Square is empty
                    valid_moves.append((x_possible, y))
                else:
                    if is_occupied_by(board, x_possible, y, enemy_color):
                        valid_moves.append((x_possible, y))

            if 0 <= y_possible <= 7:
                # Vertical squares
                if not is_occupied(board, x, y_possible):  # Square is empty
                    valid_moves.append((x, y_possible))
                else:
                    if is_occupied_by(board, x, y_possible, enemy_color):
                        valid_moves.append((x, y_possible))

            if 0 <= x_possible <= 7 and 0 <= y_possible <= 7:
                # Diagonal squares
                if not is_occupied(board, x_possible, y_possible):  # Square is empty
                    valid_moves.append((x_possible, y_possible))
                else:
                    if is_occupied_by(board, x_possible, y_possible, enemy_color):
                        valid_moves.append((x_possible, y_possible))

            if 0 <= x_possible <= 7 and 0 <= y_opposite <= 7:
                if not is_occupied(board, x_possible, y_opposite):  # Square is empty
                    valid_moves.append((x_possible, y_opposite))
                else:
                    if is_occupied_by(board, x_possible, y_opposite, enemy_color):
                        valid_moves.append((x_possible, y_opposite))

        # Castling options
        castle_right = position.get_castle_rights()

        if color == 'w':
            # Kingside castle
            if castle_right[0][0]:
                if board[7][5] == 0 and board[7][6] == 0:
                    valid_moves.append((6, 7))
            # Queenside castle
            if castle_right[0][1]:
                if board[7][1] == 0 and board[7][2] == 0 and board[7][3] == 0:
                    valid_moves.append((2, 7))
        elif color == 'b':
            # Kingside castle
            if castle_right[1][0]:
                if board[0][5] == 0 and board[0][6] == 0:
                    valid_moves.append((6, 0))
            # Queenside castle
            if castle_right[1][1]:
                if board[0][1] == 0 and board[0][2] == 0 and board[0][3] == 0:
                    valid_moves.append((2, 0))

    return valid_moves, position