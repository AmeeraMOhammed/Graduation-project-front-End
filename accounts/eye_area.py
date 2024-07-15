import cv2
import mediapipe as mp
import numpy as np

def hex_to_bgr(hex_color):
    hex_color = hex_color.lstrip('#')
    h_len = len(hex_color)
    return tuple(int(hex_color[i:i + h_len // 3], 16) for i in range(0, h_len, h_len // 3))[::-1]

def calculate_and_draw_eye_areas(image_obj):
    # Initialize Mediapipe Face Mesh model
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.1, min_tracking_confidence=0.1)

    # Convert image object to NumPy array
    image_data = np.asarray(bytearray(image_obj.read()), dtype=np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    if image is None:
        print(f"Error: Unable to read the image ")
        return None, None, None

    # Resize the image to 300x300 pixels
    image = cv2.resize(image, (300, 300))

    image_with_areas = image.copy()  # Create a copy to draw on

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect facial landmarks using Face Mesh model
    results_mesh = face_mesh.process(image_rgb)

    if not results_mesh.multi_face_landmarks:
        # If no face is detected, return the original image
        return image, None, None

    for face_landmarks in results_mesh.multi_face_landmarks:
        # Specify the landmarks for the right eye (swapped)
        right_eye_landmarks = [133, 173, 157, 158, 159, 160, 161, 246, 33, 7, 163, 144, 145, 153, 154, 155]

        # Specify the landmarks for the left eye (swapped)
        left_eye_landmarks = [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382]

        # Extract landmark coordinates for the right and left eyes (swapped)
        right_eye_coords = [(int(face_landmarks.landmark[idx].x * image.shape[1]), int(face_landmarks.landmark[idx].y * image.shape[0])) for idx in right_eye_landmarks]
        left_eye_coords = [(int(face_landmarks.landmark[idx].x * image.shape[1]), int(face_landmarks.landmark[idx].y * image.shape[0])) for idx in left_eye_landmarks]

        # Connect the landmarks to form closed polygons for the right and left eyes (swapped)
        right_eye_polygon = np.array(right_eye_coords, np.int32)
        right_eye_polygon = right_eye_polygon.reshape((-1, 1, 2))

        left_eye_polygon = np.array(left_eye_coords, np.int32)
        left_eye_polygon = left_eye_polygon.reshape((-1, 1, 2))

        # Define the custom color
        line_color = hex_to_bgr('#173156')

        # Draw the connected landmarks for the right and left eyes on the image (swapped)
        cv2.polylines(image_with_areas, [right_eye_polygon], isClosed=True, color=line_color, thickness=2)
        cv2.polylines(image_with_areas, [left_eye_polygon], isClosed=True, color=line_color, thickness=2)

        # Display "LD" and "RD" text slightly shifted outwards and bolder (swapped)
        cv2.putText(image_with_areas, "RA", (right_eye_coords[0][0] - 20, right_eye_coords[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, line_color, 2)
        cv2.putText(image_with_areas, "LA", (left_eye_coords[0][0] + 5, left_eye_coords[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, line_color, 2)

        # Calculate the area between the connected landmarks for the right and left eyes (swapped)
        right_eye_area_pixels = cv2.contourArea(right_eye_polygon)
        left_eye_area_pixels = cv2.contourArea(left_eye_polygon)

        # Pixel-to-millimeter conversion factor (replace this with the actual factor)
        pixel_to_mm_conversion = 0.1  # Example: 1 pixel = 0.1 mm

        # Convert the areas to square millimeters
        right_eye_area_mm2 = right_eye_area_pixels * pixel_to_mm_conversion ** 2
        left_eye_area_mm2 = left_eye_area_pixels * pixel_to_mm_conversion ** 2
        
        # Calculate the absolute area difference between the two eyes
        abs_area_difference = abs(right_eye_area_mm2 - left_eye_area_mm2) 

        return image_with_areas, right_eye_area_mm2, left_eye_area_mm2, abs_area_difference

    return image, None, None, None