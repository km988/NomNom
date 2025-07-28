import cv2

# Load the predefined dictionary
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

# Generate and save three different markers
for marker_id in [1, 2, 3]:
    marker_img = cv2.aruco.drawMarker(aruco_dict, marker_id, 200)  # 200x200 pixels
    filename = f"aruco_marker_{marker_id}.png"
    cv2.imwrite(filename, marker_img)
    print(f"Saved {filename}")
