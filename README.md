# NAVI AI

NAVI AI (referred to as NAVI) is an indoor navigation and emergency evacuation routing system designed for complex campus and building environments.
The system uses graph-based navigation and the A* pathfinding algorithm to guide users through indoor environments and dynamically reroute paths during emergencies.

The project is being developed in multiple phases, evolving from a prototype navigation system into a full web-based indoor navigation platform.

---------------------

## Example

**Scenario:**  
A visitor at Block A wants to reach Block B during an emergency.

If the Central Courtyard is blocked:
No valid route is displayed.

Reason:
- Central Courtyard is due to emergency
- No alternate path exists

NAVI doesn't just fail - it explains why.

---------------------

## Future Plans

- Multi-floor elevator logic
- Modified UI aesthetics  
- Larger campus maps  
- Live sensor input  
- Mobile or web interface  
- Java backend version  

---------------------

## Phase 1: Basic Prototype (Completed)

Phase 1 focuses on NAVI’s basic navigation logic.

### Key Features
- Basic routing using BFS (Breath First Search) Algorithm.
- CustomTkinter UI for displaying the route.

This phase establishes the foundation for advanced navigation features such as
emergency routing, accessibility-aware paths, and intelligent UX improvements.

---------------------

## Phase 2: Map Visualisation (Completed)

Phase 2 focuses on visualising NAVI’s navigation logic through an interactive map representation of a building.

### Key Features
- Visual floor maps using PyQt
- Corridor-based routing visualisation
- Clear separation between navigation logic and UI rendering

This phase establishes the foundation for advanced navigation features such as
emergency routing, accessibility-aware paths, and intelligent UX improvements.

---------------------

## Phase 2.5: Frontend + Backend Update (Completed)

Phase 2.5 focuses on updating NAVI's Frontend and Backend with A* Pathfinding Algorithm and Web-based UI.

### Key Features
- Graph-based indoor navigation model
- A* pathfinding algorithm
- Web-based Navigation Console
- Control Console for emergency management
- Dynamic blocked location handling
- Automatic evacuation routing to nearest exit
- Flask backend with API-based routing
- Interactive building navigation interface
- Emergency status monitoring
- Modular system design (map, pathfinding, backend, frontend)
- Update Technology Stack

---------------------

## License

This project is a personal and experimental system.  
Inspired by fictional navigation concepts, but implemented independently.
