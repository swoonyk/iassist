from .imports import *
from .scene import Scene

def main():
    cap = cv2.VideoCapture(1) #shium 0
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
 
            cv2.imshow("Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
 
    finally:
        # scene.speech.stop()
        cap.release()
        cv2.destroyAllWindows()
 
if __name__ == "__main__":
    main()