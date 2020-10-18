import os
import pygame

from utils.game_state import initialize_board, get_all_images, rescale_all_images, chess_coord_to_pixels, \
    pixel_coord_to_chess, get_piece, draw_board, create_pieces
from rules import is_occupied, is_occupied_by, make_move

# Make the GUI
pygame.init()

# Load the screen with any arbitrary size for now
temp_screen = pygame.display.set_mode((600, 600))

# Starting position
position = initialize_board()

# Load all the Media
background = pygame.image.load(os.path.join('Media', 'board.png')).convert()
pieces_image = pygame.image.load(os.path.join('Media', 'Chess_Pieces_Sprite.png')).convert_alpha()
images = get_all_images()

# Getting sizes
size_of_bg = background.get_rect().size
square_width = size_of_bg[0] // 8
square_height = size_of_bg[1] // 8

# Rescale the Media so that each piece can fit in a square:
pieces_image = pygame.transform.scale(pieces_image, (square_width * 6, square_height * 2))
images = rescale_all_images(square_height, square_width, **images)

# Make a window of the same size as the background, set its title, and
# load the background image onto it (the board):
screen = pygame.display.set_mode(size_of_bg)
pygame.display.set_caption('Chess')
screen.blit(background, (0, 0))
draw_board(screen, background, position, pieces_image, square_width, square_height, images)


def main():
    global screen, background, position, pieces_image, square_width, square_height, images

    # Game variables
    isDown = False
    isClicked = False
    isTransition = False
    isRightClicked = []
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comicsans", 30, True)

    while position.get_play():
        clock.tick(60)  # 60 fps

        # Update board position
        player = position.get_player()
        board = position.get_board()

        # Get user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                position.set_play(False)
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                position.set_play(False)
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                position.set_play(False)
                break

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right mouse
                pos = pygame.mouse.get_pos()
                chess_coord = pixel_coord_to_chess(pos, square_width, square_height)
                right_x = chess_coord[0]
                right_y = chess_coord[1]

                isClicked = True
                if (right_x, right_y) not in isRightClicked:
                    isRightClicked.append((right_x, right_y))
                else:
                    index = isRightClicked.index((right_x, right_y))
                    isRightClicked.pop(index)

            if (isDown or isClicked) and event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                pos = pygame.mouse.get_pos()
                chess_coord = pixel_coord_to_chess(pos, square_width, square_height)
                right_x2 = chess_coord[0]
                right_y2 = chess_coord[1]

                if (right_x, right_y) != (right_x2, right_y2):

                    begin_x = right_x * square_width - square_width / 2
                    begin_y = right_y * square_height - square_height / 2

                    end_x = right_x2 * square_width - square_width / 2
                    end_y = right_y2 * square_height - square_height / 2

                    # Arrow tips
                    left_tip = (end_x - square_width / 2, end_y)
                    right_tip = (end_x + square_width / 2, end_y)

                    arrow = ((begin_x, begin_y), (end_x, end_y), left_tip, (end_x, end_y), right_tip)

                isClicked = False

            if not isDown and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                isRightClicked = []
                pos = pygame.mouse.get_pos()
                chess_coord = pixel_coord_to_chess(pos, square_width, square_height)
                x = chess_coord[0]
                y = chess_coord[1]

                if not is_occupied_by(board, x, y, 'wb'[player]):
                    isDown = False
                    continue

                dragPiece = get_piece(position, square_width, square_height, chess_coord)
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
                           square_width, square_height, images, drag_coord=chess_coord)

                # Blit dragged piece on mouse position
                screen.blit(pieces_image, pos, subsection)

            # If the dragged piece is released, check the move and if valid, make the move.
            if (isDown or isClicked) and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                isDown = False  # Mouse is released
                dragPiece.set_pos((-1, -1))  # Set back to coordinate position

                pos = pygame.mouse.get_pos()
                chess_coord = pixel_coord_to_chess(pos, square_width, square_height)
                x2 = chess_coord[0]
                y2 = chess_coord[1]

                isTransition = False
                if (x, y) == (x2, y2):
                    # Check if piece was just clicked
                    draw_board(screen, background, position, pieces_image,
                               square_width, square_height, images, is_clicked=isClicked)
                    print("Same position! No move made!")
                    continue
                else:
                    position = make_move(position, x, y, x2, y2)
                    previous_move = position.get_previous_move()
                    if previous_move[-1] == (x2, y2):
                        isTransition = True
                        dragPiece.set_coord((x2, y2))  # Update position of selected piece

                if not isTransition:
                    pieces = create_pieces(position, square_width, square_height)
                    w_pieces, b_pieces = pieces["white"], pieces["black"]
                else:
                    movingPiece = dragPiece
                    origin = chess_coord_to_pixels((x, y), square_width, square_height)
                    destiny = chess_coord_to_pixels((x2, y2), square_width, square_height)
                    movingPiece.set_pos(origin)
                    step = (destiny[0] - origin[0], destiny[1] - origin[1])

                # Update board, with move
                draw_board(screen, background, position, pieces_image, square_width, square_height, images)

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
                    pieces = create_pieces(position, square_width, square_height)
                    w_pieces, b_pieces = pieces["white"], pieces["black"]

                    # No more transitioning
                    isTransition = False

                else:
                    # Move it closer to its destination.
                    movingPiece.set_pos((p + step[0] / n, q + step[1] / n))
                    chess_coord, color, subsection, pos = movingPiece.get_info()
                    draw_board(screen, background, position, pieces_image,
                               square_width, square_height, images, drag_coord=chess_coord)
                    screen.blit(pieces_image, pos, subsection)

        if not isDown and not isClicked and not isTransition:
            # Update board after each turn, when transition is done
            draw_board(screen, background, position, pieces_image,
                       square_width, square_height, images,
                       right_clicked=isRightClicked, is_clicked=isClicked)

        # Update display and show last move
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
