import cv2

# Initialize VideoCapture with the camera index (usually 0 for default camera)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

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

    # Save the frame if 's' key is pressed
    key = cv2.waitKey(1)
    if key == ord('s'):
        cv2.imwrite('captured_frame.jpg', frame)
        print("Frame saved as captured_frame.jpg")

    # Break the loop if 'q' key is pressed
    elif key == ord('q'):
        break

# Release the VideoCapture and close any open windows
cap.release()
cv2.destroyAllWindows()
