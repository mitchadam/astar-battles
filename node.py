class Node:
    """
          Description: This class is used to determine what each square on
                the maps role is

          Arguments:
            p (bool): Whether this node is a path
            p1w (bool): Whether this node is a player 1 wall
            p2w (bool): Whether this node is a player 2 wall
            p1f (bool): Whether this node is a player 1 finder
            p2f (bool): Whether this node is a player 2 finder
            p1g (bool): Whether this node is a player 1 flag
            p2g (bool): Whether this node is a player 2 flag
            b (bool): Whether this node is a barrier


    """

    def __init__(self, p, p1w, p2w, p1f, p2f, p1g, p2g, b):
        # Sets all of the node properties
        self.path = p
        self.player_wall = [p1w, p2w]
        self.player1_wall = p1w
        self.player2_wall = p2w
        self.player1_finder = p1f
        self.player2_finder = p2f
        self.player1_flag = p1g
        self.player2_flag = p2g
        self.barrier = b
        self.set_empty()
        self.set_color()

    # Checks if the  node is empty and if a path can be placed there
    def set_empty(self):
        """
            Description: Used to check if a node is empty and can be used
                    as a path

            Arguments:
              self (node object): This node object

            Returns:
              None

        """
        self.empty = self.path or not (self.player_wall[0] or
                                       self.player_wall[1] or
                                       self.player1_finder or
                                       self.player2_finder or
                                       self.player1_flag or
                                       self.player2_flag or
                                       self.barrier)
        self.safe_path = self.path or not (self.player_wall[0] or
                                           self.player_wall[1] or
                                           self.player1_finder or
                                           self.player2_finder or
                                           self.barrier)

    # Sets the color of the node to corresponding role
    def set_color(self):
        """
         Description: Sets the color of all nodes

         Arguments:
           self (node object): This node object

         Returns:
           None

         """
        if self.player_wall[0]:
            self.color = (89, 221, 255)
        elif self.player_wall[1]:
            self.color = (255, 89, 8)
        elif self.player1_finder:
            self.color = (89, 221, 255)
        elif self.player2_finder:
            self.color = (255, 89, 8)
        elif self.path:
            self.color = (244, 66, 209)
        elif self.empty:
            self.color = (255, 255, 255)
        elif self.player1_flag:
            self.color = (0, 255, 0)
        elif self.player2_flag:
            self.color = (0, 255, 0)
        elif self.barrier:
            self.color = (48, 48, 48)
