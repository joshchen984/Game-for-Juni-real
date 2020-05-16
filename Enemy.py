import pygame
pygame.init()
from Entity import Entity

class Enemy(Entity):
  walkRight = (pygame.image.load('enemy12.png'),pygame.image.load('enemy8.png'), pygame.image.load('enemy7.png'))
  walkLeft = (pygame.image.load('enemy11.png'),pygame.image.load('enemy5.png'), pygame.image.load('enemy6.png'))
  walkDown = (pygame.image.load('enemy9.png'),pygame.image.load('enemy1.png'), pygame.image.load('enemy2.png'))

  def __init__(self, x, width, height, speed, y = -73):
    super().__init__( x, y, width, height, speed)
    self.walkCount = 0
    self.left = False
    self.right = False
    self.down = False

  def move(self, winWidth, winHeight, t):
    self.down = True
    self.y += self.speed * t
    if(self.y > winHeight):
      return True

  def draw(self, win, winWidth, winHeight, t):
    if(self.move(winWidth, winHeight, t)):
      return True
    if self.walkCount + 1 >=9:
      self.walkCount = 0
    if self.left:
      win.blit(Enemy.walkLeft[self.walkCount//3], (self.x, self.y))
      self.walkCount+=1
    elif self.right:
      win.blit(Enemy.walkRight[self.walkCount//3], (self.x, self.y))
      self.walkCount+=1
    elif self.down:
      win.blit(Enemy.walkDown[self.walkCount//3], (self.x, self.y))
      self.walkCount+=1



    
