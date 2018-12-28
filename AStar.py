from astarNode import AstarNode


def astar(map, begin_node, end_node, game_size, resolution):
    """
          Description: Uses Astar path finding to find the path of nodes to
                        get from the begin_node to the end_node

          Arguments:
            map (list): This is the 2D list of all the map nodes
            begin_node (tuple): Contains x and y of starting location
            end_node (tuple): Contains the x and y of the ending location
            game_size (int): How many rows and columns there are
            resolution (int): How wide each node is

          Returns:
            route[] (tuple): This is a list of nodes, in order, to travel from
                        the beginning to the end

    """
    # Open nodes are active nodes on the "wavefront"
    open_nodes = []
    # Closed nodes have already been checked
    close_nodes = []

    # Create node for the beginning
    bx, by = begin_node
    begin = AstarNode(bx, by, None)
    # Add the beginning node to the open nodes
    open_nodes.append(begin)

    # Create node for the end
    fx, fy = end_node
    end = AstarNode(fx, fy, None)

    # This loops until solution found or there is no solution
    while len(open_nodes) > 0:

        # This just resets the current node and current index to the first one
        # Before the next iteration of the loop
        current_node = open_nodes[0]
        current_index = 0

        # This selects from all the open nodes the node with the
        # lowest f value (f = g+ h)
        # obtains the node and the index of node
        # this is the node which is the best option we have currently
        for index, node in enumerate(open_nodes):
            if node.f < current_node.f:
                current_node = node
                current_index = index

        # Remove the selected node from the open lists and
        # add it to closed since we will now look at it
        open_nodes.pop(current_index)
        close_nodes.append(current_node)

        # this checks of the node we selected was the end node
        if current_node.x == end.x and current_node.y == end.y:
            # Start the route by adding the flag node
            route = [(current_node.x, current_node.y)]
            # This retraces all of the parent nodes in order to get the route
            # of nodes
            # Every node has its own parent and we keep going down the lineage
            # Beginning node has parent == None
            while current_node.parent is not None:
                current_node = current_node.parent
                route.append((current_node.x, current_node.y))

            # Then reverse the list in order to start to the beginning
            route.reverse()
            # Return the route the the flag
            return route

        # These are all of the surrounding nodes from the current node
        # Note that we have chosen to not include diagonals
        # (-1, -1), (-1, 1), (1, -1), (1, 1)]
        adjacent_position = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        adjacent_nodes = []

        # Here the adjacent nodes are created
        for pos in adjacent_position:
            new_x = current_node.x + pos[0]
            new_y = current_node.y + pos[1]

            # Check to ensure adjacent nodes are within map bounds
            if ((new_x >= 0) and (new_x <= game_size - 1) and
                    (new_y >= 0) and (new_y <= game_size - 1)):
                # Check to make sure that the adjacent node is empty
                map[new_x][new_y].set_empty()
                if map[new_x][new_y].safe_path:
                    # if all conditions are met then at the node to be checked
                    # later
                    adjacent_nodes.append(AstarNode(new_x,
                                                    new_y, current_node))

        # Checks the nodes which passed the above conditions
        for node in adjacent_nodes:
            check_open = True
            check_close = True

            # Skips the node if has already been checked
            for c_node in close_nodes:
                if node.x == c_node.x and node.y == c_node.y:
                    check_close = False

            # Calculates the fitness of each adjacent node
            # lower fitness is favoured
            # g is the distance from the beginning measured in moves
            node.g = current_node.g + 1
            # h is the distance to the end measured as square of the diagonal
            node.h = ((node.x - end.x) ** 2 + (node.y - end.y) ** 2)
            # f is sum of g and h
            node.f = node.g + node.h

            # Checks if the node is already in the open nodes
            for o_node in open_nodes:
                if node.x == o_node.x and node.y == o_node.y:
                    # if node is already in open nodes
                    # we check if this path to the node is short than the
                    # previous path take the lower g fitness
                    old_parent = node.parent
                    old_g = node.g
                    node.parent = current_node
                    node.g = node.parent.g + 1
                    new_g = node.g
                    if old_g > new_g:
                        node.parent = old_parent
                    check_open = False

            # if node is not in either closed or open lists than add it to be
            # check in next loop iteration
            if check_close and check_open:
                open_nodes.append(node)
    # if no path is found return 0
    return 0
