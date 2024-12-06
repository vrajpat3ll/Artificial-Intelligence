from typing import List, Tuple
import heapq

# change the penalties that you want to give to each of the
penalties = {
    'R': 0,
    'G': 1,
    'M': 2,
    'P': 0,
    'O': 0,
}
costs = {
    'R': 1,                     # Main Road
    'G': 3 + penalties['G'],    # Gali
    'M': 5 + penalties['M'],    # Market
    'P': 2,                     # Park
    'O': float('inf')           # Obstacle
}

# coordinates
headquarters = (0, 0)
stations = {
    'lights': (7, 3),
    'sweets': (2, 4),
    'diya': (6, 0),
    'rangoli': (5, 7)
}
# city map
example_grid = [
    ['R', 'R', 'G', 'P', 'M', 'R', 'O', 'R'],
    ['R', 'P', 'O', 'G', 'R', 'R', 'R', 'R'],
    ['R', 'R', 'M', 'R', 'R', 'O', 'R', 'R'],
    ['R', 'R', 'R', 'P', 'R', 'R', 'G', 'R'],
    ['R', 'R', 'R', 'R', 'M', 'O', 'R', 'P'],
    ['P', 'O', 'R', 'R', 'R', 'R', 'R', 'R'],
    ['M', 'R', 'P', 'R', 'G', 'R', 'R', 'R'],
    ['R', 'R', 'R', 'R', 'R', 'P', 'R', 'M']
]


class Cell:
    def __init__(self, x: int, y: int, cell_type: str):
        self.x = x
        self.y = y
        self.cell_type = cell_type
        # Define movement costs based on cell type
        self.cost = costs[cell_type]

    def __lt__(self, other):
        # Required for heap operations
        return False


class FestivalGrid:
    def __init__(self, grid: List[List[str]]):
        self.height = len(grid)
        self.width = len(grid[0])
        self.grid = [[Cell(i, j, cell_type) for j, cell_type in enumerate(row)]
                     for i, row in enumerate(grid)]

    def get_neighbors(self, cell: Cell) -> List[Cell]:
        """Get valid neighboring cells (up, down, left, right)."""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbors = []

        for dx, dy in directions:
            new_x, new_y = cell.x + dx, cell.y + dy
            if (0 <= new_x < self.height and 0 <= new_y < self.width and
                    self.grid[new_x][new_y].cost != float('inf')):
                neighbors.append(self.grid[new_x][new_y])

        return neighbors


def manhattan_distance(start: Cell, goal: Cell) -> int:
    """Calculate Manhattan distance heuristic."""
    return abs(start.x - goal.x) + abs(start.y - goal.y)


def weighted_manhattan_distance(start: Cell, goal: Cell, grid: FestivalGrid) -> float:
    """Enhanced heuristic that considers terrain costs."""
    base_distance = manhattan_distance(start, goal)
    # Use minimum possible cost to ensure admissibility
    return base_distance * min(costs.values())


def AStarSearch(grid: FestivalGrid, start_pos: Tuple[int, int],
                goal_pos: Tuple[int, int]):
    """
    Implement A* search algorithm for finding optimal path.
    Returns: (path, total_cost)
    """
    start = grid.grid[start_pos[0]][start_pos[1]]
    goal = grid.grid[goal_pos[0]][goal_pos[1]]

    # Priority queue for open set
    open_set = [(0., start)]
    heapq.heapify(open_set)

    # Keep track of visited nodes and their costs
    came_from = {}
    g_score = {(start.x, start.y): 0}
    f_score = {(start.x, start.y): weighted_manhattan_distance(start, goal, grid)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if (current.x, current.y) == (goal.x, goal.y):
            # Reconstruct path
            path = []
            current_pos = (current.x, current.y)
            while current_pos in came_from:
                path.append(current_pos)
                current_pos = came_from[current_pos]
            path.append((start.x, start.y))
            path.reverse()
            return path, g_score[(goal.x, goal.y)]

        for neighbor in grid.get_neighbors(current):
            tentative_g_score = g_score[(current.x, current.y)] + neighbor.cost

            if ((neighbor.x, neighbor.y) not in g_score or
                    tentative_g_score < g_score[(neighbor.x, neighbor.y)]):

                came_from[(neighbor.x, neighbor.y)] = (current.x, current.y)
                g_score[(neighbor.x, neighbor.y)] = tentative_g_score
                f_score[(neighbor.x, neighbor.y)] = (tentative_g_score +
                                                     weighted_manhattan_distance(neighbor, goal, grid))
                heapq.heappush(
                    open_set, (f_score[(neighbor.x, neighbor.y)], neighbor))

    return None, float('inf')  # No path found

# Example usage


def solve_festival_planning():
    # Example grid from assignment

    grid = FestivalGrid(example_grid)
    headquarters = (0, 0)
    stations = {
        'lights': (7, 3),
        'sweets': (2, 4),
        'diya': (6, 0),
        'rangoli': (5, 7)
    }
    remaining_stations_other_than_light_house = ['sweets', 'diya', 'rangoli']

    # First visit lights station (required)
    results = []
    pathToLightHouse, costToLightHouse = AStarSearch(
        grid, headquarters, stations['lights'])
    if pathToLightHouse:
        results.append(('Lights Station', pathToLightHouse, costToLightHouse + costs[example_grid[headquarters[0]][headquarters[1]]]))
    
    # Visit remaining stations in optimal order
    for idx, station in enumerate(remaining_stations_other_than_light_house):
        if idx != 0: 
            if pathToLightHouse:
                results.append(('Lights Station', pathToLightHouse, costToLightHouse))

        path, cost = AStarSearch(grid, stations['lights'], stations[station])
        if path:
            results.append((f'{station.capitalize()} Station', path, cost))
            # Return to headquarters
            return_path, return_cost = AStarSearch(
                grid, stations[station], headquarters)
            if return_path:
                results.append(('Return to HQ', return_path, return_cost))

    return results


if __name__ == "__main__":
    results = solve_festival_planning()
    total_cost = 0

    # -------------------------Printing statements--------------------------------------
    print("Festival Planning Results:")
    maxStationLen = max([len(results[i][0]) for i in range(0, len(results))])
    maxPathlen = max([len(str(results[i][1])) for i in range(0, len(results))])
    maxCostLen = max([len(str(results[i][2])) for i in range(0, len(results))])
    total_cost = sum(cost for _, _, cost in results)
    maxCostLen = max(len(str(total_cost)), maxCostLen)

    print('+'+"-" * (maxStationLen+2)+'+' + '-' *
          (maxPathlen+2)+'+'+'-' * (maxCostLen+2)+'+')
    print("|" + "Destination".center(maxStationLen+2) + "|" +
          "Path".center(maxPathlen+2) + "|" + "Cost".center(maxCostLen+2) + "|")
    print('+'+"-" * (maxStationLen+2)+'+' + '-' *
          (maxPathlen+2)+'+'+'-' * (maxCostLen+2)+'+')

    for station, path, cost in results:
        print("|"+f"{station}".center(maxStationLen+2)+"|" +
              f"{path}".center(maxPathlen+2)+"|" + f"{cost}".center(maxCostLen+2) + "|")

    print('+'+"-" * (maxStationLen+2)+'+' + '-' *
          (maxPathlen+2)+'+'+'-' * (maxCostLen+2)+'+')
    print("|"+"Total Cost for all trips".center(maxStationLen +
          maxPathlen+5)+"|"+f"{total_cost}".center(maxCostLen+2)+"|")
    print('+'+"-" * (maxStationLen+2)+'+' + '-' *
          (maxPathlen+2)+'+'+'-' * (maxCostLen+2)+'+')
