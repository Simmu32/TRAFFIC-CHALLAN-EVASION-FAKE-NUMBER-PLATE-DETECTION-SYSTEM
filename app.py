try:
    from flask import Flask, request, jsonify
except ImportError as e:
    raise ImportError(
        "Flask is not installed. Install it with `pip install flask`."
    ) from e
from config import Config
from utils import response_formatter, validate_input, export_to_csv
from database_setup import get_db_connection
import pattern_matcher as pm
import kmp_search as kmp
import ownership_graph as og
import greedy_camera_optimization as gco
import logging

app = Flask(__name__)
app.config.from_object(Config)
logger = logging.getLogger(__name__)

@app.after_request
def add_cors_headers(response):
    origins = Config.CORS_ORIGINS
    if isinstance(origins, (list, tuple)):
        origins = ', '.join(origins)
    response.headers['Access-Control-Allow-Origin'] = origins
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

# ------------------- Core Verification APIs -------------------
@app.route('/api/validate_plate', methods=['POST'])
@validate_input(['plate_number'])
def validate_plate():
    data = request.get_json()
    plate = data['plate_number']
    valid_format = pm.validate_plate_format(plate)
    char_valid, char_msg = pm.check_character_validity(plate)
    fakes = pm.detect_common_fakes(plate)
    return jsonify(response_formatter(True, data={
        'format_valid': valid_format,
        'character_valid': char_valid,
        'character_message': char_msg,
        'fake_patterns': fakes
    }))

@app.route('/api/search_plate', methods=['POST'])
@validate_input(['partial_plate'])
def search_plate():
    data = request.get_json()
    partial = data['partial_plate']
    matches = kmp.search_plate_in_database(partial)
    return jsonify(response_formatter(True, data={'matches': matches, 'count': len(matches)}))

@app.route('/api/check_ownership', methods=['POST'])
@validate_input(['owner_id'])
def check_ownership():
    data = request.get_json()
    owner_id = data['owner_id']
    G = og.build_ownership_graph()
    vehicles = og.find_connected_vehicles(G, owner_id)
    suspicious = og.detect_suspicious_patterns(G)
    owner_susp = [s for s in suspicious if s['owner'] == owner_id]
    return jsonify(response_formatter(True, data={
        'owner': owner_id,
        'connected_vehicles': vehicles,
        'suspicious': owner_susp
    }))

@app.route('/api/verify_complete', methods=['POST'])
@validate_input(['plate_number', 'owner_id'])
def verify_complete():
    data = request.get_json()
    plate = data['plate_number']
    owner = data['owner_id']
    # Pattern check
    pattern_valid = pm.validate_plate_format(plate)
    # KMP search to see if plate exists
    exists = len(kmp.search_plate_in_database(plate)) > 0
    # Ownership graph
    G = og.build_ownership_graph()
    vehicles = og.find_connected_vehicles(G, owner)
    suspicious = any(s['owner'] == owner for s in og.detect_suspicious_patterns(G))
    return jsonify(response_formatter(True, data={
        'plate': plate,
        'pattern_valid': pattern_valid,
        'registered': exists,
        'connected_vehicles': vehicles,
        'suspicious_ownership': suspicious
    }))

# ------------------- Data Retrieval APIs (paginated) -------------------
def paginate(query, page, per_page):
    conn = get_db_connection()
    cursor = conn.cursor()
    offset = (page-1)*per_page
    cursor.execute(query + f" LIMIT {per_page} OFFSET {offset}")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.route('/api/vehicles')
def get_vehicles():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    data = paginate("SELECT * FROM RegisteredVehicles", page, per_page)
    return jsonify(response_formatter(True, data=data))

@app.route('/api/challans')
def get_challans():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    data = paginate("SELECT * FROM ChallanHistory", page, per_page)
    return jsonify(response_formatter(True, data=data))

@app.route('/api/vehicle/<plate>')
def get_vehicle(plate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM RegisteredVehicles WHERE plate_number=?", (plate,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify(response_formatter(True, data=dict(row)))
    return jsonify(response_formatter(False, error="Vehicle not found")), 404

@app.route('/api/owner/<owner_id>')
def get_owner(owner_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM RegisteredVehicles WHERE owner_id=?", (owner_id,))
    vehicles = [dict(row) for row in cursor.fetchall()]
    cursor.execute("SELECT * FROM ChallanHistory WHERE violator_id=?", (owner_id,))
    challans = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(response_formatter(True, data={'vehicles': vehicles, 'challans': challans}))

@app.route('/api/challan/<int:challan_id>')
def get_challan(challan_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ChallanHistory WHERE challan_id=?", (challan_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify(response_formatter(True, data=dict(row)))
    return jsonify(response_formatter(False, error="Challan not found")), 404

# ------------------- Statistics APIs -------------------
@app.route('/api/stats/overview')
def stats_overview():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM RegisteredVehicles")
    total_vehicles = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM ChallanHistory")
    total_challans = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(amount) FROM ChallanHistory WHERE paid_status=1")
    total_collected = cursor.fetchone()[0] or 0
    conn.close()
    return jsonify(response_formatter(True, data={
        'total_vehicles': total_vehicles,
        'total_challans': total_challans,
        'total_amount_collected': total_collected
    }))

@app.route('/api/stats/violations')
def stats_violations():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT violation_type, COUNT(*) as cnt FROM ChallanHistory GROUP BY violation_type")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(response_formatter(True, data=rows))

@app.route('/api/stats/payment')
def stats_payment():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT paid_status, COUNT(*) FROM ChallanHistory GROUP BY paid_status")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(response_formatter(True, data=rows))

@app.route('/api/stats/states')
def stats_states():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUBSTR(plate_number,1,2) as state, COUNT(*) FROM RegisteredVehicles GROUP BY state")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(response_formatter(True, data=rows))

# ------------------- Integration APIs for Person 2 & 4 -------------------
@app.route('/api/owners/features')
def owners_features():
    G = og.build_ownership_graph()
    features = []
    for node in G.nodes:
        if G.nodes[node].get('node_type') == 'owner':
            features.append({
                'owner_id': node,
                'num_vehicles': len(og.find_connected_vehicles(G, node))
            })
    return jsonify(response_formatter(True, data=features))

@app.route('/api/network/graph')
def network_graph():
    G = og.build_ownership_graph()
    data = og.export_graph_json(G)
    return jsonify(response_formatter(True, data=data))

@app.route('/api/camera/optimization')
def camera_optimization():
    result = gco.greedy_camera_optimization()
    return jsonify(response_formatter(True, data=result))

@app.route('/api/camera/costbenefit')
def camera_costbenefit():
    result = gco.cost_benefit_analysis()
    return jsonify(response_formatter(True, data=result))

# ------------------- Health Check -------------------
@app.route('/api/health')
def health():
    return jsonify(response_formatter(True, data={'status': 'healthy'}))

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=5001)