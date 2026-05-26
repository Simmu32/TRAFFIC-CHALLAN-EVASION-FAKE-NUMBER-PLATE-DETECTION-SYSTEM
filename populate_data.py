import sqlite3
import random
import datetime
from database_setup import get_db_connection

INDIAN_STATES = {
    'AP', 'AR', 'AS', 'BR', 'CG', 'DL', 'GA', 'GJ', 'HR', 'HP', 'JK', 'JH', 'KA', 'KL', 'MP', 'MH', 'MN', 'ML', 'MZ', 'NL', 'OD', 'PB', 'RJ', 'SK', 'TN', 'TS', 'TR', 'UK', 'UP', 'WB'
}
VEHICLE_TYPES = ['2W', '4W', 'LCV', 'HCV']
VIOLATION_TYPES = ['Speeding', 'Red Light Jump', 'Wrong Parking', 'No Helmet', 'No Seatbelt', 'Drunk Driving', 'Overloading']

def generate_plate():
    state = random.choice(list(INDIAN_STATES))
    district = f"{random.randint(1,99):02d}"
    series = random.choice(['A','B','C','D','E','F','G','H','J','K'])
    number = f"{random.randint(1,9999):04d}"
    return f"{state}{district}{series}{number}"

def populate_all():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Clear existing
    cursor.execute('DELETE FROM RegisteredVehicles')
    cursor.execute('DELETE FROM ChallanHistory')
    cursor.execute('DELETE FROM OwnershipGraph')
    cursor.execute('DELETE FROM CityMap')
    cursor.execute('DELETE FROM CameraLocations')
    
    # 1. Registered Vehicles (1000)
    vehicles = []
    owners = {}
    for _ in range(1000):
        plate = generate_plate()
        owner_id = f"OWN{random.randint(1000,9999)}"
        owners[plate] = owner_id
        vehicles.append((
            plate,
            f"Owner_{owner_id}",
            owner_id,
            random.choice(VEHICLE_TYPES),
            (datetime.datetime.now() - datetime.timedelta(days=random.randint(0,1000))).strftime('%Y-%m-%d')
        ))
    cursor.executemany('INSERT INTO RegisteredVehicles VALUES (?,?,?,?,?)', vehicles)
    
    # 2. Challan History (800)
    challans = []
    for i in range(800):
        plate = random.choice([v[0] for v in vehicles])
        challans.append((
            i+1,
            plate,
            owners[plate],
            round(random.uniform(200, 2000), 2),
            random.choice(VIOLATION_TYPES),
            (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
            random.choice([0,1]),
            None if random.random() > 0.7 else (datetime.datetime.now() - datetime.timedelta(days=random.randint(0,30))).strftime('%Y-%m-%d')
        ))
    cursor.executemany('INSERT INTO ChallanHistory (challan_id, plate_number, violator_id, amount, violation_type, date, paid_status, payment_date) VALUES (?,?,?,?,?,?,?,?)', challans)
    
    # 3. Ownership transfers (300)
    transfers = []
    for i in range(300):
        plate = random.choice([v[0] for v in vehicles])
        owner_id = owners[plate]
        new_owner = f"OWN{random.randint(1000,9999)}"
        transfers.append((
            i+1,
            owner_id,
            plate,
            'transfer',
            (datetime.datetime.now() - datetime.timedelta(days=random.randint(10, 500))).strftime('%Y-%m-%d')
        ))
    cursor.executemany('INSERT INTO OwnershipGraph (id, owner_id, plate_number, relationship, transfer_date) VALUES (?,?,?,?,?)', transfers)
    
    # 4. City Map (50 intersections)
    intersections = []
    for i in range(50):
        intersections.append((
            f"INT{i+1:03d}",
            round(12.935 + random.uniform(-0.2, 0.2), 6),
            round(77.617 + random.uniform(-0.2, 0.2), 6),
            f"Intersection_{i+1}"
        ))
    cursor.executemany('INSERT INTO CityMap VALUES (?,?,?,?)', intersections)
    
    # 5. Camera Locations (30 cameras)
    cameras = []
    for i in range(30):
        inter = random.choice(intersections)[0]
        cameras.append((
            f"CAM{i+1:03d}",
            inter,
            round(random.uniform(50, 200), 1),
            (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 500))).strftime('%Y-%m-%d'),
            random.choice(['active', 'active', 'active', 'inactive'])
        ))
    cursor.executemany('INSERT INTO CameraLocations VALUES (?,?,?,?,?)', cameras)
    
    conn.commit()
    conn.close()
    print("Populated 1000 vehicles, 800 challans, 300 transfers, 50 intersections, 30 cameras")

if __name__ == '__main__':
    populate_all()