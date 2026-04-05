from flask import Flask, request, jsonify, render_template

# Import modules
from pattern_matching import is_valid_plate
from kmp_searching import search_plate_in_db
from ownership_graph import check_suspicious
from Plate_check import check_single_plate

app = Flask(__name__)

# -------------------------------
# HOME PAGE
# -------------------------------
@app.route('/')
def home():
    return render_template("home.html")

# -------------------------------
# FULL CHECK API
# -------------------------------
@app.route('/api/full_check', methods=['POST'])
def full_check():
    data = request.get_json()
    plate = data.get("plate", "").upper()

    # Step 1: Format check
    valid = is_valid_plate(plate)
    if not valid:
        return jsonify({
            "plate": plate,
            "status": "Invalid Format ❌"
        })

    # Step 2: Search DB
    search_result = search_plate_in_db(plate)

    # Step 3: Ownership
    ownership = check_suspicious(plate)

    # Step 4: Similarity
    similarity = check_single_plate(plate, [
        "DL01AB1234",
        "DL02CD5678",
        "UP03EF9012"
    ])

    return jsonify({
        "plate": plate,
        "valid_format": valid,
        "search_result": search_result,
        "ownership": ownership,
        "similarity": similarity
    })

# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)