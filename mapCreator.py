import pickle
import random

from node import Node


def create_map(type_of_map, game_size, resolution, screen, seed, text):
    """
          Description: Creates all maps

          Arguments:
            type_of_map (string): The difficulty of map chose
            game_size (int): How many rows and columns there are
            resolution (int): How wide each node
            screen (string): What the map is going to be used for, determines
                                what is and is not drawn
            seed(int): Used to create the random barriers
            text(string): name of map if custom map is used


          Returns:
            maps (list): List of all map node
            begin(tuple): x and y coordinates of start
            walls(list): List of location of player walls
            end(tuple): x and y coordinates of end

    """
    # Sets the random seed when playing multiplayer to create common map
    random.seed(seed)

    # Used for drawing
    center = round(game_size / 2)
    quarter = round(center / 2)

    # Keeps track of map additions
    # ie walls barriers etc
    walls = []
    begin = []
    end = []

    # Sets the background array of nodes
    # everything to do with the map is stored in this
    map = [[0 for x in range(game_size + 1)] for y in range(game_size + 1)]
    for i in range(0, game_size + 1):
        for j in range(0, game_size + 1):
            # Initially all nodes have no role
            map[i][j] = Node(False, False, False, False,
                             False, False, False, False)

    # If game is selected snakes and 2 ends are drawn in
    if screen == "game":
        # Easy mode - no barriers and everything is pre-set
        if type_of_map == "easy":
            # Sets position of each playerFinder
            # For easy these are fixed
            map[1][center].player1_finder = True
            map[game_size - 2][center].player2_finder = True
            # Begin is used for path finding
            begin = [(1, center), (round(game_size - 2), center)]

        # Medium or hard - has barriers and random start end
        if type_of_map == "hard" or type_of_map == "medium":
            # Randomly sets the first player finders start
            x = random.randint(0, game_size - 1)
            y = random.randint(0, game_size - 1)
            map[x][y].player1_finder = True
            # Begin is used for path finding
            begin.append((x, y))

            # Randomly sets the second players finder
            x = random.randint(0, game_size - 1)
            y = random.randint(0, game_size - 1)
            map[x][y].player2_finder = True
            # Begin is used for path finding
            begin.append((x, y))

        # This means that a custom map needs to be loaded
        if type_of_map == "Custom":

            # Get the text argument
            file_name = str(text) + ".txt"

            # Attempt to open map name
            try:
                with open(file_name, "rb") as fid:
                    # Loads the map object with pickle
                    map_object = pickle.load(fid)
                    print("Map did open")
                    # Sets it to the main map
                    map = map_object.map
                    # Begin and end used for path finding
                    begin = map_object.begin
            except:
                print("Map did not open")

        # Sets the position of the player walls
        player2_walls = [[quarter, center - 2], [quarter, center - 1],
                         [quarter, center], [quarter, center + 1],
                         [quarter, center + 2]]
        player1_walls = [[quarter * 3, center - 2], [quarter * 3, center - 1],
                         [quarter * 3, center], [quarter * 3, center + 1],
                         [quarter * 3, center + 2]]
        walls = [player1_walls, player2_walls]

        # Sets the position of the players flags
        # These are always fixed
        map[center][center].player1_flag = True
        map[center][center].player2_flag = True
        # Sets the end used for path finding
        end = [(center, center), (center, center)]

        # Sets the corresponding walls the wall nodes in the map
        for i in range(0, len(walls[0])):
            map[walls[0][i][0]][walls[0][i][1]].player_wall[0] = True
            map[walls[1][i][0]][walls[1][i][1]].player_wall[1] = True

    # This means that only one start point and no snake is drawn
    # Used only for visual purposes
    if screen == "start":
        # Randomly sets the flag
        x = random.randint(0, game_size - 1)
        y = random.randint(0, game_size - 1)
        map[x][y].player1_flag = True
        end = (x, y)

        # Randomly sets the finder
        x = random.randint(0, game_size - 1)
        y = random.randint(0, game_size - 1)
        map[x][y].player1_finder = True
        begin = (x, y)

    # This sets the barriers for medium and hard mode
    if type_of_map == "medium":
        # Medium has 5% barriers
        for i in range(0, round(game_size * resolution * 0.05)):
            add_barrier = False
            # this continues to randomly add a barrier
            # until empty position is found
            while not add_barrier:
                x = random.randint(0, game_size - 1)
                y = random.randint(0, game_size - 1)
                map[x][y].set_empty()
                # Checks if node is empty
                if map[x][y].empty:
                    map[x][y].barrier = True
                    add_barrier = True
    elif type_of_map == "hard":
        # Hard has 15% barrier
        for i in range(0, round(game_size * resolution * 0.15)):
            add_barrier = False
            # this continues to randomly add a barrier
            # until empty position is found
            while not add_barrier:
                x = random.randint(0, game_size - 1)
                y = random.randint(0, game_size - 1)
                # Checks if node is empty
                map[x][y].set_empty()
                if map[x][y].empty:
                    map[x][y].barrier = True
                    add_barrier = True

    return map, walls, begin, end
