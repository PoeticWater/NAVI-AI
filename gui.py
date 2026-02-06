import os
import customtkinter as ctk
from PIL import Image
from directions import generate_directions

GF_COORDS = {
    "AIDS Block - Entrance (GF)": (400, 420),
    "AIDS Block - Stairs (GF)": (400, 340),
    "AIDS Block - Data Science Lab [CC18] (GF)": (400, 260),

    "AIDS Block - AV Hall 1 (GF)": (250, 420),
    "AIDS Block - RL Lab (GF)": (250, 340),

    "AIDS Block - Staff Room (GF)": (550, 340),
    "AIDS Block - Deep Learning Lab [CC16] (GF)": (650, 340),

    "AIDS Block - AV Hall 2 (GF)": (200, 180),
    "AIDS Block - OOPS Lab [CC20] (GF)": (300, 180),
    "AIDS Block - HOD & Staff Room (GF)": (500, 180),
}

# ---- THEME ----
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark")

def launch_gui(panels, campus, navi):
    app = ctk.CTk()
    app.configure(fg_color="#000000")
    app.title("NAVI Navigation Panel")
    app.geometry("900x900")
    app.resizable(False, False)

    # ---- Logo ----
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(BASE_DIR, "assets", "navi_logo.png")

    logo_img = ctk.CTkImage(
        light_image=Image.open(logo_path),
        dark_image=Image.open(logo_path),
        size=(120, 120)
    )

    ctk.CTkLabel(app, image=logo_img, text="").pack(pady=10)

    # ---- Header ----
    ctk.CTkLabel(
        app,
        text="NAVI — Campus Navigation Interface",
        font=("Segoe UI", 18, "bold"),
        text_color="#ff2a2a"
    ).pack(pady=5)

    status = ctk.CTkLabel(app, text="SYSTEM READY", text_color="#ff2a2a")
    status.pack()

    # ---- Emergency Mode ----
    emergency_var = ctk.BooleanVar(value = False)

    def toggle_emergency():
        if emergency_var.get():
            campus.block_location("Central Courtyard")
            status.configure(text="EMERGENCY MODE - rerouting in effect")
        else:
            campus.unblock_location("Central Courtyard")
            status.configure(text="Emergency cleared")
            
        compute_route()

    ctk.CTkSwitch(app, text="Emergency Mode",
    variable=emergency_var, command=toggle_emergency,
    text_color="#ff2a2a", fg_color="#222222",
    progress_color="#ff2a2a").pack(pady=6)

    # ---- Controls Frame ----
    frame = ctk.CTkFrame(app, fg_color="#000000")
    frame.pack(pady=15)

    # Panel
    panel_var = ctk.StringVar(value=list(panels.panels.keys())[0])
    ctk.CTkLabel(frame, text="Panel:", text_color="#ff2a2a")\
        .grid(row=0, column=0, sticky="w", pady=6, padx=8)
    ctk.CTkOptionMenu(frame, variable=panel_var,
        values=list(panels.panels.keys()), fg_color="#0a0a0a",
        button_color="#ff2a2a", button_hover_color="#ff5555",
        text_color="#ff2a2a", dropdown_fg_color="#0a0a0a",
        dropdown_text_color="#ff2a2a", dropdown_hover_color="#222222"
    ).grid(row=0, column=1, padx=12)
    
    # Role
    role_var = ctk.StringVar(value="visitor")
    ctk.CTkLabel(frame, text="Role:", text_color="#ff2a2a")\
        .grid(row=1, column=0, sticky="w", pady=6)
    ctk.CTkOptionMenu(frame, variable=role_var,
    values=["visitor", "staff"], fg_color="#0a0a0a",
    button_color="#ff2a2a", button_hover_color="#ff5555",
    text_color="#ff2a2a", dropdown_fg_color="#0a0a0a",
    dropdown_text_color="#ff2a2a", dropdown_hover_color="#222222"
    ).grid(row=1, column=1, padx=12)
    
    # Preference
    pref_var = ctk.StringVar(value="none")
    ctk.CTkLabel(frame, text="Preference:", text_color="#ff2a2a")\
        .grid(row=2, column=0, sticky="w", pady=6)
    ctk.CTkOptionMenu(frame, variable=pref_var,
    values=["none", "stairs", "elevator"], fg_color="#0a0a0a",
    button_color="#ff2a2a", button_hover_color="#ff5555",
    text_color="#ff2a2a", dropdown_fg_color="#0a0a0a",
    dropdown_text_color="#ff2a2a", dropdown_hover_color="#222222"
    ).grid(row=2, column=1, padx=12)
    
    # Destination
    dest_var = ctk.StringVar(value=list(campus.graph.keys())[0])
    ctk.CTkLabel(frame, text="Destination:", text_color="#ff2a2a")\
        .grid(row=3, column=0, sticky="w", pady=6)
    ctk.CTkOptionMenu(frame, variable=dest_var,
    values=list(campus.graph.keys()), fg_color="#0a0a0a",
    button_color="#ff2a2a", button_hover_color="#ff5555",
    text_color="#ff2a2a", dropdown_fg_color="#0a0a0a",
    dropdown_text_color="#ff2a2a", dropdown_hover_color="#222222"
    ).grid(row=3, column=1, padx=12)

    # ---- Canvas (MAP) ----
    canvas = ctk.CTkCanvas(
        app,
        width=800,
        height=500,
        bg="#050505",
        highlightthickness=0
    )
    canvas.pack(pady=10)

    canvas.create_text(400, 250, text="MAP CANVAS ACTIVE", fill="white", font=("Arial", 20))

    # ---- Output Console ----
    output = ctk.CTkTextbox(app,
        width=680, height=180,
        fg_color="#0a0a0a",
        text_color="#ff2a2a",
        border_color="#ff2a2a",
        border_width=1)
    output.pack(pady=15)

    # ---- Draw room layout ----
    def draw_rooms():
        ROOM_W, ROOM_H = 120, 50

        for name, (x, y) in GF_COORDS.items():
            canvas.create_rectangle(
                x - ROOM_W // 2,
                y - ROOM_H // 2,
                x + ROOM_W // 2,
                y + ROOM_H // 2,
                outline="#ff2a2a",
                width=2
            )

            canvas.create_text(
                x, y,
                text=name.replace("AIDS Block - ", "").replace(" (GF)", ""),
                fill="#ff2a2a",
                font=("Segoe UI", 9),
                width=110
            )

    # ---- Draw connections ----
    def draw_connections():
        for (a, b) in campus.connection_type.keys():
            if a in GF_COORDS and b in GF_COORDS:
                x1, y1 = GF_COORDS[a]
                x2, y2 = GF_COORDS[b]

                canvas.create_line(
                    x1, y1, x2, y2,
                    fill="#888888",
                    width=3
                )
                
    draw_connections()
    draw_rooms()

    # ---- Navigation Logic ----
    output.delete("1.0", "end")
    
    def compute_route():
        print("START: ", panel_var.get())
        print("DESTINATION: ", dest_var.get())
        print("ROLE: ", role_var.get())
        print("BLOCKED: ", campus.blocked)

        if not panel_var.get() or not dest_var.get():
            return

        status.configure(text="Computing route...")

        start = panels.get_location(panel_var.get())
        pref = pref_var.get()
        if pref == "none":
            pref = None

        path, reasons = navi.find_path(start, dest_var.get(), role_var.get(), pref)

        while path and isinstance(path[0], list):
            path = path[0]

        if path:
            output.insert("end", "ROUTE FOUND: \n")
            for line in generate_directions(path):
                output.insert("end", "• " + line + "\n")
            status.configure(text="Route generated.")

            if reasons:
                output.insert("end", "\nWHY THIS ROUTE: \n")
                for r in set(reasons):
                    output.insert("end", "- " + r + "\n")
        else:
            output.insert("end", "⚠ No valid route.\n")
            status.configure(text="Route failed.")

            if reasons:
                output.insert("end", "\nREASON:\n")
                for r in set(reasons):
                    output.insert("end", "- " + r + "\n")

    ctk.CTkButton(app, 
        text="NAVIGATE", command=compute_route,
        fg_color="#ff2a2a", hover_color="#ff5555",
        text_color="black"
    ).pack(pady=10)
    
    update_job = None

    def auto_update(*args):
        nonlocal update_job
        if update_job:
            app.after_cancel(update_job)
        update_job = app.after(300, compute_route)

    app.mainloop()