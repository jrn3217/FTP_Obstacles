
from a_star import Node
import heapq
import board

def find_neighbors(grid, point, points, eps):

    neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    neighborhood = set()
    closed_list = set()
    open_list = []

    start_node = Node(point)

    current_node = start_node

    heapq.heappush(open_list, start_node)

    # Loop until we find the end
    while open_list:
        current_node = heapq.heappop(open_list)        # Get the current node 
        closed_list.add(current_node.position)         # Add the current node to the closed list

        if current_node.position != start_node.position and \
            current_node.position in points:
             neighborhood.add(current_node.position)
             
        for offset in neighbors:
            neighbor_pos = (current_node.position[0] + offset[0], current_node.position[1] + offset[1])

            if neighbor_pos[0] >= len(grid) or neighbor_pos[0] < 0 or neighbor_pos[1] >= len(grid[0]) or neighbor_pos[1] < 0:
                continue  
                    
            if grid[neighbor_pos[0]][neighbor_pos[1]] == 1:  # Ensure the node is walkable (not a wall)
                continue
            
            neighbor_node = Node(neighbor_pos, current_node) # Create a new node and calculate its cost
            
            if neighbor_node.position in closed_list: # Skip if the neighbor is already in the closed list
                continue

            neighbor_node.g = current_node.g + 1
            
            if neighbor_node.g > eps:
                 continue

            if any(open_node for open_node in open_list if neighbor_node == open_node and neighbor_node.g > open_node.g):
                    continue   
            
            heapq.heappush(open_list, neighbor_node) # Add the neighbor to the open list
        
    return neighborhood


def create_cluster(cluster:set, point:tuple, core_points:dict, clustered_points:set):

    unclustered_neighbors = core_points[point].difference(clustered_points)

    cluster.add(point)
    clustered_points.add(point)

    cluster.update(unclustered_neighbors)
    clustered_points.update(unclustered_neighbors)

    rem_core_neighbors = (unclustered_neighbors.intersection(set(core_points.keys())))
    for rcn in rem_core_neighbors:
        create_cluster(cluster, rcn, core_points, clustered_points)

def db_scan(grid, points, eps, min_points):

    # identify core points border points and noise points
    core_neighbors = set()
    
    noise_points = {}
    # border_points = {}
    core_points = {}

    for p in points:
        neighborhood = find_neighbors(grid, p, points, eps)
        if len(neighborhood) >= min_points:
            core_points[p] = neighborhood
            core_neighbors.update(neighborhood)
        else:
            noise_points[p] = neighborhood
    
    # for k in list(noise_points.keys()):
    #     if k in core_neighbors:
    #         neighborhood = noise_points.pop(k)
    #         border_points[k] = neighborhood


    core_point_set = set(core_points.keys())

    clustered_points = set()
    clusters = []

    for p in core_points.keys():
        if p not in clustered_points:
            cluster = set()
            create_cluster(cluster, p, core_points, clustered_points)
            clusters.append(cluster)

    for p in noise_points.keys():
        if p not in clustered_points:
            clusters.append({p})
    return clusters
