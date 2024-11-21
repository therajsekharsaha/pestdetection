#!/usr/bin/env python3

import cv2
from ultralytics import YOLO
import os
import tkinter as tk
from tkinter import filedialog

# Load the YOLOv8 model (update the path to your model file)
model = YOLO('/home/rajsekhar/Desktop/project/best.pt')  # Replace with your actual model path

# Initialize tkinter for the file dialog
root = tk.Tk()
root.withdraw()  # Hide the root window

# Ask the user to select a video file using the file dialog
video_path = filedialog.askopenfilename(title="Select a Video File", filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*")))

# Destroy the tkinter root window after the dialog to prevent it from staying in the background
root.destroy()

# Check if the user selected a file
if not video_path:
    print("No video file selected. Exiting...")
    exit()

# Open the video file
cap = cv2.VideoCapture(video_path)

# Ensure the output directory exists
output_dir = "/home/rajsekhar/Desktop/project/"  # Replace with your desired output directory
os.makedirs(output_dir, exist_ok=True)

# Open the video writer for the output file (using Linux-style paths)
out = cv2.VideoWriter(os.path.join(output_dir, 'result.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (1280, 720))

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Write the annotated frame to the output video file
        out.write(annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
out.release()
cv2.destroyAllWindows()

