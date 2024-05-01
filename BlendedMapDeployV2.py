import cv2
import os

def capture_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    frames = []
    print("Press 'space' to capture a frame, need two frames. Press 'q' to quit without completing.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        cv2.imshow('Frame', frame)
        key = cv2.waitKey(1)
        if key == ord(' '):
            frames.append(frame)
            if len(frames) == 2:
                break
            print(f"Frame {len(frames)} captured, press 'space' again to capture another frame.")
        elif key == ord('q'):
            print("Exiting program as requested.")
            break

    cap.release()
    cv2.destroyAllWindows()
    return frames

def generate_unique_filename(path, filename, prefix):
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = f"{prefix}{counter:02}{extension}"
    while os.path.exists(os.path.join(path, new_filename)):
        counter += 1
        new_filename = f"{prefix}{counter:02}{extension}"
    return new_filename

def process_and_save_frames(frames, save_path):
    if len(frames) < 2:
        print("Not enough frames captured to process.")
        return

    diff = cv2.absdiff(frames[0], frames[1])
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    alpha_mask = thresh.copy()
    color_masked = cv2.bitwise_and(frames[1], frames[1], mask=alpha_mask)
    rgba = cv2.cvtColor(color_masked, cv2.COLOR_BGR2BGRA)
    rgba[:, :, 3] = alpha_mask  # Set alpha channel

    # Generate unique filenames for each type of image
    difference_image_filename = generate_unique_filename(save_path, 'difference_image.png', 'difference')
    alpha_mask_filename = generate_unique_filename(save_path, 'alpha_mask.png', 'layer')

    cv2.imwrite(os.path.join(save_path, difference_image_filename), color_masked)
    cv2.imwrite(os.path.join(save_path, alpha_mask_filename), rgba)
    print(f"Color difference image saved as '{difference_image_filename}'.")
    print(f"Color alpha mask saved as '{alpha_mask_filename}'.")

    cv2.imshow('Color Difference Image', color_masked)
    cv2.imshow('Color Alpha Mask', rgba)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    save_path = '/Users/chi/Desktop/BlendedMap'  # Update path as necessary
    frames = capture_frames()
    process_and_save_frames(frames, save_path)

if __name__ == "__main__":
    main()
