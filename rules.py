"""Functions to check if moves are legal"""


def opposite(color):
    """Returns opposite color"""
    if color == 'w':
        return 'b'
    elif color == 'b':
        return 'w'


def is_captured(board, target_x, target_y):
    return board[target_y][target_x] != 0


def is_promotion(position, y):
    return y == position.get_player() * 7


def get_piece_position(position, piece):
    board = position.get_board()
    for x in range(8):
        for y in range(8):
            if board[y][x] == piece:
                return x, y


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


def all_possible_moves(position, color):
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


def make_move(position, x, y, x2, y2):
    """Check if move is valid, if so update position."""
    player = position.get_player()
    color = 'wb'[player]
    enemy_color = opposite(color)
    HMC = position.get_HMC()
    inCheck = False

    # Check if player is not in check
    king_position = get_piece_position(position, 'K' + color)  # Find position of the king of player
    attacked_squares = is_attacked_by(position,
                                      king_position[0], king_position[1],
                                      enemy_color)  # Check if king is attacked by enemy

    # Get all valid moves of selected piece of current player
    valid_moves, position = valid_piece_move(position, x, y, color)

    # Remove moves that lead to player getting into check
    # for pieces in attacked_squares:
    #     if pieces in valid_moves or pieces == (x, y):
    #         inCheck = True

    if (x2, y2) in valid_moves and not inCheck:
        board = position.get_board()
        castle_right = position.get_castle_rights()

        # Check additional move options
        if board[y][x][0] == 'P':
            position = en_passant_rights(position, x2, y2)
            position.set_HMC(0)  # Reset 50 move rule
            if is_promotion(position, y2):
                board[y][x] = 'Q' + 'wb'[player]  # Automatic promotion to queen
                position.set_board(board)
        elif board[y][x][0] == 'K':
            position = castle_rights(position, x2, y2)
        elif board[y][x][0] == 'R':
            if x == 0 and (y == 0 or y == 7) and castle_right[player][0]:
                castle_right[player][0] = False
            elif x == 7 and (y == 0 or y == 7) and castle_right[player][1]:
                castle_right[player][1] = False
            position.set_castle_rights(castle_right)
        elif is_captured(board, x2, y2):
            position.set_HMC(0)  # Reset 50 move rule
        else:
            HMC += 1
            position.set_HMC(HMC)

        # Make the move
        board = position.get_board()
        board[y2][x2] = board[y][x]
        board[y][x] = 0

        # Check if the move caused checkmate or stalemate
        player_moves = all_possible_moves(position, enemy_color)
        print(player_moves)
        # position = is_checkmate(position, enemy_color)
        # position = is_stalemate(position, enemy_color)

        # Update position
        position.set_history(position)
        player = 1 - player
        position.set_board(board)
        position.set_player(player)
        position.set_previous_move([(x, y), (x2, y2)])
        position.set_EPT(-1)
        position.set_castle_rights(castle_right)

        # Check if 3-move repetition is of power
        for value in position.history.values():
            if value == 3:
                position.set_play(False)

    else:
        print("Not a valid move, try again!")
    return position
