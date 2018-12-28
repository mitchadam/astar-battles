import asyncio

import gameOnline
from Game import game
from GameOver import over
from StartScreen import start

if __name__ == "__main__":

    # Sets screen size parameters
    game_size = 25
    resolution = 32

    # Wins of Blue and Orange Players
    win_count = [0, 0]

    playGame = True
    while playGame:

        # Loads the start screen
        # - map_select is easy/medium/hard/custom
        # - seed is used to randomly generate map
        # - player_number if multi-player, given by server
        # - map_name if custom map used
        map_select, seed, player_number, map_name = start(game_size,
                                                          resolution)

        # Runs the local game
        if player_number == -1:
            winner, win_msg = game(game_size, resolution, map_select,
                                   seed, map_name)
        # Runs the multi-player game
        else:
            winner, win_msg = asyncio.get_event_loop().run_until_complete(
                gameOnline.game(game_size, resolution, map_select,
                                seed, player_number - 1))

        # Runs the Game Over screen
        win_count = over(game_size, resolution, winner, win_msg, win_count)
