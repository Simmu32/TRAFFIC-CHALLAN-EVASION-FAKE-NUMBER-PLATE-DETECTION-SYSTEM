from database_setup import get_db_connection
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def load_city_map():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT intersection_id, latitude, longitude, intersection_name FROM CityMap")
    intersections = cursor.fetchall()
    conn.close()
    return [dict(row) for row in intersections]

def calculate_coverage(camera, intersections, radius_km):
    covered = []
    for inter in intersections:
        dist = haversine(camera['latitude'], camera['longitude'], inter['latitude'], inter['longitude'])
        if dist <= radius_km:
            covered.append(inter['intersection_id'])
    return set(covered)

def greedy_set_cover(camera_candidates, all_intersection_ids, coverage_func):
    uncovered = set(all_intersection_ids)
    selected = []
    while uncovered:
        best_cam = None
        best_cover = set()
        for cam in camera_candidates:
            cover = coverage_func(cam)
            new_covered = len(cover & uncovered)
            if new_covered > len(best_cover):
                best_cover = cover
                best_cam = cam
        if not best_cam:
            break
        selected.append(best_cam)
        uncovered -= best_cover
    return selected

def greedy_camera_optimization():
    intersections = load_city_map()
    all_ids = [i['intersection_id'] for i in intersections]
    
    # Assume potential cameras at every intersection
    candidates = []
    for inter in intersections:
        candidates.append({
            'camera_id': f"CAND_{inter['intersection_id']}",
            'latitude': inter['latitude'],
            'longitude': inter['longitude'],
            'radius': 0.5  # km coverage
        })
    
    def coverage_func(cam):
        return set([inter['intersection_id'] for inter in intersections if haversine(cam['latitude'], cam['longitude'], inter['latitude'], inter['longitude']) <= cam['radius']])
    
    selected = greedy_set_cover(candidates, set(all_ids), coverage_func)
    
    coverage_percentage = (len(set.union(*[coverage_func(c) for c in selected])) / len(all_ids)) * 100 if selected else 0
    
    return {
        'selected_cameras': selected,
        'coverage_percentage': coverage_percentage,
        'num_cameras': len(selected),
        'uncovered_intersections': list(set(all_ids) - set.union(*[coverage_func(c) for c in selected]))
    }

def cost_benefit_analysis():
    result = greedy_camera_optimization()
    # Assume cost per camera = 50000 INR
    cost = result['num_cameras'] * 50000
    benefit = result['coverage_percentage'] * 10000  # arbitrary
    return {
        'total_cost': cost,
        'estimated_benefit': benefit,
        'roi': benefit/cost if cost>0 else 0
    }

def export_visualization_data():
    result = greedy_camera_optimization()
    intersections = load_city_map()
    return {
        'intersections': intersections,
        'selected_cameras': result['selected_cameras'],
        'uncovered': result['uncovered_intersections']
    }