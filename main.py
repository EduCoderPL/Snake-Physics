import random
import pygame
from pygame.locals import *
from constants import *
from snake import Snake
from apple import Apple





class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 48)
        self.player = Snake(300, 300, self)
        self.apple = Apple(600, 600, self)
        self.points = 0

        self.game_loop()
    def game_loop(self):
        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            # ------------- CONTROLS --------------- #
            keys = pygame.key.get_pressed()

            if keys[K_w]:
                self.player.yVel -= 0.5
            if keys[K_s]:
                self.player.yVel += 0.5
            if keys[K_a]:
                self.player.xVel -= 0.5
            if keys[K_d]:
                self.player.xVel += 0.5

            # ------------- GAME LOGIC --------------- #
            self.player.update()
            self.apple.update()

            if self.player.check_self_collision():
                running = False

            if self.player.rect.colliderect(self.apple.rect):

                self.player.make_snake_longer()
                self.apple.change_position()

                self.points += 1

            # ------------- GRAPHICS --------------- #
            self.screen.fill((0, 0, 0))
            self.player.draw()
            self.apple.draw()

            text = self.font.render(f'Score: {self.points}', True, (255, 255, 255))
            self.screen.blit(text, (10, 10))

            # ------------- GAME UPDATE --------------- #
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


game = Game()