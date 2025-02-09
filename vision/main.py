import cv2
import time
from ultralytics.utils.plotting import Annotator, colors
from .imports import *
from .scene import Scene

def main():
    cap = cv2.VideoCapture(0) # iphone 0 mac 1
    time.sleep(2)
    if not cap.isOpened():
        print("Error: Camera not accessible")
        return
 
    scene = Scene(memory_duration=5.0)
    frame_buffer, timestamp_buffer = [], []
    buffer_duration = 2.0   # Analyze frames from the last 2 seconds
    frame_skip = 3          # Process one in every 3 frames
    frame_count = 0
 
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1
            if frame_count % frame_skip != 0:
                continue
 
            current_time = time.time()
            frame_buffer.append(frame)
            timestamp_buffer.append(current_time)
 
            # Remove frames older than buffer_duration
            while timestamp_buffer and current_time - timestamp_buffer[0] > buffer_duration:
                frame_buffer.pop(0)
                timestamp_buffer.pop(0)
 
            if current_time - scene.last_seen >= buffer_duration:
                guidance = scene.process_frame_batch(frame_buffer, timestamp_buffer)
                print("[Scene]", guidance)
                scene.speak_guidance(guidance)
                scene.last_seen = current_time
                
                # Add annotation to the frame
                annotator = Annotator(frame, line_width=2)
                for obj in scene.tracked_objects.values():
                    # Convert normalized coordinates back to pixel coordinates
                    x = int(obj.position[0] * frame.shape[1])
                    y = int(obj.position[1] * frame.shape[0])
                    w = int(obj.size[0] * frame.shape[1])
                    h = int(obj.size[1] * frame.shape[0])
                    bbox = [x-w//2, y-h//2, x+w//2, y+h//2]  # Convert to xyxy format
                    
                    color = colors(obj.object_id, True)
                    annotator.box_label(
                        bbox,
                        f"{obj.class_name} {obj.object_id}",
                        color=color
                    )
                frame = annotator.result()
 
            cv2.imshow("Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
 
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()