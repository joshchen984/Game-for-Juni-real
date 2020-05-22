import pygame
pygame.init()

class Button:
  def __init__(self, msg, color, size, rectColor, changeY = 0):
    self.msg = msg
    self.color = color
    self.size = size
    self.rectColor = rectColor
    self.changeY = changeY
    # self.font = pygame.font.SysFont(None, self.size)
    # self.rendered_text = self.font.render(self.msg, True, self.color)
    # self.rect = self.rendered_text.get_rect()
    self.createButton()
    self.clicking = False

  def display(self, win, winWidth, winHeight):
    self.rect.center = (winWidth//2, winHeight//2+self.changeY)
    pygame.draw.rect(win, self.rectColor, self.rect)
    win.blit(self.rendered_text, self.rect)

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
      self.createButton(10)
      if(self.clicking):
        action()
        return (False, self.clicking)
      
    return (True, self.clicking)

