import asyncio

import pygame
from pygame.locals import *
from constants import *
from scripts.scenes.gameScene import GameScene
from scripts.scenes.gameSceneManager import GameSceneManager
from scripts.scenes.menuScene import MenuScene
from scripts.gameObjects.snake import Snake
from scripts.gameObjects.apple import Apple

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 48)

        self.gameStateManager = GameSceneManager('menu')
        self.sceneMenu = MenuScene(self, self.gameStateManager)
        self.sceneGame = GameScene(self, self.gameStateManager)

        self.states = {'menu': self.sceneMenu, 'game': self.sceneGame}

        self.player = Snake(300, 300, self)
        self.apple = Apple(600, 600, self)
        self.points = 0
        self.running = True

    async def start_game(self):
        await self.game_loop()

    async def game_loop(self):

        while self.running:
            self.trigger_close_game()
            self.states[self.gameStateManager.get_state()].run()

            pygame.display.flip()
            self.clock.tick(60)
            await asyncio.sleep(0)

    def trigger_close_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

    def update_input(self):
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            self.player.yVel -= 0.5
        if keys[K_s]:
            self.player.yVel += 0.5
        if keys[K_a]:
            self.player.xVel -= 0.5
        if keys[K_d]:
            self.player.xVel += 0.5

    def update_game_logic(self):
        self.player.update()
        self.apple.update()
        if self.player.check_self_collision():
            self.gameStateManager.set_state('menu')

        if self.player.rect.colliderect(self.apple.rect):
            self.player.make_snake_longer()
            self.apple.change_position()
            self.points += 1

    def update_graphics(self):
        self.screen.fill((0, 0, 0))
        self.player.draw()
        self.apple.draw()

        text = self.font.render(f'Score: {self.points}', True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def show_main_menu(self):

        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            self.gameStateManager.set_state('game')
            self.reset_game()
        if keys[K_ESCAPE]:
            self.running = False

        self.screen.fill((0, 0, 0))
        menu_text = self.font.render("Snake Game", True, (255, 255, 255))
        menu_text_rect = menu_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
        self.screen.blit(menu_text, menu_text_rect)

        start_text = self.font.render("Press SPACE to start", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
        self.screen.blit(start_text, start_text_rect)

        start_text = self.font.render("Press Esc to exit.", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 150))
        self.screen.blit(start_text, start_text_rect)

    def reset_game(self):
        self.player = Snake(300, 300, self)
        self.apple = Apple(600, 600, self)
        self.points = 0
        self.running = True