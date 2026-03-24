import sqlite3
import numpy as np
from sklearn.cluster import KMeans
from scipy.stats import chi2_contingency

from kmp_searching import search_plate_in_db
from ownership_graph import check_suspicious
from pattern_matching import is_valid_plate

# hamming
def hamming_distance(s1,s2):
    if len(s1)!=len(s2):
        return float('inf')
    return sum(c1!=c2 for c1,c2 in zip(s1,s2))


# K-Means
def run_kmeans():
    conn=sqlite3.connect("traffic_system.db")
    cursor=conn.cursor()

    cursor.execute("SELECT fine_amount FROM ChallanHistory")
    data=cursor.fetchall()
    conn.close()

    if len(data)==0:
        print("No data")
        return

    arr=np.array(data)

    kmeans=KMeans(n_clusters=2,random_state=0)
    kmeans.fit(arr)

    print("Clusters:",kmeans.labels_)
    print("Centers:",kmeans.cluster_centers_)


# Chi-Square
def run_chi_square():
    conn=sqlite3.connect("traffic_system.db")
    cursor=conn.cursor()

    cursor.execute("SELECT status, COUNT(*) FROM ChallanHistory GROUP BY status")
    data=cursor.fetchall()
    conn.close()

    paid=0
    unpaid=0

    for s,c in data:
        if s=="Paid":
            paid=c
        else:
            unpaid=c

    table=[[paid,unpaid],[paid,unpaid]]

    chi,p,_,_=chi2_contingency(table)

    print("Chi:",chi)
    print("p:",p)

    if p<0.05:
        print("Suspicious")
    else:
        print("Normal")


# Hamming + KMP
def run_hamming():
    inp=input("Enter plate: ")

    if not is_valid_plate(inp):
        print("Invalid format")
        return

    result=search_plate_in_db(inp)

    if result["found"]:
        print("Exact match:",result["plate"])
        print("Owner:",result["owner"])
    else:
        print("Checking similarity...")

        conn=sqlite3.connect("traffic_system.db")
        cursor=conn.cursor()
        cursor.execute("SELECT plate_number FROM RegisteredVehicles")
        plates=cursor.fetchall()
        conn.close()

        for (db_plate,) in plates:
            dist=hamming_distance(inp,db_plate)
            if dist<=1:
                print("Similar to:",db_plate,"| Diff:",dist)


# OCR + integration
def ocr_demo():
    print("Reading image...")
    detected="DL01AB1234"
    print("Detected:",detected)

    if not is_valid_plate(detected):
        print("Invalid format")
        return

    result=search_plate_in_db(detected)

    if result["found"]:
        print("Owner:",result["owner"])
    else:
        print("Plate not found")


# BFS check
def run_bfs():
    name=input("Enter person name: ")
    result=check_suspicious(name)

    print("People:",result["connected_people"])
    print("Vehicles:",result["connected_vehicles"])

    if result["suspicious"]:
        print("Suspicious")
    else:
        print("Normal")


# main
def main():
    while True:
        print("\n1. K-Means")
        print("2. Chi-Square")
        print("3. Hamming + Search")
        print("4. OCR Check")
        print("5. BFS Suspicious")
        print("6. Exit")

        ch=input("Enter choice: ")

        if ch=="1":
            run_kmeans()

        elif ch=="2":
            run_chi_square()

        elif ch=="3":
            run_hamming()

        elif ch=="4":
            ocr_demo()

        elif ch=="5":
            run_bfs()

        elif ch=="6":
            break

        else:
            print("Invalid")

if __name__=="__main__":
    main()
