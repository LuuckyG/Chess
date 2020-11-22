import json
import math
import random
from copy import deepcopy
from chess.model.pieces import *


class Node:
    
    def __init__(self, position, state, children):
        self.position = position
        self.state = state
        self.children = children
        self.value = self.get_value()
    
    def get_value(self):
        value = 0
        for row in self.position:
            for square in row:
                if not isinstance(square, Empty): 
                    if square.color == 'w': value += square.value
                    if square.color == 'b': value -= square.value
        return value

class AI:
    
    OPENINGS = 'chess/model/openings.json'
    LOOKUP = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        
    def __init__(self, color, depth, settings):
        self.color = color
        self.depth = depth
        self.settings = settings
        self.is_opening = True

        with open(self.OPENINGS) as jsonfile: self.openings = json.load(jsonfile)
        
    def think(self, board):
        """AI looks at all possible moves and makes the best one"""
        self.is_thinking = True
        self.board = board
        self.setup_clone(self.board)
        
        if self.is_opening:
            move = self.play_opening()
            
            if move:
                x, y = move[0]
                piece = board.position[y][x]
                return piece, move
            
        self.get_moves()
        
        # self.create_tree()
        
        # Look for move
        # best_move = self.minimax(board)
        best_move = random.choice(self.clone.all_possible_moves[self.color])
        
        # Found best move
        self.is_thinking = False
        x, y = best_move[0]
        piece = board.position[y][x]
        return piece, best_move
        
    def setup_clone(self, board):
        """Create clone of current board position"""
        self.clone = deepcopy(board)
    
    
    def splitter(self, move, order):
        try:
            m = move.split()
            try:
                white, black = m[0], m[1]
                order.extend([white, black])
            except:
                order.extend(move)
            
        except ValueError:
            order.append(move)
    
    def walk(self):
        pass
    
    def get_piece(self, symbol, x, y, extra=None):
        for piece in self.clone.pieces[self.color]:
            if piece.symbol == symbol:
                if [(piece.x, piece.y), (x, y)] in piece.valid_moves:
                    if extra:
                        if self.LOOKUP[extra] == piece.x: return (piece.x, piece.y)
                    else:
                        return (piece.x, piece.y)
        
    def notation_to_pos(self, notation):
        if notation == 'O-O':
            y1 = 0 if self.color == 'w' else 7
            y2 = y1
            x1 = 4
            x2 = 6
        elif notation == 'O-O-O':
            y1 = 0 if self.color == 'w' else 7
            y2 = y1
            x1 = 4
            x2 = 2
        elif len(notation) == 4:
            capture = False
            if notation[1] == 'x': capture = True
            if notation[1] in 'abcdefgh': extra = notation[1]
            else: extra = None
            
            if notation[0] not in 'abcdefgh': symbol = notation[0]
            else: symbol = 'P'
            
            if capture:
                x2 = self.LOOKUP[notation[2]]
                y2 = int(notation[3]) - 1
            else:
                x2 = self.LOOKUP[notation[1]]
                y2 = int(notation[2]) - 1
                
            x1, y1 = self.get_piece(symbol, x2, y2, extra)
        elif len(notation) == 2:
            # Pawn move
            symbol = 'P'
            x2 = self.LOOKUP[notation[0]]
            y2 = int(notation[1]) - 1
            x1, y1 = self.get_piece(symbol, x2, y2)
        else:
            symbol = notation[0]
            x2 = self.LOOKUP[notation[1]]
            y2 = int(notation[2]) - 1
            x1, y1 = self.get_piece(symbol, x2, y2)
        
        return [(x1, y1), (x2, y2)]
    
    def play_opening(self):
        """Let AI play opening theory """
        prev_moves = ' '.join(self.clone.move_history)
        length = len(prev_moves)
        possibilities = []
        
        for name, moves in self.openings.items():
            if prev_moves in moves:
                possibilities.append(name)

        if possibilities:
            name = random.choice(possibilities)
            opening = self.openings[name]
            print(name)
            
            if length >= len(opening):
                self.is_opening = False
                return None
            
            next_move = opening[length:].split()[0]
            next_move = self.notation_to_pos(next_move)
            return next_move
        
        else: 
            self.is_opening = False
            return None
        
    
    def get_moves(self):
        """Get all possible moves in the current position"""
        self.clone.update_possible_moves()
    
    def create_tree(self):
        """Create search tree, based on possible moves"""
        for move in self.clone.all_possible_moves:
            (x1, y1), (x2, y2) = move
            piece = self.clone[y1][x1]
            self.clone.move_piece(self.color, piece, move)
    
    def minimax(self, node, depth, maximizing_player):
        if depth == 0 or node.state == 'terminal':
            return node.value
        
        if maximizing_player:
            value = -math.inf
            
            for child in node.children:
                value = max(value, self.minimax(child, depth - 1, False))
            return value
        
        else:
            value = math.inf
            for child in node.children:
                value = min(value, self.minimax(child, depth - 1, True))
            return value
    
    def evaluate(self, board):
        return [(0, 0), (0, 0)]    
    