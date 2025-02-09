from .imports import *
from .detected_obj import DetectedObject
    
class Scene:
    def __init__(self):
        load_dotenv()
        self.model = YOLO("yolov8n.pt")
        self.tracked_objects = {}
        self.llm = ollama.Client()
        self.memory_buffer = deque(maxlen=5)
        self.last_seen = time.time()

        if not os.getenv("GROQ_API_KEY"):
            raise ValueError("GROQ_API_KEY not found in environment variables")

    def _format_memory(self) -> str:
        """Format memory buffer into context"""
        if not self.memory_buffer:
            return "No previous context."
        
        timestamps = []
        summaries = []
        for timestamp, summary in self.memory_buffer:
            time_ago = round(time.time() - timestamp, 1)
            timestamps.append(f"{time_ago}s ago")
            summaries.append(summary)
            
        return "\n".join([
            f"[{t}]: {s}" for t, s in zip(timestamps, summaries)
        ])
    
    def _get_position(self, x: float, y: float) -> str:
        """Convert coordinates to position description"""
        horizontal = "center"
        if x < 213:  # Left third
            horizontal = "left"
        elif x > 426:  # Right third
            horizontal = "right"
        return horizontal

    def _get_movement_direction(self, dx: float, dy: float) -> str:
        """Convert position changes to movement direction"""
        if abs(dx) > abs(dy):
            return "right" if dx > 150 else "left"
        else:
            return "down" if dy > 150 else "up"

    def _detect_objects(self, frames: List[np.ndarray], timestamps: List[float]) -> List[DetectedObject]:
        detections = []
        for frame, timestamp in zip(frames, timestamps):
            results = self.model.track(frame, persist=True)[0]
            
            if not hasattr(results.boxes, "id") or results.boxes.id is None:
                continue
                
            boxes = results.boxes
            for box, track_id, conf, cls in zip(
                boxes.xyxy,
                boxes.id,
                boxes.conf,
                boxes.cls
            ):
                x1, y1, x2, y2 = box.tolist()
                class_name = self.model.names[int(cls)]
                
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                width = x2 - x1
                height = y2 - y1
                
                curr_obj = DetectedObject(
                    object_id=int(track_id),
                    class_name=class_name,
                    confidence=float(conf),
                    position=(center_x, center_y),
                    size=(width, height),
                    last_seen=timestamp
                )
                detections.append(curr_obj)
        return detections

    def annotate_frame(self, frame: np.ndarray) -> np.ndarray:
        """Draw bounding boxes and labels on frame"""
        annotated = frame.copy()
        detections = self._detect_objects([frame], [time.time()])
        
        for det in detections:
            x, y = det.position
            w, h = det.size
            x1, y1 = int(x - w/2), int(y - h/2)
            x2, y2 = int(x + w/2), int(y + h/2)
            
            # Draw box
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Add label
            label = f"{det.class_name} ({det.confidence:.2f})"
            cv2.putText(annotated, label, (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return annotated
        
    def process_movement(self, tracking_buffer):
        """Process recent frames to detect significant movement and provide clear guidance"""
        if len(tracking_buffer) < 4:
            return None
                
        prev_frame, prev_time = tracking_buffer[-4]
        curr_frame, curr_time = tracking_buffer[-1]
        
        prev_detections = self._detect_objects([prev_frame], [prev_time])
        curr_detections = self._detect_objects([curr_frame], [curr_time])
        
        # Track movements by object type
        movements = defaultdict(lambda: {'count': 0, 'direction': '', 'speed': 0})
        
        for curr in curr_detections:
            for prev in prev_detections:
                if curr.object_id == prev.object_id:
                    dx = curr.position[0] - prev.position[0]
                    dy = curr.position[1] - prev.position[1]
                    
                    if abs(dx) > 250 or abs(dy) > 250:  # Significant movement threshold
                        speed = np.sqrt(dx*dx + dy*dy)
                        direction = self._get_movement_direction(dx, dy)
                        
                        obj_type = curr.class_name
                        movements[obj_type]['count'] += 1
                        movements[obj_type]['direction'] = direction
                        movements[obj_type]['speed'] = max(movements[obj_type]['speed'], speed)
        
        # Generate movement summary
        if not movements:
            return None
            
        summary_parts = []
        guidance = []
        
        for obj_type, data in movements.items():
            count = data['count']
            direction = data['direction']
            speed = data['speed']
            
            # Add movement description
            if count > 1:
                summary_parts.append(f"{count} {obj_type}s moving {direction}")
            else:
                summary_parts.append(f"{obj_type} moving {direction}")
                
            # Add guidance for fast moving objects
            if speed > 175:  # Adjust threshold as needed
                opposite_direction = "right" if direction == "left" else "left" if direction == "right" else "back" if direction == "up" else "forward"
                guidance.append(f"move {opposite_direction} to avoid {obj_type}")
        
        summary = ", ".join(summary_parts)
        if guidance:
            summary += " - " + ", ".join(guidance)
            return f"[HIGH] {summary}"
        return f"[LOW] {summary}"

    def summarize_scene(self, analysis_buffer) -> str:
        """Generate detailed scene summary from buffer"""
        if not analysis_buffer:
            return "[LOW] No data available"
            
        latest_frame, _ = analysis_buffer[-1]
        detections = self._detect_objects([latest_frame], [time.time()])
        
        # Count objects and track positions
        counts = defaultdict(int)
        positions = defaultdict(list)
        
        for det in detections:
            counts[det.class_name] += 1
            pos = self._get_position(det.position[0], det.position[1])
            positions[det.class_name].append(pos)
        
        # Build summary
        summary_parts = []
        for obj_type, count in counts.items():
            if count > 2:
                summary_parts.append(f"{count} {obj_type}s")
            else:
                for pos in positions[obj_type]:
                    summary_parts.append(f"{obj_type} on {pos}")
                    
        return "[LOW] " + ", ".join(summary_parts) if summary_parts else "[LOW] Path clear"
    
    
    def find_tag(self, response: str) -> str:
        """Find and return the highest-priority tag in the response."""
        priority = ["[EMERGENCY]", "[HIGH]", "[LOW]"]  # Highest to lowest priority
        
        for tag in priority:
            if re.search(re.escape(tag), response):  # Direct search instead of list
                return tag

        return "[LOW]"  # Default to lowest priority
    
    def llm_summarize(self, analysis_buffer) -> str:
        if not analysis_buffer:
            return "[LOW] No data available"
            
        scene_summary = self.summarize_scene(analysis_buffer)
        memory_context = self._format_memory()

        context = {
            "previous_observations": memory_context,
            "current_scene": scene_summary
        }

        prompt = (
            f'''You are iAssist, a virtual assistant helping navigate surroundings.\n'''
            f'''Previous observations:\n{context["previous_observations"]}\n'''
            f'''Current scene: {context["current_scene"]}\n'''
            f'''Provide a concise (1-3 sentences) summary comparing current and previous scenes.\n'''
            f'''Include position-based guidance only if objects pose potential risks.\n'''
            f'''Use appropriate tags:\n'''
            f'''[EMERGENCY] - Immediate danger\n'''
            f'''[HIGH] - Caution needed\n'''
            f'''[LOW] - Normal situation\n'''
        )
        

        client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            model="llama-3.2-3b-preview"
        )

        try:
            response = chat_completion.choices[0].message.content.strip()
            tag = self.find_tag(response)
                
            # Store in memory buffer
            self.memory_buffer.append((time.time(), scene_summary))
            
            return response, tag
        except Exception as e:
            print(f"[LLM] Error: {e}")
            return "[LOW] Path is clear"
    
    def _format_for_priority_queue(self, response: str, tag: str) -> Tuple[str, int]:
        priority_map = {
            "[EMERGENCY]": 3,  # Urgent
            "[HIGH]": 2,      # Important
            "[LOW]": 1        # Info
        }
        
        # Clean up the response by removing tags
        clean_response = response
        for t in ["[EMERGENCY]", "[HIGH]", "[LOW]"]:
            clean_response = clean_response.replace(t, "").strip()
        
        # Extract first sentence for conciseness
        first_sentence = clean_response.split('.')[0].strip()
        
        # Return format matching NavigationQueue's expected input
        return (first_sentence, priority_map.get(tag, 1))

