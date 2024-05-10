import pygame
from pygame.locals import *
import random


class Apple:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.rect = Rect(self.x, self.y, 50, 50)

        self.xVel = 0
        self.yVel = 0

        self.state = 0
        self.game = game
        self.colorList = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        self.color = self.colorList[0]

    def change_position(self):
        self.x = random.randint(50, self.game.screen.get_width() - 50)
        self.y = random.randint(50, self.game.screen.get_height() - 50)
        self.rect = Rect(self.x, self.y, 50, 50)

        self.state = random.randint(0, 3)
        self.xVel = random.uniform(-5, 5)
        self.yVel = random.uniform(-5, 5)

    def move_fixed(self):
        self.x += self.xVel
        self.y += self.yVel

        if self.x < 0:
            self.x = 0
            self.xVel *= -1

        if self.x > self.game.screen.get_width() - 50:
            self.x = self.game.screen.get_width() - 50
            self.xVel *= -1

        if self.y < 0:
            self.y = 0
            self.yVel *= -1

        if self.y > self.game.screen.get_height() - 50:
            self.y = self.game.screen.get_height() - 50
            self.yVel *= -1

    def move_fixed_gravity(self):
        self.yVel += 0.1

        self.x += self.xVel
        self.y += self.yVel

        if self.x < 0:
            self.x = 0
            self.xVel *= -1

        if self.x > self.game.screen.get_width() - 50:
            self.x = self.game.screen.get_width() - 50
            self.xVel *= -1

        if self.y < 0:
            self.y = 0
            self.yVel = 0

        if self.y > self.game.screen.get_height() - 50:
            self.y = self.game.screen.get_height() - 50
            self.yVel *= -3

    def flee(self):
        vectorToTargetX = self.x - self.game.player.x
        vectorToTargetY = self.y - self.game.player.y

        vectorToTargetMagnitude = vectorToTargetX ** 2 + vectorToTargetY ** 2
        vectorToTargetNormalizedX = vectorToTargetX / vectorToTargetMagnitude
        vectorToTargetNormalizedY = vectorToTargetY / vectorToTargetMagnitude

        self.xVel += vectorToTargetNormalizedX * 75
        self.yVel += vectorToTargetNormalizedY * 75

        self.yVel += 0.1

        self.x += self.xVel
        self.y += self.yVel

        if self.x < 0:
            self.x = 0
            self.xVel *= -1

        if self.x > self.game.screen.get_width() - 50:
            self.x = self.game.screen.get_width() - 50
            self.xVel *= -1

        if self.y < 0:
            self.y = 0
            self.yVel *= -1

        if self.y > self.game.screen.get_height() - 50:
            self.y = self.game.screen.get_height() - 50
            self.yVel *= -1

    def update(self):
        if self.state == 1:
            self.move_fixed()
        if self.state == 2:
            self.move_fixed_gravity()
        if self.state == 3:
            self.flee()

        self.color = self.colorList[self.state - 1]

        self.rect = Rect(self.x, self.y, 50, 50)

    def draw(self):
        pygame.draw.ellipse(self.game.screen, self.color, self.rect)
