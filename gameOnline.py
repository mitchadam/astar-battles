import sys

import pygame
import websockets

from AStar import astar
from mapCreator import create_map


async def game(game_size, resolution, map_select, seed, player_number):
    """
         Description: The is the online main game loop. Uses async in order to
                       wait for player action

         Arguments:
           game_size (int): How many rows and columns there are
           resolution (int): How wide each node is drawn
           map_select (string): Map difficulty chosen
           seed (int): Seed used to randomly create map
           player_number (int): Which player to control

         Returns:
           winner (string): Which player won
           win_msg (string): How the game ended

    """
    print("Start Game")
    # Connects to server using websockets asynchronously
    async with websockets.connect('ws://localhost:8888/play') as websocket:
        # awaits for the Paired confirmation from server
        paired = await websocket.recv()
        print(paired)
        # awaits for the Paired confirmation from server for player 2
        if paired == "2":
            paired = await websocket.recv()
            print("Round 2 " + paired)

        # Initializes the map features
        global map
        global walls
        global begin
        global end
        global waiting
        # sets the initial waiting states for player turns
        if player_number == 0:
            waiting = True
        elif player_number == 1:
            waiting = False

        # Generates a map using a common seed between player 1 and player 2
        map, walls, begin, end = create_map(map_select, game_size,
                                            resolution, "game", seed, None)

        # Initialize pygame
        pygame.init()
        # Initializes the display surface of pygame
        screen = pygame.display.set_mode(
            (game_size * resolution, game_size * resolution))
        pygame.display.set_caption('astar Battle!')
        # Load fonts
        font = pygame.font.Font("media/ChakraPetch-Regular.ttf", 30)

        # initializes
        global winner
        winner = -1
        global win_msg
        win_msg = ""

        async def wait_opponent():
            """
                  Description: Waits for the opponent to move and then will
                            move the opponent on the client game screen

                  Arguments:
                    None

                  Returns:
                    None

            """
            # waits to receive the opponent's move from the server
            move = await websocket.recv()

            # Moves the opponent
            if move == "up":
                move_opponent(abs(player_number - 1), pygame.K_w)
            if move == "down":
                move_opponent(abs(player_number - 1), pygame.K_s)
            if move == "left":
                move_opponent(abs(player_number - 1), pygame.K_a)
            if move == "right":
                move_opponent(abs(player_number - 1), pygame.K_d)

        def move_opponent(player_number, key):
            """
                  Description: Moves the opponent once their moved is received

                  Arguments:
                    player_number (int): Which player to move
                    key (pygame constant): the move that the opponent took

                  Returns:
                    None

            """

            # Sets movement keys
            up = pygame.K_w
            down = pygame.K_s
            right = pygame.K_d
            left = pygame.K_a

            # Moves the opponent up and ensure opponent is not blocked
            if (key == up and
                (walls[player_number][0][1] - 1) != -1 and
                map[walls[player_number][0][0]][
                    walls[player_number][0][1] - 1].empty):
                # Adds new wall above
                walls[player_number].insert(0, [walls[player_number][0][0],
                                            walls[player_number][0][1] - 1])
                # Gets rid of the last wall
                pop_item = walls[player_number].pop()
                # Updates the node of new wall
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].player_wall[
                    player_number] = True
                # Updates the node of removed wall
                map[pop_item[0]][pop_item[1]].player_wall[
                                              player_number] = False
                # Resets the colour of the new node roles
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].set_empty()
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].set_color()

            # Moves the opponent down and ensure opponent is not blocked
            elif (key == down and
                  (walls[player_number][0][1] + 1) != game_size and
                  map[walls[player_number][0][0]][
                      walls[player_number][0][1] + 1].empty):
                # Adds new wall below
                walls[player_number].insert(0, [walls[player_number][0][0],
                                            walls[player_number][0][1] + 1])
                # Gets rid of the last wall
                pop_item = walls[player_number].pop()
                # Updates the node of new wall
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].player_wall[
                    player_number] = True
                # Updates the node of removed wall
                map[pop_item[0]][pop_item[1]].player_wall[
                                              player_number] = False
                # Resets the colour of the new node roles
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].set_empty()
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].set_color()

            # Moves the opponent left and ensure opponent is not blocked
            elif (key == left and
                  (walls[player_number][0][0] - 1) != -1 and
                  map[walls[player_number][0][0] - 1][
                      walls[player_number][0][1]].empty):
                # Adds new wall left
                walls[player_number].insert(0, [walls[player_number][0][0] - 1,
                                            walls[player_number][0][1]])
                # Gets rid of the last wall
                pop_item = walls[player_number].pop()
                # Updates the node of new wall
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].player_wall[
                    player_number] = True
                # Updates the node of removed wall
                map[pop_item[0]][pop_item[1]].player_wall[
                                              player_number] = False
                # Resets the colour of the new node roles
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].set_empty()
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].set_color()

            # Moves the opponent right and ensure opponent is not blocked
            elif (key == right and
                  (walls[player_number][0][0] + 1) != game_size and
                  map[walls[player_number][0][0] + 1][
                      walls[player_number][0][1]].empty):
                # Adds new wall right
                walls[player_number].insert(0, [walls[player_number][0][0] + 1,
                                            walls[player_number][0][1]])
                # Gets rid of the last wall
                pop_item = walls[player_number].pop()
                # Updates the node of new wall
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].player_wall[
                    player_number] = True
                # Updates the node of removed wall
                map[pop_item[0]][pop_item[1]].player_wall[
                                              player_number] = False
                # Resets the colour of the new node roles
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].set_empty()
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].set_color()

        async def move_player(player_number):
            """
                  Description: Moves the player's snake

                  Arguments:
                    player_number (int): Which player to move

                  Returns:
                    None

          """
            # waits for input from the player to move and end the players turn
            key = "INVALID"
            while key == "INVALID":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    # Checks if player key down
                    if event.type == pygame.KEYDOWN:
                        key = event.key

            # Sets the movement keys
            up = pygame.K_w
            down = pygame.K_s
            right = pygame.K_d
            left = pygame.K_a
            # Defaults move to invalid
            move = "invalid"

            # Moves the player up and ensure player is not blocked
            # Also set move to be messaged to server
            if (key == up and
                (walls[player_number][0][1] - 1) != -1 and
                map[walls[player_number][0][0]][
                    walls[player_number][0][1] - 1].empty):
                # Adds new wall up
                walls[player_number].insert(0, [walls[player_number][0][0],
                                            walls[player_number][0][1] - 1])
                # Gets rid of the last wall
                pop_item = walls[player_number].pop()
                # Updates the node of new wall
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].player_wall[
                    player_number] = True
                # Updates the node of removed wall
                map[pop_item[0]][pop_item[1]].player_wall[
                                              player_number] = False
                # Resets the colour of the new node roles
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].set_empty()
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].set_color()
                move = "up"

            # Moves the player down and ensure player is not blocked
            # Also set move to be messaged to server
            elif (key == down and
                  (walls[player_number][0][1] + 1) != game_size and
                  map[walls[player_number][0][0]][
                      walls[player_number][0][1] + 1].empty):
                # Adds new wall down
                walls[player_number].insert(0, [walls[player_number][0][0],
                                            walls[player_number][0][1] + 1])
                # Gets rid of the last wall
                pop_item = walls[player_number].pop()
                # Updates the node of new wall
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].player_wall[
                    player_number] = True
                # Updates the node of removed wall
                map[pop_item[0]][pop_item[1]].player_wall[
                                              player_number] = False
                # Resets the colour of the new node roles
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].set_empty()
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].set_color()
                move = "down"

            # Moves the player left and ensure player is not blocked
            # Also set move to be messaged to server
            elif (key == left and
                  (walls[player_number][0][0] - 1) != -1 and
                  map[walls[player_number][0][0] - 1][
                      walls[player_number][0][1]].empty):
                # Adds new wall left
                walls[player_number].insert(0, [walls[player_number][0][0] - 1,
                                            walls[player_number][0][1]])
                # Gets rid of the last wall
                pop_item = walls[player_number].pop()
                # Updates the node of new wall
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].player_wall[
                    player_number] = True
                # Updates the node of removed wall
                map[pop_item[0]][pop_item[1]].player_wall[
                                              player_number] = False
                # Resets the colour of the new node roles
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].set_empty()
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].set_color()
                move = "left"

            # Moves the player right and ensure player is not blocked
            # Also set move to be messaged to server
            elif (key == right and
                  (walls[player_number][0][0] + 1) != game_size and
                  map[walls[player_number][0][0] + 1][
                      walls[player_number][0][1]].empty):
                # Adds new wall right
                walls[player_number].insert(0, [walls[player_number][0][0] + 1,
                                            walls[player_number][0][1]])
                # Gets rid of the last wall
                pop_item = walls[player_number].pop()
                # Updates the node of new wall
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].player_wall[
                                                player_number] = True
                # Updates the node of removed wall
                map[pop_item[0]][pop_item[1]].player_wall[
                                              player_number] = False
                # Resets the colour of the new node roles
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].set_empty()
                map[walls[player_number][0][0]][
                    walls[player_number][0][1]].set_color()
                move = "right"

            # Sends move to server if the move is valid
            if move != "invalid":
                await websocket.send(move)
            # If move is invalid, calls move_player again to get valid move
            else:
                await move_player(player_number)

        # Checks if the user cannot move
        def check_trapped(player_number):
            """
              Description: Checks if a player is trapped

              Arguments:
                player_number (int): Which player to check

              Returns:
                game (bool): Used to control main game loop
                winner (string): Which player won
                win_msg (string): How the game ended

            """
            winner = -1
            win_msg = ""
            # If user cannot move
            if not (map[walls[player_number][0][0] - 1][
                        walls[player_number][0][1]].empty or
                    map[walls[player_number][0][0] + 1][
                        walls[player_number][0][1]].empty or
                    map[walls[player_number][0][0]][
                        walls[player_number][0][1] - 1].empty or
                    map[walls[player_number][0][0]][
                        walls[player_number][0][1] + 1].empty):
                # Set the winner and win message
                if player_number == 0:
                    winner = "Orange Player!"
                elif player_number == 1:
                    winner = "Blue Player!"
                win_msg = "A player got trapped! "
            return winner, win_msg

        # Moves the finder
        def moveFinder(finder_number):
            """
                Description: Moves the finder

                Arguments:
                    finder_number (int): Which player's finder to move

                Returns:
                    gam e(bool): Used to control main game loop
                    winner (string): Which player won
                    win_msg (string): How the game ended

            """
            winner = -1
            win_msg = ""
            # Moves player 1's finder
            if finder_number == 0:
                # Get the route using astar
                route = astar(map, begin[0], end[0], game_size, resolution)
                # Check if a route was found
                if route != 0:
                    if len(route) > 1:
                        # Remove the first node as it is current position
                        route.pop(0)
                    # Select the next node to move to next turn
                    next_spot = route[0]
                    # Update the previous spot to path
                    map[begin[0][0]][begin[0][1]].path = True
                    map[begin[0][0]][begin[0][1]].player1_finder = False
                    map[next_spot[0]][next_spot[1]].player1_finder = True
                    # Update the upcoming spot
                    # Needed to be done with two next spots in order to
                    # correctly end the game
                    begin[0] = next_spot
                    # Checks if next spot is end
                    if begin[0][0] == end[0][0] and begin[0][1] == end[0][1]:
                        # Set the winner and win message
                        winner = "Blue Player!"
                        win_msg = "A flag was captured! "

            # Moves player 2's finder
            elif finder_number == 1:
                # Get the route using astar
                route = astar(map, begin[1], end[1], game_size, resolution)
                # Check if a route was found
                if route != 0:
                    if len(route) > 1:
                        # Remove the first node as it is current position
                        route.pop(0)
                    # Select the next node to move to next turn
                    next_spot = route[0]
                    # Update the previous spot to path
                    map[begin[1][0]][begin[1][1]].path = True
                    map[begin[1][0]][begin[1][1]].player2_finder = False
                    map[next_spot[0]][next_spot[1]].player2_finder = True
                    # Update the upcoming spot
                    # Needed to be done with two next spots in order to
                    # correctly end the game
                    begin[1] = next_spot
                    # Check if finder is at the end
                    if begin[1][0] == end[1][0] and begin[1][1] == end[1][1]:
                        # Set winner and win message
                        winner = "Orange Player!"
                        win_msg = "A flag was captured! "
            return winner, win_msg

        def update_display():
            """
                  Description: Updates all items on the map for drawing

                  Arguments:
                    None

                  Returns:
                    None

            """

            # Updates the player_walls position
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

            # Prints which players turn it is in top corner
            if player_number == 0 and waiting:
                text = font.render("Blue", True, (89, 221, 255))
            if player_number == 0 and not waiting:
                text = font.render("Waiting...", True, (255, 89, 8))
            if player_number == 1 and waiting:
                text = font.render("Orange", True, (255, 89, 8))
            if player_number == 1 and not waiting:
                text = font.render("Waiting...", True, (89, 221, 255))

            text_rect = text.get_rect(
                center=(game_size * resolution / 9,
                        game_size * resolution / 25))
            screen.blit(text, text_rect)

            pygame.display.update()
            pygame.display.flip()

        # Draw display initially
        update_display()
        clock = pygame.time.Clock()
        # Main loop
        while winner == -1:
            # Set max fps
            clock.tick(60)

            # Controls player 1's turn
            if player_number == 0:
                waiting = False
                # Wait for player to move
                await move_player(player_number)
                # Check if player 1 trapped
                winner, win_msg = check_trapped(0)
                # End game if winner
                if winner != -1:
                    break
                # Move player 1's finder
                winner, win_msg = moveFinder(0)
                # End game if winner
                if winner != -1:
                    break
                # update display to shove moved players and finders
                update_display()
                waiting = True
                # Wait for opponent to move
                await wait_opponent()
                # check if player 2 trapped
                winner, win_msg = check_trapped(1)
                if winner != -1:
                    break
                # Move player 2's finder
                winner, win_msg = moveFinder(1)
                # End game if winner
                if winner != -1:
                    break
                # update display to shove moved players and finders
                update_display()

            # Controls player 2's turn
            if player_number == 1:
                waiting = True
                # Wait for opponent to move
                await wait_opponent()
                # check if player 1 trapped
                winner, win_msg = check_trapped(0)
                # End game if winner
                if winner != -1:
                    break
                # Move player 1's finder
                winner, win_msg = moveFinder(0)
                # End game if winner
                if winner != -1:
                    break
                # update display to shove moved players and finders
                update_display()
                waiting = False
                # Wait for player to move
                await move_player(player_number)
                # Check if player 2 trapped
                winner, win_msg = check_trapped(1)
                # End game if winner
                if winner != -1:
                    break
                # Move player 2's finder
                winner, win_msg = moveFinder(1)
                # End game if winner
                if winner != -1:
                    break
                # update display to shove moved players and finders
                update_display()

        return winner, win_msg
