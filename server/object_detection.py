import cv2
import sys
import time
from dataclasses import dataclass
from typing import List, Tuple
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors

def init_camera():
    cap = cv2.VideoCapture(1)
    time.sleep(5)
    
    if not cap.isOpened():
        print("Error: Could not access camera")
        sys.exit(1)
        
    return cap

@dataclass
class DetectionContext:
    object_id: int
    class_name: str
    position: str
    confidence: float
    bbox: Tuple[int, int, int, int]

def process_frame(model, frame) -> List[DetectionContext]:
    results = model.track(frame, persist=True)
    context = []
    
    if results[0].boxes.id is not None:
        boxes = results[0].boxes
        for box, track_id, conf, cls in zip(
            boxes.xyxy,
            boxes.id,
            boxes.conf,
            boxes.cls
        ):
            x1, y1, x2, y2 = box.int().tolist()
            center_x = (x1 + x2) / 2
            position = "left" if center_x < 320 else "right" if center_x > 320 else "center"
            
            context.append(DetectionContext(
                object_id=int(track_id),
                class_name=results[0].names[int(cls)],
                position=position,
                confidence=float(conf),
                bbox=(x1, y1, x2, y2)
            ))
    
    return context

def main():
    cap = init_camera()
    model = YOLO("yolo11n-seg.pt")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Process frame and get context
            context = process_frame(model, frame)
            
            # Visualize results
            annotator = Annotator(frame, line_width=2)
            for obj in context:
                color = colors(obj.object_id, True)
                annotator.box_label(
                    obj.bbox, 
                    f"{obj.class_name} {obj.object_id}", 
                    color=color
                )
            
            # Display frame
            cv2.imshow("Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
            # Return context for LLM processing
            yield context
            
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    for context in main():
        print([f"{obj.class_name} {obj.object_id}: {obj.position}" for obj in context])