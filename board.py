from collections import deque
import random

maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

board1 = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,0,0,1,1,1,0],
    [0,1,0,0,0,0,0,0,1,0],
    [0,0,0,0,1,1,0,0,0,0],
    [0,0,0,0,1,1,0,0,0,0],
    [0,1,0,0,0,0,0,0,1,0],
    [0,1,1,1,0,0,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
]

board2 = [
    [0,0,0,0,0],
    [0,1,0,1,0],
    [0,1,0,1,0],
    [0,1,0,1,0],
    [0,0,0,0,0]
]

board3 = [
    [0,0,0,0,0],
    [1,1,0,1,0],
    [0,0,0,1,0],
    [0,1,0,0,0],
    [0,0,0,1,0]
]

empty_10 = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
]

def dims(board):
    return (len(board), len(board[0]))

def isfully0connected(maze):
    rows, cols = len(maze), len(maze[0])
    
    # Find the first '0' to start BFS
    start = None
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 0:
                start = (r, c)
                break
        if start:
            break
    
    if not start:
        # No valid '0' positions in the maze
        return False
    
    # Directions for movement: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    visited = set()
    queue = deque([start])
    visited.add(start)
    
    while queue:
        r, c = queue.popleft()
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))
    
    # After BFS, check if all '0' positions were visited
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 0 and (r, c) not in visited:
                return False
    
    return True

def density(board):
    cells = 0
    wall_cells = 0
    for row in board:
        for cell in row:
            cells += 1
            if cell == 1: wall_cells += 1
    return wall_cells / cells

def randomize_robots(board, robot_count, seed=None):
    if seed is not None:
        random.seed(seed)
        
    empty_cells = []
    robots = []

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0: empty_cells.append((i,j))

    if len(empty_cells) < robot_count:
        return None
    
    while len(robots) < robot_count:
        r = random.choice(empty_cells)
        empty_cells.remove(r)
        robots.append(r)
    return robots

def print_board(board, special_coords = []):
    n = len(board)  # Assuming a square NxN board

    # Unpack the special coordinates
    x_coord = special_coords[0] if len(special_coords) > 0 else None
    o_coords = special_coords[1:] if len(special_coords) > 1 else []

    # Top border
    print("-" * (n * 2 + 3))

    # Board rows with side borders
    for i, row in enumerate(board):
        row_str = "| "
        for j, cell in enumerate(row):
            # Determine what to print at each position
            if (i, j) == x_coord:
                row_str += "X "
            elif (i, j) in o_coords:
                row_str += "O "
            else:
                row_str += "# " if cell == 1 else "  "
        print(row_str + "|")

    # Bottom border
    print("-" * (n * 2 + 3))

def main():
    print_board(board3)

if __name__ == "__main__":
    main()
        