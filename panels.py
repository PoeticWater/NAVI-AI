class PanelRegistry:
    def __init__(self):
        self.panels = {}

    def add_panel(self, panel_id, location):
        self.panels[panel_id] = location

    def get_location(self, panel_id):
        if panel_id not in self.panels:
            raise KeyError(f"Error! Unknown panel detected: {panel_id}")
        return self.panels.get(panel_id)
