import os 
import pygame


class GameView:

    BACKGROUND_IMG = pygame.image.load(os.path.join('media', 'board.png'))

    def __init__(self):
        """Make a window of the same size as the background, set its title, and
        load the background image onto it (the board)"""

        # Background
        self.size_of_bg = self.BACKGROUND_IMG.get_rect().size
        self.screen = pygame.display.set_mode(self.size_of_bg)
        self.background = self.BACKGROUND_IMG.convert()
        self.screen.blit(self.background, (0, 0))

        self.square_width = self.size_of_bg[0] // 8
        self.square_height = self.size_of_bg[1] // 8

        pygame.display.set_caption('Chess')

        # Pieces
        self.pieces_image = pygame.image.load(os.path.join('media', 'Chess_Pieces_Sprite.png')).convert_alpha()
        self.pieces_image = pygame.transform.scale(self.pieces_image, (self.square_width * 6, self.square_height * 2))
        self.images = self.get_orig_images()
      
    def get_orig_images(self):
        """Load all the media into one dictionary"""
        circle_image_green = pygame.image.load(os.path.join('media', 'green_circle_small.png')).convert_alpha()
        circle_image_capture = pygame.image.load(os.path.join('media', 'green_circle_neg.png')).convert_alpha()
        circle_image_red = pygame.image.load(os.path.join('media', 'red_circle_big.png')).convert_alpha()
        green_box_image = pygame.image.load(os.path.join('media', 'green_box.png')).convert_alpha()
        circle_image_yellow = pygame.image.load(os.path.join('media', 'yellow_circle_big.png')).convert_alpha()
        circle_image_green_big = pygame.image.load(os.path.join('media', 'green_circle_big.png')).convert_alpha()
        yellow_box_image = pygame.image.load(os.path.join('media', 'yellow_box.png')).convert_alpha()

        images = {
            'circle_image_green': circle_image_green,
            'circle_image_capture': circle_image_capture,
            'circle_image_red': circle_image_red,
            'green_box': green_box_image,
            'circle_image_yellow': circle_image_yellow,
            'circle_image_green_big': circle_image_green_big,
            'yellow_box': yellow_box_image
            }

        images = self.rescale_images(**images)
        return images
        
    def rescale_images(self, **kwargs):
        """Rescale the Media so that each piece can fit in a square"""
        rescaled_images = {}
        for key, image in kwargs.items():
            image = pygame.transform.scale(image, (self.square_height, self.square_width))
            rescaled_images[key] = image
        return rescaled_images
    
    def draw_board(self, right_clicked=[], is_clicked=False, drag_coord=None):
        """Update chess board. Don't update moving piece, indicated by drag_coord"""
        previous_move = self.position.get_previous_move()
        self.screen.blit(self.all_images.background, (0, 0))

        # Show square
        mouse_pos = pygame.mouse.get_pos()
        mouse_chess_coord = pixel_coord_to_chess(mouse_pos, self.square_width, self.square_height)
        pygame.draw.rect(self.screen, (225, 0, 0, 50),
                        (mouse_chess_coord[0] * self.square_width, mouse_chess_coord[1] * self.square_height,
                        self.square_width, self.square_height), 2)

        if previous_move != [(-1, -1), (-1, -1)]:
            for chess_pos in previous_move:
                pos = chess_coord_to_pixels(chess_pos, self.square_width, self.square_height)
                self.screen.blit(self.images['yellow_box'], pos)

        if right_clicked:
            for pos in right_clicked:
                pygame.draw.rect(self.screen, (225, 0, 0, 50),
                                (pos[0] * self.square_width, pos[1] * self.square_height,
                                self.square_width, self.square_height))
        elif is_clicked:
            pass

        # Blit over other pieces
        order = [self.position.pieces["white"], self.position.pieces["black"]] if self.position.get_player() == 1 \
            else [self.position.pieces["black"], self.position.pieces["white"]]

        for piece_color in order:
            for piece in piece_color:
                pixel_coord = chess_coord_to_pixels(piece.chess_coord, self.square_width, self.square_height)
                
                # Don't blit moving piece
                if piece.chess_coord != drag_coord:  
                    if piece.pos == (-1, -1):
                        # Default square
                        self.screen.blit(self.all_images.pieces_image, pixel_coord, piece.subsection)
                    else:
                        # Specific pixels:
                        self.screen.blit(self.all_images.pieces_image, pos, piece.subsection)
