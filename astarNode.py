class AstarNode:
    """
          Description: This class is used to keep track of each node for
                AStar path finding

    """

    def __init__(self, x, y, parent):
        """
            Description: This function is the constructor of AstarNodes

            Arguments:
              self (AstarNode object): This node
              x, y (int): location on map
              parent (AstarNode object): Which node we got to this node from

            Returns:
              None

        """
        self.parent = parent

        self.x = x
        self.y = y

        # Fitness values
        self.g = 0
        self.h = 0
        self.f = 0
