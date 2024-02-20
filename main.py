import random

import pygame
from pygame.locals import *


class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.xVel = 0
        self.yVel = 0

        self.rect = Rect(self.x, self.y, 50, 50)

        self.tail = []
        self.colorList = []
        self.length = 5

        self.dangerLimit = 60
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
        if self.x > SCREEN_WIDTH - 50:
            self.x = SCREEN_WIDTH - 50
            self.xVel *= -1
        if self.y < 0:
            self.y = 0
            self.yVel *= -1
        if self.y > SCREEN_HEIGHT - 50:
            self.y = SCREEN_HEIGHT - 50
            self.yVel *= -1

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
                pygame.draw.rect(screen, (255, 100, 100), newRect.scale_by(1.2))

            pygame.draw.rect(screen, blendedColor, newRect)
    def draw_head(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect.scale_by(1.1))
        pygame.draw.rect(screen, (255, 255, 0), self.rect)

class Apple:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = Rect(self.x, self.y, 50, 50)

        self.xVel = 0
        self.yVel = 0

        self.state = 0

    def change_position(self):
        self.x = random.randint(50, SCREEN_WIDTH - 50)
        self.y = random.randint(50, SCREEN_HEIGHT - 50)
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

        if self.x > SCREEN_WIDTH - 50:
            self.x = SCREEN_WIDTH - 50
            self.xVel *= -1

        if self.y < 0:
            self.y = 0
            self.yVel *= -1

        if self.y > SCREEN_HEIGHT - 50:
            self.y = SCREEN_HEIGHT - 50
            self.yVel *= -1

    def move_fixed_gravity(self):
        self.yVel += 0.1

        self.x += self.xVel
        self.y += self.yVel

        if self.x < 0:
            self.x = 0
            self.xVel *= -1

        if self.x > SCREEN_WIDTH - 50:
            self.x = SCREEN_WIDTH - 50
            self.xVel *= -1

        if self.y < 0:
            self.y = 0
            self.yVel = 0

        if self.y > SCREEN_HEIGHT - 50:
            self.y = SCREEN_HEIGHT - 50
            self.yVel *= -3

    def update(self):
        if self.state == 1:
            self.move_fixed()
        if self.state == 2:
            self.move_fixed_gravity()

        self.rect = Rect(self.x, self.y, 50, 50)
    def draw(self):
        pygame.draw.ellipse(screen, (255, 0, 0), self.rect)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 48)

# PLAYER:
player = Snake(300, 300)
apple = Apple(600, 600)

points = 0

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    keys = pygame.key.get_pressed()

    if keys[K_w]:
        player.yVel -= 0.5
    if keys[K_s]:
        player.yVel += 0.5
    if keys[K_a]:
        player.xVel -= 0.5
    if keys[K_d]:
        player.xVel += 0.5

    player.update()

    apple.update()


    if player.check_self_collision():
        running = False
    if player.rect.colliderect(apple.rect):

        player.make_snake_longer()
        apple.change_position()

        points += 1

    screen.fill((0, 0, 0))
    player.draw()
    apple.draw()

    text = font.render(f'Score: {points}', True, (255, 255, 255))
    screen.blit(text, (10, 10))

    clock.tick(60)
    pygame.display.flip()

pygame.quit()