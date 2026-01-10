import os
from PIL import Image, ImageTk
import tkinter as tk
from directions import generate_directions

def launch_gui(panels, campus, navi):
    root = tk.Tk()
    root.configure(bg="#000000")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(BASE_DIR,"assets","navi_logo.png")

    logo_img = Image.open(logo_path).resize((120, 120))
    logo = ImageTk.PhotoImage(logo_img)

    logo_label = tk.Label(root, image = logo, bg="#000000")
    logo_label.image = logo
    logo_label.pack(pady=10)

    root.title("NAVI Navigation Panel")
    root.geometry("700x500")

    header = tk.Label(
        root,
        text="NAVI — Campus Navigation Interface",
        font=("Segoe UI", 16, "bold")
    )
    header.pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    print("Logo path:", logo_path)
    print("Exists?", os.path.exists(logo_path))

    # Panel
    tk.Label(frame, text="Panel:", anchor="w").grid(row=0, column=0, sticky="w")
    panel_var = tk.StringVar(value=list(panels.panels.keys())[0])
    tk.OptionMenu(frame, panel_var, *panels.panels.keys()).grid(row=0, column=1)

    # Role
    tk.Label(frame, text="Role:", anchor="w").grid(row=1, column=0, sticky="w")
    role_var = tk.StringVar(value="visitor")
    tk.OptionMenu(frame, role_var, "visitor", "staff").grid(row=1, column=1)

    # Preference
    tk.Label(frame, text="Vertical Preference:", anchor="w").grid(row=2, column=0, sticky="w")
    pref_var = tk.StringVar(value="none")
    tk.OptionMenu(frame, pref_var, "none", "stairs", "elevator").grid(row=2, column=1)

    # Destination
    tk.Label(frame, text="Destination:", anchor="w").grid(row=3, column=0, sticky="w")
    dest_var = tk.StringVar(value=list(campus.graph.keys())[0])
    tk.OptionMenu(frame, dest_var, *campus.graph.keys()).grid(row=3, column=1)

    # Output
    output = tk.Text(root, height=12, width=80, font=("Consolas", 10))
    output.pack(pady=10)

    status = tk.Label(root, text="Ready.", anchor="w")
    status.pack(fill="x")

    def navigate():
        output.delete("1.0", tk.END)
        status.config(text="Computing route...")

        start = panels.get_location(panel_var.get())
        pref = pref_var.get()
        if pref == "none":
            pref = None

        path = navi.find_path(start, dest_var.get(), role_var.get(), pref)

        if path:
            for line in generate_directions(path):
                output.insert(tk.END, "• " + line + "\n")
            status.config(text="Route generated successfully.")
        else:
            output.insert(tk.END, "⚠ No valid route available.\n")
            status.config(text="Route failed.")

    tk.Button(root, text="Navigate", command=navigate).pack(pady=5)

    root.mainloop()