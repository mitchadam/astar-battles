import random
import sys

import pygame

from AStar import astar
from mapCreator import create_map


def wait_screen(player_number):
    """
          Description: This is used after player 1 connects to the online
                server. From here, player 1 can then select the game
                difficulty. Similar to the start function in StartScreen.py,
                this function also visualizes the A* algorithm.

          Arguments:
            player_number (int): the assigned player number of each player.

          Returns:
            difficulty (int): This value represents the chosen game difficutlty
                1 for easy, 2 for medium and 3 for hard.

          """
    pygame.init()

    # Loads fonts
    font = pygame.font.Font("media/ChakraPetch-Regular.ttf", 30)
    font_title = pygame.font.Font("media/ChakraPetch-Regular.ttf", 100)
    game_size = 25
    resolution = 32

    screen = pygame.display.set_mode(
        (game_size * resolution, game_size * resolution))

    # Used to control if difficulty has been set yet
    difficulty = -1

    # All used to control the background map
    map_select = "easy"
    route_count = 0
    speed_count = 0
    speed = 5
    update_map = True
    route = []

    # Main loop
    wait_screen_control = True
    while wait_screen_control:

        # New map needs to be created
        if update_map:
            map, __, begin, end = create_map(
                map_select, game_size, resolution, "start",
                random.randint(0, 123124131412), None)
            route = astar(map, begin, end, game_size, resolution)

            # Reset drawing parameters
            route_count = 0
            speed_count = 0

            # If route has been successfully found draw the first path
            if route != 0:
                map[route[0][0]][route[0][1]].path = True
                update_map = False

        speed_count += 1

        # If route and not at the end of the router
        # peedCounter and speed used to determine how fast path is drawn
        if (route != 0 and
                route_count < (len(route) - 1) and
                speed_count % speed == 0):
            # Set the corresponding map node to path
            map[route[route_count][0]][route[route_count][1]].path = True
            route_count += 1

            # This means reached the end of the route and new map needed
            if route_count == (len(route) - 1):
                update_map = True

        # This updates the colours of all the map nodes
        for i in range(0, game_size):
            for j in range(0, game_size):
                # Checks if empty and sets colour to corresponding node role
                map[i][j].set_empty()
                map[i][j].set_color()

                # Draws all of the nodes
                pygame.draw.rect(screen, map[i][j].color, (
                    i * resolution, j * resolution,
                    i * resolution + resolution,
                    j * resolution + resolution))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:

                # If difficulty has been set, can leave screen
                if event.key == pygame.K_RETURN and difficulty != -1:
                    wait_screen_control = False
                    break
                # Easy mode set
                if event.key == pygame.K_1:
                    difficulty = 1
                    map_select = "easy"
                    update_map = True
                # Medium mode set
                if event.key == pygame.K_2:
                    difficulty = 2
                    map_select = "medium"
                    update_map = True
                # Hard mode set
                if event.key == pygame.K_3:
                    difficulty = 3
                    map_select = "hard"
                    update_map = True

        # Draws the rectangle across bottom of screen
        pygame.draw.rect(screen, (48, 48, 48), [
            0, game_size * resolution * 0.95,
            game_size * resolution,
            game_size * resolution * 0.05])

        # Displays title
        text = font_title.render("MULTIPLAYER", True, (244, 163, 0))
        text_rect = text.get_rect(
            center=(game_size * resolution / 2,
                    game_size * resolution * 0.2))
        screen.blit(text, text_rect)

        # if the player is player 1 they get to determine the difficulty
        if player_number == 1:
            text = font.render("Press Enter To PLay", True, (244, 163, 0))
            text_rect = text.get_rect(
                center=(game_size * resolution / 2,
                        game_size * resolution * 0.3))
            screen.blit(text, text_rect)

            text = font.render(
                "'1'  Easy '2'  Medium '3' Hard", True, (244, 163, 0))
            text_rect = text.get_rect(
                center=(game_size * resolution / 2,
                        game_size * resolution * 0.97))
            screen.blit(text, text_rect)

        pygame.display.update()
        pygame.display.flip()

    return difficulty
