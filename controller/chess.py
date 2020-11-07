from view.view import GameView
from model.board import Board
from model.pieces import Empty


class Chess:
    """Controller class of the game Chess"""

    def __init__(self):
        """Setup of Chess game. All game state variables, positin, and the 
        view are created."""

        # Game state variables
        self.play = True
        self.status = 'game'
        
        # Board is flipped if white is shown on top of the board
        self.is_flipped = False
        
        # Mouse events
        self.is_down = False
        self.is_dragged = None
        self.is_clicked = None
        self.left_click = False
        self.right_click = False

        # Dragging pieces coordinates
        self.moves = []
        self.left_click_coordinates = None

        # Drawing arrows coordinates
        self.right_click_coordinates = None
        
        # Win conditions
        self.winner = None
        self.end_conditions = {'resignation': False,
                               'checkmate': False, 
                               'stalemate': False, 
                               'HMC': False, 
                               '3_fold_rep': False}
        self.HMC = 0

        # Move and player variables
        self.move_nr = 0
        self.previous_move = []
        self.player_list = []
        self.current_player = 0
        self.current_color = 'wb'[self.current_player]
        
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

        if self.status == 'start_screen':
            self.start_screen(x, y)
        elif self.status == 'settings':
            self.update_settings(x, y)
        elif self.status == 'game':
            self.play_game(x, y, is_up)
        elif self.status == 'replay':
            self.new_game(x, y)
    
    
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

        button_groups = ['vs_computer', 'ai_level']

        # Check if button is clicked
        for button in self.view.all_buttons:
            if button.group in button_groups and button.is_clicked(x, y):
                
                # Update view of other buttons that are not selected
                for related_button in self.view.all_buttons:
                    if related_button.group == button.group and related_button.selected:
                        self.view.update_button_look(related_button, False, 
                                    self.view.LIGHT_GRAY, self.view.BLACK)

                # Update view of clicked button
                self.view.update_button_look(button, True, 
                                    self.view.GREEN, self.view.WHITE)
        
        # Check if user is satisfied with settings and wants to return to
        # start screen to start playing the game
        if self.view.back_button.is_clicked(x, y):
            self.status = 'start_screen'
            

    def start_game(self):
        """The game is started with the selected settings.
        The default settings are: human vs. human."""

        # Create players
        #TODO

        # Change starting screen to Chess board
        self.board = Board(square_width=self.view.square_width, 
                           square_height=self.view.square_height,
                           is_flipped=self.is_flipped)


    def play_game(self, mouse_x, mouse_y, is_up):
        """"""
        tile_x, tile_y = self.pixel_coord_to_tile(mouse_x, mouse_y)
        tile = self.board.get_tile_at_pos(tile_x, tile_y)

        if is_up:
            self.moves = self.is_clicked.moves(self.board, self.previous_move)

            # Check possible moves, and if possible
            # make the move.
            if (tile_x, tile_y) != self.left_click_coordinates:
                if (tile_x, tile_y) in self.moves:
                    self.make_move(self.is_clicked, 
                                   self.left_click_coordinates[0], self.left_click_coordinates[1],
                                   tile_x, tile_y)
                self.moves = []
                self.is_dragged = None
            else:
                # Show possible moves of piece
                # Piece is not dragged
                self.is_dragged = None
        else:
            if tile is not None:

                if isinstance(tile.state, Empty):
                    self.reset_highlights_and_arrows()

                else:
                    piece = self.board.get_piece(tile)
                    self.is_clicked = piece
                    self.is_dragged = piece

                    self.left_click_coordinates = (tile_x, tile_y)


    def reset_highlights_and_arrows(self):
        """Reset highlights and arrows from board"""
        self.moves = []
        self.board.highlighted_tiles = []
        self.board.arrow_coordinates = []


    def remove_arrow(self, arrow):
        """An arrow is removed if it is drawn twice"""
        return arrow in self.board.arrow_coordinates


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
            if (x, y) != self.right_click_coordinates:
                x1, y1 = self.right_click_coordinates
                arrow = [(x1, y1), (x, y)]

                # Check if user wants to remove arrow by drawing opposite arrow
                if self.remove_arrow(arrow):
                    index = self.board.arrow_coordinates.index(arrow)
                    self.board.arrow_coordinates.pop(index)
                else:
                    self.board.arrow_coordinates.append(arrow)                   

            else:
                # User does not want to draw arrow but wants to highlight tiles
                if (x, y) not in self.board.highlighted_tiles:
                    self.board.highlighted_tiles.append((x, y))
                else:
                    index = self.board.highlighted_tiles.index((x, y))
                    self.board.highlighted_tiles.pop(index)

        # Mouse button is pressed
        else:
            self.right_click_coordinates = (x, y)          


    def ai_move(self):
        """"""
        pass

    
    def next_turn(self):
        """Update game state variables"""
        
        self.current_player = 0 if self.current_player == 1 else 1
        self.current_color = 'wb'[self.current_player]
        
        # Only update move nr is white is back in turn
        if self.current_player == 'w': self.move_nr += 1
        if self.settings['flip']: self.is_flipped = not self.is_flipped
        

    def check_move(self):
        """Check if move is valid"""
        pass


    def make_move(self, moving_piece, x1, tile_y1, x2, tile_y2):
        # Get king and check for check etc
        #TODO
        
        piece_y1 = self.tile_coord_to_piece(tile_y1)
        piece_y2 = self.tile_coord_to_piece(tile_y2)
        moving_piece.make_move(x2, piece_y2)
        
        previous_tile = self.board.get_tile_at_pos(x1, tile_y1)
        next_tile = self.board.get_tile_at_pos(x2, tile_y2)
        
        next_tile.state = moving_piece
        previous_tile.state = Empty(x1, piece_y1)
        

    # def make_move(self, x, y, x2, y2):
    #     """Make valid move"""
    #     player = self.position.player
    #     color = 'wb'[player]
    #     # enemy_color = opposite(color)
    #     HMC = self.position.HMC

    #     king_position = self.position.get_piece_position('K' + color)
    #     king = self.position.get_piece(king_position)
        
    #     if king.is_checkmate() or king.is_stalemate() or self.position.resignation(color):
    #         # return play = False
    #         pass
    #     elif king.is_check():
    #         pass
    #     elif king.is_pinned():
    #         # Find pinned piece and remove moves from possible moves
    #         pass
    #     else:
    #         # Player can move everywhere, except the king into attacked squares

    #         # reset attacked squares
    #         self.position.reset_attacking_squares()

        # # Check if player is not in check
        # king_position = get_piece_position(self.position, 'K' + color)  # Find position of the king of player
        # attacked_squares = is_attacked_by(self.position,
        #                                 king_position[0], king_position[1],
        #                                 enemy_color)  # Check if king is attacked by enemy

        # # Get all valid moves of selected piece of current player
        # valid_moves, self.position = valid_piece_move(self.position, x, y, color)

        # # Remove moves that lead to player getting into check
        # # for pieces in attacked_squares:
        # #     if pieces in valid_moves or pieces == (x, y):
        # #         in_check = True

        # if (x2, y2) in valid_moves and not in_check:
        #     board = self.position.get_board()
        #     castle_right = self.position.get_castle_rights()

        #     # Check additional move options
        #     if board[y][x][0] == 'P':
        #         self.position = en_passant_rights(self.position, x2, y2)
        #         self.position.set_HMC(0)  # Reset 50 move rule
        #         if is_promotion(self.position, y2):
        #             board[y][x] = 'Q' + 'wb'[player]  # Automatic promotion to queen
        #             self.position.set_board(board)
        #     elif board[y][x][0] == 'K':
        #         self.position = castle_rights(self.position, x2, y2)
        #     elif board[y][x][0] == 'R':
        #         if x == 0 and (y == 0 or y == 7) and castle_right[player][0]:
        #             castle_right[player][0] = False
        #         elif x == 7 and (y == 0 or y == 7) and castle_right[player][1]:
        #             castle_right[player][1] = False
        #         self.position.set_castle_rights(castle_right)
        #     elif is_captured(board, x2, y2):
        #         self.position.set_HMC(0)  # Reset 50 move rule
        #     else:
        #         HMC += 1
        #         self.position.set_HMC(HMC)

        #     # Make the move
        #     board[y2][x2] = board[y][x]
        #     board[y][x] = 0

        #     # Update position
        #     self.update(self.position, board, player, (x, y), (x2, y2), castle_right)

        #     # Check if 3-move repetition is of power
        #     for value in self.position.history.values():
        #         if value == 3:
        #             self.position.set_play(False)
            
        #     # Check for checkmate or stalemate
        #     self.check_end_game()

        # return self.position


    def check_end_game(self):
        """Check if move causes game to end with checkmate or stalemate"""
        # player_moves = all_possible_moves(position, enemy_color)
        # position = is_checkmate(position, enemy_color)
        # position = is_stalemate(position, enemy_color)
        return False


    def new_game(self, x, y):
        pass


    def chess_coord_to_pixels(self, board_x, board_y):
        """Get pixel coordinates from chess board coordinates"""
        return board_x * self.view.square_width, board_y * self.view.square_height


    def pixel_coord_to_tile(self, pixel_x, pixel_y):
        """Get board coordinates from pixel board coordinates"""
        return pixel_x // self.view.square_width, pixel_y // self.view.square_height
    
    
    def tile_coord_to_piece(self, y):
        return y if self.board.is_flipped else (7 - y)
