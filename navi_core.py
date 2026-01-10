from collections import deque

class NAVICore:
    def __init__(self, campus_map):
        self.map = campus_map

    def find_path(self, start, destination, role, preference=None):
        print("find_path() function called.")
        reasons = []

        if self.map.is_blocked(destination):
            reasons.append(f"Warning! The {destination} is blocked due to emergency.")
            return None, reasons
        
        if not self.map.is_accessible(destination, role):
            reasons.append(f"Notice! This {destination} is restricted for your '{role}' role.")
            return None, reasons

        queue = deque([[start]])
        visited = set()

        if preference:
            reasons.append(f"Routing preference applied: {preference}")

        while queue:
            path = queue.popleft()
            current = path[-1]

            if self.map.is_blocked(current):
                reasons.append(f"Warning! The {current} is blocked due to emergency.")
                continue

            if current == destination:
                print("Returning...", type(path), path)
                return path, reasons

            if current in visited:
                continue

            visited.add(current)

            neighbors = self.map.graph[current]

            if preference:
                neighbors = sorted(
                    neighbors,
                    key=lambda n: self.map.get_connection_type(current, n) != preference
                )

            for neighbor in neighbors:
                if self.map.is_blocked(neighbor):
                    reasons.append(f"Warning! The {neighbor} is blocked due to emergency.")
                    continue

                if not self.map.is_accessible(neighbor, role):
                    reasons.append(f"Notice! The {neighbor} is restricted for your '{role}' role.")
                    continue

                queue.append(path + [neighbor])

        reasons.append("Sorry, there is no valid route with the current constraints.")
        return None, reasons