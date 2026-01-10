class BuildingMap:
    def __init__(self):
        self.graph = {}
        self.restricted = {}     # role-based access
        self.blocked = set()     # emergency blocks
        self.connection_type = {}  # stairs / elevator / normal

    def add_location(self, location, allowed_roles=None):
        if allowed_roles is None:
            self.restricted.pop(location, None)
        if location not in self.graph:
            self.graph[location] = []
        if allowed_roles is not None:
            self.restricted[location] = allowed_roles

    def connect(self, loc1, loc2, ctype="normal"):
        if loc1 not in self.graph or loc2 not in self.graph:
            raise ValueError(f"Cannot connect unknown locations: {loc1}, {loc2}")
        
        self.graph[loc1].append(loc2)
        self.graph[loc2].append(loc1)
        self.connection_type[(loc1, loc2)] = ctype
        self.connection_type[(loc2, loc1)] = ctype

    def block_location(self, location):
        self.blocked.add(location)

    def unblock_location(self, location):
        self.blocked.discard(location)

    def is_blocked(self, location):
        return location in self.blocked

    def is_accessible(self, location, role):
        if location in self.blocked:
            return False
        if location not in self.restricted:
            return True
        return role in self.restricted[location]

    def get_connection_type(self, a, b):
        return self.connection_type.get((a, b), "normal")


