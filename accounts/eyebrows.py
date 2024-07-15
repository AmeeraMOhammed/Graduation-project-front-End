import cv2
import mediapipe as mp
import numpy as np
def hex_to_bgr(hex_color):
    hex_color = hex_color.lstrip('#')
    h_len = len(hex_color)
    return tuple(int(hex_color[i:i + h_len // 3], 16) for i in range(0, h_len, h_len // 3))[::-1]

def calculate_distances(image_obj):
    # Initialize Mediapipe Face Detection and Face Mesh models
    mp_face_detection = mp.solutions.face_detection
    mp_face_mesh = mp.solutions.face_mesh

    face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.1)
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.1, min_tracking_confidence=0.1)

    # Convert image object to NumPy array
    image_data = np.asarray(bytearray(image_obj.read()), dtype=np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"The image could not be loaded. Please check the file path and ensure it's a valid image.")
    
    # Resize the image to 300x300 pixels
    image = cv2.resize(image, (300, 300))
    
    # If image is loaded and resized successfully, continue with processing
    image_with_distances = image.copy()  # Create a copy to draw on
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect face using Face Detection model
    results_detection = face_detection.process(image_rgb)
    if not results_detection.detections:
        # If no face is detected, return the original image
        return image, None, None

    for detection in results_detection.detections:
        bboxC = detection.location_data.relative_bounding_box
        ih, iw, _ = image.shape
        x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

        # Crop face to a standard size
        face_cropped = image[y:y+h, x:x+w]

        # Detect facial landmarks using Face Mesh model
        results_mesh = face_mesh.process(cv2.cvtColor(face_cropped, cv2.COLOR_BGR2RGB))
        if results_mesh.multi_face_landmarks:
            face_landmarks = results_mesh.multi_face_landmarks[0]

            # Extract coordinates of relevant landmarks
            nose_tip = (int(face_landmarks.landmark[4].x * w) + x, int(face_landmarks.landmark[4].y * h) + y)
            eyebrow_peak_right = (int(face_landmarks.landmark[53].x * w) + x, int(face_landmarks.landmark[53].y * h) + y)
            eyebrow_peak_left = (int(face_landmarks.landmark[283].x * w) + x, int(face_landmarks.landmark[283].y * h) + y)

            # Calculate distances in pixels
            distance_right_pixels = ((eyebrow_peak_right[0] - nose_tip[0])**2 + (eyebrow_peak_right[1] - nose_tip[1])**2)**0.5
            distance_left_pixels = ((eyebrow_peak_left[0] - nose_tip[0])**2 + (eyebrow_peak_left[1] - nose_tip[1])**2)**0.5

            # Convert distances to centimeters or millimeters based on average face width
            average_face_width_mm = 145  # Set your average face width in mm
            pixel_to_mm_conversion = average_face_width_mm / w
            distance_right_mm = distance_right_pixels * pixel_to_mm_conversion
            distance_left_mm = distance_left_pixels * pixel_to_mm_conversion

            # Define the custom color
            line_color = hex_to_bgr('#173156')  # Convert hex color to BGR
            
            # Draw lines and display "LD" and "RD" on the original image
            cv2.line(image_with_distances, nose_tip, eyebrow_peak_right, line_color, 2, cv2.LINE_AA)
            cv2.line(image_with_distances, nose_tip, eyebrow_peak_left, line_color, 2, cv2.LINE_AA)
            cv2.putText(image_with_distances, "RD", (nose_tip[0] - 45, nose_tip[1] +2), cv2.FONT_HERSHEY_SIMPLEX, 0.7, line_color, 2)
            cv2.putText(image_with_distances, "LD", (nose_tip[0] + 15, nose_tip[1] +2), cv2.FONT_HERSHEY_SIMPLEX, 0.7, line_color, 2)
            
            # Calculate the absolute difference between the two distances
            abs_difference = abs(distance_right_mm - distance_left_mm) 


        return image_with_distances, distance_right_mm, distance_left_mm, abs_difference

    # If no facial landmarks are detected, return the original image
    return image, None, None, None

