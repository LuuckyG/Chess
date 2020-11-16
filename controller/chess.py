from view.view import GameView
from model.board import Board


class Chess:
    """Controller class of the game Chess"""

    def __init__(self):
        """Setup of Chess game. All game state variables, positin, and the 
        view are created."""

        # Game state variables
        self.play = True
        self.status = 'start_screen'
        self.win_condition = None
        
        self.move = []
        
        # Board is flipped if white is shown on top of the board
        self.is_flipped = False
        
        # Mouse events
        self.is_down = False
        self.is_dragged = None
        self.is_clicked = None
        self.left_click = None
        self.right_click = None
        
        # Settings
        self.settings = {'flip': False, 
                         'vs_computer': False, 
                         'ai_level': 1}

        # View
        self.view = GameView()


    def process_click(self, x, y, is_up=False):
        """The main method of the controller.
        This method determines in which phase of the game we are and 
        what method needs to be executed based on the phase.

        Args:
        - x: x-coordinate of mouse at click (in px)
        - y: y-coordinate of mouse at click (in px)
        """

        if self.status == 'start_screen': self.start_screen(x, y)
        elif self.status == 'settings': self.update_settings(x, y)
        elif self.status == 'game': self.play_game(x, y, is_up)
        elif self.status == 'replay': self.play_again(x, y)
    
    
    def start_screen(self, x, y):
        """Start screen of the game.
        There are three options: start the game, look and 
        change the game settings, or quit the game.
        
        Args:
        - x: x-coordinate of mouse at click (in px)
        - y: y-coordinate of mouse at click (in px)
        """

        if self.view.start_game_button.is_clicked(x, y):
            self.status = 'game'
            self.get_settings()
            self.start_game()
        elif self.view.settings_button.is_clicked(x, y):
            self.status = 'settings'
        elif self.view.quit_game_button.is_clicked(x, y):
            self.status = 'end_game'
            self.play = False


    def get_settings(self):
        """Get the selected settings by the user"""
        
        for button in self.view.all_buttons:
            group = button.group
            if (group == 'vs_computer' or group == 'ai_level') and button.selected:
                self.settings[group] = button.value


    def update_settings(self, x, y):
        """Settings page.
        Determine what settings the user changes. The values that can be changed are: 
        the opponent (human or AI), and the level of the AI (1, 2 or 3).
        
        Args:
        - x: x-coordinate of mouse at click (in px)
        - y: y-coordinate of mouse at click (in px)
        """

        button_groups = ['flip', 'vs_computer', 'ai_level']

        # Check if button is clicked
        for button in self.view.all_buttons:
            if button.group in button_groups and button.is_clicked(x, y):
                
                # Update view of other buttons that are not selected
                for related_button in self.view.all_buttons:
                    if related_button.group == button.group and related_button.selected:
                        related_button.update(False, self.view.LIGHT_GRAY, self.view.BLACK)

                # Update view of clicked button
                button.update(True, self.view.GREEN, self.view.WHITE)
        
        # Check if user is satisfied with settings and wants to return to
        # start screen to start playing the game
        if self.view.back_button.is_clicked(x, y):
            self.status = 'start_screen'
            

    def start_game(self):
        """The game is started with the selected settings.
        The default settings are: human vs. human."""

        # Change starting screen to Chess board
        self.board = Board(square_width=self.view.square_width, 
                           square_height=self.view.square_height,
                           is_flipped=self.is_flipped)

        # Create players
        self.board.player_list.append('Human')
        
        if self.settings['vs_computer']: self.board.player_list.append('AI')
        else: self.board.player_list.append('Human')
        
        
    def play_game(self, mouse_x, mouse_y, is_up):
        """[summary]

        Args:
            mouse_x ([type]): [description]
            mouse_y ([type]): [description]
            is_up (bool): [description]
        """
        
        tile_x, tile_y = self.pixel_coord_to_tile(mouse_x, mouse_y)
        tile = self.board.get_tile_at_pos(tile_x, tile_y)
        
        # Check if button is clicked
        if self.view.draw_game_button.is_clicked(mouse_x, mouse_y) or \
            self.view.resign_game_button.is_clicked(mouse_x, mouse_y): 
                self.new_game(mouse_x, mouse_y)

        elif is_up and self.is_clicked:
            # Check possible moves, and if possible
            # make the move.
            self.board.moves = self.is_clicked.valid_moves
                
            if (tile_x, tile_y) != self.left_click:
                self.move = [self.left_click, (tile_x, tile_y)]
                
                if self.is_clicked.can_move and self.move in self.is_clicked.valid_moves:
                    self.board.move_piece(color=self.board.current_color, 
                                          moving_piece=self.is_clicked, 
                                          move=self.move)
                    
                    self.update()
                    
                    self.board.next_turn(self.is_clicked, self.move)
                                        
                    if self.settings['flip']: self.is_flipped = not self.is_flipped
                    self.board.is_flipped = self.is_flipped
                    
                self.board.moves = []
                self.is_clicked = None
                self.is_dragged = None
                
            else: self.is_dragged = None
        
        else:
            if tile is not None and not (self.is_clicked and self.is_dragged):
                piece = self.board.get_piece(tile)

                if piece and piece.color == self.board.current_color:
                    self.is_clicked = piece
                    self.is_dragged = piece
                    self.left_click = (tile_x, tile_y)
                
                else: self.reset_highlights_and_arrows()


    def reset_highlights_and_arrows(self):
        """Reset highlights and arrows from board"""
        self.board.moves = []
        self.board.highlighted_tiles = []
        self.board.arrow_coordinates = []


    def process_right_click(self, mouse_x, mouse_y, is_up):
        """Get annotations drawn on the board using the right mouse button.

        Args:
            mouse_x (int): x-coordinate of the mouse (in px)
            mouse_y (int): y-coordinate of the mouse (in px)
            is_up (bool): variable indicating whether the mouse button is pressed
                or released.
        """
        
        x, y = self.pixel_coord_to_tile(mouse_x, mouse_y)

        # Mouse button is released
        if is_up:
            
            # Check for possible arrows
            if (x, y) != self.right_click:
                x1, y1 = self.right_click
                arrow = [(x1, y1), (x, y)]

                # Check if user wants to remove arrow by drawing opposite arrow
                if arrow in self.board.arrow_coordinates:
                    index = self.board.arrow_coordinates.index(arrow)
                    self.board.arrow_coordinates.pop(index)
                else: self.board.arrow_coordinates.append(arrow)                   

            else:
                # User does not want to draw arrow but wants to highlight tiles
                if (x, y) not in self.board.highlighted_tiles:
                    self.board.highlighted_tiles.append((x, y))
                else:
                    index = self.board.highlighted_tiles.index((x, y))
                    self.board.highlighted_tiles.pop(index)

        # Mouse button is pressed
        else: self.right_click = (x, y)          


    def ai_move(self):
        """"""
        pass

    
    def update(self):
        """"""
        if self.status == 'game':
            self.board.update_possible_moves()
            self.check_for_game_end()

        
    def check_for_game_end(self):
        """"""
        for condition, state in self.board.end_conditions.items():
            if state: self.win_condition = condition
        
        if self.win_condition: self.status = 'replay'


    def new_game(self, x, y):
        """"""
        if self.view.draw_game_button.is_clicked(x, y): 
            self.board.end_conditions['draw_agreed'] = True
            self.board.winner = 'Draw'
            
        if self.view.resign_game_button.is_clicked(x, y): 
            self.board.end_conditions['resignation'] = True
            winner = 1 if self.board.current_player == 0 else 0
            self.board.winner = ['white', 'black'][winner]
        
        self.status = 'replay'
    
    
    def play_again(self, x, y):
        if self.view.play_again_button.is_clicked(x, y): self.status = 'start_screen'
        if self.view.nomore_game_button.is_clicked(x, y): 
            self.status = 'end_game'
            self.play = False


    def chess_coord_to_pixels(self, board_x, board_y):
        """Get pixel coordinates from chess board coordinates"""
        return board_x * self.view.square_width, board_y * self.view.square_height


    def pixel_coord_to_tile(self, pixel_x, pixel_y):
        """Get board coordinates from pixel board coordinates"""
        return pixel_x // self.view.square_width, pixel_y // self.view.square_height
