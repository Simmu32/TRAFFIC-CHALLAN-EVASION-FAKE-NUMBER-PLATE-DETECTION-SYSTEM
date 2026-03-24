import sqlite3

def create_database():
    # Connect to SQLite database (creates file if not exists)
    conn = sqlite3.connect("traffic_system.db")
    cursor = conn.cursor()

    print("Connected to database successfully!")

    # -------------------------------
    # 1. Registered Vehicles Table
    # -------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS RegisteredVehicles (
        plate_number TEXT PRIMARY KEY,
        owner_name TEXT NOT NULL,
        vehicle_type TEXT NOT NULL
    )
    """)

    # -------------------------------
    # 2. Challan History Table
    # -------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ChallanHistory (
        challan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate_number TEXT,
        fine_amount INTEGER,
        status TEXT CHECK(status IN ('Paid', 'Unpaid')),
        FOREIGN KEY (plate_number) REFERENCES RegisteredVehicles(plate_number)
    )
    """)

    # -------------------------------
    # 3. Ownership Graph Table
    # -------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS OwnershipGraph (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_name TEXT NOT NULL,
        plate_number TEXT NOT NULL,
        FOREIGN KEY (plate_number) REFERENCES RegisteredVehicles(plate_number)
    )
    """)

    print("All tables created successfully!")

    # Commit and close connection
    conn.commit()
    conn.close()
    print("Database setup completed!")

# Run the function
if __name__ == "__main__":
    create_database()