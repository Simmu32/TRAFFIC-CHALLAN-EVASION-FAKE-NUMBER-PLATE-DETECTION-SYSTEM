# ===============================
# CAMERA PLACEMENT 
# ===============================

def greedy_camera_placement():
    # Intersections (to be covered)
    intersections = {1, 2, 3, 4, 5, 6, 7}
    # Camera locations and what they cover
    camera_options = {
        'A': {1, 2, 3},
        'B': {2, 3, 4, 5},
        'C': {4, 5, 6},
        'D': {6, 7}
    }

    uncovered = set(intersections)
    selected_cameras = []
    print("\nStep-by-step selection:\n")

    while uncovered:
        best_cam = max(camera_options, key=lambda cam: len(camera_options[cam] & uncovered))
        selected_cameras.append(best_cam)
        covered_now = camera_options[best_cam] & uncovered
        uncovered -= camera_options[best_cam]
        print(f"Selected Camera: {best_cam}")
        print(f"Covers: {covered_now}")
        print(f"Remaining uncovered: {uncovered}\n")

    print("✅ Final Selected Cameras:", selected_cameras)


# RUN
if __name__ == "__main__":
    greedy_camera_placement()
