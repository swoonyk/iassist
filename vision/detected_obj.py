from .imports import *

@dataclass
class DetectedObject:
    object_id: int
    class_name: str
    confidence: float
    position: Tuple[float, float]  # (x, y) center in pixels
    size: Tuple[float, float]      # (width, height) in pixels
    last_seen: float
    frequency: int = 1
    movement: Tuple[float, float] = (0.0, 0.0)  # (dx, dy)

    def get_position(self) -> Tuple[float, float, float, float]:
        """Return bbox coordinates (x1, y1, x2, y2)"""
        x, y = self.position
        w, h = self.size
        return (x - w/2, y - h/2, x + w/2, y + h/2)
    
