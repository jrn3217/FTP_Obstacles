import sys
import board
from metrics import runtime_eval
from greedy_static_ftp import freeze_tag_greedy_static as ftp_gs
from greedy_dynamic_ftp import freeze_tag_greedy_dynamic as ftp_gd
from random_ftp import freeze_tag_random as ftp_r

DEMO_1 = {
    "board": board.board3,
    "robots": [(0,0), (0,4), (4,0), (4,4)],
    "f": ftp_gs,
    "time": True
}

DEMO_2 = {
    "board": board.board3,
    "robots": [(0,0), (0,4), (4,0), (4,4)],
    "f": ftp_r,
    "time": True
}

DEMO_3 = {
    "board": board.empty_10,
    "robots": [(5,8), (4,8), (3,8), (8,8), (9,8), (9,9), (0,0), (0,1)],
    "f": ftp_gs,
    "time": True
}

DEMO_4 = {
    "board": board.empty_10,
    "robots": [(5,8), (4,8), (3,8), (8,8), (9,8), (9,9), (0,0), (0,1)],
    "f": ftp_gd,
    "time": True
}

DEMO_5 = {
    "board": board.empty_10,
    "robots": [(5,8), (4,8), (3,8), (8,8), (9,8), (9,9), (0,0), (0,1)],
    "f": ftp_r,
    "time": True
}


def run_test(args):
    robots = None
    test_board = args["board"]
    f = args["f"]
    
    results = None
    time = None

    if "robots" in args: robots = args["robots"]
    else: robots = board.randomize_robots(test_board, (board.dims(test_board)[0] / 2))


    print(f"BOARD:")
    board.print_board(test_board, robots)
    print()
    print(f"ROBOTS: {robots}")
    print(f"ALGORITHM: {f.__name__}")

    if args["time"]:
        results, time = runtime_eval(args["f"], [test_board, robots])
    else:
        results = f(test_board, robots)


    total_steps, paths = results

    if time is not None:
        print(f"RUNTIME: {time}")
    print(f"TOTAL STEPS: {total_steps}")
    
    print("PATHS:")
    for path in paths:
        print(path)
    
    


def main():

    demo = sys.argv[1]
    if demo == "demo1":
        run_test(DEMO_1)
    elif demo == "demo2":
        run_test(DEMO_2)
    elif demo == "demo3":
        run_test(DEMO_3)
    elif demo == "demo4":
        run_test(DEMO_4)
    elif demo == "demo5":
        run_test(DEMO_5)
    else:
        print("Invalid Demo")






if __name__ == "__main__":
    main()