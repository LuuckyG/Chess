import os
import pygame

from board import GamePosition
from utils.game_state import chess_coord_to_pixels, pixel_coord_to_chess, get_piece, \
    draw_board, create_pieces, make_move, is_occupied_by

# Make the GUI
pygame.init()

# Load the screen with any arbitrary size for now
temp_screen = pygame.display.set_mode((600, 600))

# Initialize the board:
board = [['Rb', 'Nb', 'Bb', 'Qb', 'Kb', 'Bb', 'Nb', 'Rb'],  # 8
         ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'],  # 7
         [0, 0, 0, 0, 0, 0, 0, 0],                          # 6
         [0, 0, 0, 0, 0, 0, 0, 0],                          # 5
         [0, 0, 0, 0, 0, 0, 0, 0],                          # 4
         [0, 0, 0, 0, 0, 0, 0, 0],                          # 3
         ['Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw'],  # 2
         ['Rw', 'Nw', 'Bw', 'Qw', 'Kw', 'Bw', 'Nw', 'Rw']]  # 1

player = 0  # 0 is white, 1 is black

# Castling rights (King side, Queen side)
castling_rights = [[True, True], [True, True]]

# This variable will store a coordinate if there is a square that can be
# en passant captured on. Otherwise it stores -1, indicating lack of en passant targets
En_Passant_Target = -1

# This variable stores the number of reversible moves that have been played so far.
half_move_clock = 0

# Generate an instance of GamePosition class to store the above data:
position = GamePosition(board, player, castling_rights, En_Passant_Target, half_move_clock)

# Load all the Media
background = pygame.image.load(os.path.join('Media', 'board.png')).convert()
pieces_image = pygame.image.load(os.path.join('Media', 'Chess_Pieces_Sprite.png')).convert_alpha()
circle_image_green = pygame.image.load(os.path.join('Media', 'green_circle_small.png')).convert_alpha()
circle_image_capture = pygame.image.load(os.path.join('Media', 'green_circle_neg.png')).convert_alpha()
circle_image_red = pygame.image.load(os.path.join('Media', 'red_circle_big.png')).convert_alpha()
greenbox_image = pygame.image.load(os.path.join('Media', 'green_box.png')).convert_alpha()
circle_image_yellow = pygame.image.load(os.path.join('Media', 'yellow_circle_big.png')).convert_alpha()
circle_image_green_big = pygame.image.load(os.path.join('Media', 'green_circle_big.png')).convert_alpha()
yellowbox_image = pygame.image.load(os.path.join('Media', 'yellow_box.png')).convert_alpha()

# Getting sizes
size_of_bg = background.get_rect().size

# Get size of the individual squares
square_width = size_of_bg[0] // 8
square_height = size_of_bg[1] // 8

# Rescale the Media so that each piece can fit in a square:
pieces_image = pygame.transform.scale(pieces_image, (square_width * 6, square_height * 2))
circle_image_green = pygame.transform.scale(circle_image_green, (square_width, square_height))
circle_image_capture = pygame.transform.scale(circle_image_capture, (square_width, square_height))
circle_image_red = pygame.transform.scale(circle_image_red, (square_width, square_height))
greenbox_image = pygame.transform.scale(greenbox_image, (square_width, square_height))
yellowbox_image = pygame.transform.scale(yellowbox_image, (square_width, square_height))
circle_image_yellow = pygame.transform.scale(circle_image_yellow, (square_width, square_height))
circle_image_green_big = pygame.transform.scale(circle_image_green_big, (square_width, square_height))

# Make a window of the same size as the background, set its title, and
# load the background image onto it (the board):
screen = pygame.display.set_mode(size_of_bg)
pygame.display.set_caption('Chess')
screen.blit(background, (0, 0))
board = position.get_board()
player = position.get_player()

# Create images of separate pieces
w_pieces, b_pieces = create_pieces(position, square_width, square_height)
AllPieces = w_pieces, b_pieces

# Game variables
isDown = False
isClicked = False
isTransition = False
previous_move = [-1, -1, -1, -1]

# Main loop
font = pygame.font.SysFont("comicsans", 30, True)
play = True
clock = pygame.time.Clock()
draw_board(screen, background, position, pieces_image, square_width, square_height)
dragPiece = None

while play:
    clock.tick(60)  # 60 fps

    # Update board position
    player = position.get_player()
    board = position.get_board()

    # Get user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
            break
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            play = False
            break
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            play = False
            break

        if not isDown and event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            chess_coord = pixel_coord_to_chess(pos, square_width, square_height)
            x = chess_coord[0]
            y = chess_coord[1]

            if not is_occupied_by(board, x, y, 'wb'[player]):
                isDown = False
                continue

            dragPiece = get_piece(AllPieces, chess_coord)

            # print(dragPiece.get_info())
            chess_coord, color, subsection, pos = dragPiece.get_info()
            pixel_coord = chess_coord_to_pixels(chess_coord, square_width, square_height)
            isDown = True  # A piece is being dragged

        # If a piece is being dragged let the dragging piece follow the mouse:
        if isDown:
            m, k = pygame.mouse.get_pos()
            dragPiece.set_pos((m - square_width / 2, k - square_height / 2))
            chess_coord, color, subsection, pos = dragPiece.get_info()

            # Update board, except for moving piece
            draw_board(screen, background, position, pieces_image,
                       square_width, square_height, drag_coord=chess_coord)

            # Blit dragged piece on mouse position
            screen.blit(pieces_image, pos, subsection)

        # If the dragged piece is released, check the move and if valid, make the move.
        if (isDown or isClicked) and event.type == pygame.MOUSEBUTTONUP:
            isDown = False  # Mouse is released
            dragPiece.set_pos((-1, -1))  # Set back to coordinate position

            pos = pygame.mouse.get_pos()
            chess_coord = pixel_coord_to_chess(pos, square_width, square_height)
            x2 = chess_coord[0]
            y2 = chess_coord[1]

            isTransition = False
            if (x, y) == (x2, y2):
                # Check if piece was just clicked
                print("Same position! No move made!")
                continue
            else:
                isTransition = True

            position = make_move(position, x, y, x2, y2)
            previous_move = [x, y, x2, y2]
            dragPiece.set_coord((x2, y2))  # Update position of selected piece

            if not isTransition:
                w_pieces, b_pieces = create_pieces(position, square_width, square_height)
            else:
                movingPiece = dragPiece
                # print("First move:", movingPiece.get_info())
                origin = chess_coord_to_pixels((x, y), square_width, square_height)
                destiny = chess_coord_to_pixels((x2, y2), square_width, square_height)
                movingPiece.set_pos(origin)
                step = (destiny[0] - origin[0], destiny[1] - origin[1])

            # Update board, with move
            draw_board(screen, background, position, pieces_image,
                       square_width, square_height)

        # Visualize the valid move with transition
        if isTransition:
            p, q = movingPiece.get_pos()
            dx2, dy2 = destiny
            n = 30.0

            if abs(p - dx2) <= abs(step[0] / n) and abs(q - dy2) <= abs(step[1] / n):
                # The moving piece has reached its destination
                # Snap it back to its grid position
                movingPiece.set_pos((-1, -1))

                # Generate new piece list in case one got captured
                w_pieces, b_pieces = create_pieces(position, square_width, square_height)

                # No more transitioning
                isTransition = False

            else:
                # Move it closer to its destination.
                movingPiece.set_pos((p + step[0] / n, q + step[1] / n))
                chess_coord, color, subsection, pos = movingPiece.get_info()
                draw_board(screen, background, position, pieces_image,
                           square_width, square_height, drag_coord=chess_coord)
                screen.blit(pieces_image, pos, subsection)

    AllPieces = w_pieces + b_pieces

    # Update display
    pygame.display.update()

pygame.quit()
