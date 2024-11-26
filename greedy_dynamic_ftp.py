import a_star
from robot import Robot

def freeze_tag_greedy_dynamic(board, robots_positions):

    awake = {}
    awake_queue = []
    asleep = {}    
    not_targeted = {}   

    # create robot objects and populate 
    r0 = Robot(0, robots_positions[0])
    awake[robots_positions[0]] = r0

    for i in range(1, len(robots_positions)):
        init_pos = robots_positions[i]
        ri = Robot(i, init_pos)
        asleep[init_pos] = ri
        not_targeted[init_pos] = ri

    # continue until all robots are awake
    while len(asleep) > 0:

        if len(awake_queue) > 0: # only do dynamic assignment when a robot is awoken
        
        # assign each asleep robot to the closest awake robot
            for r in asleep.values():
                possible_targets = {}
                for ar in awake.values():
                    ar_pos = ar.get_position()
                    ar_dist = ar.get_target_distance()
                    if ar_pos in possible_targets and ar_dist is not None:  
                        # use the robot with the greatest distance
                        other_dist = possible_targets[ar_pos].get_target_distance()
                        if other_dist is not None and other_dist < ar_dist:
                            possible_targets[ar_pos] = ar
                    else: 
                        possible_targets[ar_pos] = ar
                    
                paths = a_star.astar_search(board, r.get_position(), list(possible_targets.keys()), 1)
                if len(paths) <= 0:
                    raise Exception("No path found")
                path = paths[0]
                target = possible_targets[path[-1]]

                # the awake node is closer to the current
                # asleep node than it's previous target
                if target.target is None:
                    if r.targeted_by is not None:   # clear previous targets
                        for tb in r.targeted_by:
                            tb.target = None
                        r.targeted_by = None
                        

                    r.add_targeted_by(target)
                    target.target = r
                    target.path = path[-2::-1]  # reverse the path then prune the first point

                    if path[0] in not_targeted:
                        not_targeted.pop(path[0])   # remove r from the not targeted set
                        

                elif target.get_target_distance() > len(path) - 1:
                    tt = target.target
                    not_targeted[tt.get_position()] = tt
                    tt.remove_targeted_by(target)   # remove awake node from it's old target's 
                                                    # set of targets

                    if r.targeted_by is not None:   # clear previous targets
                        for tb in r.targeted_by:
                            tb.target = None
                        r.targeted_by = None

                    r.add_targeted_by(target)
                    target.target = r
                    target.path = path[-2::-1]

                    if path[0] in not_targeted:
                        not_targeted.pop(path[0])   # remove r from the not targeted set

                # otherwise there is a better option for the awake node

        # any remaining robots are assigned using greedy static
        for r in awake.values():
            if r.target is None:
                possible_targets = list(not_targeted.keys()) if len(not_targeted) > 0 else list(asleep.keys())
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

        awake_queue = []
        # Move each awake robot one step forward
        # If the robot has reached it's target, wake the target:
        # - remove the target from the asleep list and put it in the awake list
        # - For each robot in the target's "targeted by": remove the target. 
        # - Remove "targeted by" 
        for r in awake.values():
            r.move()
            if r.is_goal() and r.target is not None:
                target = asleep.pop(r.get_position())
                awake_queue.append(target)
                for tb in target.targeted_by:
                    tb.target = None
                target.targeted_by = None
        
        for r in awake_queue:
            awake[r.get_position()] = r


    # calculate the total steps it took to wake all robots
    total_steps = len(r0.history)
    
    # extract the paths each robot took and pad the front of those from formerly asleep robots
    final_paths = []

    for r in awake.values():
        start = r.history[0]
        gap = total_steps - len(r.history)
        final_paths.append([start] * gap + r.history)


    return total_steps, final_paths
