import json
import math
import random
from copy import deepcopy

from numpy.lib.polynomial import polysub
# from numba import jit, cuda
from chess.model.pieces import *
from chess.model.tree import Tree, Node

class AI:
    
    OPENINGS = 'chess/model/openings.json'
    LOOKUP = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        
    def __init__(self, color, depth, settings):
        self.color = color
        self.depth = depth
        self.settings = settings
        self.is_opening = True
        self.maximizer = False

        with open(self.OPENINGS) as jsonfile: self.openings = json.load(jsonfile)
    
    # @jit(target='cuda', forceobj=True)
    def think(self, board):
        """AI looks at all possible moves and makes the best one"""
        self.is_thinking = True
        self.board = board
        self.get_moves()
        self.clone = deepcopy(board)
        
        # Play opening
        if self.is_opening:
            move = self.play_opening()
            
            if move:
                self.is_thinking = False
                x, y = move[0]
                piece = self.board.position[y][x]
                return piece, move
        
        # Search for move
        self.create_tree()
        best_move = self.minimax(self.tree.root, self.depth, self.maximizer)
        # best_move = random.choice(self.clone.all_possible_moves[self.color])
        
        # Found best move
        self.is_thinking = False
        x, y = best_move[0]
        piece = self.board.position[y][x]
        return piece, best_move
        
    def get_piece(self, symbol, x, y, extra=None):
        for piece in self.clone.pieces[self.color]:
            if piece.symbol == symbol:
                if [(piece.x, piece.y), (x, y)] in piece.valid_moves:
                    if extra:
                        if self.LOOKUP[extra] == piece.x: return (piece.x, piece.y)
                    else:
                        return (piece.x, piece.y)
        
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
        self.board.update_possible_moves()
    
    def create_tree(self):
        """Create search tree, based on possible moves"""
        self.tree = Tree()
        self.tree.root = Node([], self.board, self.color, [], None)
        
        # Create children of root
        for move in self.clone.all_possible_moves[self.color]:
            (x1, y1), (x2, y2) = move
            piece = self.clone.position[y1][x1]
            self.clone.move_piece(self.color, piece, move)
            self.tree.root.children.append(Node(move, self.clone, self.color, [], self.tree.root))
            self.clone.position = deepcopy(self.board.position)
            self.tree.size += 1
            print(self.tree.size)
        
        # Create children up to depth = 'self.depth'
        for node in self.tree.root.children:
            self.populate_nodes(node)
    
    def populate_nodes(self, node):
        """Populate the tree nodes"""
        node.value = node.get_value()
        node.depth = node.get_depth()
        
        # Reached end of tree
        if node.depth == self.depth:
            node.state = 'terminal'
            return
        
        # Check for terminal states
        color = 'b' if node.color == 'w' else 'w'
        legal_moves = node.board.update_possible_moves()[color]
        if not legal_moves:
            node.state = 'terminal'
            if node.board.end_conditions['stalemate']: node.value = 0
            elif node.board.end_conditions['checkmate']: 
                node.value = 10000 if self.node.color == 'w' else -10000
            elif node.board.end_conditions['FMR']: node.value = 0
            elif node.board.end_conditions['3_fold_rep']: node.value = 0
            return
        
        # Fill children of the current node
        clone = deepcopy(node.board)
        for move in legal_moves:
            node.moves_analysed += 1
            (x1, y1), _ = move
            piece = node.board.position[y1][x1]
            node.board.move_piece(node.color, piece, move)
            node.children.append(Node(move, node.board, color, [], node))
            node.board.position = deepcopy(clone.board.position)
            self.tree.size += 1
            self.populate_nodes(node.children[-1])
        
        print(self.tree.size)
        
    def minimax(self, node, depth, maximizing_player):
        """The minimax algorithm"""
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
            if notation[1] != 'x':
                x2 = self.LOOKUP[notation[1]]
                y2 = int(notation[2]) - 1
            else:
                x2 = self.LOOKUP[notation[2]]
                y2 = int(notation[3]) - 1
                
            x1, y1 = self.get_piece(symbol, x2, y2)
        
        return [(x1, y1), (x2, y2)]
