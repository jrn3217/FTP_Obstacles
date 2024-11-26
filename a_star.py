import heapq

# A* Search Algorithm
class Node:
    def __init__(self, position, parent=None):
        self.position = position  # (x, y) tuple
        self.parent = parent      # Reference to parent node
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic cost from current to goal node

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.g + self.h < other.g + other.h

    def __repr__(self):
        return f"{self.position}, g={self.g}, h={self.h}, f={self.g + self.h}"

# Manhattan Distance
def dist_l1(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

# A* Algorithm
def astar_search(grid, start, end_points, target_point_count):
    
    paths = []

    # Create start and end node
    start_node = Node(start)
    
    # Initialize open and closed lists
    open_list = []
    closed_list = set()
    
    # Add the start node to the open list
    heapq.heappush(open_list, start_node)

    # Loop until we find the end
    while open_list:
        current_node = heapq.heappop(open_list)        # Get the current node 
        closed_list.add(current_node.position)         # Add the current node to the closed list
        
        if current_node.position in end_points:    # If we've reached the goal, reconstruct the path
            path = []
            end_points.remove(current_node.position)  # remove target from end points


            curr = current_node
            while curr:
                path.append(curr.position)
                curr = curr.parent
            
            paths.append(path[::-1])    # add to list of paths

            if len(paths) >= target_point_count or len(end_points) <= 0:
                return paths
            
            for node in open_list:  # update heuristic values
                node.h = min([dist_l1(node.position, end) for end in end_points])

        
        neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)] # Generate valid neighbors
        
        for offset in neighbors:
            neighbor_pos = (current_node.position[0] + offset[0], current_node.position[1] + offset[1])
            
            # Make sure the position is within the bounds of the grid
            if neighbor_pos[0] >= len(grid) or neighbor_pos[0] < 0 or \
               neighbor_pos[1] >= len(grid[0]) or neighbor_pos[1] < 0:
                continue  
               
            if grid[neighbor_pos[0]][neighbor_pos[1]] == 1:  # Ensure the node is walkable (not a wall)
                continue
            
            neighbor_node = Node(neighbor_pos, current_node) # Create a new node and calculate its cost
            
            if neighbor_node.position in closed_list: # Skip if the neighbor is already in the closed list
                continue

            neighbor_node.g = current_node.g + 1
            neighbor_node.h = min([dist_l1(neighbor_node.position, end) for end in end_points])

            # Check if this path is worse than any existing paths in the open list
            if any(open_node for open_node in open_list if neighbor_node == open_node and neighbor_node.g >= open_node.g):
                continue
            
            heapq.heappush(open_list, neighbor_node) # Add the neighbor to the open list
    
    return paths
