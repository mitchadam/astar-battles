import sys

import pygame

from AStar import astar
from mapCreator import create_map


def game(game_size, resolution, map_select, seed, map_name):
    """
          Description: The main game loop

          Arguments:
            game_size (int): How many rows and columns there are
            resolution (int): How wide each node is
            map_select (string): Map difficulty chosen
            seed (int): Seed used to randomly create map
            map_name(string): Name of map if custom map chosen

          Returns:
            winner(string): Which player one
            win_msg(string): How the game ended

          """
    # Create Map of nodes
    map, walls, begin, end = create_map(map_select, game_size, resolution,
                                        "game", seed, map_name)

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(
        (game_size * resolution, game_size * resolution))
    pygame.display.set_caption('astar Battle!')

    # Loads the fonts
    font = pygame.font.Font("media/ChakraPetch-Regular.ttf", 30)

    # Determines whether the player moves
    global player_turn
    player_turn = [True, False]
    # Determines whether the finder moves
    global finder_turn
    finder_turn = [False, False]
    # This checks if a player can no longer move
    global check_trap_turn
    check_trap_turn = [False, False]

    def move_player(player_number, key):
        """
              Description: Moves the players snake

              Arguments:
                player_number (int): Which player to move
                key (string): which key was pressed for the move

              Returns:

              """

        # Depending on the player change what keys are used
        if player_number == 0:
            up = pygame.K_UP
            down = pygame.K_DOWN
            right = pygame.K_RIGHT
            left = pygame.K_LEFT

        elif player_number == 1:
            up = pygame.K_w
            down = pygame.K_s
            right = pygame.K_d
            left = pygame.K_a

        # If up
        if (key == up and
            (walls[player_number][0][1] - 1) != -1 and
            map[walls[player_number][0][0]][
                walls[player_number][0][1] - 1].empty):
            # Adds new wall above
            walls[player_number].insert(0,
                                        [walls[player_number][0][0],
                                         walls[player_number][0][1] - 1])
            # Gets rid of the last wall
            pop_item = walls[player_number].pop()
            # Updates the node of new wall
            map[walls[player_number][0][0]][
                walls[player_number][0][1]].player_wall[player_number] = True
            # Updates the node of removed wall
            map[pop_item[0]][pop_item[1]].player_wall[player_number] = False
            # Resets the colour of the new node roles
            map[walls[player_number][0][0]][
                walls[player_number][0][1]].set_empty()
            map[walls[player_number][0][0]][
                walls[player_number][0][1]].set_color()
            # Marks player turn as complete
            player_turn[player_number] = False
            # Player has moved
            check_trap_turn[player_number] = True
        # If down
        elif (key == down and
              (walls[player_number][0][1] + 1) != game_size and
              map[walls[player_number][0][0]][
                  walls[player_number][0][1] + 1].empty):
            # Adds new wall below
            walls[player_number].insert(0,
                                        [walls[player_number][0][0],
                                         walls[player_number][0][1] + 1])
            # Gets rid of the last wall
            pop_item = walls[player_number].pop()
            # Updates the node of new wall
            map[walls[player_number][0][0]][
                walls[player_number][0][1]].player_wall[player_number] = True
            # Updates the node of removed wall
            map[pop_item[0]][pop_item[1]].player_wall[player_number] = False
            # Resets the colour of the new node roles
            map[walls[player_number][0][0]][
                walls[player_number][0][1]].set_empty()
            map[walls[player_number][0][0]][
                walls[player_number][0][1]].set_color()
            # Marks player turn as complete
            player_turn[player_number] = False
            # Player has moved
            check_trap_turn[player_number] = True
        # If left
        elif (key == left and
              (walls[player_number][0][0] - 1) != -1 and
              map[walls[player_number][0][0] - 1][
                  walls[player_number][0][1]].empty):
            # Adds new wall left
            walls[player_number].insert(0,
                                        [walls[player_number][0][0] - 1,
                                         walls[player_number][0][1]])
            # Gets rid of the last wall
            pop_item = walls[player_number].pop()
            # Updates the node of new wall
            map[walls[player_number][0][0]][
                walls[player_number][0][1]].player_wall[player_number] = True
            # Updates the node of removed wall
            map[pop_item[0]][pop_item[1]].player_wall[player_number] = False
            # Resets the colour of the new node roles
            map[walls[player_number][0][0]][
                walls[player_number][0][1]].set_empty()
            map[walls[player_number][0][0]][
                walls[player_number][0][1]].set_color()
            # Marks player turn as complete
            player_turn[player_number] = False
            # Player has moved
            check_trap_turn[player_number] = True
        # If right
        elif (key == right and
              (walls[player_number][0][0] + 1) != game_size and
              map[walls[player_number][0][0] + 1][walls[
                                                  player_number][0][1]].empty):
            # Adds new wall right
            walls[player_number].insert(0,
                                        [walls[player_number][0][0] + 1,
                                         walls[player_number][0][1]])
            # Gets rid of the last wall
            pop_item = walls[player_number].pop()
            # Updates the node of new wall
            map[walls[player_number][0][0]][
                walls[player_number][0][1]].player_wall[player_number] = True
            # Updates the node of removed wall
            map[pop_item[0]][pop_item[1]].player_wall[player_number] = False
            # Resets the colour of the new node roles
            map[walls[player_number][0][0]][
                walls[player_number][0][1]].set_empty()
            map[walls[player_number][0][0]][
                walls[player_number][0][1]].set_color()
            # Marks player turn as complete
            player_turn[player_number] = False
            # Player has moved
            check_trap_turn[player_number] = True

    def check_trapped(player_number):
        """
              Description: Checks if a player is stick

              Arguments:
                player_number (int): Which player to check

              Returns:
                game(bool): Used to control main game loop
                winner(string): Which player one
                win_msg(string): How the game ended

              """

        # Used to display necessary info in the game over screen
        winner = -1
        win_msg = ""
        game = True

        # Update which player/finders turn it is
        check_trap_turn[player_number] = False
        finder_turn[player_number] = True

        # This checks if the player can no longer move
        if not (map[walls[player_number][0][0] - 1][
                    walls[player_number][0][1]].empty or
                map[walls[player_number][0][0] + 1][
                    walls[player_number][0][1]].empty or
                map[walls[player_number][0][0]][
                    walls[player_number][0][1] - 1].empty or
                map[walls[player_number][0][0]][
                    walls[player_number][0][1] + 1].empty):
            # if player is trapped end game
            game = False
            # Set message to correct player win/lose
            if player_number == 0:
                winner = "Orange Player!"
            elif player_number == 1:
                winner = "Blue Player!"
            win_msg = "A player got trapped! "

            # mUpdate the flag
            finder_turn[player_number] = False

        return game, winner, win_msg

    def move_finder(finder_number):
        """
        Description: Moves the finder

        Arguments:
            finder_number (int): Which finder to move

        Returns:
            game(bool): Used to control main game loop
            winner(string): Which player one
            win_msg(string): How the game ended

        """

        # Used to display necessary info in the game over screen
        game = True
        winner = -1
        win_msg = ""

        # Separate cases necessary for each finder as the flags set are
        # different for each finder and need to determine which player was
        # the winner Player 1 finder
        if finder_number == 0:
            # Call astar to obtain the path
            route = astar(map, begin[0], end[0], game_size, resolution)
            # Checks if a route has been found
            if route != 0:
                # Remove first spot as it is current finder position
                if len(route) > 1:
                    route.pop(0)
                # Select the next node to move to next turn
                next_spot = route[0]
                # Update the previous spot to path
                map[begin[0][0]][begin[0][1]].path = True
                # Update the finder location
                map[begin[0][0]][begin[0][1]].player1_finder = False
                map[next_spot[0]][next_spot[1]].player1_finder = True
                # Update the upcoming spot
                # Needed to be done with two next spots in order to correctly
                # end the game
                begin[0] = next_spot
                # Checks if the next spot is the end
                if begin[0][0] == end[0][0] and begin[0][1] == end[0][1]:
                    # end game and set win message and winner
                    game = False
                    winner = "Blue Player!"
                    win_msg = "A flag was captured! "

        # Player 1 finder
        elif finder_number == 1:
            # Call astar to obtain the path
            route = astar(map, begin[1], end[1], game_size, resolution)
            # Checks if a route has been found
            if route != 0:
                # Remove first spot as it is current finder position
                if len(route) > 1:
                    route.pop(0)
                # Select the next node to move to next turn
                next_spot = route[0]
                # Update the previous spot to path
                map[begin[1][0]][begin[1][1]].path = True
                # Update the finder location
                map[begin[1][0]][begin[1][1]].player2_finder = False
                map[next_spot[0]][next_spot[1]].player2_finder = True
                # Update the upcoming spot
                begin[1] = next_spot
                # Check if upcoming spot is end
                if begin[1][0] == end[1][0] and begin[1][1] == end[1][1]:
                    # End the game and set the winner
                    game = False
                    winner = "Orange Player!"
                    win_msg = "A flag was captured! "
        # Set the player turn to the other player
        player_turn[abs(finder_number - 1)] = True
        # Set that finder has moved
        finder_turn[finder_number] = False
        return game, winner, win_msg

    # Used to display necessary info in the game over screen
    winner = -1
    win_msg = ""
    game = True

    # main game loop
    while game:

        # Updates the position of the nodes to players walls
        for i in range(0, len(walls[0])):
            map[walls[0][i][0]][walls[0][i][1]].player1_wall = True
            map[walls[1][i][0]][walls[1][i][1]].player2_wall = True

        # This updates the colours of the nodes
        for i in range(0, game_size):
            for j in range(0, game_size):
                # Checks if empty and sets colour
                map[i][j].set_empty()
                map[i][j].set_color()

                # Draws all of the nodes
                pygame.draw.rect(screen, map[i][j].color, (i * resolution,
                                                           j * resolution,
                                                           i * resolution +
                                                           resolution,
                                                           j * resolution +
                                                           resolution))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Checks if player turn and key down (turn has been player)
            if event.type == pygame.KEYDOWN and player_turn[0]:
                key = event.key
                move_player(0, key)
            if event.type == pygame.KEYDOWN and player_turn[1]:
                key = event.key
                move_player(1, key)

        # Determines if a player is trapped
        if check_trap_turn[0]:
            game, winner, win_msg = check_trapped(0)
        elif check_trap_turn[1]:
            game, winner, win_msg = check_trapped(1)

        # Determines the finders turns and moves corresponding finder
        if finder_turn[0]:
            game, winner, win_msg = move_finder(0)
        elif finder_turn[1]:
            game, winner, win_msg = move_finder(1)

        # Check if player 1 turn
        if player_turn[0]:
            text = font.render("Blue", True, (89, 221, 255))
        # Check if player 2 turn
        elif player_turn[1]:
            text = font.render("Orange", True, (255, 89, 8))
        # Draw the players turn it is
        text_rect = text.get_rect(
            center=(game_size * resolution / 9, game_size * resolution / 25))
        screen.blit(text, text_rect)

        pygame.display.update()

    return winner, win_msg
