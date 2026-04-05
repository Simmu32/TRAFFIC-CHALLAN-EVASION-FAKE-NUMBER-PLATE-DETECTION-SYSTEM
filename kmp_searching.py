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
    database = [
        "DL01AB1234",
        "DL02CD5678",
        "UP03EF9012"
    ]

    if plate in database:
        return {"found": True, "message": "Plate found in database"}
    else:
        return {"found": False, "message": "Plate not found"}


