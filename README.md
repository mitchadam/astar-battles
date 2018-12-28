-------------------------------------
-CMPUT 274 Final Project
-Dec. 2018
-Mitchell Adam
-1528592
-Nayan Prakash
-1533064
-------------------------------------

$$$$$$\                 $$$$$$$\             $$\     $$\     $$\                     
$$  __$$\  $$\$$\        $$  __$$\            $$ |    $$ |    $$ |                    
$$ /  $$ | \$$$  |       $$ |  $$ | $$$$$$\ $$$$$$\ $$$$$$\   $$ | $$$$$$\   $$$$$$$\
$$$$$$$$ |$$$$$$$\       $$$$$$$\ | \____$$\\_$$  _|\_$$  _|  $$ |$$  __$$\ $$  _____|
$$  __$$ |\_$$$ __|      $$  __$$\  $$$$$$$ | $$ |    $$ |    $$ |$$$$$$$$ |\$$$$$$\  
$$ |  $$ | $$ $$\        $$ |  $$ |$$  __$$ | $$ |$$\ $$ |$$\ $$ |$$   ____| \____$$\
$$ |  $$ | \__\__|       $$$$$$$  |\$$$$$$$ | \$$$$  |\$$$$  |$$ |\$$$$$$$\ $$$$$$$  |
\__|  \__|               \_______/  \_______|  \____/  \____/ \__| \_______|\_______/

Welcome to A*Star battle, a fun multiplayer game which pits
human vs machine as each player must battle the 'finder' of the
opponent.

The finder utilizes the path finding algorithm A star in order
to try and reach a common goal before the opponents.

GOAL:
The goal of the game is to move your snake in such a way that
it blocks the opponents finder from reaching the target.
You want your finder (which is the same colour as you) to reach
the green goal square first. Each finder leaves a pink path behind
it but players and their walls can still pass through these paths.

Included Files:
    - AStar.py
    - astarNode.py
    - client.py
    - custommap.txt
    - Game.py
    - gameOnline.py
    - GameOver.py
    - main.py
    - mapCreator.py
    - mapDesign.py
    - node.py
    - README
    - server.py
    - StartScreen.py
    - waitingScreen.py

Running Instructions:

    Local:

    1. Start up a game by running "python3 main.py" from the command line while
        in the directory containing 'main.py'

    2. Then push '1' and press enter in order to enter in the local mode

    3. The home screen displays the algorithm in use and it navigates to the green
        square from the start point

    4. First you are able to select between game modes by pressing either '1','2' or '3'
        The harder the game mode the more obstacles are placed on the map

    5. However, if you would like to create your own map you can press 'c' which will bring you
        to the map designer screen

    6. The map designer screen works as follows:
        - Press down on the cursor to place a barrier
        - Press '1' to place player 1 flag
        - Press '2' to place the player 2 flag
        - NOTE: You must place player 1 flag first

    7. To then save your custom map press 's' and enter in the name of the map. Then press enter

    8. To load a custom map press 'v' and enter the name of the map. Then press enter.
        To see a custom map that we have created load 'custommap'

    9. Now that the map has been selected, press enter to play the game

    10. The blue player is controlled with the keypad and the orange player is controlled with 'WASD'

    11. The Game is over when either a finder reaches the goal or a player snake becomes stuck and cannot move

    12. From the GameOver screen the user can play again by pressing enter

    Multiplayer:

        - Client:

        1. By default, multiplayer will attempt to connect to a server on 'localhost'.
            If you wish to connect to another server, replace 'localhost' on line 29 of
            'client.py' and on line 29 of 'gameOnline.py' with the desired web address.

        2. By default, multiplayer will attempt to connect over port '8888'. If you
            wish to connect over another port, replace '8888' on line 29 of 'client.py'
            and on line 29 of 'gameOnline.py' with the desired port number.

        3. Start up a game by running "python3 main.py" from the command line while
            in the directory containing main.py

        4. Then push '2' and press enter in order to enter in the multiplayer mode

        5. If you are the first player to connect to the server, you will be asked to
            set the game difficulty. Enter '1', '2' or '3' for easy, medium and difficult
            respectively. Otherwise, if you are player 2, you will wait for the other player to
            set the game difficulty.

        6. Upon connecting, play the game the same way that it is played locally, however
            both players now used 'WASD' for controls.

        - Server:

        1. By default, multiplayer is played over port '8888'. If you wish to connect
            over another port, replace '8888' on line 146 of 'server.py' with the
            desired port number.

        2. In the directory containing 'server.py', run 'python3 server.py'.

        3. Players should then be able to connect to the address of the server.


Requirements:

    In order to run our game requires:
        - Pygame version
        - pickle
        - tornado
        - websocket
        - asyncio

    This libraries can be installed on the VM by running the following, respectively:
        - pip3 install asyncio
        - pip3 install websocket


Notes and Assumptions:

    Some lines of code are very long, especially when dealing with multidimensional
    lists. Sometimes these especially long lines of code do not pass the pep8 line
    length limit, however they were left these lengths to improve readability.

    In the Map Designer, Player 1's flag must be placed BEFORE Player 2's flag
    by pressing '1' AND THEN '2'.

    In the Map Designer, both flags MUST be placed before saving, otherwise the
    map will not load.

Reference:

    The following was used as reference material throughout the course of the project:
        - For the cool ASCII Art in the README: http://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20
        - For help on A*star: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
        - For help on Pygame: https://www.pygame.org/docs/
