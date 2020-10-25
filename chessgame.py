import os
import pygame

from setup.images import Images
from setup.position import GamePosition
from setup.utils import opposite, chess_coord_to_pixels, pixel_coord_to_chess, position_to_key


class ChessGame:

    def __init__(self):
        self.position = GamePosition()
        
        self.all_images = Images()
        self.images = self.all_images.images
        self.screen = self.all_images.screen

        self.square_width = self.all_images.square_width
        self.square_height = self.all_images.square_height

        self.position.create_pieces(self.square_width, self.square_height)

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
    
    def check_move(self):
        """Check if move is valid"""
        pass

    def make_move(self, x, y, x2, y2):
        """Make valid move"""
        player = self.position.get_player()
        color = 'wb'[player]
        enemy_color = opposite(color)
        HMC = self.position.get_HMC()

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

    def update(self, position, board, player, orig_coord, new_coord, castle_right):
        """Update the position with the move made"""
        self.position.set_history(self.position)
        self.position.set_board(board)
        self.position.set_player(1 - player)
        self.position.set_previous_move([orig_coord, new_coord])
        self.position.set_EPT(-1)
        self.position.set_castle_rights(castle_right)

    def check_end_game(self):
        """Check if move causes game to end with checkmate or stalemate"""
        # player_moves = all_possible_moves(position, enemy_color)
        # position = is_checkmate(position, enemy_color)
        # position = is_stalemate(position, enemy_color)
        return False
