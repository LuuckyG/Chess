import os 
import pygame
from pygame.transform import scale2x

from view.button import Button
from model.pieces import Empty, King
from model.utils import opposite, chess_coord_to_pixels, pixel_coord_to_chess, position_to_key


class GameView:
    STARTSCREEN_IMG = pygame.image.load(os.path.join('view/media', 'startscreen.jpg')) 
    BACKGROUND_IMG =  pygame.image.load(os.path.join('view/media', 'board.png'))
    PIECES_IMG =      pygame.image.load(os.path.join('view/media', 'pieces.png'))

    WHITE = (255, 255, 255)
    YELLOW = (255, 233, 33)
    ORANGE = (255,237,194)
    RED = (255, 82, 82)
    RED_HIGHLIGHT = (225, 0, 0, 50)
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
        pygame.display.set_caption('Chess')
        self.clock = pygame.time.Clock()
        self.limit_fps = True
        self.fps_max = 40
        
        self.border = border
        self.line_width = line_width
        self.all_buttons = []

        # Setup screen
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode((self.screen_size + 360, self.screen_size))

        # Fonts
        self.font = pygame.font.SysFont(None, 30)
        self.big_font = pygame.font.SysFont(None, 50)
        self.small_font = pygame.font.SysFont(None, 20)

        # Startscreen image
        scale_factor = 1.3
        self.start_screen_image = self.STARTSCREEN_IMG.convert_alpha()  # Original size: 930 x 590 px
        self.size_of_ssi = self.start_screen_image.get_rect().size
        self.start_screen_image = pygame.transform.scale(self.start_screen_image, (round(self.size_of_ssi[0] / scale_factor), round(self.size_of_ssi[1] / scale_factor)))

        # Get image of board
        self.background = self.BACKGROUND_IMG.convert()
        self.size_of_bg = self.background.get_rect().size

        self.square_width = self.size_of_bg[0] // 8
        self.square_height = self.size_of_bg[1] // 8
        
        # Pieces
        self.pieces_image = self.PIECES_IMG.convert_alpha()
        self.pieces_image = pygame.transform.scale(self.pieces_image, (self.square_width * 6, self.square_height * 2))
        self.images = self.get_orig_images()

        # Buttons
        self.create_buttons()


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
        """Track mouse movement and if hovered over a button 
        tile, change the color of the button to indicate focus."""
        for button in self.all_buttons:
            if button.is_hover(x, y):
                button.color = self.YELLOW
            else:
                if button.selected:
                    button.color = self.GREEN
                else:
                    if button.group == 'start_screen':
                        if button.text == 'Quit': button.color = self.RED
                        else: button.color = self.LIGHT_GRAY
                    
                    elif button.group == 'game':
                        if button.text == 'Draw': button.color = self.BLACK
                        if button.text == 'Resign': button.color = self.RED
                    
                    else: button.color = self.LIGHT_GRAY
                    

    def draw_position(self, board, dragged_piece):
        self.screen.blit(self.background, (0, 0))
        self.draw_captured_pieces(board)
        self.draw_move_list(board)
        self.draw_highlighed_tiles(board)
        self.draw_arrows(board)
        if board.previous_move: self.draw_previous_move(board)
        self.draw_possible_moves(board)
        self.draw_all_pieces(board, dragged_piece)
        if dragged_piece: self.draw_dragged_piece(dragged_piece)
        

    def draw_highlighed_tiles(self, board):
        for x, y in board.highlighted_tiles:
            pygame.draw.rect(self.screen, self.RED_HIGHLIGHT, 
                            (x * self.square_width, y * self.square_height, self.square_width, self.square_height), 0)
    
    
    def draw_previous_move(self, board):
        (x1, y1), (x2, y2) = board.previous_move
        self.screen.blit(self.images['yellow_box'], (x1 * self.square_width, y1 * self.square_height))
        self.screen.blit(self.images['yellow_box'], (x2 * self.square_width, y2 * self.square_height))
            
    
    def draw_arrows(self, board):
        ##### FOR NOW: DRAW 2 TILES AT BEGIN AND END POSITION ######
        for arrow in board.arrow_coordinates:
            (x1, y1), (x2, y2) = arrow
            pygame.draw.rect(self.screen, self.GREEN, 
                            (x1 * self.square_width, y1 * self.square_height, self.square_width, self.square_height), 0)
            pygame.draw.rect(self.screen, self.GREEN, 
                            (x2 * self.square_width, y2 * self.square_height, self.square_width, self.square_height), 0)


    def draw_possible_moves(self, board):
        for _, (x2, y2) in board.moves:
            self.screen.blit(self.images['circle_image_green'], (x2 * self.square_width, y2 * self.square_height))
    
    
    def draw_all_pieces(self, board, dragged_piece):
        player = 0 # Show white under (make this flexible)
        for rows in board.position:
            for tile in rows:
                if not isinstance(tile.state, Empty):
                    piece = board.get_piece(tile)
                    if dragged_piece is not None: 
                        if piece.id != dragged_piece.id:
                            if isinstance(piece, King): 
                                if piece.in_check: self.screen.blit(self.images['circle_image_red'], (tile.x * self.square_width, 
                                                                                                      tile.y * self.square_height), piece.subsection)
                            self.screen.blit(self.pieces_image, (tile.x * self.square_width, tile.y * self.square_height), piece.subsection)
                    else: self.screen.blit(self.pieces_image, (tile.x * self.square_width, tile.y * self.square_height), piece.subsection)

    
    def draw_dragged_piece(self, dragged_piece):
        x, y = pygame.mouse.get_pos()
        self.screen.blit(self.pieces_image, (x - self.square_width / 2, y - self.square_height / 2), dragged_piece.subsection)


    def draw_captured_pieces(self, board):
        color = self.BLACK
        bkg = self.LIGHT_GRAY
        
        self.screen.fill(self.LIGHT_GRAY, (self.screen_size, 0, self.screen.get_width() - self.screen_size, self.screen_size))
        
        black = self.small_font.render('Black', 1, color, bkg)
        white = self.small_font.render('White', 1, color, bkg)
        
        self.screen.blit(black, (self.screen_size + 10, 5))
        self.screen.blit(white, (self.screen_size + 10, 200))
        
        counter = {'w': {'P': 0, 'N': 0, 'B': 0, 'R': 0, 'Q': 0}, 
                   'b': {'P': 0, 'N': 0, 'B': 0, 'R': 0, 'Q': 0}}
        
        piece_valuation = {'w': 0, 'b': 0}

        for color, pieces in board.captured_pieces.items():
            for piece in pieces:
                if piece.symbol == 'K': continue
                
                x_multiplier = 1.2 if piece.symbol != 'P' else 1
                x_offset = 22 * x_multiplier * counter[piece.color][piece.symbol]
                y_offset = 210 if piece.color == 'w' else 10
                                
                if piece.symbol == 'P': piece_loc = [self.screen_size + 10, y_offset + 5]
                elif piece.symbol == 'N': piece_loc = [self.screen_size + 10, y_offset + 80]
                elif piece.symbol == 'B': piece_loc = [self.screen_size + 115, y_offset + 80]
                elif piece.symbol == 'R': piece_loc = [self.screen_size + 205, y_offset + 80]
                else: piece_loc = [self.screen_size + 225, y_offset + 5]
                
                counter[piece.color][piece.symbol] += 1
                piece_valuation[color] += piece.points
                
                self.screen.blit(self.pieces_image, (piece_loc[0] + x_offset, piece_loc[1]), piece.subsection)
        
        valuation = piece_valuation['w'] - piece_valuation['b']
        if valuation == 0: return
        elif valuation > 0: y = 5
        else: y = 200
        
        text = ': +' + str(abs(valuation))
        text = self.small_font.render(text, 1, (0, 0, 0))
        self.screen.blit(text, (self.screen_size + 50, y))
        

    def draw_move_list(self, board):
        """"""
        # Setup
        color = self.BLACK
        bkg = self.LIGHT_GRAY
        line_spacing = 2
        font = pygame.font.SysFont(None, 18)
        font_height = font.size("Tg")[1]
        
        # Title
        title = self.small_font.render('Moves', 1, color, bkg)
        self.screen.blit(title, (self.screen_size + 10, 400))

        # Get box where moves are blitted
        move_list = board.move_history
        move_rect = pygame.Rect((self.screen_size + 10, 420, 300, self.screen_size - 260))
        move_rect.inflate(-5, -5)
        
        y = move_rect.top
        text = ' '.join(move_list)
        
        # Check if moves need to be wrapped
        while move_list:
            i = 1
            
            if y + font_height > move_rect.bottom: break
            while font.size(text[:i])[0] < move_rect.width and i < len(text): i += 1
            
            if i < len(text): i = text.rfind(" ", 0, i) + 1
            
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
            
            self.screen.blit(image, (move_rect.left, y))
            
            y += font_height + line_spacing
            text = text[i:]
            
        # Draw `draw` and `resign` buttons
        self.draw_game_button.draw(self.screen, self.font)
        self.resign_game_button.draw(self.screen, self.font)
            

    def show_message(self, message, font, text_color=(255, 255, 255), background=(0, 0, 0)):
        """Show message with info to the user at the bottom of the window, below the play board"""       
        text = font.render(message, True, text_color, background)
        text_box = text.get_rect()
        text_box.center = (self.screen.get_width() / 2, 0.1 * self.screen_size)

        # Show message
        self.screen.blit(text, text_box)


    def draw_start_screen(self):
        """Start screen"""
        self.screen.fill(self.BLACK)
        
        # Centering image
        size = self.start_screen_image.get_rect().size       
        x_pos = (self.screen.get_width() - size[0]) // 2
        y_pos = (self.screen.get_height() - size[1]) // 2
        self.screen.blit(self.start_screen_image, (x_pos, y_pos))

        # Title
        text = self.big_font.render('Yellow Chess', True, self.YELLOW, self.BLACK)
        text_box = text.get_rect()
        text_box.center = (self.screen.get_width() / 2, 0.1 * self.screen_size)
        self.screen.blit(text, text_box)

        # Drawing buttons
        self.settings_button.draw(self.screen, self.small_font, thickness=1)
        self.start_game_button.draw(self.screen, self.big_font)
        self.quit_game_button.draw(self.screen, self.small_font, thickness=1)

   
    def draw_settings_screen(self):
        """Settings screen"""
        self.screen.fill(self.LIGHT_GRAY)
        
        width = self.screen.get_width()
        height = self.screen.get_height()

        # Title
        title_text = self.big_font.render('Settings', True, self.BLACK, self.LIGHT_GRAY)
        title_text_box = title_text.get_rect()
        title_text_box.center = (0.22 * width, 0.28 * height)
        
        # Show settings
        # Human vs. Human or Human vs. AI
        game_type_text = self.font.render('Game Type', True, self.BLACK, self.LIGHT_GRAY)
        game_type_text_box = game_type_text.get_rect()
        game_type_text_box.center = (0.2 * width, 0.4 * height)

        self.human_vs_human_button.draw(self.screen, self.small_font)
        self.human_vs_ai_button.draw(self.screen, self.small_font)

        # AI level
        ai_level_text = self.font.render('AI Strength', True, self.BLACK, self.LIGHT_GRAY)
        ai_level_text_box = ai_level_text.get_rect()
        ai_level_text_box.center = (0.2 * width, 0.5 * height)

        self.ai_level_1_button.draw(self.screen, self.small_font)
        self.ai_level_2_button.draw(self.screen, self.small_font)
        self.ai_level_3_button.draw(self.screen, self.small_font)
        
        # Flip board
        board_text = self.font.render('Flip Board?', True, self.BLACK, self.LIGHT_GRAY)
        board_text_box = board_text.get_rect()
        board_text_box.center = (0.2 * width, 0.6 * height)

        self.dont_flip_board_button.draw(self.screen, self.small_font)
        self.flip_board_button.draw(self.screen, self.small_font)

        # Go back button
        self.back_button.draw(self.screen, self.small_font)

        # Blit everything to screen
        self.screen.blit(title_text, title_text_box)
        self.screen.blit(game_type_text, game_type_text_box)
        self.screen.blit(ai_level_text, ai_level_text_box)
        self.screen.blit(board_text, board_text_box)


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
        self.screen.fill(self.BLACK)
        
        # Centering image
        size = self.start_screen_image.get_rect().size       
        x_pos = (self.screen.get_width() - size[0]) // 2
        y_pos = (self.screen.get_height() - size[1]) // 2
        self.screen.blit(self.start_screen_image, (x_pos, y_pos))
        
        self.show_message('Thanks for Playing!', self.big_font, text_color=self.YELLOW, background=self.BLACK)


    def get_orig_images(self):
        """Load all the media into one dictionary"""
        circle_image_green = pygame.image.load(os.path.join('view/media', 'green_circle_small.png')).convert_alpha()
        circle_image_capture = pygame.image.load(os.path.join('view/media', 'green_circle_neg.png')).convert_alpha()
        circle_image_red = pygame.image.load(os.path.join('view/media', 'red_circle_big.png')).convert_alpha()
        green_box_image = pygame.image.load(os.path.join('view/media', 'green_box.png')).convert_alpha()
        circle_image_yellow = pygame.image.load(os.path.join('view/media', 'yellow_circle_big.png')).convert_alpha()
        circle_image_green_big = pygame.image.load(os.path.join('view/media', 'green_circle_big.png')).convert_alpha()
        yellow_box_image = pygame.image.load(os.path.join('view/media', 'yellow_box.png')).convert_alpha()

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
    
    
    def create_buttons(self):
        """Function to create the buttons needed to navigate throught the game"""
        
        width = self.screen.get_width()
        height = self.screen.get_height()

        #### Start Screen ####
        self.settings_button = Button(color=self.LIGHT_GRAY, 
                                      x=0.10 * width, 
                                      y=height - 60, 
                                      width=0.2 * width, 
                                      height=40, 
                                      value='settings', 
                                      group='start_screen', 
                                      selected=False, 
                                      text_color=self.BLACK, 
                                      text='Settings')

        self.start_game_button = Button(color=self.GREEN, 
                                        x=0.35 * width, 
                                        y=height - 80, 
                                        width=0.3 * width, 
                                        height=70, 
                                        value='start', 
                                        group='start_screen', 
                                        selected=True, 
                                        text_color=self.WHITE, 
                                        text='PLAY!')

        self.quit_game_button = Button(color=self.LIGHT_GRAY, 
                                       x=0.70 * width, 
                                       y=height - 60, 
                                       width=0.2 * width, 
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
                                            x=0.4 * width, 
                                            y=0.4 * height - 15, 
                                            width=0.2 * width, 
                                            height=30, 
                                            value=False,
                                            group='vs_computer', 
                                            selected=True, 
                                            text_color=self.WHITE, 
                                            text='Human vs. Human')

        self.human_vs_ai_button = Button(color=self.LIGHT_GRAY, 
                                         x=0.65 * width, 
                                         y=0.4 * height - 15, 
                                         width=0.2 * width, 
                                         height=30,
                                         value=True,
                                         group='vs_computer', 
                                         selected=False, 
                                         text_color=self.BLACK, 
                                         text='Human vs. AI')
        
        # Create buttons to select the strength of the AI
        self.ai_level_1_button = Button(color=self.GREEN, 
                                        x=0.4 * width, 
                                        y=0.5 * height - 15, 
                                        width=0.1 * width, 
                                        height=30, 
                                        value=1,
                                        group='ai_level', 
                                        selected=True, 
                                        text_color=self.WHITE, 
                                        text='1')

        self.ai_level_2_button = Button(color=self.LIGHT_GRAY, 
                                        x=0.55 * width, 
                                        y=0.5 * height - 15, 
                                        width=0.1 * width, 
                                        height=30, 
                                        value=2,
                                        group='ai_level', 
                                        selected=False, 
                                        text_color=self.BLACK, 
                                        text='2')
                                          
        self.ai_level_3_button = Button(color=self.LIGHT_GRAY, 
                                        x=0.7 * width, 
                                        y=0.5 * height - 15, 
                                        width=0.1 * width, 
                                        height=30, 
                                        value=3,
                                        group='ai_level', 
                                        selected=False, 
                                        text_color=self.BLACK, 
                                        text='3')

        # Create buttons to select if one wants to flip the board after each turn
        self.dont_flip_board_button = Button(color=self.GREEN, 
                                             x=0.4 * width, 
                                             y=0.6 * height - 15, 
                                             width=0.2 * width, 
                                             height=30, 
                                             value=True,
                                             group='flip', 
                                             selected=True, 
                                             text_color=self.WHITE, 
                                             text='No Flip')

        self.flip_board_button = Button(color=self.LIGHT_GRAY, 
                                        x=0.65 * width, 
                                        y=0.6 * height - 15, 
                                        width=0.2 * width, 
                                        height=30,
                                        value=False,
                                        group='flip', 
                                        selected=False, 
                                        text_color=self.BLACK, 
                                        text='Flip')
        
        # Go back button
        self.back_button = Button(color=self.LIGHT_GRAY, 
                                  x=0.15 * width, 
                                  y=0.80 * height, 
                                  width=0.1 * width, 
                                  height=30, 
                                  value='cancel', 
                                  group='cancel', 
                                  selected=False, 
                                  text_color=self.BLACK, 
                                  text='Back')
        
        # ---------------------------------------------------------------------------------- #

        #### Game ####
        self.draw_game_button = Button(color=self.BLACK, 
                                       x=width - 340, 
                                       y=600, 
                                       width=150, 
                                       height=30, 
                                       value=False,
                                       group='game', 
                                       selected=False, 
                                       text_color=self.WHITE, 
                                       text='Draw')

        self.resign_game_button = Button(color=self.RED, 
                                         x=width - 170, 
                                         y=600, 
                                         width=150, 
                                         height=30, 
                                         value=False,
                                         group='game', 
                                         selected=False, 
                                         text_color=self.BLACK, 
                                         text='Resign')        
        
        # ---------------------------------------------------------------------------------- #

        #### End Screen ####
        self.play_again_button = Button(color=self.GREEN, 
                                        x=0.25 * self.screen_size, 
                                        y=0.50 * height + 5, 
                                        width=0.2 * self.screen_size, 
                                        height=40, 
                                        value=True,
                                        group='end_screen', 
                                        selected=True, 
                                        text_color=self.WHITE, 
                                        text='Yes!!')

        self.nomore_game_button = Button(color=self.RED, 
                                         x=0.55 * self.screen_size, 
                                         y=0.50 * height + 5, 
                                         width=0.2 * self.screen_size, 
                                         height=40, 
                                         value=False,
                                         group='end_screen', 
                                         selected=False, 
                                         text_color=self.BLACK, 
                                         text='No')
        
        # ---------------------------------------------------------------------------------- #
        
        # Collect all buttons
        self.all_buttons.extend((self.settings_button, self.start_game_button, self.quit_game_button,           # Start screen
                                 self.human_vs_human_button, self.human_vs_ai_button,                           # Game type
                                 self.ai_level_1_button, self.ai_level_2_button, self.ai_level_3_button,        # AI strength
                                 self.dont_flip_board_button, self.flip_board_button,                           # Flip board or not
                                 self.back_button,                                                              # Go back to start screen
                                 self.draw_game_button, self.resign_game_button,                                # Draw or resign game
                                 self.play_again_button, self.nomore_game_button))                              # Play or don't play again
