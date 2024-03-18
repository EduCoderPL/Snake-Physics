
class GameScene:
    def __init__(self, game, gameStateManager):
        self.game = game
        self.gameStateManager = gameStateManager

    def run(self):
        self.game.update_input()
        self.game.update_game_logic()
        self.game.update_graphics()