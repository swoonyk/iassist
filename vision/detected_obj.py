from .imports import *

@dataclass
class DetectedObject:
    object_id: int
    class_name: str
    confidence: float
    position: Tuple[float, float] #to be normalized
    size: Tuple[float, float] #to also be normalized
    last_seen: float #time
    movement: Tuple[float, float] = (0.0, 0.0) #dx, dy
    frequency: int = 1

    def get_position(self) -> Tuple[float, float, float, float]:
        x, y = self.position
        w, h = self.size
        return (x - w/2, y - h/2, x + w/2, y + h/2)
    
