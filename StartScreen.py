import asyncio
import random
import sys

import pygame

import client
from AStar import astar
from mapCreator import create_map
from mapDesign import map_maker


def start(game_size, resolution):
    """
          Description: This function is used to display the start screen of the
                    game. From here, players can choose between local or online
                    play, can create or load a custom map, and can set the game
                    difficulty. This start screen also visualizes our A*
                    algorithm working.

          Arguments:
            game_size (int): How many rows and columns there are
            resolution (int): How wide each node is

          Returns:
            map_select (string): Map difficulty chosen
            seed (int): Seed used to randomly create map
            player_number (int): the assigned player number of each player.
                By default, this value is -1 for local games.
            map_text (string): Name of map if custom map chosen. By default,
                this is set to an empty string, ""

    """
    pygame.init()

    # Fonts used in screen
    font = pygame.font.Font("media/ChakraPetch-Regular.ttf", 30)
    font_title = pygame.font.Font("media/ChakraPetch-Regular.ttf", 100)

    # Creates Pygame Surface
    screen = pygame.display.set_mode(
        (game_size * resolution, game_size * resolution))

    # Used to run main while loop
    start_screen = True

    # Used to toggle between local and multiplayer
    # And keep track of neccesary parameters
    mutli_select = "local"
    online = True
    difficulty = False
    player_number = -1

    # Used to determine what level of map to create
    map_select = "easy"

    # Should a new map be created for background
    # Stores if custom map us being used
    update_map = True
    custom_map = False
    keep_custom = False

    # Name of map to load
    map_text = ""

    # Contols the pathfinding visulaization
    speed = 5
    speed_count = 0
    route_count = 1

    while start_screen:

        # If a custom map has been chosen run this special process
        if custom_map:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # Push enter to after typing in map name
                    if event.key == pygame.K_RETURN:
                        map_select = "Custom"
                        # Used to keep track of path finding route
                        route = []

                        # Attempts to open the custom map
                        try:
                            map, __, begin, end = create_map(
                                map_select, game_size, resolution, "game",
                                0, map_text)
                            print("looking for route")
                            route = astar(map, begin[0], end[0], game_size,
                                          resolution)

                            # Makes it so that map doesnt update when
                            # finder reaches the end
                            keep_custom = True
                            update_map = False

                        # If cant open map then simply chose to make a new map
                        # background
                        except:
                            print("Could not load map")

                            # Needed so new map is created
                            keep_custom = False
                            update_map = True
                        custom_map = False

                        # Reset the parameters used to draw the finder
                        route_count = 0
                        speed_count = 0

                    else:
                        # This gets the text input from the user of name of map
                        map_text = map_text + event.unicode

        # If not a custom map then run the usual background map process
        if not custom_map:
            # If a new map needs to be created
            if update_map:
                # Create a random map
                # Special Parameter "start" means that no snake is made and
                # only on start
                map, __, begin, end = create_map(
                    map_select, game_size, resolution, "start",
                    random.randint(0, 123124131412), None)
                route = astar(map, begin, end, game_size, resolution)
                # Reset the parameters used to draw the finder
                route_count = 0
                speed_count = 0

                # If route has been succesfully returned draw the first square
                if route != 0:
                    map[route[0][0]][route[0][1]].path = True

                # Set so a new map is not created
                update_map = False

            # If a route has been returned and the finder is not at the end
            # Speed and speed counter are used to control how fast new square
            # is drawn
            if (route != 0 and
                    route_count < (len(route) - 1) and
                    speed_count % speed == 0):
                # Set next node in path to a path block
                map[route[route_count][0]][route[route_count][1]].path = True
                route_count += 1

                # This means that we have reached the goal and should make
                # a new map
                if not keep_custom and route_count == (len(route) - 1):
                    update_map = True

        # This updates the colours of all the map nodes
        for i in range(0, game_size):
            for j in range(0, game_size):
                # Checks if empty and sets colour to corresponding role of node
                map[i][j].set_empty()
                map[i][j].set_color()

                # Draws all of the nodes
                pygame.draw.rect(screen, map[i][j].color, (
                    i * resolution, j * resolution,
                    i * resolution + resolution,
                    j * resolution + resolution))

        # Custom map only available for local
        # Only lets user chose multiplayer if custom map not chosen
        if not custom_map:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and online:
                    key = event.key
                    # Local mode chosen
                    if key == pygame.K_RETURN and mutli_select == "local":
                        online = False
                        difficulty = True
                    # online mode chosen
                    elif key == pygame.K_RETURN and mutli_select == "online":
                        online = False
                        try:
                            map_select, seed, player_number = \
                                asyncio.get_event_loop().run_until_complete(
                                    client.start_game())
                            start_screen = False
                            break
                        except:
                            difficulty = True
                    elif key == pygame.K_1:
                        mutli_select = "local"
                    elif key == pygame.K_2:
                        mutli_select = "online"
                elif event.type == pygame.KEYDOWN and difficulty:
                    key = event.key
                    if key == pygame.K_RETURN:
                        seed = random.randint(0, 9999999)
                        start_screen = False
                        break
                    # Easy mode
                    elif key == pygame.K_1:
                        map_select = "easy"
                        update_map = True
                    # Medium mode
                    elif key == pygame.K_2:
                        map_select = "medium"
                        update_map = True
                    # Hard mode
                    if key == pygame.K_3:
                        map_select = "hard"
                        update_map = True
                    # Open the map maker screen
                    if key == pygame.K_c:
                        map_maker(game_size, resolution)
                    # Load up a custom map
                    if key == pygame.K_v:
                        custom_map = True
                        map_text = ""

        # Displays title
        text = font_title.render("A*STAR BATTLE", True, (244, 163, 0))
        text_rect = text.get_rect(
            center=(game_size * resolution / 2, game_size * resolution * 0.2))
        screen.blit(text, text_rect)

        # Displays sub-title
        text = font.render("Press Enter To PLay", True, (244, 163, 0))
        text_rect = text.get_rect(
            center=(game_size * resolution / 2, game_size * resolution * 0.3))
        screen.blit(text, text_rect)

        # Draw the rectangle across bottom of screen
        pygame.draw.rect(screen, (48, 48, 48), [
            0, game_size * resolution * 0.95,
            game_size * resolution,
            game_size * resolution * 0.05])

        # If still waiting for local/online choice
        if online:
            text = font.render(
                "'1' for Local '2' for online", True, (244, 163, 0))
            text_rect = text.get_rect(
                center=(game_size * resolution / 2,
                        game_size * resolution * 0.97))
            screen.blit(text, text_rect)

        # If local mode
        elif not online and difficulty:
            if not custom_map:
                # Display instruction
                text = font.render(
                    "'1'  Easy '2'  Medium '3' Hard 'C' Create 'V' Load",
                    True, (244, 163, 0))
                text_rect = text.get_rect(
                    center=(game_size * resolution / 2,
                            game_size * resolution * 0.97))
                screen.blit(text, text_rect)
            # if custom map needs to be loaded
            if custom_map:
                # Text associated with getting user input
                text = font.render(
                    "Enter name of map to Load:", True, (244, 163, 0))
                text_rect = text.get_rect(
                    center=(game_size * resolution / 2,
                            game_size * resolution * 0.05))
                screen.blit(text, text_rect)
                text = font.render(
                    map_text, True, (244, 163, 0))
                text_rect = text.get_rect(
                    center=(game_size * resolution / 2,
                            game_size * resolution * 0.1))
                screen.blit(text, text_rect)
                text = font.render(
                    "Enter to continue", True, (244, 163, 0))
                text_rect = text.get_rect(
                    center=(game_size * resolution / 2,
                            game_size * resolution * 0.97))
                screen.blit(text, text_rect)

        # Updates drawing
        pygame.display.update()
        speed_count += 1

    return map_select, seed, player_number, map_text
