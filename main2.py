import cv2
import numpy as np

# Load the images
blank_wall = cv2.imread(r'C:\Users\nicho\OneDrive\Desktop\InteractiveMapProject\blank_wall.jpg')
wall_with_paper = cv2.imread(r'C:\Users\nicho\OneDrive\Desktop\InteractiveMapProject\wall_with_paper.jpg')

# Resize the images
resized_blank_wall = cv2.resize(blank_wall, (400, 300))
resized_wall_with_paper = cv2.resize(wall_with_paper, (400, 300))

# Convert the images to grayscale
gray_blank_wall = cv2.cvtColor(resized_blank_wall, cv2.COLOR_BGR2GRAY)
gray_wall_with_paper = cv2.cvtColor(resized_wall_with_paper, cv2.COLOR_BGR2GRAY)

# Compute the absolute difference between the two images
difference = cv2.absdiff(gray_blank_wall, gray_wall_with_paper)

# Apply thresholding to highlight the differences
_, thresholded_difference = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)

# Find contours in the thresholded difference image
contours, _ = cv2.findContours(thresholded_difference, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterate over contours and extract the regions with differences
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)

    # Extract the region of interest (ROI) from the wall with paper
    paper_roi = resized_wall_with_paper[y:y+h, x:x+w]

    # Save the extracted paper as a separate image
    cv2.imwrite(r'C:\Users\nicho\OneDrive\Desktop\InteractiveMapProject\extracted_paper.jpg', paper_roi)

# Display the images for visualization (optional)
cv2.imshow('Resized Blank Wall', resized_blank_wall)
cv2.imshow('Resized Wall with Paper', resized_wall_with_paper)
cv2.imshow('Difference Image', difference)
cv2.imshow('Extracted Paper', paper_roi)
cv2.waitKey(0)
cv2.destroyAllWindows()
