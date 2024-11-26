import sys
import board
from metrics import runtime_eval
from greedy_static_ftp import freeze_tag_greedy_static as ftp_gs
from greedy_dynamic_ftp import freeze_tag_greedy_dynamic as ftp_gd
from cluster_ftp import freeze_tag_cluster as ftp_c
from random_ftp import freeze_tag_random as ftp_r

seed = 1

demos = {
    "demo1": {
        "board": board.board3,
        "robots": [(0,0), (0,4), (4,0), (4,4)],
        "f": ftp_gs,
        "time": True
    }, "demo2": {
        "board": board.board3,
        "robots": [(0,0), (0,4), (4,0), (4,4)],
        "f": ftp_r,
        "time": True
    }, "demo3": {
        "board": board.empty_10,
        "robots": [(5,8), (4,8), (3,8), (8,8), (9,8), (9,9), (0,0), (0,1)],
        "f": ftp_gs,
        "time": True
    }, "demo4":{
        "board": board.empty_10,
        "robots": [(5,8), (4,8), (3,8), (8,8), (9,8), (9,9), (0,0), (0,1)],
        "f": ftp_gd,
        "time": True
    }, "demo5":{
        "board": board.empty_10,
        "robots": [(5,8), (4,8), (3,8), (8,8), (9,8), (9,9), (0,0), (0,1)],
        "f": ftp_r,
        "time": True
    }, "demo6":{
        "board": board.empty_10,
        "robots": [(5,8), (4,8), (3,8), (8,8), (9,8), (9,9), (0,0), (0,1)],
        "f": ftp_c,
        "time": True,
        "cluster_args": [1,2]
    }, "demo7":{
        "board": board.board1,
        "robots": None,
        "f": ftp_gs,
        "time": True,
        "cluster_args": []
    }, "demo8":{
        "board": board.board1,
        "robots": None,
        "f": ftp_gd,
        "time": True,
        "cluster_args": []
    }, "demo9":{
        "board": board.board1,
        "robots": None,
        "f": ftp_c,
        "time": True,
        "cluster_args": [3,2]
    }, "demo10": {
        "board": board.board1,
        "robots": None,
        "f": ftp_r,
        "time": True,
        "cluster_args": []
    }
}



def run_test(args, seed):
    robots = None
    test_board = args["board"]
    f = args["f"]
    
    results = None
    time = None

    if "robots" in args and args["robots"] is not None: robots = args["robots"]
    else: robots = board.randomize_robots(test_board, (board.dims(test_board)[0]), seed)


    print(f"BOARD:")
    board.print_board(test_board, robots)
    print()
    print(f"ROBOTS: {robots}")
    print(f"ALGORITHM: {f.__name__}")

    cluster_args = args["cluster_args"] if "cluster_args" in args else []

    input_args = [test_board, robots] + cluster_args
    if args["time"]:
        results, time = runtime_eval(args["f"], input_args)
    else:
        results = f(*input_args)


    total_steps, paths = results

    if time is not None:
        print(f"RUNTIME: {time}")
    print(f"TOTAL STEPS: {total_steps}")
    
    print("PATHS:")
    for path in paths:
        print(path)

def main():

    demo = sys.argv[1]
    seed = sys.argv[2] if len(sys.argv) == 3 else None
    if demo not in demos:
        print("INVALID DEMO")
    else:
        run_test(demos[demo], seed)


if __name__ == "__main__":
    main()