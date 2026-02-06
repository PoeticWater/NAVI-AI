import sys
from PyQt5.QtWidgets import (
    QComboBox, QPushButton, QWidget,
    QVBoxLayout, QHBoxLayout,
    QApplication, QMainWindow,
    QGraphicsScene, QGraphicsView
)
from PyQt5.QtGui import QPen, QColor, QPainter
from PyQt5.QtCore import Qt

GF_COORDS = {
    "AIDS Block - Entrance (GF)": (100, 350),
    "AIDS Block - RL Lab (GF)": (100, 260),
    "AIDS Block - AV Hall 1 (GF)": (100, 440),

    "AIDS Block - Data Science Lab [CC18] (GF)": (300, 350),
    "AIDS Block - Deep Learning Lab [CC16] (GF)": (480, 350),

    "AIDS Block - OOPS Lab [CC20] (GF)": (300, 260),
    "AIDS Block - HOD & Staff Room (GF)": (480, 260),

    "AIDS Block - AV Hall 2 (GF)": (300, 180),
}
F1_COORDS = {
    "AIDS Block - Stairs (F1)": (300, 350),
    "AIDS Block - Machine Learning [CC17] (F1)": (300, 260),
    "AIDS Block - KEIS Lab [CC37] (F1)": (480, 260),
    "AIDS Block - Staff Room (F1)": (480, 350),
}
F2_COORDS = {
    "AIDS Block - Stairs (F2)": (300, 350),
    "AIDS Block - Robotics Lab [CC19] (F2)": (300, 260),
    "AIDS Block - AV Hall 3 (F2)": (480, 260),
}

def get_floor(room_name):
    if "(GF)" in room_name:
        return "GF"
    if "(F1)" in room_name:
        return "F1"
    if "(F2)" in room_name:
        return "F2"
    return None

def get_coords_for_floor(floor):
    if floor == "GF":
        return GF_COORDS
    if floor == "F1":
        return F1_COORDS
    if floor == "F2":
        return F2_COORDS
    return None

def split_path_by_floor(path):
    floors = {}
    for room in path:
        floor = get_floor(room)
        if floor:
            floors.setdefault(floor, []).append(room)
    return floors

class NaviWindow(QMainWindow):
    def __init__(self, campus, navi):
        super().__init__()
        self.campus = campus
        self.navi = navi
        self.current_floor = "GF"

        self.route_items = []
        self.full_path = []
        self.path_by_floor = {}

        self.setWindowTitle("NAVI — Map Visualisation (PyQt5)")
        self.setGeometry(100, 100, 900, 600)

        # ---- Scene (map world) ----
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QColor("#050505"))

        # ---- View (camera) ----
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(self.view)

        control_widget = QWidget()
        control_layout = QHBoxLayout()

        self.floor_combo = QComboBox()
        self.floor_combo.addItems(["GF", "F1", "F2"])
        self.floor_combo.setFixedWidth(80)

        control_layout.addWidget(self.floor_combo)
        self.floor_combo.currentTextChanged.connect(self.on_floor_changed)

        self.start_combo = QComboBox()
        self.dest_combo = QComboBox()

        self.start_combo.clear()
        self.dest_combo.clear()
        
        all_rooms = sorted(self.campus.graph.keys())
        self.start_combo.addItems(all_rooms)
        self.dest_combo.addItems(all_rooms)

        navigate_btn = QPushButton("Navigate")
        
        control_layout.addWidget(self.start_combo)
        control_layout.addWidget(self.dest_combo)
        control_layout.addWidget(navigate_btn)

        control_widget.setLayout(control_layout)
        control_widget.setFixedHeight(50)

        main_layout = QVBoxLayout()
        main_layout.addWidget(control_widget)
        main_layout.addWidget(self.view)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        navigate_btn.clicked.connect(self.on_navigate_clicked)

        self.redraw_floor()

    def on_floor_changed(self, floor):
        self.current_floor = floor
        self.redraw_floor()

    def format_label(self, text):
        text = text.replace("AIDS Block - ", "").replace(" (GF)", "")
        
        if len(text) > 18:
            words = text.split(" ")
            mid = len(words) // 2
            return " ".join(words[:mid]) + "\n" + " ".join(words[mid:])
        
        return text

    def draw_rooms(self, coords):
        ROOM_W, ROOM_H = 140, 60
        room_pen = QPen(QColor("#ff2a2a"))
        room_pen.setWidth(2)
        text_color = QColor("#ff2a2a")

        for room, (x, y) in coords.items():
            self.scene.addRect(x, y, ROOM_W, ROOM_H, room_pen)
            
            label_text = self.format_label(room)
            text_item = self.scene.addText(label_text)

            font = text_item.font()
            font.setPointSize(9)
            font.setBold(True)
            text_item.setFont(font)
            text_item.setDefaultTextColor(text_color)

            text_rect = text_item.boundingRect()
            text_item.setPos( 
                x + (ROOM_W - text_rect.width()) / 2,
                y + (ROOM_H - text_rect.height()) / 2
            )

    def draw_corridors(self, coords):
        corridor_pen = QPen(QColor("#888888"))
        corridor_pen.setWidth(4)
        ROOM_W, ROOM_H = 140, 60
        
        for (a, b), _ in self.campus.connection_type.items():
            if a in coords and b in coords:
                x1, y1 = coords[a]
                x2, y2 = coords[b]
                
                cx1 = x1 + ROOM_W // 2
                cy1 = y1 + ROOM_H // 2
                cx2 = x2 + ROOM_W // 2
                cy2 = y2 + ROOM_H // 2

                self.scene.addLine(cx1, cy1, cx2, cy2, corridor_pen)
    
    def clear_route(self):
        for item in getattr(self, "route_items", []):
            self.scene.removeItem(item)
        self.route_items = []

    def redraw_floor(self):
        self.scene.clear()
        self.route_items = []

        coords = get_coords_for_floor(self.current_floor)
        if not coords:
            return
        
        self.draw_corridors(coords)
        self.draw_rooms(coords)

        floor_path = self.path_by_floor.get(self.current_floor, [])
        if len(floor_path) > 1:
            self.draw_route(floor_path)

    def advance_floor(self):
        floors = list(self.path_by_floor.keys())
        if self.current_floor in floors:
            idx = floors.index(self.current_floor)
            if idx + 1 < len(floors):
                self.current_floor = floors[idx + 1]
                self.redraw_floor()

    def draw_route(self, path):
        self.clear_route()

        route_pen = QPen(QColor("#ff2a2a"))
        route_pen.setWidth(6)
        route_pen.setCapStyle(Qt.RoundCap)

        ROOM_W, ROOM_H = 140, 60

        for i in range(len(path) - 1):
            a = path[i]
            b = path[i + 1]

            if get_floor(a) != self.current_floor:
                continue

            coords = get_coords_for_floor(self.current_floor)
            if a not in coords or b not in coords:
                continue

            x1, y1 = coords[a]
            x2, y2 = coords[b]

            cx1 = x1 + ROOM_W // 2
            cy1 = y1 + ROOM_H // 2
            cx2 = x2 + ROOM_W // 2
            cy2 = y2 + ROOM_H // 2
                
            line = self.scene.addLine(cx1, cy1, cx2, cy2, route_pen)
            self.route_items.append(line)

    def navigate(self, start, destination, role = "visitor", preference = None):
        path = self.navi.find_path(start, destination, role, preference)

        if isinstance(path, tuple):
            path = path[0]

        if not path:
            self.clear_route()
            return
        
        self.full_path = path
        self.path_by_floor = split_path_by_floor(path)

        self.current_floor = get_floor(path[0])
        self.redraw_floor()

    def on_navigate_clicked(self):
        start = self.start_combo.currentText()
        destination = self.dest_combo.currentText()

        self.navigate(start, destination)

    def update_route(self, path):
        if isinstance(path, tuple):
            path = path[0]

        if path:
            self.draw_route(path)
        else:
            self.clear_route()

def launch_qt_gui(campus):
    app = QApplication(sys.argv)
    window = NaviWindow(campus)
    window.show()
    sys.exit(app.exec_())