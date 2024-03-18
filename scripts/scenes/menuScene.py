class MenuScene:
    def __init__(self, game, gameStateManager):
        self.game = game
        self.gameStateManager = gameStateManager

    def run(self):
        self.game.show_main_menu()