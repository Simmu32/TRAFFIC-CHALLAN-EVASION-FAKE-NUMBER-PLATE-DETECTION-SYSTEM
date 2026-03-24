import sqlite3
from collections import deque

# -------------------------------
# Build Graph from Database
# -------------------------------
def build_graph():
    conn = sqlite3.connect("traffic_system.db")
    cursor = conn.cursor()

    cursor.execute("SELECT person_name, plate_number FROM OwnershipGraph")
    data = cursor.fetchall()

    conn.close()

    graph = {}

    for person, plate in data:
        # Connect person -> plate
        if person not in graph:
            graph[person] = []
        graph[person].append(plate)

        # Connect plate -> person (undirected graph)
        if plate not in graph:
            graph[plate] = []
        graph[plate].append(person)

    return graph


# -------------------------------
# BFS Traversal
# -------------------------------
def bfs_traversal(start):
    graph = build_graph()

    visited = set()
    queue = deque([start])

    connected_people = set()
    connected_vehicles = set()

    while queue:
        node = queue.popleft()

        if node not in visited:
            visited.add(node)

            # Separate people and vehicles
            if node.isalpha() or " " in node:
                connected_people.add(node)
            else:
                connected_vehicles.add(node)

            # Traverse neighbors
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    queue.append(neighbor)

    return connected_people, connected_vehicles


# -------------------------------
# Suspicious Detection
# -------------------------------
def check_suspicious(start):
    people, vehicles = bfs_traversal(start)

    suspicious = False

    # Simple rule: if a person has more than 2 vehicles
    if len(vehicles) > 2:
        suspicious = True

    return {
        "connected_people": list(people),
        "connected_vehicles": list(vehicles),
        "suspicious": suspicious
    }


# -------------------------------
# Test
# -------------------------------
if __name__ == "__main__":
    start_node = "Ramesh Kumar"   # try person name or plate
    result = check_suspicious(start_node)
    print(result)