from chess.model.board import Empty


class Tree:
    
    def __init__(self):
        self.root = None
        self.size = 1
    
    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.root.__iter__() 


class Node:
    
    def __init__(self, move, board, color, children, parent):
        self.move = move
        self.board = board
        self.color = color
        self.children = children
        self.parent = parent
        self.moves_analysed = 0
        self.state = ''
    
    def get_value(self):
        self.value = 0
        for row in self.board.position:
            for square in row:
                if not isinstance(square, Empty): 
                    if square.color == 'w': self.value += square.value
                    if square.color == 'b': self.value -= square.value

    def get_highest_node(self):
        highest_node = self
        while True:
            if highest_node.parent is not None:
                highest_node = highest_node.parent
            else:
                return highest_node

    def get_depth(self):
        depth = 0
        highest_node = self
        while True:
            if highest_node.parent is not None:
                highest_node = highest_node.parent
                depth += 1
            else:
                return depth
