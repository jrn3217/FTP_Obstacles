import a_star
from robot import Robot
import metrics
import board
import random

def freeze_tag_greedy_static(board, robots_positions):


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
                possible_targets = list(not_targeted.keys()) if len(not_targeted) > 0 else list(asleep.keys())
                random_target = [random.choice(possible_targets)]
                path = a_star.astar_search(board, r.get_position(), random_target, 1)[0]
                target = asleep[path[-1]]
                if len(not_targeted) > 0: 
                    not_targeted.pop(path[-1])
                r.target = target
                target.add_targeted_by(r)
                r.path = path[1:]   # the current position of Robot r is the start of the path

        
        # Move each awake robot one step forward
        # If the robot has reached it's target, wake the target:
        # - remove the target from the asleep list and put it in the awake list
        # - For each robot in the target's "targeted by": remove the target. 
        # - Remove "targeted by" 
        for r in awake:
            r.move()
            if r.is_goal() and r.target is not None:
                target = asleep.pop(r.get_position())
                awake_queue.append(target)
                for tb in target.targeted_by:
                    tb.target = None
                target.targeted_by = None
        
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

    
        


    
### Testing functionality
def main():



    robots1 = ((0,9),(0,0), (9, 0), (9, 9), (3,2), (3, 7), (6, 2), (6, 7))

    robots2 = [(0,0),(0,4),(2,2), (4,4)]

    # maze_bots = [(9, 10),(1,1), (17,18), (3, 15), (17, 1)]

    result, time = metrics.runtime_eval(freeze_tag_greedy_static, [board.board2, robots2])
    total_steps, paths = result



    print(f"RUNTIME: {time}")
    print(f"TOTAL STEPS: {total_steps}")
    
    print("PATHS:")
    for path in paths:
        print(path)

if __name__ == "__main__":
    main()