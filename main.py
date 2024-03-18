
import asyncio

from scripts.game import Game


async def main():
    game = Game()
    await game.start_game()


if __name__ == "__main__":
    asyncio.run(main())
