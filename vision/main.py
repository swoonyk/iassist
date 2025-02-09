from .imports import *
from .scene import Scene

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not accessible")
        return

    # Fast tracking settings
    tracking_buffer_size = 5  # Keep last 5 frames for movement
    tracking_frame_skip = 1   # Process every frame for movement

    # Slow analysis settings
    analysis_buffer_size = 30  # Larger buffer for scene analysis
    analysis_frame_skip = 5   # Process every __ th frame for analysis
    analysis_interval = 2.0    # Summarize scene every 2 seconds

    scene = Scene()
    
    # Separate buffers for tracking and analysis
    tracking_buffer = deque(maxlen=tracking_buffer_size)
    analysis_buffer = deque(maxlen=analysis_buffer_size)
    
    frame_count = 0
    last_analysis = time.time()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            current_time = time.time()

            # Fast tracking loop
            if frame_count % tracking_frame_skip == 0:
                tracking_buffer.append((frame, current_time))
                movement = scene.process_movement(tracking_buffer)
                if movement:  # Only print if significant movement detected
                    print("[Movement]", movement)

            # Slower analysis loop
            if frame_count % analysis_frame_skip == 0:
                analysis_buffer.append((frame, current_time))

            # Periodic scene analysis
            if current_time - last_analysis >= analysis_interval:
                summary = scene.summarize_scene(analysis_buffer)
                print("[Scene]", summary)
                last_analysis = current_time

            # Display frame with annotations
            annotated_frame = scene.annotate_frame(frame)
            cv2.imshow("Camera", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()