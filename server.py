import json
import random

import tornado.ioloop
import tornado.web
import tornado.websocket


class ConnectionHandler(tornado.websocket.WebSocketHandler):
    """
          Description: This class is the Handler which is used to carry out the
                        handshake when connecting two players.

          Arguments:
            tornado.websocket.WebSocketHandler (object): this is the inherited
                        WebSocketHandler class that comes from tornado

    """
    # Initializes players, seed and difficulty variables
    players = []
    seed = -1
    difficulty = 0

    def __init__(self, application, request, **kwargs):
        """
            Description: This function is used to initialize websocket
                connections objects.
        """
        super().__init__(application, request, **kwargs)

    def open(self):
        """
            Description: This function is used to add players to the players
                list and assign players their player number upon opening a
                websockets connection

            Arguments:
              self (object): The ConnectionHandler object of the websockets
                    connection

            Returns:
              None

        """
        print("Got Connection")
        # check amount of players connected
        amountPlayers = len(ConnectionHandler.players)
        # Adds ConnectionHandler object to list of players
        ConnectionHandler.players.append(self)
        # Generate a common seed if first player connected
        if amountPlayers == 0:
            ConnectionHandler.seed = random.randint(0, 10000000000000)
            # Tell first connected player he is player 1
            self.write_message(u"1")
        # If both players connected, tell player 1 he is paired and tell player
        # 2 that he is player 2
        elif amountPlayers < 2:
            self.write_message(u"2")
            ConnectionHandler.players[0].write_message(u"Paired")
        # Prevent too many players from joining
        else:
            self.write_message(u"Too many players")

    def on_message(self, message):
        """
            Description: This function is used to send both players the game
                seed and difficulty after receiving a websockets message of the
                difficulty from player 1

            Arguments:
              self (object): The ConnectionHandler object of the websockets
                    message
              message (string): The websockets message

            Returns:
              None

        """
        message = json.loads(message)
        if 'difficulty' in message.keys():
            # Set difficulty after receiving difficulty message from player 1
            ConnectionHandler.difficulty = message['difficulty']
            # writes a common seed and difficulty to both players
            for player in ConnectionHandler.players:
                player.write_message(json.dumps(
                                   {'difficulty': ConnectionHandler.difficulty,
                                    'seed': ConnectionHandler.seed}))

    def on_close(self):
        """
            Description: This function is used to remove ConnectionHandler
                objects from the players list upon closing a websockets
                connection

            Arguments:
              self (object): The ConnectionHandler object of the websockets
                    connection

            Returns:
              None

        """
        print("Close Connection")
        # Removes the ConnectionHandler object from the list of players
        ConnectionHandler.players.remove(self)


class GameHandler(tornado.websocket.WebSocketHandler):
    """
          Description: This class is the Handler used to play the game between
              player 1 and player 2

          Arguments:
            tornado.websocket.WebSocketHandler (class): this is the inherited
                        WebSocketHandler class that comes from tornado

    """
    # Initializes an empty list of players
    players = []

    def __init__(self, application, request, **kwargs):
        """
            Description: This function is used to initialize websocket
                connections objects.
        """
        super().__init__(application, request, **kwargs)

    def open(self):
        """
            Description: This function is used to add players to the players
                list and notify players when they are paired with their
                opponent

            Arguments:
              self (object): The ConnectionHandler object of the websockets
                    connection

            Returns:
              None

        """
        print("Got Game Connection")
        # Check amount of connected players
        amountPlayers = len(GameHandler.players)
        # Add GameHandler object to list of players
        GameHandler.players.append(self)
        # if only one player connected, both players are not paired yet
        if amountPlayers == 0:
            pass
        elif amountPlayers < 2:
            self.write_message(u"2")
            # Sends both players a paired message
            for player in GameHandler.players:
                player.write_message(u"Paired")
        # prevent too many players from connecting
        else:
            self.write_message(u"Too many players")

    def on_message(self, message):
        """
            Description: Upon receiving a websocket message of a player's move,
                this function is used to write a websockets message to the
                player's opponent of their move.

            Arguments:
              self (object): The GameHandleer object of the websockets
                    message
            message (string): The websockets message of a player's move

            Returns:
              None

        """
        print(message)
        # find if message is from player 1 or player 2
        player = GameHandler.players.index(self)
        # Send opposite player a message of the player's move
        GameHandler.players[abs(player - 1)].write_message(message)

    def on_close(self):
        """
            Description: This function is used to remove GameHandler
                objects from the players list upon closing a websockets
                connection

            Arguments:
              self (object): The GameHandler object of the websockets
                    connection

            Returns:
              None

        """
        # Remove GameHandler object from list of players
        GameHandler.players.remove(self)


def make_app():
    """
        Description: This function is used to create the tornado app and set
            the URLs of each Handler used by the append

        Arguments:
          None

        Returns the generated tornado web app
    """
    return tornado.web.Application([
        (r"/", ConnectionHandler),
        (r"/play", GameHandler),
    ])


if __name__ == "__main__":
    """
        Description: This is the main function that will run after calling
            'python3 server.py' from a terminal. This will run the server
    """
    # Creates the tornado app
    app = make_app()
    # Sets the default port of websocket connections
    app.listen(8888)
    # This begins the main loop of the tornado app
    tornado.ioloop.IOLoop.current().start()
