from map import BuildingMap
from navi_core import NAVICore
from panels import PanelRegistry
from qt_gui import NaviWindow, launch_qt_gui
from PyQt5.QtWidgets import QApplication
import sys

def run_gui():
    campus = setup_campus()
    navi = NAVICore(campus)
    
    app = QApplication(sys.argv)
    window = NaviWindow(campus, navi)
    
    window.show()
    sys.exit(app.exec_())

def setup_campus():
    campus = BuildingMap()
    add_block_aids(campus)
    return campus

def add_block_aids(campus):
    # ----------- Add rooms ---------
    campus.add_location("AIDS Block - Entrance (GF)")
    campus.add_location("AIDS Block - Staff Room (GF)")
    campus.add_location("AIDS Block - HOD & Staff Room (GF)")
    campus.add_location("AIDS Block - Data Science Lab [CC18] (GF)")
    campus.add_location("AIDS Block - Deep Learning Lab [CC16] (GF)")
    campus.add_location("AIDS Block - OOPS Lab [CC20] (GF)")
    campus.add_location("AIDS Block - RL Lab (GF)")
    campus.add_location("AIDS Block - AV Hall 1 (GF)")
    campus.add_location("AIDS Block - AV Hall 2 (GF)")
    campus.add_location("AIDS Block - Stairs (GF)")
    
    campus.add_location("AIDS Block - Staff Room (F1)")
    campus.add_location("AIDS Block - KEIS Lab [CC37] (F1)")
    campus.add_location("AIDS Block - Machine Learning [CC17] (F1)")
    campus.add_location("AIDS Block - Stairs (F1)")

    campus.add_location("AIDS Block - AV Hall 3 (F2)")
    campus.add_location("AIDS Block - Robotics Lab [CC19] (F2)")
    campus.add_location("AIDS Block - Stairs (F2)")

    # --------- Connect rooms --------
    campus.connect("AIDS Block - Entrance (GF)", "AIDS Block - RL Lab (GF)")
    campus.connect("AIDS Block - Entrance (GF)", "AIDS Block - AV Hall 1 (GF)")
    campus.connect("AIDS Block - Entrance (GF)", "AIDS Block - Staff Room (GF)")
    campus.connect("AIDS Block - Entrance (GF)", "AIDS Block - Data Science Lab [CC18] (GF)")
    campus.connect("AIDS Block - Entrance (GF)", "AIDS Block - Deep Learning Lab [CC16] (GF)")
    campus.connect("AIDS Block - Data Science Lab [CC18] (GF)", "AIDS Block - OOPS Lab [CC20] (GF)")
    campus.connect("AIDS Block - Data Science Lab [CC18] (GF)", "AIDS Block - HOD & Staff Room (GF)")
    campus.connect("AIDS Block - OOPS Lab [CC20] (GF)", "AIDS Block - AV Hall 2 (GF)")

    campus.connect("AIDS Block - Stairs (F1)", "AIDS Block - Machine Learning [CC17] (F1)")
    campus.connect("AIDS Block - Machine Learning [CC17] (F1)", "AIDS Block - KEIS Lab [CC37] (F1)")
    campus.connect("AIDS Block - KEIS Lab [CC37] (F1)", "AIDS Block - Staff Room (F1)")

    campus.connect("AIDS Block - Stairs (F2)", "AIDS Block - AV Hall 3 (F2)")
    campus.connect("AIDS Block - Stairs (F2)", "AIDS Block - Robotics Lab [CC19] (F2)")

    campus.connect("AIDS Block - Entrance (GF)", "AIDS Block - Stairs (GF)")
    campus.connect("AIDS Block - Stairs (GF)", "AIDS Block - Stairs (F1)", "stairs")
    campus.connect("AIDS Block - Stairs (F1)", "AIDS Block - Stairs (F2)", "stairs")

def setup_panels():
    panels = PanelRegistry()
    panels.add_panel("AIDS Block - GF Stairs (Panel)", "AIDS Block - Stairs (GF)")
    panels.add_panel("AIDS Block - F1 Stairs (Panel)", "AIDS Block - Stairs (F1)")
    panels.add_panel("AIDS Block - F2 Stairs (Panel)", "AIDS Block - Stairs (F2)")
    return panels

# ENTRY POINT
if __name__ == "__main__":
    run_gui()