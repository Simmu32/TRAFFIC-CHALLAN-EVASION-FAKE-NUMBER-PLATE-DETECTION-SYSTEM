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
from collections import deque

def check_suspicious(start):
    graph = {
        "DL01AB1234": ["Amit", "Rahul"],
        "Rahul": ["Suresh"],
        "DL02CD5678": ["Vikas"],
    }

    visited = set()
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)

        if node in graph:
            for neighbor in graph[node]:
                queue.append(neighbor)

    if len(visited) > 3:
        return {"suspicious": True, "chain": list(visited)}
    else:
        return {"suspicious": False, "chain": list(visited)}

