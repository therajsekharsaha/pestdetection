#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog
from ultralytics import YOLO
import cv2

def select_file_and_run_yolo():
    # Open file dialog to select image file
    file_path = filedialog.askopenfilename(
        title="Select an Image File",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp")]
    )
    
    if not file_path:
        print("No file selected!")
        return

    # Load the YOLOv8 model (update the path to your model file)
    model = YOLO('/home/rajsekhar/Desktop/project/best.pt')  # Replace with your actual model path
    
    # Load the selected image
    image = cv2.imread(file_path)
    if image is None:
        print("Error loading image!")
        return

    # Detect objects in the image
    results = model(image)

    # Process and display results
    for r in results:
        im_array = r.plot()
        
        # Show the image with annotations
        cv2.imshow('Image with Annotations', im_array)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Save the result image (update path for saving result)
        save_path = file_path.rsplit('.', 1)[0] + "_result.jpg"
        cv2.imwrite(save_path, im_array)
        print(f"Result saved to: {save_path}")

if __name__ == "__main__":
    # Create a simple GUI for file selection
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    select_file_and_run_yolo()
