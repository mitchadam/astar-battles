import asyncio
import json

import websockets

from waitingScreen import wait_screen


async def start_game():
    """
          Description: This function is used by clients to connect to the
                        server and carry out a handshake between the two
                        players and gather the required information to play
                        online

          Arguments:
            None

          Returns:
            difficulty (string): this is either 'easy', 'medium', or 'hard'
            seed (int): this is the seed that will be used to psuedorandomly
                        the map
            player_number (int): this is either 1 or 2 and represents which
                        player you will be, blue or orange

    """
    # Creates websocket connection with server aysnchronously
    async with websockets.connect(
            'ws://localhost:8888') as websocket:
        # Receives player_number from server
        player_number = await websocket.recv()
        player_number = int(player_number)
        # Allows player 1 to select the multiplayer difficulty and send the
        # difficulty to the server
        if player_number == 1:
            print(await websocket.recv())
            difficulty = wait_screen(player_number)
            difficulty = str(difficulty)
            await websocket.send(json.dumps({'difficulty': difficulty}))
        # Receive difficulty and seed from server and load JSON as dictionary
        start_info = await websocket.recv()
        start_info = json.loads(start_info)
        # Set difficulty to difficulty received from server
        difficulty = int(start_info['difficulty'])
        if difficulty == 1:
            difficulty = "easy"
        elif difficulty == 2:
            difficulty = "medium"
        elif difficulty == 3:
            difficulty = "hard"
        # Set seed to seed received from server
        seed = int(start_info['seed'])
        return difficulty, seed, player_number
