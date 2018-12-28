import pickle
import sys

import pygame

from mapCreator import create_map


class CustomMap:
    """
          Description: This class is used to create a map object so it can be
                saved.

          Arguments:
            map (list): This is a list of all map nodes

    """

    def __init__(self, map, begin):
        # Stores array of map nodes
        self.map = map
        # Stores finder beginning locations
        self.begin = begin


def map_maker(game_size, resolution):
    """
          Description: The screen when a user wants to create a custom map

          Arguments:
            game_size (int): How many rows and columns there are
            resolution (int): How wide each node is

          Returns:
            None

    """
    pygame.init()

    # Create surface
    screen = pygame.display.set_mode(
        (game_size * resolution, game_size * resolution))
    screen.fill((255, 255, 255))

    # Load fonts
    font = pygame.font.Font("media/ChakraPetch-Regular.ttf", 30)

    # Keep track if new map needs to be created
    update_map = True

    # Keeps track of where finders are added
    begin = []

    # Used in saving the map
    save_map = False

    # Name of map
    map_text = ""

    def map_saver(map, begin, text):
        """
              Description: This saves the  custom map to a file for later use

              Arguments:
                map (list): List of all map nodes
                begin (tuple): contains the x y coordinates of the beginning
                text (string): Name of map

              Returns:

        """
        # Creates object to save
        custom_map1 = CustomMap(map, begin)

        # Creates file name
        file_name = text + ".txt"

        # Attempts to save map with pickle
        try:
            with open(file_name, 'wb') as fid:
                pickle.dump(custom_map1, fid)
            print("Saved map")
        except:
            print("Failed to save map")

    # Main loop
    map_make = True
    while map_make:

        # Creates a new blank map array if needed
        # Just returns a blank map with snakes and end flag
        if update_map:
            map, __, __, __ = create_map(
                "maker", game_size, resolution, "game", 0, None)
            update_map = False

        # If the user is not attempting to save
        # Run the creation process
        if not save_map:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # Press return to exit without saving
                    if event.key == pygame.K_RETURN:
                        map_make = False
                        break
                    # press s to save the map
                    if event.key == pygame.K_s:
                        save_map = True

                    # Places the first players finder down
                    if event.key == pygame.K_1:
                        mouse_pos = pygame.mouse.get_pos()
                        m_pos = [mouse_pos[0], mouse_pos[1]]

                        # Scaled the mouse position to correspond to nodes
                        m_pos[0] = round(m_pos[0] / resolution)
                        m_pos[1] = round(m_pos[1] / resolution)

                        # Update the node
                        map[m_pos[0]][m_pos[1]].player1_finder = True
                        begin.append((m_pos[0], m_pos[1]))

                    # Places the second players finder down
                    if event.key == pygame.K_2:
                        mouse_pos = pygame.mouse.get_pos()
                        m_pos = [mouse_pos[0], mouse_pos[1]]

                        # Scaled the mouse position to correspond to nodes
                        m_pos[0] = round(m_pos[0] / resolution)
                        m_pos[1] = round(m_pos[1] / resolution)

                        # Update the node
                        map[m_pos[0]][m_pos[1]].player2_finder = True
                        begin.append((m_pos[0], m_pos[1]))

                # Press to place a barriers
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    m_pos = [mouse_pos[0], mouse_pos[1]]

                    # Scaled the mouse position to correspond to nodes
                    m_pos[0] = round(m_pos[0] / resolution)
                    m_pos[1] = round(m_pos[1] / resolution)

                    # Update the node
                    if m_pos[0] < game_size and m_pos[1] < game_size:
                        map[m_pos[0]][m_pos[1]].barrier = True

        # User is trying to save the map
        if save_map:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Trigger the pickling and exit the map creator screen
                        map_saver(map, begin, map_text)
                        map_make = False
                        break
                    else:
                        # Get the name of the map to save the map as
                        map_text = map_text + event.unicode

        # Updates all the nodes for drawing purposes
        for i in range(0, game_size):
            for j in range(0, game_size):
                # Checks if empty and sets colour
                map[i][j].set_empty()
                map[i][j].set_color()

                # Draws all of the nodes
                pygame.draw.rect(screen, map[i][j].color, (
                    i * resolution, j * resolution,
                    i * resolution + resolution,
                    j * resolution + resolution))

        # Creates the rectangle along the bottom of the screen
        pygame.draw.rect(screen, (48, 48, 48), [
            0, game_size * resolution * 0.95,
            game_size * resolution, game_size * resolution * 0.05])

        # Displays the text when user is saving
        # ie the name of map and prompt of what the name should be
        if save_map:
            if CustomMap:
                text = font.render(
                    "Enter name of map to save:", True, (244, 163, 0))
                text_rect = text.get_rect(center=(game_size * resolution / 2,
                                          game_size * resolution * 0.05))
                screen.blit(text, text_rect)
                text = font.render(
                    map_text, True, (244, 163, 0))
                text_rect = text.get_rect(center=(game_size * resolution / 2,
                                          game_size * resolution * 0.1))
                screen.blit(text, text_rect)
                text = font.render(
                    "Press Enter to continue", True, (244, 163, 0))
                text_rect = text.get_rect(
                    center=(game_size * resolution / 2,
                            game_size * resolution * 0.97))
                screen.blit(text, text_rect)
        # Display creation instructions
        else:
            text = font.render("'S' save;'Enter' exit;'1' Blue flag '2';" +
                               "Orange flag;'Press' Barrier",
                               True, (244, 163, 0))
            text_rect = text.get_rect(
                center=(game_size * resolution / 2,
                        game_size * resolution * 0.97))
            screen.blit(text, text_rect)

        pygame.display.update()
    return
