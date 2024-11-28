# Plant Pest Detection Using YOLOv8 Nano 🦟

> **Note**  
> This is the second iteration of the model.

## Installation 🔧

To set up and run the model, follow these steps:

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/pest-detection.git
   cd pest-detection
   pip install -r requirements.txt
   python manage.py

## Overview
This model was developed as part of our thesis project, **"GroPro: Grow and Protect"**, focused on detecting and mitigating plant pests in urban gardens using both object and audio detection technologies. It enables real-time pest detection in images, videos, and other media formats.

## Model Architecture 🤖
The model uses the **YOLOv8 Nano** architecture, a compact and efficient variant of the YOLOv8 object detection model, optimized for edge devices like the Raspberry Pi 4. The model was trained on a custom dataset of plant pest images, collected via web scraping from various online sources. YOLOv8 Nano is designed for real-time, low-power pest detection in urban gardens.

## Performance Metrics ⚙️
The model's performance was evaluated based on **mean Average Precision (mAP)** across various Intersection over Union (IoU) thresholds, ranging from 0.5 to 0.95 (with a step size of 0.05). The overall mAP achieved was **0.195** on the validation set. Here's a breakdown of mAP for each pest class:

- **Aphid**: 0.0899
- **Fruit Fly**: 0.292
- **Scale Insect**: 0.202

### Speed:
- **Preprocessing**: 0.3 ms per image
- **Inference**: 33.7 ms per image
- **Postprocessing**: 4.3 ms per image

While the model shows promising results, there is still room for improvement, especially in detecting **aphids**, which currently have lower accuracy.

## Demo 🦟
Below is a demonstration of the model’s performance on a test video. The model successfully detects and labels various plant pests in real-time:

![Pest Detection Demo](https://github.com/spoodzxs2345/pest-detection/assets/104749581/a4ea3f94-d186-4fdf-ab59-fa6f2180c6b3)
