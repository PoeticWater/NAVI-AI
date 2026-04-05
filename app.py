from flask import Flask, render_template, request, jsonify
from building_map import BuildingMap
from pathfinding import a_star_search
import copy

app = Flask(__name__)

bm = BuildingMap()
graph = bm.get_graph()
coordinates = bm.get_coordinates()

emergency_state = {
    "active": False,
    "blocked": None
}


@app.route("/")
def home():
    return render_template("navigation.html")


@app.route("/navigation")
def navigation_page():
    return render_template("navigation.html")


@app.route("/control")
def control_page():
    return render_template("control.html")


@app.route("/find_path", methods=["POST"])
def find_path():
    data = request.get_json()
    start = data.get("start")
    end = data.get("end")

    if not bm.is_valid_location(start):
        return jsonify({"result": "Invalid start location entered."})

    if emergency_state["active"]:
        emergency_graph = copy.deepcopy(graph)
        blocked = emergency_state["blocked"]

        if blocked in emergency_graph:
            del emergency_graph[blocked]

        for node in emergency_graph:
            if blocked in emergency_graph[node]:
                emergency_graph[node].remove(blocked)

        safe_path = None
        chosen_exit = None
        shortest_length = float("inf")

        for exit_node in bm.exits:
            if exit_node in emergency_graph and start in emergency_graph:
                possible_path = a_star_search(emergency_graph, coordinates, start, exit_node)
                if possible_path:
                    path_length = len(possible_path)
                    if path_length < shortest_length:
                        shortest_length = path_length
                        safe_path = possible_path
                        chosen_exit = exit_node

        if safe_path:
            return jsonify({
                "result": f"🚨 Emergency Active\nBlocked Location: {blocked}\nNearest Safe Exit: {chosen_exit}\nEvacuation Path: {' → '.join(safe_path)}"
            })
        else:
            return jsonify({
                "result": f"🚨 Emergency Active\nBlocked Location: {blocked}\nNo safe evacuation route found."
            })

    if not bm.is_valid_location(end):
        return jsonify({"result": "Invalid destination entered."})

    path = a_star_search(graph, coordinates, start, end)

    if path:
        return jsonify({"result": "Navigation Path: " + " → ".join(path)})
    else:
        return jsonify({"result": "No path found."})


@app.route("/trigger_emergency", methods=["POST"])
def trigger_emergency():
    data = request.get_json()
    blocked = data.get("blocked")

    if not bm.is_valid_location(blocked):
        return jsonify({"result": "Invalid blocked location."})

    emergency_state["active"] = True
    emergency_state["blocked"] = blocked

    return jsonify({
        "result": f"Emergency triggered successfully.\nBlocked Location: {blocked}"
    })


@app.route("/reset_emergency", methods=["POST"])
def reset_emergency():
    emergency_state["active"] = False
    emergency_state["blocked"] = None

    return jsonify({"result": "Emergency status reset successfully."})


@app.route("/status", methods=["GET"])
def status():
    return jsonify(emergency_state)


if __name__ == "__main__":
    app.run(debug=True)