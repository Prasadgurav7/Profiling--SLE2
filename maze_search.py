"""
maze_search.py
--------------
Maze generation, neighbor expansion, and the two search algorithms
profiled in the report:
    Algorithm A: Breadth-First Search (BFS)
    Algorithm B: Depth-First Search (DFS), depth-limited to 1000

Maze representation:
    A 2D list of 0/1 ints. 0 = open cell, 1 = wall.
    Positions are (row, col) tuples.
"""

import random
from collections import deque


def generate_maze(rows, cols, seed=None, loop_factor=0.12):
    """
    Generate a grid maze with a guaranteed start->goal path using an
    iterative randomized depth-first "carve" (recursive-backtracker
    algorithm, implemented with an explicit stack so it's safe on
    large mazes with no recursion-depth limit).

    A plain recursive-backtracker produces a "perfect" maze -- a
    spanning tree with exactly ONE path between any two cells, which
    would make BFS and DFS always return the same path. Real walled
    mazes usually have loops/alternate routes, so after carving we
    knock down an extra fraction (`loop_factor`) of the remaining
    interior walls to create shortcuts and dead-end alternatives --
    this is what lets DFS take a longer, suboptimal route in practice.

    rows, cols: requested size (bumped up to the next odd number,
                since the carving algorithm needs odd dimensions).
    Returns: (maze, start, goal)
    """
    rnd = random.Random(seed)

    R = rows if rows % 2 == 1 else rows + 1
    C = cols if cols % 2 == 1 else cols + 1

    maze = [[1] * C for _ in range(R)]
    start = (0, 0)
    maze[0][0] = 0

    stack = [start]
    while stack:
        r, c = stack[-1]
        dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        rnd.shuffle(dirs)

        carved = False
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and maze[nr][nc] == 1:
                maze[nr][nc] = 0
                maze[r + dr // 2][c + dc // 2] = 0  # knock down wall between
                stack.append((nr, nc))
                carved = True
                break

        if not carved:
            stack.pop()

    goal = (R - 1, C - 1)
    if maze[goal[0]][goal[1]] == 1:
        # make sure the goal cell (and one approach to it) is open
        maze[goal[0]][goal[1]] = 0
        maze[goal[0]][goal[1] - 1] = 0

    # --- add loops so multiple routes exist between start and goal ---
    for r in range(1, R - 1):
        for c in range(1, C - 1):
            if maze[r][c] == 1 and rnd.random() < loop_factor:
                open_neighbors = sum(
                    1 for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
                    if maze[r + dr][c + dc] == 0
                )
                if open_neighbors >= 2:
                    maze[r][c] = 0

    return maze, start, goal


def get_neighbors(maze, pos):
    """
    Return the valid, in-bounds, non-wall neighbours of `pos`.
    Fixed check order: down, right, up, left -- this ordering is what
    gives DFS its bias toward the bottom-right of the grid, discussed
    in the report's Section 4 justification.
    """
    r, c = pos
    rows, cols = len(maze), len(maze[0])
    neighbors = []
    for dr, dc in ((1, 0), (0, 1), (-1, 0), (0, -1)):  # down, right, up, left
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
            neighbors.append((nr, nc))
    return neighbors


def bfs(maze, start, goal):
    """
    Breadth-First Search.
    Returns (path_length, nodes_expanded, path) -- same signature as dfs()
    so the two can be compared on equal footing.
    """
    frontier = deque([start])
    came_from = {start: None}
    nodes_expanded = 0

    while frontier:
        current = frontier.popleft()
        nodes_expanded += 1  # a node "expanded" = popped off the frontier

        if current == goal:
            break

        for nxt in get_neighbors(maze, current):
            if nxt not in came_from:
                came_from[nxt] = current
                frontier.append(nxt)

    if goal not in came_from:
        return None, nodes_expanded, None

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()

    return len(path), nodes_expanded, path


def dfs(maze, start, goal, depth_limit=1000):
    """
    Depth-First Search, depth-limited to `depth_limit`.
    Returns (path_length, nodes_expanded, path).
    """
    stack = [(start, [start])]
    visited = set()
    nodes_expanded = 0

    while stack:
        current, path = stack.pop()

        if current in visited:
            continue
        visited.add(current)
        nodes_expanded += 1  # a node "expanded" = popped off the stack

        if current == goal:
            return len(path), nodes_expanded, path

        if len(path) > depth_limit:
            continue

        for nxt in get_neighbors(maze, current):
            if nxt not in visited:
                stack.append((nxt, path + [nxt]))

    return None, nodes_expanded, None
