import pygame
pygame.init()

class Button:
    def __init__(self, msg, color, size, rectColor, coordinates,isCenter = False, changeY = 0):
        self.isCenter = isCenter
        self.msg = msg
        self.color = color
        self.size = size
        self.rectColor = rectColor
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.changeY = changeY
        self.createButton()
        self.rectLocation()
        self.clicking = False

    def display(self, win):
        pygame.draw.rect(win, self.rectColor, self.rect)
        win.blit(self.rendered_text, self.rect)

    def rectLocation(self):
        if(self.isCenter):
            self.rect.center = (self.x, self.y+self.changeY)
        else:
            self.rect.x = self.x
            self.rect.y = self.y
        self.center = self.rect.center

    def createButton(self, changeSize = 0):
        self.font = pygame.font.SysFont(None, self.size + changeSize)
        self.rendered_text = self.font.render(self.msg, True, self.color)
        self.rect = self.rendered_text.get_rect()

    def check_clicking(self, action, checked_clicking = False, isClicking = False):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.clicking = isClicking
        if not(checked_clicking):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return (False, self.clicking)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if(event.button == 1):
                        self.clicking = True
        if(self.rect.collidepoint((mouse_x, mouse_y))):
            self.createButton(self.size//20)
            self.rect.center = self.center
            if(self.clicking):
                action()
                return (False, self.clicking)
        else:
            self.createButton()
            self.rect.center = self.center
        return (True, self.clicking)

