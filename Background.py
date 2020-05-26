import pygame
pygame.init()

class Background():
    def __init__(self, height, speed, bg1, bg2):
        self.stopY = height
        self.initialY = -height
        self.x = 0
        self.y = 0
        self.x2 = 0
        self.y2 = self.initialY
        self.speed = speed
        self.bg1 = bg1
        self.bg2 = bg2

    def moveScreen(self, t):
        self.y+=self.speed * t
        self.y2+=self.speed * t
        if(self.y > self.stopY):
            self.y = self.initialY
        elif(self.y2 > self.stopY):
            self.y2 = self.initialY  

    def draw(self, win, t):
        self.moveScreen(t)
        win.blit(self.bg1, (self.x, self.y))
        win.blit(self.bg2, (self.x2, self.y2))