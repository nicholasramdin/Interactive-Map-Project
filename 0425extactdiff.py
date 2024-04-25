import cv2

def capture_frames():
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    frames = []
    print("Press 'space' to capture a frame, need two frames. Press 'q' to quit without completing.")

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        # Display the resulting frame
        cv2.imshow('Frame', frame)
        
        key = cv2.waitKey(1)
        if key == ord(' '):  # space bar to capture frames
            frames.append(frame)
            if len(frames) == 2:
                break
            print(f"Frame {len(frames)} captured, press 'space' again to capture another frame.")
        elif key == ord('q'):  # 'q' to quit the program
            print("Exiting program as requested.")
            break
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return frames

def process_and_save_frames(frames):
    if len(frames) < 2:
        print("Not enough frames captured to process.")
        return
    
    # Calculate the absolute difference between frames
    diff = cv2.absdiff(frames[0], frames[1])
    
    # Convert to grayscale
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    
    # Apply a threshold
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

    # Save the result
    cv2.imwrite('difference_image.png', thresh)
    print("Difference image saved as 'difference_image.png'.")

    # Optionally, show the result
    cv2.imshow('Difference Image', thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    frames = capture_frames()
    process_and_save_frames(frames)

if __name__ == "__main__":
    main()
