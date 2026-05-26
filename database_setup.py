import sqlite3
import os
from config import Config

def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Registered Vehicles
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS RegisteredVehicles (
            plate_number TEXT PRIMARY KEY,
            owner_name TEXT NOT NULL,
            owner_id TEXT NOT NULL,
            vehicle_type TEXT CHECK(vehicle_type IN ('2W', '4W', 'LCV', 'HCV')),
            registration_date TEXT NOT NULL
        )
    ''')
    
    # Challan History
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ChallanHistory (
            challan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate_number TEXT NOT NULL,
            violator_id TEXT NOT NULL,
            amount REAL NOT NULL,
            violation_type TEXT NOT NULL,
            date TEXT NOT NULL,
            paid_status INTEGER DEFAULT 0,
            payment_date TEXT,
            FOREIGN KEY (plate_number) REFERENCES RegisteredVehicles(plate_number)
        )
    ''')
    
    # Ownership Graph (transfers)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS OwnershipGraph (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id TEXT NOT NULL,
            plate_number TEXT NOT NULL,
            relationship TEXT NOT NULL,
            transfer_date TEXT NOT NULL
        )
    ''')
    
    # City Map
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CityMap (
            intersection_id TEXT PRIMARY KEY,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            intersection_name TEXT NOT NULL
        )
    ''')
    
    # Camera Locations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CameraLocations (
            camera_id TEXT PRIMARY KEY,
            intersection_id TEXT NOT NULL,
            coverage_radius REAL NOT NULL,
            installation_date TEXT NOT NULL,
            status TEXT CHECK(status IN ('active', 'inactive')),
            FOREIGN KEY (intersection_id) REFERENCES CityMap(intersection_id)
        )
    ''')
    
    # Indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_challan_plate ON ChallanHistory(plate_number)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_challan_violator ON ChallanHistory(violator_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_ownership_owner ON OwnershipGraph(owner_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_ownership_plate ON OwnershipGraph(plate_number)')
    
    conn.commit()
    conn.close()
    print("Database setup complete.")

if __name__ == '__main__':
    setup_database()