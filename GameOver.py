import sys

import pygame


def over(game_size, resolution, winner, win_msg, win_count):
    """
        Description: The screen when the game is over

        Arguments:
          game_size (int): How many rows and columns there are
          resolution (int): How wide each node is
          winner(string): Which player one
          win_msg(string): How the game ended
          win_count(string): What the total wins are for each player

        Returns:
          win_count(string): What the total wins are for each player

    """
    pygame.init()

    # Creates surface
    screen = pygame.display.set_mode(
        (game_size * resolution, game_size * resolution))
    screen.fill((48, 48, 48))

    # Loads fonts
    font = pygame.font.Font("media/ChakraPetch-Regular.ttf", 30)
    font_title = pygame.font.Font("media/ChakraPetch-Regular.ttf", 100)

    # Increments the win counter
    if winner == "Orange Player!":
        win_count[1] += 1
    elif winner == "Blue Player!":
        win_count[0] += 1

    over_screen = True
    while over_screen:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # This means user has chosen to play again
                if event.key == pygame.K_RETURN:
                    # End game over screen
                    over_screen = False
                    break

        # Displays all text
        text = font_title.render("Game Over", True, (244, 163, 0))
        text_rect = text.get_rect(
            center=(game_size * resolution / 2, game_size * resolution * 0.2))
        screen.blit(text, text_rect)

        win_text = win_msg + "Winner is : " + str(winner)
        text = font.render(win_text, True, (244, 163, 0))
        text_rect = text.get_rect(
            center=(game_size * resolution / 2, game_size * resolution * 0.3))
        screen.blit(text, text_rect)

        text = font.render("Press Enter To Play Again", True, (244, 163, 0))
        text_rect = text.get_rect(
            center=(game_size * resolution / 2, game_size * resolution * 0.35))
        screen.blit(text, text_rect)

        text = font.render(
            "Blue Wins: " + str(win_count[0]), True, (244, 163, 0))
        text_rect = text.get_rect(
            center=(game_size * resolution / 4, game_size * resolution * 0.4))
        screen.blit(text, text_rect)

        text = font.render("Orange Wins: " + str(win_count[1]),
                           True, (244, 163, 0))
        text_rect = text.get_rect(
            center=(3 * game_size * resolution / 4,
                    game_size * resolution * 0.4))
        screen.blit(text, text_rect)

        pygame.display.update()
    return win_count
