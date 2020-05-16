import pygame
from time import time
from Player import Player
from Background import Background
from Enemy import Enemy
from random import randint
from math import hypot
pygame.init()


def getTextRect(msg, color, font):
  text = font.render(msg, True, color)
  msgRect = text.get_rect()
  return text, msgRect

def screenMessage(win, msg, color, size, changeY = 0):
  font = pygame.font.SysFont(None, size)
  text, textRect = getTextRect(msg, color, font)
  textRect.center = (winWidth//2, winHeight//2+changeY)
  win.blit(text, textRect)
  return textRect

def showScore(win, score):
  font = pygame.font.SysFont(None, 40)
  text = font.render("Score: " + str(score), True, (255, 255, 255))
  win.blit(text, (0, 0))

def createEnemies(enemies, num, speed):
  for i in range(num):
    enemies.append(Enemy(randint(5,649), 51, 73, speed))

def checkEnemyCollision(enemies, t):
  for enemy in enemies:
    if(p.isCollide(enemy)):
      return True
    if(enemy.draw(win, winWidth, winHeight, t) ):
      enemies.remove(enemy)
  return False

def instructions():
  running = True
  text = ("Use the arrow keys to move the player.", "Blue players are the infected people.", "If you touch an infected person you lose", "Try to stay healthy as long as you can.")
  font = pygame.font.SysFont(None, 40)
  rendered_text = []
  for line in text:
    rendered_text.append(font.render(line, True, (0,0,0)))
  arrow = pygame.image.load("arrow.png")
  x = 39
  y = 39
  radius = 39
  clicking = False
  while running:
    win.fill((255,255,255))
    win.blit(arrow, (0,0))
    for i in range(0,len(rendered_text)):
      win.blit(rendered_text[i], (100, 100 + i*40))
    mx, my = pygame.mouse.get_pos()

    #finding distance from mouse to back button
    arrow_distance = int(hypot(mx-x, my-y))
    if(arrow_distance <= radius and clicking):
      main_menu()

    clicking = False
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if(event.button == 1):
          clicking = True
    pygame.display.update()
    clock.tick(60)

def main_menu():
  print('hello')
  running = True
  clicking = False
  while running:
    win.fill((255,255,255))
    play_button = screenMessage(win, "Play", (0,0,0), 100)
    instruction_button = screenMessage(win, "How to Play", (0,0,0), 50, 100)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if(play_button.collidepoint((mouse_x, mouse_y)) and clicking):
      game()
      running = False
    elif(instruction_button.collidepoint((mouse_x, mouse_y)) and clicking):
      instructions()
      running = False

    clicking = False
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if(event.button == 1):
          clicking = True
    pygame.display.update()
    clock.tick(60)
  pygame.quit()
        


def game():
  bg = pygame.image.load("road.png")
  bg2 = pygame.image.load('road2.png')
  background = Background(winHeight, 2, bg, bg2)

  #Creating the enemies
  enemies = []
  createEnemies(enemies, 2, 5)


  score = 0
  last_time = time()
  enemyTime = pygame.USEREVENT + 1
  pygame.time.set_timer(enemyTime, 1500)
  gameOver = False
  run = True
  #start of game
  while run:
    #Game Over Screen
    while(gameOver):
      win.fill((255,255,255))
      screenMessage(win, "Game Over!", (255, 0, 0), 100)
      screenMessage(win, "Press P to play again or Q to quit", (255, 0, 0), 45, 50)
      screenMessage(win, "Score: " + str(score), (255,0,0), 75, 100)
      pygame.display.update()

      # Checking for player action
      for event in pygame.event.get():
        if(event.type == pygame.QUIT):
          run = False  
          gameOver = False
        elif(event.type == pygame.KEYDOWN):
          if(event.key == pygame.K_p):
            p.x = 250
            p.y = 400
            p.speed = 5
            background.speed = 2
            score = 0 
            enemies = []
            createEnemies(enemies, 2, 5)
            last_time = time()
            gameOver = False
            
          elif(event.key == pygame.K_q):
            run = False
            gameOver = False

    t = time()-last_time
    t*=60
    last_time = time()

    #Increasing score and speed
    score +=1
    p.walkSpeed = 5+score//300
    background.speed = 2+ score//300

    #Checking if the player closed the screen or if it's time for a new enemy to come on the screen
    for event in pygame.event.get():
      if(event.type == pygame.QUIT):
        run = False  
      if(event.type == enemyTime):
        if(score//150 >5):
          createEnemies(enemies, randint(3,6), 5 + score//300)
        else:
          createEnemies(enemies, 1 + randint(score//300,score//150), 5+score//300)
    #drawing background      
    background.draw(win, t)

    #drawing enemies and checking collision between enemies and player
    gameOver = checkEnemyCollision(enemies, t)

    #drawing player
    p.draw(win, winWidth, winHeight, t)

    showScore(win, score)
    pygame.display.update()
    clock.tick(60)

# Setting up background
winWidth = 700
winHeight = 600
win = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("Juni Game")
clock = pygame.time.Clock()
#creating player
p  = Player(250, 400, 51, 73, 5)

#starting the game
print("yes")
main_menu()