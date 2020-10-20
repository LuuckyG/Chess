import os 
import pygame


class Images:

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
