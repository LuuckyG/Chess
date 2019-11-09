"""
Helper functions to run the game.
This includes initializing and updating the chess board, loading additional images and rescaling them, and calculating
chess coordinates from pixel coordinates and the reverse.
"""

import os
import pygame
from pieces import Piece
from board import GamePosition


def initialize_board():
    """Initialize the board with starting position"""
    board = [['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb'],  # 8
             ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'],  # 7
             [0, 0, 0, 0, 0, 0, 0, 0],  # 6
             [0, 0, 0, 0, 0, 0, 0, 0],  # 5
             [0, 0, 0, 0, 0, 0, 0, 0],  # 4
             [0, 0, 0, 0, 0, 0, 0, 0],  # 3
             ['Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw'],  # 2
             ['Rw', 'Nw', 'Bw', 'Qw', 'Kw', 'Bw', 'Nw', 'Rw']]  # 1

    player = 0  # 0 is white, 1 is black

    # Castling rights (King side, Queen side)
    castling_rights = [[True, True], [True, True]]

    # This variable will store a coordinate if there is a square that can be
    # en passant captured on. Otherwise it stores -1, indicating lack of en passant targets
    en_passant_target = -1

    # This variable stores the number of reversible moves that have been played so far.
    half_move_clock = 0
    position = GamePosition(board, player, castling_rights, en_passant_target, half_move_clock)
    return position


def get_all_images():
    """Load all the media into one dictionary"""
    circle_image_green = pygame.image.load(os.path.join('Media', 'green_circle_small.png')).convert_alpha()
    circle_image_capture = pygame.image.load(os.path.join('Media', 'green_circle_neg.png')).convert_alpha()
    circle_image_red = pygame.image.load(os.path.join('Media', 'red_circle_big.png')).convert_alpha()
    green_box_image = pygame.image.load(os.path.join('Media', 'green_box.png')).convert_alpha()
    circle_image_yellow = pygame.image.load(os.path.join('Media', 'yellow_circle_big.png')).convert_alpha()
    circle_image_green_big = pygame.image.load(os.path.join('Media', 'green_circle_big.png')).convert_alpha()
    yellow_box_image = pygame.image.load(os.path.join('Media', 'yellow_box.png')).convert_alpha()

    images = {
        'circle_image_green': circle_image_green,
        'circle_image_capture': circle_image_capture,
        'circle_image_red': circle_image_red,
        'green_box': green_box_image,
        'circle_image_yellow': circle_image_yellow,
        'circle_image_green_big': circle_image_green_big,
        'yellow_box': yellow_box_image
        }
    return images


def rescale_all_images(square_h, square_w, **kwargs):
    """Rescale the Media so that each piece can fit in a square"""
    rescaled_images = {}
    for key, image in kwargs.items():
        image = pygame.transform.scale(image, (square_h, square_w))
        rescaled_images[key] = image
    return rescaled_images


def chess_coord_to_pixels(chess_coord, square_width, square_height):
    """Get pixel coordinates from chess board coordinates"""
    x, y = chess_coord
    return x * square_width, y * square_height


def pixel_coord_to_chess(pixel_coord, square_width, square_height):
    """Get board coordinates from pixel board coordinates"""
    x, y = pixel_coord
    return x // square_width, y // square_height


def create_pieces(position, square_width, square_height):
    """Create piece objects based on board position"""
    board = position.get_board()

    white_pieces, black_pieces = [], []
    for x in range(8):
        for y in range(8):
            if board[x][y] != 0:
                p = Piece(board[x][y], board[x][y][1], (y, x), square_width, square_height)
                if board[x][y][1] == 'w':
                    white_pieces.append(p)
                else:
                    black_pieces.append(p)
    return white_pieces, black_pieces


def get_piece(position, square_width, square_height, mouse_coord):
    """Get piece selected by mouse click"""
    white_pieces, black_pieces = create_pieces(position, square_width, square_height)
    pieces = white_pieces + black_pieces

    for piece in pieces:
        if piece.chess_coord == mouse_coord:
            return piece


def draw_board(screen, background, position, pieces_image, square_width, square_height, images,
               right_clicked=[], is_clicked=False, drag_coord=None):
    """Update chess board. Don't update moving piece, indicated by drag_coord"""
    previous_move = position.get_previous_move()
    screen.blit(background, (0, 0))
    player = position.get_player()
    w_pieces, b_pieces = create_pieces(position, square_width, square_height)

    # Show square
    mouse_pos = pygame.mouse.get_pos()
    mouse_chess_coord = pixel_coord_to_chess(mouse_pos, square_width, square_height)
    pygame.draw.rect(screen, (225, 0, 0, 50),
                     (mouse_chess_coord[0] * square_width, mouse_chess_coord[1] * square_height,
                      square_width, square_height), 2)

    if previous_move != [(-1, -1), (-1, -1)]:
        for chess_pos in previous_move:
            pos = chess_coord_to_pixels(chess_pos, square_width, square_height)
            screen.blit(images['yellow_box'], pos)

    if right_clicked:
        for pos in right_clicked:
            pygame.draw.rect(screen, (225, 0, 0, 50),
                             (pos[0] * square_width, pos[1] * square_height,
                              square_width, square_height))
    elif is_clicked:
        pass

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
