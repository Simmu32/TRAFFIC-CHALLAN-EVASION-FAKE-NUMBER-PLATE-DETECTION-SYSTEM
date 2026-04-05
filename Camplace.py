from flask import Flask, request, jsonify
import sqlite3
from sklearn.linear_model import LogisticRegression

try:
    from lifelines import KaplanMeierFitter
except ImportError:
    KaplanMeierFitter = None

app = Flask(__name__)

# ==============================
# DATABASE CONNECTION
# ==============================

def get_db():
    return sqlite3.connect("traffic_system.db")


# ==============================
# 1. GREEDY ALGORITHM
# ==============================

def optimize_cameras(intersections, camera_coverage):
    uncovered = set(intersections)
    selected = []

    while uncovered:
        best_cam = None
        max_cover = set()

        for cam, covers in camera_coverage.items():
            covered = uncovered.intersection(covers)

            if len(covered) > len(max_cover):
                best_cam = cam
                max_cover = covered

        if not best_cam:
            break

        selected.append(best_cam)
        uncovered -= max_cover

    return selected


# ==============================
# 2. LOGISTIC REGRESSION
# ==============================

def train_model():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT plate_number,
               COUNT(*) as total,
               SUM(CASE WHEN status='Paid' THEN 1 ELSE 0 END) as paid
        FROM ChallanHistory
        GROUP BY plate_number
    """)

    data = cursor.fetchall()
    conn.close()

    X, y = [], []

    for row in data:
        total = row[1]
        paid = row[2] if row[2] else 0

        X.append([total, paid])

        if paid >= total / 2:
            y.append(1)
        else:
            y.append(0)

    if not X:
        return None

    model = LogisticRegression()
    model.fit(X, y)
    return model


def predict_payment(plate):
    model = train_model()
    if model is None:
        return 0.5

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*),
               SUM(CASE WHEN status='Paid' THEN 1 ELSE 0 END)
        FROM ChallanHistory
        WHERE plate_number = ?
    """, (plate,))

    row = cursor.fetchone()
    conn.close()

    total = row[0]
    paid = row[1] if row[1] else 0

    if total == 0:
        return 0.5

    prob = model.predict_proba([[total, paid]])[0][1]
    return float(prob)


# ==============================
# 3. SURVIVAL ANALYSIS (SIMPLE)
# ==============================

def survival_analysis():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT fine_amount,
               CASE WHEN status='Paid' THEN 1 ELSE 0 END
        FROM ChallanHistory
    """)

    data = cursor.fetchall()
    conn.close()

    durations = []
    events = []

    for row in data:
        durations.append(row[0])  # using fine as dummy time
        events.append(row[1])

    if not durations or KaplanMeierFitter is None:
        return {}

    kmf = KaplanMeierFitter()
    kmf.fit(durations, event_observed=events)

    return kmf.survival_function_.to_dict()


# ==============================
# API ENDPOINTS (REQUIRED)
# ==============================

# 1. Camera Optimization API
@app.route('/api/optimize_cameras', methods=['POST'])
def camera_api():
    data = request.json

    intersections = data['intersections']
    coverage = data['camera_coverage']

    result = optimize_cameras(intersections, coverage)

    return jsonify({
        "optimal_cameras": result
    })


# 2. Payment Prediction API
@app.route('/api/predict_payment/<plate>', methods=['GET'])
def payment_api(plate):
    probability = predict_payment(plate)

    return jsonify({
        "plate": plate,
        "payment_probability": probability
    })


# ==============================
# RUN SERVER
# ==============================

if __name__ == "__main__":
    app.run(debug=True)
