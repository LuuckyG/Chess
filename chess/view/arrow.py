import math


class Arrow:
    
    def __init__(self, x1, y1, x2, y2, square_width, square_height):
        """"""        
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        
        self.square_width = square_width
        self.square_height = square_height
        
        self.factor = 0.25
        
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        
        self.begin = None
        self.middle = None
        self.end = None
    
    def create(self):
        """Create arrow"""
        self.get_begin()
        if (abs(self.x1 - self.x2) == 2 and abs(self.y1 - self.y2) == 1 
            or abs(self.x1 - self.x2) == 1 and abs(self.y1 - self.y2) == 2): 
            self.get_middle()    
        self.get_end()
    
    def get_begin(self):
        """Get beginning of arrow"""
        # Middle of begin square
        x = self.x1 * self.square_width  + 0.5 * self.square_width
        y = self.y1 * self.square_height + 0.5 * self.square_height
        
        # X-coordinate
        if self.x1 < self.x2: self.right = True          
        elif self.x1 > self.x2: self.left = True
        
        # Y-coordinate
        if self.y1 < self.y2: self.up = True
        elif self.y1 > self.y2: self.down = True      
        
        # Getting start location
        if not self.right and not self.left:
            start_x = x
            if self.up: start_y = y + self.factor * self.square_height
            else: start_y = y - self.factor * self.square_height
        
        elif not self.up and not self.down:
            start_y = y
            if self.right: start_x = x + self.factor * self.square_width
            else: start_x = x - self.factor * self.square_width
        
        else:
            start_x = x
            start_y = y
            
            if self.right: start_x = start_x + self.factor * self.square_width
            if self.left: start_x = start_x - self.factor * self.square_width
            if self.up: start_y = start_y + self.factor * self.square_height
            if self.down: start_y = start_y - self.factor * self.square_height
            
        self.begin = (start_x, start_y)
    
    def get_middle(self):
        """Draw arrow with L-shape (knight moves)"""
        # Center of middle square
        self.middle = (self.x2 * self.square_width  + 0.5 * self.square_width, 
                       self.y1 * self.square_height + 0.5 * self.square_height)
        
    def get_end(self):
        """Get center of end square"""       
        # Middle of ending square
        x = self.x2 * self.square_width  + 0.5 * self.square_width
        y = self.y2 * self.square_height + 0.5 * self.square_height
        
        # Check for l-shape arrow
        if self.middle: 
            if x == self.middle[0]: self.left, self.right = False, False
            if y == self.middle[1]: self.up, self.down = False, False
        
        self.end = (x, y)
        self.get_points(x, y)
    
    def get_points(self, x, y):
        """Get the points where the lines of the arrow need to drawn to"""
               
        # Straight up/down arrows
        if not self.right and not self.left:
            point_x1 = x - self.factor * self.square_width
            point_x2 = x + self.factor * self.square_width
                   
            # Up     
            if self.up:
                point_y1 = y - self.factor * self.square_width
                point_y2 = point_y1
            
            # Down
            else:
                point_y1 = y + self.factor * self.square_width
                point_y2 = point_y1
        
        # Straight left/right arrows
        elif not self.up and not self.down:
            point_y1 = y - self.factor * self.square_height
            point_y2 = y + self.factor * self.square_height
  
            # Right
            if self.right:
                point_x1 = x - self.factor * self.square_width
                point_x2 = point_x1
            
            # Left
            else:
                point_x1 = x + self.factor * self.square_width
                point_x2 = point_x1
        
        # Angled arrows
        else:
            a = 1.5 * self.factor * self.square_width     # x1
            b = 1.5 * self.factor * self.square_width     # x2
            c = 1.5 * self.factor * self.square_height    # y1
            d = 1.5 * self.factor * self.square_height    # y2
            
            if self.right and self.up: a, b, c, d = -a, 0, 0, -d
            if self.right and self.down: a, b, c, d = 0, -b, c, 0
            if self.left and self.up: a, b, c, d = 0, b, -c, 0
            if self.left and self.down: a, b, c, d = a, 0, 0, d
                
            point_x1 = x + a
            point_y1 = y + c
            point_x2 = x + b
            point_y2 = y + d
                
        self.point1 = (point_x1, point_y1)
        self.point2 = (point_x2, point_y2)
