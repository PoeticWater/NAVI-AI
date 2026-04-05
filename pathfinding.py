# pathfinding.py
# A* algorithm for indoor navigation

import heapq

def a_star_search(building_map, coordinates, start, goal):
    """
    building_map : dict -> connections between locations
    coordinates : dict -> (x, y) positions of each location
    start : str -> starting point
    goal : str -> destination
    """

    # heuristic function (Euclidean distance)
    def heuristic(a, b):
        x1, y1 = coordinates[a]
        x2, y2 = coordinates[b]
        return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5

    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}

    g_score = {node: float('inf') for node in building_map}
    g_score[start] = 0

    f_score = {node: float('inf') for node in building_map}
    f_score[start] = heuristic(start, goal)

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor in building_map[current]:
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)

                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None


# Example test
if __name__ == "__main__":

    building_map = {
        "Entrance": ["Corridor"],
        "Corridor": ["Entrance", "Room1", "Room2", "Exit"],
        "Room1": ["Corridor"],
        "Room2": ["Corridor"],
        "Exit": ["Corridor"]
    }

    coordinates = {
        "Entrance": (0,0),
        "Corridor": (1,0),
        "Room1": (2,1),
        "Room2": (2,-1),
        "Exit": (3,0)
    }

    start = "Entrance"
    goal = "Room2"

    path = a_star_search(building_map, coordinates, start, goal)

    if path:
        print("Shortest Path:", " → ".join(path))
    else:
        print("No path found")