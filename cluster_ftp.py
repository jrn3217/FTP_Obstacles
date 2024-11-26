import a_star
from dbscan import db_scan
from robot import Robot

def freeze_tag_cluster(board, robots_positions, eps, min_points):

    awake = []
    awake_queue = []
    asleep = {}    
    not_targeted = {}   

    # create robot objects and populate 
    r0 = Robot(0, robots_positions[0])
    awake.append(r0)

    for i in range(1, len(robots_positions)):
        init_pos = robots_positions[i]
        ri = Robot(i, init_pos)
        asleep[init_pos] = ri
        not_targeted[init_pos] = ri

    # setup cluster data
    cluster_points = set(asleep)
    clusters= db_scan(board, asleep, eps, min_points)
    cluster_count = len(clusters)

    pc_map = {}
    for c in clusters:
        for p in c:
            pc_map[p] = c

    # continue until all robots are awake
    while len(asleep) > 0:

        # Assign a new target if a robot does not have one:
        # - use a* to find the closest target in the not_targeted list
        # --- remove the target from the not_targeted list
        # -- if the not_targeted list is empty, use the asleep list
        # --- do not remove the target from the asleep list
        # - add the target to robot.target
        # - add the robot to the target.targeted by
        # - set the path of the robot
        for r in awake:
            if r.target is None:
                if r.cluster is not None:
                    possible_targets = list(r.cluster.intersection(not_targeted))
                    # may be empty if other robots in the cluster are awoken

                if r.cluster is None or len(possible_targets) <= 0:
                    if cluster_count > 0:
                        possible_targets = list(cluster_points)
                    else:
                        possible_targets = list(not_targeted.keys()) \
                            if len(not_targeted) > 0 else list(asleep.keys())
                    
                paths = a_star.astar_search(board, r.get_position(), possible_targets, 1)

                if len(paths) <= 0:
                        raise Exception("No path found")
                path = paths[0]
                target = asleep[path[-1]]
                if len(not_targeted) > 0: 
                    not_targeted.pop(path[-1])
                r.target = target
                target.add_targeted_by(r)
                r.path = path[1:]   # the current position of Robot r is the start of the path

                
                if cluster_count > 0 and r.cluster is None:
                    target_cluster = pc_map[path[-1]]
                    cluster_points.difference_update(target_cluster)
                    cluster_count -= 1
                    r.cluster = target_cluster


        for r in awake:
            r.move()
            if r.is_goal() and r.target is not None:
                target = asleep.pop(r.get_position())
                awake_queue.append(target)
                for tb in target.targeted_by:
                    tb.target = None
                target.targeted_by = None

                if r.cluster is not None:
                    r.cluster = r.cluster.difference({target.get_position()})
                    if len(r.cluster) == 0: r.cluster = None 
        
        awake += awake_queue
        awake_queue = []

    # calculate the total steps it took to wake all robots
    total_steps = len(r0.history)
    
    # extract the paths each robot took and pad the front of those from formerly asleep robots
    final_paths = []

    for r in awake:
        start = r.history[0]
        gap = total_steps - len(r.history)
        final_paths.append([start] * gap + r.history)


    return total_steps, final_paths
