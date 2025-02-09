from .imports import *
from .scene import Scene
from .priority_list import NavigationQueue

def main():
    frame_size = (640, 480)  # Smaller frame size for faster processing
    fps_target = 30
    frame_interval = 1.0 / fps_target

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not accessible")
        return

    # Fast tracking settings
    tracking_buffer_size = 5  # Keep last 5 frames for movement
    tracking_frame_skip = 1   # Process every frame for movement

    # Slow analysis settings
    analysis_buffer_size = 50  # Larger buffer for scene analysis
    analysis_frame_skip = 3  # Process every __ th frame for analysis
    analysis_interval = 2.0    # Summarize scene every __ seconds

    scene = Scene()
    
    # Separate buffers for tracking and analysis
    tracking_buffer = deque(maxlen=tracking_buffer_size)
    analysis_buffer = deque(maxlen=analysis_buffer_size)
    
    frame_count = 0
    last_analysis = time.time()

    try:
        last_frame_time = time.time()
        while True:
            # Frame rate control
            current_time = time.time()
            if current_time - last_frame_time < frame_interval:
                continue

            ret, frame = cap.read()
            if not ret:
                break
            
            # Resize frame for faster processing
            frame = cv2.resize(frame, frame_size)

            frame_count += 1


            # Fast tracking loop
            if frame_count % tracking_frame_skip == 0:
                tracking_buffer.append((frame, current_time))
                movement = scene.process_movement(tracking_buffer)
                if movement:  # Only print if significant movement detected
                    # print("[Movement]", movement)
                    pass


            # Slower analysis loop
            if frame_count % analysis_frame_skip == 0:
                analysis_buffer.append((frame, current_time))

            # Periodic scene analysis
            if current_time - last_analysis >= analysis_interval:
                if len(analysis_buffer) > 0:
                    summary = scene.llm_summarize(analysis_buffer)
                    print("[Scene]", summary)
                    response, tag = summary
                    priority_queue_item = scene._format_for_priority_queue(response, tag) # TURNED TO JSON
                    nav_queue = NavigationQueue()
                    nav_queue.add_json_item(priority_queue_item)
                    last_analysis = current_time
                    analysis_buffer.clear()
            
            if frame_count % analysis_frame_skip == 0:
                analysis_buffer.append((frame, current_time))

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