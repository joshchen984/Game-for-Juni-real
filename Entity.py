import pygame
pygame.init()
class Entity:
  def __init__(self, x, y, width, height,speed):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.speed = speed

  def getRect(self):
    return pygame.Rect(self.x, self.y, self.width, self.height)