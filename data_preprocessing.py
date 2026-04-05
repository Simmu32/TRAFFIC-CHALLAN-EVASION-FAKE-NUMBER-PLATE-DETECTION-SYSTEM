import sqlite3

def load_data():
    conn = sqlite3.connect("traffic_system.db")
    cursor = conn.cursor()

    # Fetch challan data
    cursor.execute("SELECT plate_number, fine_amount, paid_status FROM ChallanHistory")
    data = cursor.fetchall()

    conn.close()

    return data


def preprocess_data():
    data = load_data()

    X = []  # features
    y = []  # labels

    for row in data:
        plate, fine, paid = row

        # Feature: fine amount
        X.append([fine])

        # Label: paid or not
        if paid == "Paid":
            y.append(1)
        else:
            y.append(0)

    return X, y


# Test
if __name__ == "__main__":
    X, y = preprocess_data()
    print("Features:", X)
    print("Labels:", y)