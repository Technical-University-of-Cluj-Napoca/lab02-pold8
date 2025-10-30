from collections import deque
import sys


def read_maze(filename: str) -> list[list[str]]:
    """Reads a maze from a file and returns it as a list of lists (matrix)."""
    result = []
    with open(filename, "r") as f:
        lines = f.readlines()

    for line in lines:
        result.append(list(line.strip()))  # ✅ Convert string to list of characters
    return result


def find_start_and_target(maze: list[list[str]]) -> tuple[tuple[int, int], tuple[int, int]]:
    """Finds the coordinates of start ('S') and target ('T') in the maze."""
    start = target = (-1, -1)
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            if maze[row][column] == 'S':
                start = (row, column)
            elif maze[row][column] == 'T':
                target = (row, column)
    return start, target


def get_neighbors(maze: list[list[str]], position: tuple[int, int]) -> list[tuple[int, int]]:
    """Given a position, returns a list of valid neighboring positions (up, down, left, right)."""
    neighbors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dr, dc in directions:
        row, col = position[0] + dr, position[1] + dc
        if 0 <= row < len(maze) and 0 <= col < len(maze[row]):
            if maze[row][col] != '#':
                neighbors.append((row, col))
    return neighbors


def bfs(maze: list[list[str]], start: tuple[int, int], target: tuple[int, int]) -> list[tuple[int, int]]:
    """Performs a breadth-first search (BFS) to find the shortest path."""
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        current_node, path = queue.popleft()

        if current_node == target:
            return path

        for neighbor in get_neighbors(maze, current_node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return []  # ✅ Return empty list if no path found


def dfs(maze: list[list[str]], start: tuple[int, int], target: tuple[int, int]) -> list[tuple[int, int]]:
    """Performs a depth-first search (DFS) to find *a* path."""
    stack = [(start, [start])]
    visited = {start}

    while stack:
        current_node, path = stack.pop()

        if current_node == target:
            return path

        for neighbor in get_neighbors(maze, current_node):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))

    return []  # ✅ Return empty list if no path found


def print_maze_with_path(maze: list[list[str]], path: list[tuple[int, int]]) -> None:
    """Prints the maze to the console, marking the path with 'x' in red."""
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    maze_copy = [row[:] for row in maze]  # ✅ Deep copy of maze

    for r, c in path:
        if maze_copy[r][c] not in ('S', 'T'):
            maze_copy[r][c] = f"{RED}*{RESET}"

    for r in range(len(maze_copy)):
        for c in range(len(maze_copy[r])):
            if maze_copy[r][c] == 'S':
                maze_copy[r][c] = f"{GREEN}S{RESET}"
            elif maze_copy[r][c] == 'T':
                maze_copy[r][c] = f"{YELLOW}T{RESET}"

    for row in maze_copy:
        print("".join(row))


if __name__ == "__main__":
    # Example usage: run the script directly
    if len(sys.argv) != 3:
        print("Usage: python maze_solver.py <bfs|dfs> <maze_filename>")
        sys.exit(1)

    method = sys.argv[1].lower()
    filename = sys.argv[2]

    maze = read_maze(filename)
    start, target = find_start_and_target(maze)

    if start == (-1, -1) or target == (-1, -1):
        print("Error: Maze must contain both 'S' (start) and 'T' (target).")
        sys.exit(1)

    if method == "bfs":
        path = bfs(maze, start, target)
    elif method == "dfs":
        path = dfs(maze, start, target)
    else:
        print("Invalid method. Use 'bfs' or 'dfs'.")
        sys.exit(1)

    if not path:
        print("No path found!")
    else:
        print_maze_with_path(maze, path)