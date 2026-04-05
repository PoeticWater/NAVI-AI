class BuildingMap:
    def __init__(self):
        self.building_map = {
            "Entrance": ["Hallway 1-L", "Hallway 2", "Hallway 1-R"],

            "Hallway 1-L": ["Entrance", "Staircase #1", "Deep Learning Lab", "AV Hall #1", "Boys Restroom"],
            "Staircase #1": ["Hallway 1-L"],
            "Deep Learning Lab": ["Hallway 1-L"],
            "AV Hall #1": ["Hallway 1-L"],
            "Boys Restroom": ["Hallway 1-L"],

            "Hallway 1-R": ["Entrance", "Staff Room #1", "Project Lab", "AR/VR Lab"],
            "Staff Room #1": ["Hallway 1-R"],
            "Project Lab": ["Hallway 1-R"],
            "AR/VR Lab": ["Hallway 1-R"],

            "Hallway 2": ["Entrance", "Data Science Lab", "Exit1", "Staircase #2", "Hallway 3-L", "Hallway 3-R"],
            "Data Science Lab": ["Hallway 2", "Exit1"],
            "Staircase #2": ["Hallway 2"],

            "Hallway 3-L": ["Hallway 2", "OOPS Lab", "AV Hall #2", "Girls Restroom"],
            "OOPS Lab": ["Hallway 3-L"],
            "AV Hall #2": ["Hallway 3-L"],
            "Girls Restroom": ["Hallway 3-L"],
 
            "Hallway 3-R": ["Hallway 2", "Staff Room #2 (HOD Room)", "Class A", "Class B"],
            "Staff Room #2 (HOD Room)": ["Hallway 3-R"],
            "Class A": ["Hallway 3-R"],
            "Class B": ["Hallway 3-R"],

            "Exit1": ["Data Science Lab", "Hallway 2"]
        }
        
        self.coordinates = {
            "Entrance": (0, 0),

            "Hallway 1-L": (-1, 0),
            "Staircase #1": (-1, 1),
            "Deep Learning Lab": (-2, 1),
            "AV Hall #1": (-5, 1),
            "Boys Restroom": (-6, 1),

            "Hallway 1-R": (1, 0),
            "Staff Room #1": (1, 1),
            "Project Lab": (3, 1),
            "AR/VR Lab": (6, 1),

            "Hallway 2": (0, 3),
            "Data Science Lab": (-1, 3),
            "Staircase #2": (0, 8),

            "Hallway 3-L": (-1, 7),
            "OOPS Lab": (-1, 8),
            "AV Hall #2": (-5, 8),
            "Girls Restroom": (-6, 8),

            "Hallway 3-R": (1, 7),
            "Staff Room #2 (HOD Room)": (1, 8),
            "Class A": (3, 8),
            "Class B": (5, 8),

            "Exit1": (1, 3)
        }
        
        self.exits = ["Exit1", "Entrance"]

    # Utility functions
    def is_valid_location(self, location):
        return location in self.building_map

    def get_all_locations(self):
        return list(self.building_map.keys())

    def get_graph(self):
        return self.building_map

    def get_coordinates(self):
        return self.coordinates


# Test block
if __name__ == "__main__":
    bm = BuildingMap()

    print("Locations:")
    print(bm.get_all_locations())

    print("\nGraph:")
    print(bm.get_graph())

    print("\nCoordinates:")
    print(bm.get_coordinates())