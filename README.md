# NAVI AI 

NAVI AI (simply called NAVI) is a Python-based intelligent navigation system designed to guide users through complex campus environments.  
It provides real-time routing, role-based access control, emergency-aware pathfinding, and human-readable directions through a graphical interface.

This project was created as a personal initiative to turn a fictional navigation system into a real, functional application.

---------------------

## Features

- **Graph-Based Navigation**  
  Computes shortest and valid paths between locations using a graph model of the campus.

- **Role-Based Routing**  
  Certain locations can be restricted based on user roles (e.g., visitor, staff).

- **Emergency Mode**  
  Locations can be blocked in real time, forcing NAVI to re-route or explain why a route is unavailable.

- **Preference-Aware Routing**  
  Users can prefer stairs or elevators when moving between floors.

- **Graphical Control Panels**  
  Users interact with NAVI through virtual navigation panels placed around the campus.

- **Human-Readable Directions**  
  Routes are converted into clear step-by-step instructions.

- **Route Explanations**  
  When a route is chosen or rejected, NAVI explains why (blocked areas, role restrictions, etc.).

---------------------

## How does NAVI work?

NAVI represents the campus as a 'graph':

- Nodes = rooms, corridors, stairs, outdoor spaces  
- Edges = walkable connections between them  

Breadth-First Search (BFS) algorithm is used to find valid routes while considering:

- Emergency blocks  
- User role restrictions  
- Movement preferences (stairs or elevator)

---------------------

## User Interface

The system includes a CustomTkinter-based control panel where users can:

- Select their current panel location  
- Choose their role  
- Set movement preferences  
- Select a destination  
- Activate emergency mode  

NAVI instantly calculates and displays the best route.

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

## Technologies Used

- Python  
- CustomTkinter  
- Pillow (PIL)  
- Graph algorithms (BFS)  

---------------------

## Future Plans

- Multi-floor elevator logic
- Modified UI aesthetics  
- Larger campus maps  
- Live sensor input  
- Mobile or web interface  
- Java backend version  

---------------------

## License

This project is a personal and experimental system.  
Inspired by fictional navigation concepts, but implemented independently.