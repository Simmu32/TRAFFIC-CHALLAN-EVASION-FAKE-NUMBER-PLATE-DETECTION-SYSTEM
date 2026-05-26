from database_setup import get_db_connection

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
                length = lps[length-1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    if not pattern:
        return []
    lps = compute_lps(pattern)
    res = []
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            res.append(i - j)
            j = lps[j-1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    return res

def search_plate_in_database(partial_plate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT plate_number FROM RegisteredVehicles")
    all_plates = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    matches = []
    for plate in all_plates:
        if kmp_search(plate.upper(), partial_plate.upper()):
            matches.append(plate)
    return matches

def batch_search(partial_plates):
    return {pp: search_plate_in_database(pp) for pp in partial_plates}

def benchmark_performance(partial_plate, iterations=100):
    import time
    start = time.time()
    for _ in range(iterations):
        search_plate_in_database(partial_plate)
    elapsed = time.time() - start
    return {"iterations": iterations, "total_sec": elapsed, "avg_sec": elapsed/iterations}