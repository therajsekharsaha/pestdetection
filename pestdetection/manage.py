from flask import Flask, render_template, request, jsonify, send_from_directory, Response
from werkzeug.utils import secure_filename
import os
import cv2
from ultralytics import YOLO

# Initialize Flask app
app = Flask(__name__)

# Set upload and output folders
UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size 16MB

# Allowed file extensions for image and video
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'webp'}

# Initialize YOLO model (update with your model path)
model = YOLO('best.pt')  # Replace with your actual model path

# Ensure upload/output folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Check if file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the file is in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    # If no file is selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the file based on its type (image or video)
        if filename.lower().endswith(('jpg', 'jpeg', 'png', 'bmp', 'tiff', 'webp')):
            output_file = process_image(file_path, filename)
        elif filename.lower().endswith(('mp4', 'avi', 'mov', 'mkv')):
            output_file = process_video(file_path, filename)
        
        # Return the output file name to display in the frontend
        return jsonify({'output_file': output_file, 'status': 'success'})

    return jsonify({'error': 'File type not allowed'}), 400

# Function to process an image
def process_image(file_path, filename):
    image = cv2.imread(file_path)
    if image is None:
        return None
    
    # Run YOLOv8 inference on the image
    results = model(image)

    # Annotate the image with YOLO's results
    annotated_image = results[0].plot()

    # Save the annotated image to the output folder
    output_filename = os.path.splitext(filename)[0] + '_result.jpg'
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
    cv2.imwrite(output_path, annotated_image)
    
    return output_filename

# Function to process a video
def process_video(file_path, filename):
    cap = cv2.VideoCapture(file_path)
    
    # Ensure output folder exists
    output_file = os.path.splitext(filename)[0] + '_result.mp4'
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_file)
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (1280, 720))

    while cap.isOpened():
        success, frame = cap.read()
        
        if success:
            # Run YOLOv8 inference on each frame
            results = model(frame)
            
            # Annotate the frame with YOLO's results
            annotated_frame = results[0].plot()

            # Write the annotated frame to the output video file
            out.write(annotated_frame)
        else:
            break

    cap.release()
    out.release()
    
    return output_file

# Route to serve video files
@app.route('/static/output/<filename>')
def serve_video(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

@app.route('/start_stream')
def start_stream():
    return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Function to generate video stream
def generate_video():
    # Open the webcam (you can replace this with a video file if needed)
    cap = cv2.VideoCapture(0)  # 0 is the default webcam device index
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        # Run YOLOv8 inference on the frame
        results = model(frame)
        
        # Annotate the frame with YOLO's results
        annotated_frame = results[0].plot()

        # Convert frame to JPEG
        ret, jpeg = cv2.imencode('.jpg', annotated_frame)
        
        if ret:
            # Yield the frame as a multipart response (MJPEG stream)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()

if __name__ == '__main__':
    app.run(debug=True)
