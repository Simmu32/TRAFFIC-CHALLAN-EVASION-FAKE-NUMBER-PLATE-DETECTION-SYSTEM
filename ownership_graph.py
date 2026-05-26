import networkx as nx
from database_setup import get_db_connection
from datetime import datetime, timedelta

def build_ownership_graph():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT owner_id, plate_number FROM RegisteredVehicles")
    vehicles = cursor.fetchall()
    cursor.execute("SELECT owner_id, plate_number, relationship, transfer_date FROM OwnershipGraph")
    transfers = cursor.fetchall()
    conn.close()
    
    G = nx.Graph()
    for owner, plate in vehicles:
        G.add_node(owner, node_type='owner')
        G.add_node(plate, node_type='vehicle')
        G.add_edge(owner, plate, relationship='registration')
    
    for owner, plate, rel, tdate in transfers:
        G.add_edge(owner, plate, relationship=rel, transfer_date=tdate)
    return G

def bfs_traverse(graph, start_node):
    if start_node not in graph:
        return []
    visited = set()
    queue = [start_node]
    visited.add(start_node)
    while queue:
        node = queue.pop(0)
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return list(visited)

def find_connected_vehicles(graph, owner_id):
    nodes = bfs_traverse(graph, owner_id)
    return [n for n in nodes if graph.nodes[n].get('node_type') == 'vehicle']

def detect_suspicious_patterns(graph):
    suspicious = []
    for node in graph.nodes:
        if graph.nodes[node].get('node_type') == 'owner':
            vehicles = find_connected_vehicles(graph, node)
            if len(vehicles) > 3:
                suspicious.append({"owner": node, "reason": f"Has {len(vehicles)} vehicles (>3)"})
            # Check recent transfers
            for edge in graph.edges(node, data=True):
                if 'transfer_date' in edge[2]:
                    tdate = datetime.strptime(edge[2]['transfer_date'], '%Y-%m-%d')
                    if (datetime.now() - tdate) < timedelta(days=30):
                        suspicious.append({"owner": node, "reason": "Recent transfer (<30 days)"})
    return suspicious

def find_shortest_path(graph, node1, node2):
    try:
        return nx.shortest_path(graph, node1, node2)
    except nx.NetworkXNoPath:
        return None

def export_graph_json(graph):
    data = nx.node_link_data(graph)
    return data