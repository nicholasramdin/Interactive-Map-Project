import cv2
import os

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

        # Compute the absolute difference between frames
        if prev_frame is not None:
            difference = cv2.absdiff(prev_frame, frame)

            # Apply thresholding to create a binary difference image
            _, binary_difference = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)

            # Save the binary difference as a separate image
            diff_save_path = os.path.join(diff_directory, f'difference_frame{frame_count}.jpg')
            cv2.imwrite(diff_save_path, binary_difference)
            print(f"Difference extracted and saved as {diff_save_path}")

        # Update the previous frame
        prev_frame = frame.copy()

    # Break the loop if 'q' key is pressed
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release the VideoCapture and close any open windows
cap.release()
cv2.destroyAllWindows()
