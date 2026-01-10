from map import BuildingMap
from navi_core import NAVICore
from panels import PanelRegistry
from ui.gui import launch_gui

def setup_campus():
    campus = BuildingMap()

    # -------- Building A --------
    campus.add_location("Block A - Entrance (F1)")
    campus.add_location("Block A - Lobby (F1)")
    campus.add_location("Block A - Stairs (F1)")
    campus.add_location("Block A - Stairs (F2)")
    campus.add_location("Block A - Corridor (F2)")
    campus.add_location("Block A - Room 201 (F2)")

    campus.connect("Block A - Entrance (F1)", "Block A - Lobby (F1)")
    campus.connect("Block A - Lobby (F1)", "Block A - Stairs (F1)", "stairs")
    campus.connect("Block A - Stairs (F1)", "Block A - Stairs (F2)", "stairs")
    campus.connect("Block A - Stairs (F2)", "Block A - Corridor (F2)")
    campus.connect("Block A - Corridor (F2)", "Block A - Room 201 (F2)")

    # -------- Outdoor --------
    campus.add_location("Campus Walkway")
    campus.add_location("Central Courtyard")

    campus.connect("Block A - Entrance (F1)", "Campus Walkway")
    campus.connect("Campus Walkway", "Central Courtyard")

    # -------- Building B --------
    campus.add_location("Block B - Entrance (F1)")
    campus.add_location("Block B - Lobby (F1)")
    campus.add_location("Block B - Corridor (F1)")
    campus.add_location("Block B - Lab 102 (F1)")

    campus.connect("Central Courtyard", "Block B - Entrance (F1)")
    campus.connect("Block B - Entrance (F1)", "Block B - Lobby (F1)")
    campus.connect("Block B - Lobby (F1)", "Block B - Corridor (F1)")
    campus.connect("Block B - Corridor (F1)", "Block B - Lab 102 (F1)")

    return campus

def setup_panels():
    panels = PanelRegistry()
    panels.add_panel("Block A - Entrance (Panel)", "Block A - Entrance (F1)")
    panels.add_panel("Courtyard (Panel)", "Central Courtyard")
    panels.add_panel("Block B - Entrance (Panel)", "Block B - Entrance (F1)")
    return panels

def run_gui():
    campus = setup_campus()
    panels = setup_panels()
    navi = NAVICore(campus)
    launch_gui(panels, campus, navi)

# ENTRY POINT
if __name__ == "__main__":
    run_gui()