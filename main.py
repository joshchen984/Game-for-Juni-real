import pygame
from time import time
from Player import Player
from Background import Background
from Enemy import Enemy
from Button import Button
from random import randint
from math import hypot
pygame.init()

def screenMessage(win, msg, color, size, changeY = 0):
  font = pygame.font.SysFont(None, size)
  text = font.render(msg, True, color)
  textRect = text.get_rect()
  textRect.center = (winWidth//2, winHeight//2+changeY)
  win.blit(text, textRect)

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
    enemy_x = randint(5,649)
    enemies.append(Enemy(enemy_x, 51, 73, speed))

def checkEnemyCollision(enemies, t):
  for enemy in enemies:
    if(p.isCollide(enemy)):
      return True
    if(enemy.draw(win, winWidth, winHeight, t) ):
      enemies.remove(enemy)
  return False

def instructions():
  running = True
  text = ("To prevent the spread of COVID-19, you must practice social distancing to avoid catching the virus.","The objective of the game is to avoid running into other people while taking a neighborhood jog.","The longer you stay away from others, the higher your score will be.","Use the ARROW keys to move the player.", "Pressing the SPACE BAR will give you a short burst of speed", "If you touch another person, the game will end.")
  font = pygame.font.SysFont(None, 30)
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
      win.blit(rendered_text[i], (10, 100 + i*40))
    mx, my = pygame.mouse.get_pos()

    #finding distance from mouse to back button
    arrow_distance = int(hypot(mx-x, my-y))
    if(arrow_distance <= radius and clicking):
      main_menu()
      running = False
    if(running):
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
  while running:
    win.fill((255,255,255))
    play_button = Button( "Play", (0,0,0), 100, (0,0,200))
    instruction_button = Button("Instructions", (0,0,0), 50, (0,0,200), 100)
    play_button.display(win, winWidth, winHeight)
    instruction_button.display(win, winWidth, winHeight)

    running, isClicking = instruction_button.check_clicking(instructions)
    if(running):
      running = play_button.check_clicking(game, True, isClicking)[0]

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