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
            results = self.model.predict(frame, conf=0.5)[0]
            if not hasattr(results, "boxes") or results.boxes is None:
                continue
            for box, conf, cls in zip(results.boxes.xyxy, results.boxes.conf, results.boxes.cls):
                x1, y1, x2, y2 = box.tolist()
                class_name = self.model.names[int(cls)]

                center_x = ((x1 + x2) / 2) / frame.shape[1]
                center_y = ((y1 + y2) / 2) / frame.shape[0]
                width = (x2 - x1) / frame.shape[1]
                height = (y2 - y1) / frame.shape[0]

                curr_obj = DetectedObject(
                    object_id=1,
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
            "moving_objects": [],
            "potential_hazards": [],
            "cues": []
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
        if x < 0.33:
            horizontal = "left"
        elif x > 0.66:
            horizontal = "right"
        depth = "at medium distance"
        if y < 0.33:
            depth = "far ahead"
        elif y > 0.66:
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
            f"Your name is iAssist. You are a virtual assistant meant to help visually-impaired individuals navigate their surroundings more comfortably.\n\n"
            f"You can only name and use objects detected in the context below. Do not make any assumptions or hallucinate details that are not present in the scene context.\n"
            f"CONTEXT:\n\n"
            f"{context}\n\n"
            f"END CONTEXT\n\n"
            f"REMEMBER that this is one-way communication, so don't say anything like 'do you see the' or 'can you go to the'.\n"
            f"Based solely on the provided scene analysis above, generate immediate navigation guidance.\n"
            f"1. First, analyze the situation and assign ONE of these priority levels:\n"
            f"   EMERGENCY: Immediate danger requiring instant action (e.g., fast moving vehicles, immediate collisions)\n"
            f"   HIGH: Important but not life-threatening (e.g., obstacles in direct path, people walking nearby)\n"
            f"   LOW: General information about surroundings (e.g., static objects far away, ambient descriptions)\n"
            f"2. Format your response EXACTLY like this:\n"
            f"   [PRIORITY_LEVEL] Your guidance message\n"
            f"3. Provide immediate safety warnings and directions, if applicable (if not, don't say anything).\n"
            f"4. If there is nothing there, or nothing that will impair the individual, respond with: [LOW] nothing in the way\n"
            f"5. Be EXTREMELY concise. 1-2 sentences max. Just talk about objects, don't describe surroundings too much.\n"
            f"6. Do not recommend unnecessary actions, such as moving towards another individual, unless it is crucial for safety.\n"
            f"7. Do not ask follow-up questions or request additional scene information. Never hallucinate any details not present in the scene context.\n"
            f"Keep the response concise and suitable for text-to-speech.\n\n"
            f"Example responses:\n"
            f"[EMERGENCY] `message`\n"
            f"[HIGH] Large table directly ahead, veer left to avoid.\n"
            f"[LOW] Bookshelf on the far right side.\n"
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
 
    def _generate_fallback_guidance(self, scene_description: Dict) -> str:
        guidance = []
        if scene_description["potential_hazards"]:
            hazards = [f"{h['type']} {h.get('reason', '')}" for h in scene_description["potential_hazards"]]
            guidance.append(f"Caution: {', '.join(hazards)}")
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