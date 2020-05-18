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

def message(win, msg, coordinates):
  font = pygame.font.SysFont(None, 40)
  text = font.render(msg, True, (255, 255, 255))
  win.blit(text, coordinates)

def showScore(win, score):
  message(win, "Score: " + str(score), (0,0))

def showSprint(win):
  if(p.reloadSprint() <= 0):
    message(win, "Can Sprint", (155,0))
  else:
    message(win, str(p.reloadSprint()), (200,0))

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
  text = ("Use the arrow keys to move the player.", "Pressing the space bar will give you a short","burst of speed","Blue players are the infected people.", "If you touch an infected person you lose", "Try to stay healthy as long as you can.")
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
  createEnemies(enemies, 2, 3)


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
            p.speed = 3
            p.sprintReload = 0
            p.sprintTimer = 0
            background.speed = 2
            score = 0 
            enemies = []
            createEnemies(enemies, 2, 3)
            last_time = time()
            gameOver = False
            
          elif(event.key == pygame.K_q):
            run = False
            gameOver = False

    t = time()-last_time
    t*=50
    last_time = time()

    #Increasing score and speed
    score +=1
    p.walkSpeed = 3+score//400
    background.speed = 2+ score//400

    #Checking if the player closed the screen or if it's time for a new enemy to come on the screen
    for event in pygame.event.get():
      if(event.type == pygame.QUIT):
        run = False  
      if(event.type == enemyTime):
        if(score//200 >5):
          createEnemies(enemies, randint(3,6), 3 + score//400)
        else:
          createEnemies(enemies, 1 + randint(score//400,score//200), 3+score//400)
    #drawing background      
    background.draw(win, t)

    #drawing enemies and checking collision between enemies and player
    gameOver = checkEnemyCollision(enemies, t)

    #drawing player
    p.draw(win, winWidth, winHeight, t)

    showScore(win, score)
    showSprint(win)
    pygame.display.update()
    clock.tick(50)

# Setting up background
winWidth = 700
winHeight = 600
win = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("Juni Game")
clock = pygame.time.Clock()
#creating player
p  = Player(250, 400, 51, 73, 3)

#starting the game
main_menu()