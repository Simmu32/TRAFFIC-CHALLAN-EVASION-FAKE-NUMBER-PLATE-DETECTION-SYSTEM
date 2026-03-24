from flask import Flask, request, jsonify

# Import your modules
from pattern_matching import is_valid_plate
from kmp_searching import search_plate_in_db
from ownership_graph import check_suspicious

app = Flask(__name__)

# -------------------------------
# 1. Pattern Matching API
# -------------------------------
@app.route('/api/validate_plate', methods=['POST'])
def validate_plate():
    data = request.get_json()
    plate = data.get("plate", "").upper()

    result = is_valid_plate(plate)

    return jsonify({
        "plate": plate,
        "valid_format": result
    })


# -------------------------------
# 2. KMP Search API
# -------------------------------
@app.route('/api/search_plate', methods=['POST'])
def search_plate():
    data = request.get_json()
    plate = data.get("plate", "").upper()

    result = search_plate_in_db(plate)

    return jsonify(result)


# -------------------------------
# 3. BFS Ownership API
# -------------------------------
@app.route('/api/check_ownership', methods=['POST'])
def check_ownership_api():
    data = request.get_json()
    start = data.get("input", "")

    result = check_suspicious(start)

    return jsonify(result)

@app.route('/')
def home():
    return "Traffic Challan System API Running 🚀"
# -------------------------------
# Run Server
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)