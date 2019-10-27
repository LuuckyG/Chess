"""
Helper functions to run the game.
This includes checking for checks, checkmate, stalemate, who's move it is, etc.
"""
from pieces import Piece


def chess_coord_to_pixels(chess_coord, square_width, square_height):
    x, y = chess_coord
    return x * square_width, y * square_height


def pixel_coord_to_chess(pixel_coord, square_width, square_height):
    x, y = pixel_coord
    return x // square_width, y // square_height


def get_piece(pieces, mouse_coord):
    """Get piece selected by mouse click"""
    for piece in pieces:
        if piece.chess_coord == mouse_coord:
            return piece


def is_check(board, x, y, piece, color):
    pass


def is_checkmate(board, x, y, piece, color):
    pass


def is_stalemate(board, x, y, piece, color):
    pass


def is_promotion():
    pass


def en_passant_rights():
    pass


def castle_rights():
    pass


def valid_piece_move(board, x, y, x2, y2, piece):
    """Check if the piece makes legal move"""

    if piece == 'P':  # Pawn
        pass
    elif piece == 'R':  # Rook
        pass
    elif piece == 'N':  # Knight
        pass
    elif piece == 'B':  # Bishop
        pass
    elif piece == 'Q':  # Queen
        pass
    elif piece == 'K':  # King
        pass
    return True


def is_occupied_by(board, x, y, color):
    """Check if selected board tile has a piece of the player"""
    if 0 <= x < 8 and 0 <= y < 8:
        if board[y][x] != 0:
            if board[y][x][1] == color:  # Space occupied by own piece
                return True
    else:
        return False


def is_occupied(board, x, y, color):
    if 0 <= x < 8 and 0 <= y < 8:
        if board[y][x] == 0:
            return True
        else:
            if board[y][x][1] == color:  # Space occupied by own piece
                return False
            else:
                if board[y][x][0] == 'K':  # Cannot capture enemy King
                    return False
                else:
                    is_captured(board, x, y)  # Capture enemy piece at position (x, y)
                    return True
    else:
        return False


def is_captured(board, x, y):
    pass


def is_blocked():
    pass


def create_pieces(position, square_w, square_h):
    board = position.get_board()
    white_pieces, black_pieces = [], []
    for x in range(8):
        for y in range(8):
            if board[x][y] != 0:
                p = Piece(board[x][y], board[x][y][1], (y, x), square_w, square_h)
                if board[x][y][1] == 'w':
                    white_pieces.append(p)
                else:
                    black_pieces.append(p)
    return white_pieces, black_pieces


def make_move(position, x, y, x2, y2):
    """Check if move is valid, if so update position."""
    board = position.get_board()
    player = position.get_player()
    piece = board[y][x][0]
    color = board[y][x][1]

    if valid_piece_move(board, x, y, x2, y2, piece):
        # print(valid_piece_move(board, x, y, x2, y2, piece))
        # if not is_occupied(board, x2, y2, color):
        #     print(is_occupied(board, x2, y2, color))
        board[y2][x2] = board[y][x]
        board[y][x] = 0
        player = 1 - player
        position.set_board(board)
        position.set_player(player)
    return position


def draw_board(screen, background, position, pieces_image,
               square_width, square_height, drag_coord=None):

    screen.blit(background, (0, 0))
    player = position.get_player()
    w_pieces, b_pieces = create_pieces(position, square_width, square_height)

    # Blit over other pieces
    if player == 1:  # Player is black
        order = [w_pieces, b_pieces]
    else:
        order = [b_pieces, w_pieces]

    for piece in order[0]:
        chess_coord, color, subsection, pos = piece.get_info()
        pixel_coord = chess_coord_to_pixels(chess_coord, square_width, square_height)
        if chess_coord != drag_coord:  # Don't blit moving piece
            if pos == (-1, -1):
                # Default square
                screen.blit(pieces_image, pixel_coord, subsection)
            else:
                # Specific pixels:
                screen.blit(pieces_image, pos, subsection)

    for piece in order[1]:
        chess_coord, color, subsection, pos = piece.get_info()
        pixel_coord = chess_coord_to_pixels(chess_coord, square_width, square_height)
        if chess_coord != drag_coord:  # Don't blit moving piece
            if pos == (-1, -1):
                # Default square
                screen.blit(pieces_image, pixel_coord, subsection)
            else:
                # Specific pixels:
                screen.blit(pieces_image, pos, subsection)
