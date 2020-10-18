import os 
import pygame

def setup_screen():
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

    return screen, position