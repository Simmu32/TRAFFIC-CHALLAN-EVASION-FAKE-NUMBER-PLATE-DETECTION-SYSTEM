import sqlite3

def insert_data():
    conn = sqlite3.connect("traffic_system.db")
    cursor = conn.cursor()

    print("Inserting dummy data...")

    # -------------------------------
    # 1. Registered Vehicles
    # -------------------------------
    vehicles = [
        ("DL01AB1234", "Ramesh Kumar", "Car"),
        ("DL02CD5678", "Suresh Sharma", "Bike"),
        ("HR26EF9012", "Amit Singh", "Car"),
        ("UK07GH3456", "Priya Verma", "Scooty"),
        ("DL03IJ7890", "Ramesh Kumar", "Car"),
        ("DL04KL1111", "Ramesh Kumar", "Car"),   # suspicious (many vehicles)
        ("HR26MN2222", "Amit Singh", "Bike"),
        ("DL05OP3333", "Neha Gupta", "Car")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO RegisteredVehicles 
        (plate_number, owner_name, vehicle_type)
        VALUES (?, ?, ?)
    """, vehicles)

    # -------------------------------
    # 2. Challan History
    # -------------------------------
    challans = [
        ("DL01AB1234", 1000, "Paid"),
        ("DL02CD5678", 500, "Unpaid"),
        ("HR26EF9012", 1500, "Unpaid"),
        ("DL03IJ7890", 2000, "Paid"),
        ("DL04KL1111", 2500, "Unpaid"),
        ("HR26MN2222", 700, "Unpaid"),
        ("DL05OP3333", 1200, "Paid")
    ]

    cursor.executemany("""
        INSERT INTO ChallanHistory (plate_number, fine_amount, status)
        VALUES (?, ?, ?)
    """, challans)

    # -------------------------------
    # 3. Ownership Graph
    # -------------------------------
    ownership = [
        ("Ramesh Kumar", "DL01AB1234"),
        ("Ramesh Kumar", "DL03IJ7890"),
        ("Ramesh Kumar", "DL04KL1111"),  # suspicious cluster

        ("Suresh Sharma", "DL02CD5678"),

        ("Amit Singh", "HR26EF9012"),
        ("Amit Singh", "HR26MN2222"),

        ("Priya Verma", "UK07GH3456"),

        ("Neha Gupta", "DL05OP3333")
    ]

    cursor.executemany("""
        INSERT INTO OwnershipGraph (person_name, plate_number)
        VALUES (?, ?)
    """, ownership)

    print("Dummy data inserted successfully!")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_data()