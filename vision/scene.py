from .imports import *
from .detected_obj import DetectedObject
    
class Scene:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")
        self.tracked_objects = {}
        self.memory_buffer = deque(maxlen=5)  # Keep last 5 observations
        self.last_seen = time.time()
        load_dotenv()

    def _format_memory(self) -> str:
        """Format memory buffer into context string"""
        if not self.memory_buffer:
            return "No previous observations."
        
        memory_entries = []
        current_time = time.time()
        
        for timestamp, summary in self.memory_buffer:
            time_ago = round(current_time - timestamp, 1)
            memory_entries.append(f"[{time_ago}s ago]: {summary}")
            
        return "\n".join(memory_entries)
    
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
            return "right" if dx > 0 else "left"
        else:
            return "down" if dy > 0 else "up"

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
        """Process recent frames to detect significant movement"""
        if len(tracking_buffer) < 2:
            return None
            
        # Compare most recent frames
        prev_frame, prev_time = tracking_buffer[-2]
        curr_frame, curr_time = tracking_buffer[-1]
        
        prev_detections = self._detect_objects([prev_frame], [prev_time])
        curr_detections = self._detect_objects([curr_frame], [curr_time])
        
        # Track significant position changes
        movements = []
        for curr in curr_detections:
            for prev in prev_detections:
                if curr.object_id == prev.object_id:
                    dx = curr.position[0] - prev.position[0]
                    dy = curr.position[1] - prev.position[1]
                    if abs(dx) > 50 or abs(dy) > 50:  # Significant movement threshold
                        direction = self._get_movement_direction(dx, dy)
                        movements.append(f"{curr.class_name} moving {direction}")
        
        return ", ".join(movements) if movements else None

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
            f'''Provide a concise (10 word maximum) summary about current scene. If needed, compare to previous observations.\n'''
            f'''Include position-based guidance only if objects pose potential risks.\n'''
            f'''Use appropriate tags:\n'''
            f'''[EMERGENCY] - Immediate danger\n'''
            f'''[HIGH] - Caution needed\n'''
            f'''[LOW] - Normal situation\n'''
            f'''Examples:'''
            f'''[LOW] 2 bookshelves and a chair to your right.'''
            f'''[HIGH] Watch out for the wet floor ahead.'''
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