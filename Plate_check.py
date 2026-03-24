from itertools import combinations

#person 4 module...

# Hamming distance
def hamming_distance(s1,s2):
    if len(s1)!=len(s2):
        return float('inf')
    return sum(c1!=c2 for c1,c2 in zip(s1,s2))

# Single plate check
def check_single_plate(input_plate,database,threshold=1):
    print("\nChecking plate:",input_plate)

    for db_plate in database:
        dist=hamming_distance(input_plate,db_plate)
        if dist<=threshold:
            print("Suspicious! Similar to:",db_plate)
            print("Difference:",dist)
            return

    print("No similar plate found (may be fake or new)")

# Bulk check
def find_suspicious_plates(plates,threshold=1):
    print("\nChecking suspicious plates in dataset...")

    found=False
    for p1,p2 in combinations(plates,2):
        dist=hamming_distance(p1,p2)
        if dist<=threshold:
            print("Suspicious pair:",p1,"and",p2,"| Difference:",dist)
            found=True

    if not found:
        print("No suspicious pairs found")

# Main menu
def main():
    database=[
        "DL01AB1234",
        "DL02CD5678",
        "UP03EF9012"
    ]

    while True:
        print("\n==== MENU ====")
        print("1. Check Single Plate")
        print("2. Check Multiple Plates")
        print("3. Exit")

        choice=input("Enter choice: ")

        if choice=="1":
            plate=input("Enter number plate: ")
            check_single_plate(plate,database)

        elif choice=="2":
            plates=[]
            n=int(input("Enter number of plates: "))
            for i in range(n):
                p=input("Enter plate: ")
                plates.append(p)

            find_suspicious_plates(plates)

        elif choice=="3":
            print("Exiting...")
            break

        else:
            print("Invalid choice")

if __name__=="__main__":
    main()
