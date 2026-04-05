# =====================================
# CAMERA PLACEMENT USING GREEDY METHOD
# =====================================

def greedy_camera_placement():
    print("\n📍 SMART CAMERA PLACEMENT SYSTEM\n")

    # Intersections (areas to cover)
    intersections = {1, 2, 3, 4, 5, 6, 7}

    # Camera positions and their coverage
    camera_options = {
        'A': {1, 2, 3},
        'B': {2, 3, 4, 5},
        'C': {4, 5, 6},
        'D': {6, 7}
    }

    uncovered = set(intersections)
    selected_cameras = []

    step = 1

    while uncovered:
        # Select camera covering max uncovered intersections
        best_camera = None
        max_cover = set()

        for cam, covers in camera_options.items():
            covered_now = covers & uncovered

            if len(covered_now) > len(max_cover):
                best_camera = cam
                max_cover = covered_now

        # Add selected camera
        selected_cameras.append(best_camera)

        print(f"Step {step}:")
        print(f"➡ Selected Camera: {best_camera}")
        print(f"✔ Covers: {sorted(max_cover)}")

        # Remove covered intersections
        uncovered -= camera_options[best_camera]

        print(f"❗ Remaining uncovered: {sorted(uncovered)}\n")

        step += 1

    # Final result
    print("====================================")
    print("✅ FINAL CAMERA SELECTION:", selected_cameras)
    print("====================================")


# =====================================
# RUN PROGRAM
# =====================================
if __name__ == "__main__":
    greedy_camera_placement()