from .imports import *
from .detected_obj import DetectedObject
    
class Scene:
    def __init__(self, memory_duration=5.0):
        self.model = YOLO("yolov8n-seg.pt")
        self.llm = ollama.Client()
        self.memory_duration = memory_duration
        self.tracked_objects: Dict[int, DetectedObject] = {}
        self.next_object_id = 0
        self.last_seen = time.time()

    def _same_object(self, initial: Tuple[float, float, float, float], final: Tuple[float,float,float,float]) -> float:
        x1 = max(initial[0], final[0])
        y1 = max(initial[1], final[1])
        x2 = min(initial[2], final[2])
        y2 = min(initial[3], final[3])
        intersection = max(0, x2 - x1) * max(0, y2 - y1)
        area1 = (initial[2] - initial[0]) * (initial[3] - initial[1])
        area2 = (final[2] - final[0]) * (final[3] - final[1])  
        union = area1 + area2 - intersection
        return intersection / union if union else 0
    
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
                
                # Keep raw pixel coordinates for position
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
            
    def _update_memory(self, new_detections: List[DetectedObject]):
        curr_time = time.time()
        updated_objects: Dict[int, DetectedObject] = {}

        for obj_id, obj in self.tracked_objects.items():
            if curr_time - obj.last_seen <= self.memory_duration:
                updated_objects[obj_id] = obj
        
        for new_obj in new_detections:
            matched = False
            new_pos = new_obj.get_position()
            for obj_id, tracked_obj in updated_objects.items():
                if tracked_obj.class_name != new_obj.class_name:
                    continue
                if self._same_object(new_pos, tracked_obj.get_position()) > 0.3:
                    tracked_obj.last_seen = new_obj.last_seen
                    tracked_obj.frequency += 1
                    matched = True
                    break
            
            if not matched:
                new_obj.object_id = self.next_object_id
                self.next_object_id += 1
                updated_objects[new_obj.object_id] = new_obj
        
        self.tracked_objects = updated_objects

    def _classify_scene(self) -> Dict:
        scene_description = {
            "static_objects": [],
            "moving_objects": []
        }

        for obj in self.tracked_objects.values():
            movement_speed = np.linalg.norm(obj.movement)
            if movement_speed < 0.1 and obj.frequency > 2:
                scene_description["static_objects"].append({
                    "type": obj.class_name,
                    "position": self._get_position_description(obj.position),
                    "size": "large" if ((obj.size[0] * obj.size[1]) > 0.1) else "small"
                })
            elif movement_speed >= 0.1:
                movement_desc = self._get_movement_description(obj.movement)
                scene_description["moving_objects"].append({
                    "type": obj.class_name,
                    "movement": movement_desc
                })
        return scene_description
    
    def _get_position_description(self, pos: Tuple[float, float]) -> str:
        x, y = pos
        horizontal = "center"
        if x < 213:  # 640/3 for left third
            horizontal = "left"
        elif x > 426:  # 640*2/3 for right third
            horizontal = "right"
        depth = "at medium distance"
        if y < 160:  # 480/3 for far third
            depth = "far ahead"
        elif y > 320:  # 480*2/3 for near third
            depth = "nearby"
        return f"{horizontal} side, {depth}"
 
    def _get_movement_description(self, movement: Tuple[float, float]) -> str:
        dx, dy = movement
        speed = np.linalg.norm(movement)
        if speed < 0.1:
            return "stationary"
        directions = []
        if abs(dx) > 0.1:
            directions.append("right" if dx > 0 else "left")
        if abs(dy) > 0.1:
            directions.append("closer" if dy > 0 else "away")
        speed_desc = "quickly" if speed > 0.3 else "slowly"
        return f"moving {speed_desc} {' and '.join(directions)}"
    
    '''
    
    def _generate_guidance(self, scene_description: Dict) -> str:
        context = (
            "Scene Analysis:\n"
            "- Static Objects: {}\n".format(
                ', '.join("{} ({})".format(obj['type'], obj['position']) for obj in scene_description['static_objects'])
            ) +
            "- Moving Objects: {}\n".format(
                ', '.join("{} {}".format(obj['type'], obj['movement']) for obj in scene_description['moving_objects'])
            ) +
            "- Hazards: {}".format(
                ', '.join("{} ({})".format(obj['type'], obj.get('reason', 'unknown')) for obj in scene_description['potential_hazards'])
            )
        )
        prompt = (
            "You are a safety-critical navigation assistant for visually impaired users. "
            "Respond ONLY to explicitly detected objects from sensor data using this format:\n\n"

            "PRIORITY TIERS:\n"
            "[EMERGENCY] Immediate collision risk (3+ alarms):\n"
            "- Vehicle/person moving >15mph toward user\n"
            "- Fire/explosion within 10m\n"
            "- Falling objects overhead\n\n"

            "[HIGH] Path obstruction (2+ confirmations):\n"
            "- Solid object in 1m path\n"
            "- Moving obstacle (<5m closing distance)\n"
            "- Unmarked elevation change\n\n"

            "[LOW] All other verified objects:\n"
            "- Static objects\n"
            "- Ambient info\n"
            "- Clear paths\n\n"

            "STRICT PROTOCOLS:\n"
            "1. REJECT non-detected objects - NO INFERENCE\n"
            "2. Use ONLY 'you'/'your' directives\n"
            "3. Responses <12 words\n"
            "4. If uncertain: '[LOW] Path requires verification'\n"
            "5. NO QUESTIONS - ONLY STATEMENTS\n\n"

            "TERMINATION TRIGGERS:\n"
            "- Any mention of undetected objects\n"
            "- Probability words (maybe, possibly)\n"
            "- Any questioning or asking for input\n"
            "- Non-safety information\n\n"

            "FORMAT EXAMPLES:\n"
            "[EMERGENCY] Bus accelerating toward you - Move left NOW\n"
            "[HIGH] Construction barrier 2m ahead - Turn right\n"
            "[LOW] Trash can 1m to your right\n"
            "[LOW] Path clear\n\n"

            "COMPLIANCE ORDER:\n"
            "If scene data contains:\n"
            "- 0 objects → '[LOW] Path clear'\n"
            "- Unconfirmed detections → '[LOW] Path requires verification'\n"
            "- Emergency triggers → Immediate action command\n"
            "- Protocol violation → Reject input"
        )
        try:
            response = self.llm.generate(model="llama3.2:3b", prompt=prompt)
            # Verify response format
            if not any(level in response.response for level in ["[EMERGENCY]", "[HIGH]", "[LOW]"]):
                # If response doesn't contain priority level, prepend with LOW
                return f"[LOW] {response.response}"
            return response.response
        except Exception as e:
            print(f"[LLM] Error: {e}")
            return self._generate_fallback_guidance(scene_description)
    
    '''
 
    def _generate_guidance(self, scene_description: Dict) -> str:
        guidance = []
        if scene_description["moving_objects"]:
            moving = [f"{m['type']} {m['movement']}" for m in scene_description["moving_objects"]]
            guidance.append(f"Movement detected: {', '.join(moving)}")
        if scene_description["static_objects"]:
            static = [f"{s['type']} {s['position']}" for s in scene_description["static_objects"]]
            guidance.append(f"Surroundings: {', '.join(static)}")
        return " ".join(guidance)
 
    def process_frame_batch(self, frames: List[np.ndarray], timestamps: List[float]) -> str:
        new_detections = self._detect_objects(frames, timestamps)
        self._update_memory(new_detections)
        scene_description = self._classify_scene()
        guidance = self._generate_guidance(scene_description)
        return guidance
    
    
    def speak_guidance(self, text: str):
        print(text)