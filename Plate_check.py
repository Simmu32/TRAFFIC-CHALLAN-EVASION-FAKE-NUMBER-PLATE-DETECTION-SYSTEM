import numpy as np
from sklearn.cluster import KMeans
from scipy.stats import chi2_contingency

# hamming
def hamming_distance(s1,s2):
    if len(s1)!=len(s2):
        return float('inf')
    return sum(c1!=c2 for c1,c2 in zip(s1,s2))

# kmeans
def run_kmeans():
    data=np.array([
        [1,2],
        [2,1],
        [5,8],
        [6,9],
        [1,0],
        [9,11]
    ])

    kmeans=KMeans(n_clusters=2,random_state=0)
    kmeans.fit(data)

    print("Clusters:",kmeans.labels_)
    print("Centers:",kmeans.cluster_centers_)

# chi square
def run_chi_square():
    data=[
        [10,20],
        [20,20]
    ]

    chi,p,_,_=chi2_contingency(data)

    print("Chi value:",chi)
    print("p-value:",p)

    if p<0.05:
        print("Suspicious")
    else:
        print("Normal")

# hamming check
def run_hamming():
    p1=input("Enter plate 1: ")
    p2=input("Enter plate 2: ")

    dist=hamming_distance(p1,p2)

    print("Distance:",dist)

    if dist<=1:
        print("Very similar (Suspicious)")
    else:
        print("Not similar")

# ocr demo
def ocr_demo():
    img=input("Enter image name: ")
    print("Reading plate...")
    print("Detected: DL01AB1234")

# main
def main():
    while True:
        print("\n1. K-Means")
        print("2. Chi-Square")
        print("3. Hamming Distance")
        print("4. OCR Demo")
        print("5. Exit")

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
            break

        else:
            print("Invalid")

if __name__=="__main__":
    main()
