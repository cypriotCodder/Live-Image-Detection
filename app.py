import os
from flask import Flask, render_template, request, jsonify, send_from_directory, Response
from ultralytics import YOLO
from PIL import Image
import io
import base64
import numpy as np
import cv2

app = Flask(__name__)

# Load the ONNX model
model = YOLO("best.onnx")

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # Save the file temporarily
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Run inference
        results = model.predict(filepath)
        
        # Process results
        result = results[0]
        
        # Plot the results on the image
        # plot() returns a numpy array in BGR format
        im_array = result.plot()
        
        # Convert BGR to RGB
        im_rgb = cv2.cvtColor(im_array, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        im_pil = Image.fromarray(im_rgb)
        
        # Save to buffer
        buffered = io.BytesIO()
        im_pil.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Extract detections
        detections = []
        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = result.names[cls_id]
            detections.append({
                'label': label,
                'confidence': conf,
                'box': box.xyxy[0].tolist()
            })

        return jsonify({
            'image': f'data:image/jpeg;base64,{img_str}',
            'detections': detections
        })

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Run inference
            results = model.predict(frame, verbose=False)
            annotated_frame = results[0].plot()
            
            # Encode to JPEG
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
