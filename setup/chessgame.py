import os
import pygame

from setup.images import Images
from setup.position import GamePosition
from pieces.pieces import Piece
from game_rules.rulebook import RuleBook
from game_rules.rules import opposite, is_attacked_by, is_captured, is_occupied, is_occupied_by



class ChessGame:

    def __init__(self):
        self.rulebook = RuleBook()
        self.position = GamePosition()
        
        self.all_images = Images()
        self.images = self.all_images.images
        self.screen = self.all_images.screen

        self.square_width = self.all_images.square_width
        self.square_height = self.all_images.square_height

    def draw_board(self, right_clicked=[], is_clicked=False, drag_coord=None):
        """Update chess board. Don't update moving piece, indicated by drag_coord"""
        previous_move = self.position.get_previous_move()
        self.screen.blit(self.all_images.background, (0, 0))
        player = self.position.get_player()
        pieces = create_pieces(self.position, self.square_width, self.square_height)
        w_pieces, b_pieces = pieces["white"], pieces["black"]

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

        # pygame.draw.polygon(screen, (225, 0, 0),
        #                     ((0, 100), (0, 200), (200, 200), (200, 300),
        #                      (300, 150), (200, 0), (200, 100)))

        # Blit over other pieces
        if player == 1:  # Player is black
            order = [w_pieces, b_pieces]
        else:
            order = [b_pieces, w_pieces]

        for piece in order[0]:
            chess_coord, color, subsection, pos = piece.get_info()
            pixel_coord = chess_coord_to_pixels(chess_coord, self.square_width, self.square_height)
            if chess_coord != drag_coord:  # Don't blit moving piece
                if pos == (-1, -1):
                    # Default square
                    self.screen.blit(self.all_images.pieces_image, pixel_coord, subsection)
                else:
                    # Specific pixels:
                    self.screen.blit(self.all_images.pieces_image, pos, subsection)

        for piece in order[1]:
            chess_coord, color, subsection, pos = piece.get_info()
            pixel_coord = chess_coord_to_pixels(chess_coord, self.square_width, self.square_height)
            if chess_coord != drag_coord:  # Don't blit moving piece
                if pos == (-1, -1):
                    # Default square
                    self.screen.blit(self.all_images.pieces_image, pixel_coord, subsection)
                else:
                    # Specific pixels:
                    self.screen.blit(self.all_images.pieces_image, pos, subsection)
    
    def check_move(self):
        """Check if move is valid"""
        pass

    def make_move(self, x, y, x2, y2):
        """Make valid move"""
        player = self.position.get_player()
        color = 'wb'[player]
        enemy_color = opposite(color)
        HMC = self.position.get_HMC()
        in_check = False

        # Check if player is not in check
        king_position = get_piece_position(self.position, 'K' + color)  # Find position of the king of player
        attacked_squares = is_attacked_by(position,
                                        king_position[0], king_position[1],
                                        enemy_color)  # Check if king is attacked by enemy

        # Get all valid moves of selected piece of current player
        valid_moves, position = valid_piece_move(position, x, y, color)

        # Remove moves that lead to player getting into check
        # for pieces in attacked_squares:
        #     if pieces in valid_moves or pieces == (x, y):
        #         in_check = True

        if (x2, y2) in valid_moves and not in_check:
            board = position.get_board()
            castle_right = position.get_castle_rights()

            # Check additional move options
            if board[y][x][0] == 'P':
                position = en_passant_rights(position, x2, y2)
                position.set_HMC(0)  # Reset 50 move rule
                if is_promotion(position, y2):
                    board[y][x] = 'Q' + 'wb'[player]  # Automatic promotion to queen
                    position.set_board(board)
            elif board[y][x][0] == 'K':
                position = castle_rights(position, x2, y2)
            elif board[y][x][0] == 'R':
                if x == 0 and (y == 0 or y == 7) and castle_right[player][0]:
                    castle_right[player][0] = False
                elif x == 7 and (y == 0 or y == 7) and castle_right[player][1]:
                    castle_right[player][1] = False
                position.set_castle_rights(castle_right)
            elif is_captured(board, x2, y2):
                position.set_HMC(0)  # Reset 50 move rule
            else:
                HMC += 1
                position.set_HMC(HMC)

            # Make the move
            board = position.get_board()
            board[y2][x2] = board[y][x]
            board[y][x] = 0

            # Update position
            position.set_history(position)
            player = 1 - player
            position.set_board(board)
            position.set_player(player)
            position.set_previous_move([(x, y), (x2, y2)])
            position.set_EPT(-1)
            position.set_castle_rights(castle_right)

            # Check if 3-move repetition is of power
            for value in position.history.values():
                if value == 3:
                    position.set_play(False)
            
            # Check for checkmate or stalemate
            self.check_end_game()

        return position

    def check_end_game(self):
        """Check if move causes game to end with checkmate or stalemate"""
        player_moves = all_possible_moves(position, enemy_color)
        # position = is_checkmate(position, enemy_color)
        # position = is_stalemate(position, enemy_color)
        return False





def chess_coord_to_pixels(chess_coord, square_width, square_height):
    """Get pixel coordinates from chess board coordinates"""
    x, y = chess_coord
    return x * square_width, y * square_height


def pixel_coord_to_chess(pixel_coord, square_width, square_height):
    """Get board coordinates from pixel board coordinates"""
    x, y = pixel_coord
    return x // square_width, y // square_height


def create_pieces(position, square_width, square_height):
    """Create piece objects based on board position"""
    board = position.get_board()
    pieces = {
        "white": [],
        "black": []
    }

    for x in range(8):
        for y in range(8):
            if board[x][y] != 0:
                p = Piece(board[x][y], board[x][y][1], (y, x), square_width, square_height)
                if board[x][y][1] == 'w':
                    pieces["white"].append(p)
                else:
                    pieces["black"].append(p)
    return pieces


def get_piece(position, square_width, square_height, mouse_coord):
    """Get piece selected by mouse click"""
    pieces = create_pieces(position, square_width, square_height)
    white_pieces, black_pieces = pieces["white"], pieces["black"]
    pieces = white_pieces + black_pieces

    for piece in pieces:
        if piece.chess_coord == mouse_coord:
            return piece
