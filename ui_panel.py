def panel_interface(panels, navi, campus):
    print("\n=== NAVI PANEL INTERFACE ===")

    print("Available panels:")
    for panel in panels.panels:
        print("-", panel)

    panel_id = input("\nSelect panel ID: ").strip()
    start = panels.get_location(panel_id)

    if not start:
        print("Invalid panel.")
        return

    role = input("Enter role (visitor/staff): ").strip().lower()

    print("\nAvailable destinations:")
    for location in campus.graph:
        print("-", location)

    destination = input("\nEnter destination: ").strip()

    path = navi.find_path(start, destination, role)

    if path:
        from directions import generate_directions
        directions = generate_directions(path)
        print("\nNAVI Guidance:")
        for line in directions:
            print("•", line)
    else:
        print("\n⚠ Unable to generate route.")
        print("Reason: Access restriction, emergency block, or unreachable path.")
