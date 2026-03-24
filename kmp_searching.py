import sqlite3

# -------------------------------
# Step 1: Build LPS Array
# -------------------------------
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


# -------------------------------
# Step 2: KMP Search
# -------------------------------
def kmp_search(text, pattern):
    lps = compute_lps(pattern)
    i = 0  # index for text
    j = 0  # index for pattern

    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == len(pattern):
            return True  # Match found

        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return False


# -------------------------------
# Step 3: Search Plate in Database
# -------------------------------
def search_plate_in_db(plate):
    conn = sqlite3.connect("traffic_system.db")
    cursor = conn.cursor()

    cursor.execute("SELECT plate_number, owner_name FROM RegisteredVehicles")
    rows = cursor.fetchall()

    for db_plate, owner in rows:
        if kmp_search(db_plate, plate):
            conn.close()
            return {
                "found": True,
                "plate": db_plate,
                "owner": owner
            }

    conn.close()
    return {
        "found": False,
        "message": "Plate not found (possibly fake)"
    }


# -------------------------------
# Test
# -------------------------------
if __name__ == "__main__":
    test_plate = "DL01AB1234"
    result = search_plate_in_db(test_plate)
    print(result)