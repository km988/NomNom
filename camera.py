import cv2
import numpy as np

# Initialize the ARUCO dictionary and parameters
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()

# Predefine the marker IDs and their associated actions
marker_actions = {
    0: "Home Base",    
    1: "Chips",       
    2: "Popcorn",      
}

# Function to handle actions based on detected AR tag IDs
def handle_detected_marker(marker_id):
    if marker_id in marker_actions:
        print(f"Detected Marker ID {marker_id}: Action - {marker_actions[marker_id]}")
    else:
        print(f"Unknown marker ID: {marker_id}")

# Ask the user for the marker ID they want to search for
target_marker_id = int(input("Enter the marker ID you want to detect (e.g., 0, 1, 2): "))

# Start video capture (webcam)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detect markers in the 
    s, rejectedImgPoints = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

    if len(corners) > 0:
        # Draw the detected markers on the frame
        frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # Check if the target marker ID is detected
        for i in range(len(ids)):
            marker_id = ids[i][0]  # Get the ID of the marker
            if marker_id == target_marker_id:
                handle_detected_marker(marker_id)

    # Display the frame
    cv2.imshow("AR Tag Detection", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()
