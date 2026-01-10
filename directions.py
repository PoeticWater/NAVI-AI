def generate_directions(path):
    while path and isinstance(path[0], list):
        path = path[0]
    
    directions = []

    for i in range(len(path)):
        current = path[i]

        if i == 0:
            directions.append(f"Start at {clean_name(current)}")
            continue

        previous = path[i - 1]

        # Floor change
        if "Stairs" in previous and "Stairs" in current:
            floor = current.split("(")[-1].replace(")", "")
            directions.append(f"Take the stairs to Floor {floor.replace('F', '')}")
        elif "Entrance" in current:
            directions.append(f"Enter {clean_name(current)}")
        elif "Courtyard" in current or "Walkway" in current:
            directions.append(f"Proceed through {clean_name(current)}")
        else:
            directions.append(f"Proceed to {clean_name(current)}")

    directions.append("You have arrived at your destination.")
    return directions


def clean_name(name):
    return name.split("(")[0].strip()
