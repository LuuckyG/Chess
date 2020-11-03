import os
import pygame

from view.view import GameView
from model.position import GamePosition
from setup.utils import opposite, chess_coord_to_pixels, pixel_coord_to_chess, position_to_key


class Chess:
    """Controller class of the game Chess"""

    def __init__(self):
        """Setup of Chess game. All game state variables, positin, and the 
        view are created."""

        self.play = True
        self.status = 'start_screen'

        self.winner = None
        self.end_conditions = {'resignation': False,
                               'checkmate': False, 
                               'stalemate': False, 
                               'HMC': False, 
                               '3_fold_rep': False}
        
        self.HMC = 0
        self.castling = [[True, True], [True, True]]
        self.move_nr = 0
        self.previous_move = [(-1, -1), (-1, -1)]
        self.player_list = []
        self.current_player_nr = 0
        
        self.settings = {'vs_computer': False, 'ai_level': 1}

        self.view = GameView()
        self.position = GamePosition()
        self.position.setup(self.view.square_width, self.view.square_height)


    def process_click(self, x, y):
        pass


    def check_move(self):
        """Check if move is valid"""
        pass

    def make_move(self, x, y, x2, y2):
        """Make valid move"""
        player = self.position.player
        color = 'wb'[player]
        enemy_color = opposite(color)
        HMC = self.position.HMC

        king_position = self.position.get_piece_position('K' + color)
        king = self.position.get_piece(king_position)
        
        if king.is_checkmate() or king.is_stalemate() or self.position.resignation(color):
            # return play = False
            pass
        elif king.is_check():
            pass
        elif king.is_pinned():
            # Find pinned piece and remove moves from possible moves
            pass
        else:
            # Player can move everywhere, except the king into attacked squares

            # reset attacked squares
            self.position.reset_attacking_squares()

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
