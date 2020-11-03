import pygame

class Button:

    def __init__(self, color, x, y, width, height, value, group,
                selected=False, text_color=(0, 0, 0), text=''):
        """Class for a button to select the game style

        Args:
        - color: color of the button
        - x: top left x-coordinate of the button
        - y: top left y-coordinate of the button
        - width: width of the button
        - height: height of the button
        - value: value of the button
        - group: group of buttons the button belongs to
        - text_color: color of the text of the button
        - text: the text of the button
        - selected: boolean represting if the button is selected
        """
        
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text_color = text_color
        self.text = text
        self.value = value
        self.group = group
        self.selected = selected
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, font, thickness=2):
        """Draw the button

        Args:
        - screen: the window where the button is placed on
        - font: the text font of the button text
        - thickness: the thickness of the border of the button
        """
        pygame.draw.rect(screen, self.text_color, (self.x - thickness, self.y - thickness, 
                                    self.width + 2 * thickness, self.height + 2 * thickness), 0)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            text = font.render(self.text, 1, self.text_color)
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                               self.y + (self.height/2 - text.get_height()/2)))

    def is_hover(self, x, y):
        """Check if you hover over the button. If so, bring the button into focus.
    
        Args:
        - x: the x-coordinate of the mouse
        - y: the y-coordinate of the mouse
        """
        if self.rect.collidepoint(x, y):
            return True
        return False
    
    def is_clicked(self, x, y):
        """Check if you a button is clicked.
    
        Args:
        - x: the x-coordinate of the mouse
        - y: the y-coordinate of the mouse
        """
        if self.rect.collidepoint(x, y):
            return True
        return False
