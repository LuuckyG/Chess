"""
Helper functions to run the game.
This includes initializing and updating the chess board, loading additional images and rescaling them, and calculating
chess coordinates from pixel coordinates and the reverse.
"""

import os
import pygame

from setup.images import Images
from setup.position import GamePosition
from pieces.pieces import Piece


class ChessBoard:

    def __init__(self):
        self.position = GamePosition()
        
        all_images = Images()
        self.images = all_images.images
        self.size_of_bg = all_images.size_of_bg
        self.square_width = all_images.square_width
        self.square_height = all_images.square_height
    
    def create_screen(self):
        """Make a window of the same size as the background, set its title, and
        load the background image onto it (the board)"""
        self.screen = pygame.display.set_mode(self.size_of_bg)
        pygame.display.set_caption('Chess')
        self.screen.blit(self.background, (0, 0))
        draw_board(self.screen, self.background, 
                self.position, self.pieces_image, 
                self.square_width, self.square_height, 
                self.images)
    

    def make_move(self):
        pass


    def draw_board(screen, background, position, pieces_image, square_width, square_height, images,
               right_clicked=[], is_clicked=False, drag_coord=None):
        """Update chess board. Don't update moving piece, indicated by drag_coord"""
        previous_move = position.get_previous_move()
        screen.blit(background, (0, 0))
        player = position.get_player()
        pieces = create_pieces(position, square_width, square_height)
        w_pieces, b_pieces = pieces["white"], pieces["black"]

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

        # pygame.draw.polygon(screen, (225, 0, 0),
        #                     ((0, 100), (0, 200), (200, 200), (200, 300),
        #                      (300, 150), (200, 0), (200, 100)))

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
    pieces = {
        "white": [],
        "black": []
    }

    for x in range(8):
        for y in range(8):
            if board[x][y] != 0:
                p = Piece(board[x][y], board[x][y][1], (y, x), square_width, square_height)
                if board[x][y][1] == 'w':
                    pieces["white"].append(p)
                else:
                    pieces["black"].append(p)
    return pieces


def get_piece(position, square_width, square_height, mouse_coord):
    """Get piece selected by mouse click"""
    pieces = create_pieces(position, square_width, square_height)
    white_pieces, black_pieces = pieces["white"], pieces["black"]
    pieces = white_pieces + black_pieces

    for piece in pieces:
        if piece.chess_coord == mouse_coord:
            return piece



