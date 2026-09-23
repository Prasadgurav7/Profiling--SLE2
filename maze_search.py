import random
from collections import deque


def generate_maze(rows, cols, seed=None):
    random.seed(seed)

    if rows % 2 == 0:
        rows += 1
    if cols % 2 == 0:
        cols += 1

    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    start = (1, 1)
    goal = (rows - 2, cols - 2)

    maze[1][1] = 0

    stack = [(1, 1)]

    while stack:
        r, c = stack[-1]

        directions = [
            (2, 0),
            (-2, 0),
            (0, 2),
            (0, -2)
        ]

        random.shuffle(directions)

        found = False

        for dr, dc in directions:

            nr = r + dr
            nc = c + dc

            if 1 <= nr < rows - 1 and 1 <= nc < cols - 1:
                if maze[nr][nc] == 1:

                    maze[nr][nc] = 0

                    # Open wall between cells
                    maze[r + dr // 2][c + dc // 2] = 0

                    stack.append((nr, nc))

                    found = True
                    break

        if not found:
            stack.pop()

    # Make sure goal is open
    maze[goal[0]][goal[1]] = 0

    return maze, start, goal


def get_neighbors(maze, position):

    r, c = position

    rows = len(maze)
    cols = len(maze[0])

    neighbors = []

    directions = [
        (1, 0),    # down
        (0, 1),    # right
        (-1, 0),   # up
        (0, -1)    # left
    ]

    for dr, dc in directions:

        nr = r + dr
        nc = c + dc

        if 0 <= nr < rows and 0 <= nc < cols:

            if maze[nr][nc] == 0:
                neighbors.append((nr, nc))

    return neighbors


def bfs(maze, start, goal):

    queue = deque()

    queue.append(start)

    visited = set()
    visited.add(start)

    parent = {
        start: None
    }

    nodes_expanded = 0

    while queue:

        current = queue.popleft()

        nodes_expanded += 1

        if current == goal:
            break

        for neighbor in get_neighbors(maze, current):

            if neighbor not in visited:

                visited.add(neighbor)

                parent[neighbor] = current

                queue.append(neighbor)

    # Goal not found
    if goal not in parent:
        return None, nodes_expanded, None

    # Create path
    path = []

    current = goal

    while current is not None:

        path.append(current)

        current = parent[current]

    path.reverse()

    return len(path), nodes_expanded, path


def dfs(maze, start, goal, depth_limit=1000):

    stack = []

    stack.append((start, [start]))

    visited = set()

    nodes_expanded = 0

    while stack:

        current, path = stack.pop()

        if current in visited:
            continue

        visited.add(current)

        nodes_expanded += 1

        if current == goal:

            return len(path), nodes_expanded, path

        if len(path) >= depth_limit:
            continue

        neighbors = get_neighbors(maze, current)

        # Reverse because stack is LIFO
        for neighbor in reversed(neighbors):

            if neighbor not in visited:

                new_path = path + [neighbor]

                stack.append((neighbor, new_path))

    return None, nodes_expanded, None


def print_maze(maze, start, goal, path=None):

    if path is None:
        path = []

    path_set = set(path)

    for r in range(len(maze)):

        line = ""

        for c in range(len(maze[0])):

            position = (r, c)

            if position == start:

                line += "S "

            elif position == goal:

                line += "G "

            elif position in path_set:

                line += "* "

            elif maze[r][c] == 1:

                line += "# "

            else:

                line += ". "

        print(line)


# ==================================================
# MAIN PROGRAM
# ==================================================

print("====================================")
print("       MAZE SEARCH PROGRAM")
print("====================================")

rows = 21
cols = 21

print("\nGenerating maze...")

maze, start, goal = generate_maze(
    rows,
    cols,
    seed=42
)

print("Maze generated successfully!")

print("\nStart:", start)
print("Goal :", goal)

print("\n========== MAZE ==========")

print_maze(maze, start, goal)


# ==================================================
# BFS
# ==================================================

print("\n========== BFS ==========")

bfs_length, bfs_nodes, bfs_path = bfs(
    maze,
    start,
    goal
)

if bfs_path is None:

    print("BFS could not find a path.")

else:

    print("Path Length   :", bfs_length)
    print("Nodes Expanded:", bfs_nodes)

    print("\nBFS Path:")

    print_maze(
        maze,
        start,
        goal,
        bfs_path
    )


# ==================================================
# DFS
# ==================================================

print("\n========== DFS ==========")

dfs_length, dfs_nodes, dfs_path = dfs(
    maze,
    start,
    goal,
    1000
)

if dfs_path is None:

    print("DFS could not find a path.")

else:

    print("Path Length   :", dfs_length)
    print("Nodes Expanded:", dfs_nodes)

    print("\nDFS Path:")

    print_maze(
        maze,
        start,
        goal,
        dfs_path
    )


print("\n====================================")
print("          PROGRAM FINISHED")
print("====================================")
