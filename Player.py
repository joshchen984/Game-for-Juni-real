import pygame
pygame.init()
from Entity import Entity

class Player(Entity):
  walkRight = (pygame.image.load('sprite12.png'),pygame.image.load('sprite8.png'), pygame.image.load('sprite7.png'))
  walkLeft = (pygame.image.load('sprite11.png'),pygame.image.load('sprite5.png'), pygame.image.load('sprite6.png'))
  walkUp = (pygame.image.load('sprite10.png'),pygame.image.load('sprite3.png'), pygame.image.load('sprite4.png'))
  walkDown = (pygame.image.load('sprite9.png'),pygame.image.load('sprite1.png'), pygame.image.load('sprite2.png'))

  def __init__(self, x, y, width, height, speed):
    super().__init__(x, y, width, height, speed)
    self.walkCount = 0
    self.left = False
    self.right = False
    self.up = False
    self.down = False
    self.canSprint = True
    self.sprintTimer = 0
    self.sprintReload = 0
    self.clockTimer = pygame.time.Clock()
    self.clockReload = pygame.time.Clock()
    self.walkSpeed = speed

  def reloadSprint(self):
    self.sprintTimer-=self.clockTimer.tick()
    self.sprintReload -=self.clockReload.tick()
    if(self.sprintReload <=0):
      self.canSprint = True
    if(self.sprintTimer<=0):
      self.speed = self.walkSpeed
    return int(self.sprintReload/1000)


  def sprint(self):
    self.canSprint = False
    self.sprintTimer = 500
    self.sprintReload = 6000
    self.speed +=4

  def getMove(self, winWidth, winHeight, t):
    self.reloadSprint()
    keys = pygame.key.get_pressed()
    if(keys[pygame.K_SPACE] and self.canSprint):
      self.sprint()
    if(keys[pygame.K_LEFT] and self.x>self.speed):
      self.x-=self.speed * t
      self.left = True
      self.right = False
      self.up = False
      self.down = False
    elif (keys[pygame.K_RIGHT] and self.x<winWidth-self.width-self.speed):
      self.x+=self.speed * t
      self.left = False
      self.right = True
      self.up = False
      self.down = False
    elif (keys[pygame.K_UP] and self.y > self.speed):
      self.y-=self.speed * t
      self.left = False
      self.right = False
      self.up = True
      self.down = False
    elif (keys[pygame.K_DOWN] and self.y < winHeight-self.height-self.speed):
      self.y+=self.speed * t
      self.left = False
      self.right = False
      self.up = False
      self.down = True
    else:
      self.left = False
      self.right = False
      self.up = False
      self.down = False   

  def draw(self, win, winWidth, winHeight, t):
    self.getMove(winWidth, winHeight, t)
    if self.walkCount + 1 >=9:
      self.walkCount = 0
    if self.left:
      win.blit(Player.walkLeft[self.walkCount//3], (self.x, self.y))
      self.walkCount+=1
    elif self.right:
      win.blit(Player.walkRight[self.walkCount//3], (self.x, self.y))
      self.walkCount+=1
    elif self.down:
      win.blit(Player.walkDown[self.walkCount//3], (self.x, self.y))
      self.walkCount+=1
    else:
      win.blit(Player.walkUp[self.walkCount//3], (self.x, self.y))
      self.walkCount+=1  

  def isCollide(self, enemy):
    if(self.getRect().colliderect(enemy.getRect())):
      return True
    return False
