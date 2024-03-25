import cv2
import os
import numpy as np  # Import NumPy library

# Function to perform histogram equalization on each channel
def histogram_equalization_channels(image):
    # Split the image into its RGB channels
    b, g, r = cv2.split(image)

    # Perform histogram equalization on each channel separately
    b_eq = cv2.equalizeHist(b)
    g_eq = cv2.equalizeHist(g)
    r_eq = cv2.equalizeHist(r)

    # Merge the equalized channels back into an image
    equalized_image = cv2.merge((b_eq, g_eq, r_eq))

    return equalized_image

# Function to identify the boundary of the difference areas and create an alpha map
def create_alpha_map(image1, image2):
    # Compute the absolute difference between the two images
    difference = cv2.absdiff(image1, image2)

    # Convert the difference image to grayscale
    gray_difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to create a binary image
    _, binary_difference = cv2.threshold(gray_difference, 30, 255, cv2.THRESH_BINARY)

    # Find contours in the binary difference image
    contours, _ = cv2.findContours(binary_difference, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create an empty mask
    alpha_map = np.zeros_like(gray_difference)

    # Draw contours on the mask to create the alpha map
    cv2.drawContours(alpha_map, contours, -1, (255), thickness=cv2.FILLED)

    return alpha_map

# Initialize VideoCapture with the camera index (usually 0 for default camera)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Create a directory to save captured frames and differences
save_directory = 'captured_frames'
os.makedirs(save_directory, exist_ok=True)
diff_directory = 'differences'
os.makedirs(diff_directory, exist_ok=True)

# Set the interval (in seconds) between captures
interval_seconds = 10

# Initialize frame counter
frame_count = 0

# Initialize previous frame
prev_frame = None

# Continuously grab frames from the camera
while True:
    # Capture a frame
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    # Display the frame
    cv2.imshow('Camera Feed', frame)

    # Save the frame if the interval has passed
    frame_count += 1
    if frame_count % int(cap.get(cv2.CAP_PROP_FPS) * interval_seconds) == 0:
        save_path = os.path.join(save_directory, f'captured_frame{frame_count}.jpg')
        cv2.imwrite(save_path, frame)
        print(f"Frame {frame_count} saved as {save_path}")

        # Perform histogram equalization on each channel separately
        equalized_frame = histogram_equalization_channels(frame)

        # Save the equalized frame
        equalized_save_path = os.path.join(save_directory, f'equalized_frame{frame_count}.jpg')
        cv2.imwrite(equalized_save_path, equalized_frame)
        print(f"Equalized frame saved as {equalized_save_path}")

        # Create alpha map between current frame and previous frame
        if prev_frame is not None:
            alpha_map = create_alpha_map(prev_frame, equalized_frame)
            alpha_map_path = os.path.join(diff_directory, f'alpha_map{frame_count}.jpg')
            cv2.imwrite(alpha_map_path, alpha_map)
            print(f"Alpha map saved as {alpha_map_path}")

        # Update previous frame
        prev_frame = equalized_frame.copy()

    # Break the loop if 'q' key is pressed
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release the VideoCapture and close any open windows
cap.release()
cv2.destroyAllWindows()
