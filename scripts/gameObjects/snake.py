import pygame
from pygame.locals import *
import random


class Snake:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y

        self.xVel = 0
        self.yVel = 0

        self.rect = Rect(self.x, self.y, 50, 50)

        self.tail = []
        self.colorList = []
        self.length = 5

        self.dangerLimit = 60
        self.game = game

    def update(self):

        self.yVel += 0.1

        self.xVel *= 0.99
        self.yVel *= 0.99

        self.x += self.xVel
        self.y += self.yVel

        self.check_collision_with_borders()

        self.rect = Rect(self.x, self.y, 50, 50)

        self.manage_tail()

    def manage_tail(self):
        self.tail.append(Rect(self.x, self.y, 50, 50))
        self.colorList.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        if len(self.tail) > self.length:
            self.tail.pop(0)
            self.colorList.pop(0)

    def check_collision_with_borders(self):
        if self.x < 0:
            self.x = 0
            self.xVel *= -1
            self.game.soundWall.play()
        if self.x > self.game.screen.get_width() - 50:
            self.x = self.game.screen.get_width() - 50
            self.xVel *= -1
            self.game.soundWall.play()
        if self.y < 0:
            self.y = 0
            self.yVel *= -1
            self.game.soundWall.play()
        if self.y > self.game.screen.get_height() - 50:
            self.y = self.game.screen.get_height() - 50
            self.yVel *= -1
            self.game.soundWall.play()

    def make_snake_longer(self):
        self.length += 4


    def check_self_collision(self):
        for i, rect in enumerate(self.tail):
            newRect = rect.scale_by((i + 1) / self.length)
            if self.length - i > self.dangerLimit:
                if self.rect.colliderect(newRect):
                    return True

        return False

    def draw(self):
        self.draw_tail()
        self.draw_head()

    def draw_tail(self):
        for i, (rect, color) in enumerate(zip(self.tail, self.colorList)):

            newRect = rect.scale_by((i + 1) / self.length)
            colorBlendingCoef = (i / self.length)

            blendedColor = (
                color[0] * colorBlendingCoef,
                color[1] * colorBlendingCoef,
                color[2] * colorBlendingCoef
            )

            if self.length - i > self.dangerLimit:
                pygame.draw.rect(self.game.screen, (255, 100, 100), newRect.scale_by(1.2))

            pygame.draw.rect(self.game.screen, blendedColor, newRect)
    def draw_head(self):
        pygame.draw.rect(self.game.screen, (255, 255, 255), self.rect.scale_by(1.1))
        pygame.draw.rect(self.game.screen, (255, 255, 0), self.rect)
