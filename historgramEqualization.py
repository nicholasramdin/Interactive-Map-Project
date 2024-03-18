import cv2
import os

# Function to perform histogram equalization
def histogram_equalization(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized = cv2.equalizeHist(gray)
    return cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)

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

        # Convert the frame to grayscale and perform histogram equalization
        equalized_frame = histogram_equalization(frame)

        # Save the equalized frame
        equalized_save_path = os.path.join(save_directory, f'equalized_frame{frame_count}.jpg')
        cv2.imwrite(equalized_save_path, equalized_frame)
        print(f"Equalized frame saved as {equalized_save_path}")

    # Break the loop if 'q' key is pressed
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release the VideoCapture and close any open windows
cap.release()
cv2.destroyAllWindows()
