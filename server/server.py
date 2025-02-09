from ultralytics import YOLO
import cv2
from flask_cors import CORS
from flask import jsonify
from flask_socketio import SocketIO, emit
import numpy as np
import sys
from flask import Flask, Response

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

def init_camera():
    try:
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            socketio.emit('camera_error', {'message': 'No camera found'})
            return None
        return cap
    except Exception as e:
        socketio.emit('camera_error', {'message': str(e)})
        return None

@socketio.on('connect')
def handle_connect():
    print('Client connected', file=sys.stderr)
    emit('status', {'message': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected', file=sys.stderr)

def process_frame(model, frame):
    try:
        # Run YOLO detection
        results = model(frame)
        
        # Get the plotted frame with detection boxes
        processed_frame = results[0].plot()
        
        # Ensure the frame is a valid numpy array with correct data type
        if not isinstance(processed_frame, np.ndarray):
            raise ValueError("Processed frame is not a numpy array")
            
        # Ensure the frame is in BGR format (OpenCV default)
        if len(processed_frame.shape) != 3 or processed_frame.shape[2] != 3:
            raise ValueError("Frame must be a 3-channel BGR image")
            
        # Ensure the data type is uint8
        if processed_frame.dtype != np.uint8:
            processed_frame = processed_frame.astype(np.uint8)
            
        return processed_frame
        
    except Exception as e:
        print(f"Error in process_frame: {str(e)}", file=sys.stderr)
        return None

def gen_frames():
    cap = None
    try:
        cap = init_camera()
        model = YOLO("yolov8n.pt")
        
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                print("Failed to capture frame", file=sys.stderr)
                break
                
            # Process frame with YOLO
            processed_frame = process_frame(model, frame)
            
            # Ensure we have a valid frame before encoding
            if processed_frame is not None:
                try:
                    # Verify frame format
                    if not isinstance(processed_frame, np.ndarray):
                        raise ValueError("Frame must be a numpy array")
                        
                    # Attempt to encode the frame
                    ret, buffer = cv2.imencode('.jpg', processed_frame)
                    if not ret:
                        raise RuntimeError("Failed to encode frame")
                        
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                           
                except Exception as e:
                    print(f"Frame encoding error: {str(e)}", file=sys.stderr)
                    continue
                    
    except Exception as e:
        print(f"Error in gen_frames: {str(e)}", file=sys.stderr)
        
    finally:
        if cap is not None:
            cap.release()

@app.route('/')
def index():
    return jsonify({"status": "running"})

@app.route('/video_feed')
def video_feed():
    return Response(
        gen_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame',
        headers={
            'Access-Control-Allow-Origin': '*',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
    )

@app.route('/api/environment-messages')
def environment_messages():
    return jsonify({
        "messages": [
            "Person detected in front",
            "Car approaching from left",
            "Door ahead",
            "Clear path forward"
        ]
    }), 200, {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)

