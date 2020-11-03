import os 
import pygame

from view.button import Button


class GameView:

    BACKGROUND_IMG = pygame.image.load(os.path.join('media', 'board.png'))
    PIECES_IMG = pygame.image.load(os.path.join('media', 'pieces.png'))

    WHITE = (255, 255, 255)
    YELLOW = (255, 233, 33)
    ORANGE = (255,237,194)
    RED = (255, 82, 82)
    BLUE = (69, 125, 255)
    BLACK = (0, 0, 0)
    LIGHT_GRAY = (225, 225, 225)
    GREEN = (71, 255, 78)

    def __init__(self, screen_size=640, border=20, line_width=5):
        """Make a window of the same size as the background, set its title, and
        load the background image onto it (the board)
        
        Args:
        - screen_size: width of the screen (in px)
        - border: border around game
        - line_width: thickness of lines, for drawing the board and the symbols
        """

        # Initialise pygame
        pygame.init()
        pygame.time.Clock().tick(60)
        pygame.display.set_caption('Chess')

        self.border = border
        self.line_width = line_width
        self.all_buttons = []

        # Setup screen
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode((self.screen_size + 100, self.screen_size))

        self.font = pygame.font.SysFont(None, 30)
        self.big_font = pygame.font.SysFont(None, 40)
        self.small_font = pygame.font.SysFont(None, 20)

        # Display starting position
        self.draw_start_position()


    def draw_screens(self, status):
        """Method to control what screen is draw when tracking mouse movement.
        Default mode is drawing the starting screen."""

        if status == 'start_screen':
            self.draw_start_screen()
        elif status == 'settings':
            self.draw_settings_screen()
        elif status == 'replay':
            self.draw_play_again_screen()
        elif status == 'end_game':
            self.draw_thanks()


    def follow_mouse(self, x, y):
        """Track mouse movement and if hovered over a button or board tile, change the color
        of the button (or tile) to indicate focus."""
        pass

    def draw_start_position(self):
        """Draw board and start position of pieces"""
        
        # Draw board (background)
        self.background = self.BACKGROUND_IMG.convert()
        self.size_of_bg = self.background.get_rect().size

        self.square_width = self.size_of_bg[0] // 8
        self.square_height = self.size_of_bg[1] // 8

        self.screen.blit(self.background, (0, 0))

        # Pieces
        self.pieces_image = self.PIECES_IMG.convert_alpha()
        self.pieces_image = pygame.transform.scale(self.pieces_image, (self.square_width * 6, self.square_height * 2))
        self.images = self.get_orig_images()

    def draw_board(self):
        pass

    
    def draw_move(self, right_clicked=[], is_clicked=False, drag_coord=None):
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
    

    def draw_captured_pieces(self, board):
        pass

    def draw_start_screen(self):
        """Start screen"""
        self.screen.fill(self.WHITE)
        # self.screen.blit(self.start_screen_image, (0, 0))

        self.settings_button.draw(self.screen, self.small_font, thickness=1)
        self.start_game_button.draw(self.screen, self.big_font)
        self.quit_game_button.draw(self.screen, self.small_font, thickness=1)

   
    def draw_settings_screen(self):
        """Settings screen"""
        self.screen.fill(self.LIGHT_GRAY)

        # Title
        title_text = self.big_font.render('Settings', True, self.BLACK, self.LIGHT_GRAY)
        title_text_box = title_text.get_rect()
        title_text_box.center = (self.screen_size / 2, 0.3 * self.screen_size)
        
        # Show settings
        # Human vs. Human or Human vs. AI
        game_type_text = self.font.render('Game Type', True, self.BLACK, self.LIGHT_GRAY)
        game_type_text_box = game_type_text.get_rect()
        game_type_text_box.center = (0.2 * self.screen_size, 0.5 * self.screen_size)

        self.human_vs_human_button.draw(self.screen, self.small_font)
        self.human_vs_ai_button.draw(self.screen, self.small_font)

        # AI level
        ai_level_text = self.font.render('AI Strength', True, self.BLACK, self.LIGHT_GRAY)
        ai_level_text_box = ai_level_text.get_rect()
        ai_level_text_box.center = (0.2 * self.screen_size, 0.6 * self.screen_size)

        self.ai_level_1_button.draw(self.screen, self.small_font)
        self.ai_level_2_button.draw(self.screen, self.small_font)
        self.ai_level_3_button.draw(self.screen, self.small_font)

        # Go back button
        self.back_button.draw(self.screen, self.small_font)

        # Blit everything to screen
        self.screen.blit(title_text, title_text_box)
        self.screen.blit(game_type_text, game_type_text_box)
        self.screen.blit(ai_level_text, ai_level_text_box)


    def draw_play_again_screen(self):
        """Show message if player wants to play another game"""
        border = 2
        self.screen.fill(self.BLACK, (0.20 * self.screen_size - border, 0.40 * self.screen_size - border, 
                                       0.60 * self.screen_size + 2 * border, 0.20 * self.screen_size + 2 * border))
        self.screen.fill(self.ORANGE, (0.20 * self.screen_size, 0.40 * self.screen_size, 
                                       0.60 * self.screen_size, 0.20 * self.screen_size))

        text = self.big_font.render('Play Again?', True, self.BLACK, self.ORANGE)
        text_box = text.get_rect()
        text_box.center = (0.5 * self.screen_size, 0.45 * self.screen_size)
        self.screen.blit(text, text_box)

        self.play_again_button.draw(self.screen, self.font)
        self.nomore_game_button.draw(self.screen, self.font)


    def draw_thanks(self):
        """Show 'thank you' message before closing application."""
        self.screen.fill(self.WHITE)
        # self.screen.blit(self.start_screen_image, (0, 0))
        self.show_message('Thanks for Playing!', self.big_font, text_color=self.BLACK, background=self.WHITE)
        pygame.time.delay(500)


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
        """Rescale the media so that each piece can fit in a square"""
        rescaled_images = {}
        for key, image in kwargs.items():
            image = pygame.transform.scale(image, (self.square_height, self.square_width))
            rescaled_images[key] = image
        return rescaled_images
    
    def update_button_look(self, button, status, color, text_color):
        """Method to change look of buttons, based on the fact if they are
        selected or not."""
        
        button.selected = status
        button.color = color
        button.text_color = text_color


    def create_buttons(self):
        """Function to create the buttons needed to navigate throught the game"""

        #### Start Screen ####
        self.settings_button = Button(color=self.LIGHT_GRAY, 
                                      x=0.05 * self.screen_size, 
                                      y=self.screen_size + 30, 
                                      width=0.2 * self.screen_size, 
                                      height=40, 
                                      value='settings', 
                                      group='start_screen', 
                                      selected=False, 
                                      text_color=self.BLACK, 
                                      text='Settings')

        self.start_game_button = Button(color=self.GREEN, 
                                        x=0.30 * self.screen_size, 
                                        y=self.screen_size + 15, 
                                        width=0.4 * self.screen_size, 
                                        height=70, 
                                        value='start', 
                                        group='start_screen', 
                                        selected=True, 
                                        text_color=self.WHITE, 
                                        text='PLAY!')

        self.quit_game_button = Button(color=self.LIGHT_GRAY, 
                                       x=0.75 * self.screen_size, 
                                       y=self.screen_size + 30, 
                                       width=0.2 * self.screen_size, 
                                       height=40, 
                                       value='quit',
                                       group='start_screen', 
                                       selected=False, 
                                       text_color=self.BLACK, 
                                       text='Quit')

        # ---------------------------------------------------------------------------------- #
        #### Settings Screen ####

        # Create two buttons, one voor human vs. human and one for human vs. AI
        self.human_vs_human_button = Button(color=self.GREEN, 
                                            x=0.5 * self.screen_size, 
                                            y=0.5 * self.screen_size - 15, 
                                            width=0.2 * self.screen_size, 
                                            height=30, 
                                            value=False,
                                            group='vs_computer', 
                                            selected=True, 
                                            text_color=self.WHITE, 
                                            text='Human vs. Human')

        self.human_vs_ai_button = Button(color=self.LIGHT_GRAY, 
                                         x=0.75 * self.screen_size, 
                                         y=0.5 * self.screen_size - 15, 
                                         width=0.2 * self.screen_size, 
                                         height=30,
                                         value=True,
                                         group='vs_computer', 
                                         selected=False, 
                                         text_color=self.BLACK, 
                                         text='Human vs. AI')

        # Create buttons to select the size of the play board
        self.ai_level_1_button = Button(color=self.GREEN, 
                                          x=0.5 * self.screen_size, 
                                          y=0.6 * self.screen_size - 15, 
                                          width=0.1 * self.screen_size, 
                                          height=30, 
                                          value=1,
                                          group='ai_level', 
                                          selected=True, 
                                          text_color=self.WHITE, 
                                          text='1')

        self.ai_level_2_button = Button(color=self.LIGHT_GRAY, 
                                          x=0.65 * self.screen_size, 
                                          y=0.6 * self.screen_size - 15, 
                                          width=0.1 * self.screen_size, 
                                          height=30, 
                                          value=2,
                                          group='ai_level', 
                                          selected=False, 
                                          text_color=self.BLACK, 
                                          text='2')
                                          
        self.ai_level_3_button = Button(color=self.LIGHT_GRAY, 
                                          x=0.8 * self.screen_size, 
                                          y=0.6 * self.screen_size - 15, 
                                          width=0.1 * self.screen_size, 
                                          height=30, 
                                          value=3,
                                          group='ai_level', 
                                          selected=False, 
                                          text_color=self.BLACK, 
                                          text='3')
        
        # Go back button
        self.back_button = Button(color=self.LIGHT_GRAY, 
                                  x=0.1 * self.screen_size, 
                                  y=self.screen_size, 
                                  width=0.1 * self.screen_size, 
                                  height=30, 
                                  value='cancel', 
                                  group='cancel', 
                                  selected=False, 
                                  text_color=self.BLACK, 
                                  text='Back')
        
        # ---------------------------------------------------------------------------------- #

        #### End Screen ####
        self.play_again_button = Button(color=self.GREEN, 
                                        x=0.25 * self.screen_size, 
                                        y=0.50 * self.screen_size + 5, 
                                        width=0.2 * self.screen_size, 
                                        height=40, 
                                        value=True,
                                        group='end_screen', 
                                        selected=True, 
                                        text_color=self.WHITE, 
                                        text='Yes!!')

        self.nomore_game_button = Button(color=self.RED, 
                                         x=0.55 * self.screen_size, 
                                         y=0.50 * self.screen_size + 5, 
                                         width=0.2 * self.screen_size, 
                                         height=40, 
                                         value=False,
                                         group='end_screen', 
                                         selected=False, 
                                         text_color=self.BLACK, 
                                         text='No')
        
        # Collect all buttons
        self.all_buttons.extend((self.settings_button, self.start_game_button, self.quit_game_button,
                                 self.human_vs_human_button, self.human_vs_ai_button,
                                 self.ai_level_1_button, self.ai_level_2_button, self.ai_level_3_button,
                                 self.back_button,
                                 self.play_again_button, self.nomore_game_button))
    

