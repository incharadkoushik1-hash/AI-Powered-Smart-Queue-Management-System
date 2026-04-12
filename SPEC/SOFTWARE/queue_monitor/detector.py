import cv2
import numpy as np
import logging
from typing import List, Tuple, Optional
from ultralytics import YOLO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BoundingBox:
    def __init__(self, x1: int, y1: int, x2: int, y2: int, confidence: float, cls: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.confidence = confidence
        self.cls = cls
        
    @property
    def center(self) -> Tuple[int, int]:
        return int((self.x1 + self.x2) / 2), int((self.y1 + self.y2) / 2)
    
    @property
    def area(self) -> int:
        return (self.x2 - self.x1) * (self.y2 - self.y1)
    
    def to_dict(self) -> dict:
        return {
            'x1': self.x1, 'y1': self.y1,
            'x2': self.x2, 'y2': self.y2,
            'confidence': self.confidence,
            'class': self.cls,
            'center': self.center
        }


class PersonDetector:
    def __init__(self, config: dict):
        self.config = config
        self.model_path = config.get('model_path', 'yolov8n.pt')
        self.confidence_threshold = config.get('confidence', 0.5)
        self.target_classes = config.get('classes', [0])
        self.model = None
        self._is_loaded = False
        
    def load_model(self) -> bool:
        try:
            logger.info(f"Loading YOLO model from: {self.model_path}")
            self.model = YOLO(self.model_path)
            self._is_loaded = True
            logger.info("YOLO model loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to load YOLO model: {e}")
            return False
    
    def detect(self, frame: np.ndarray) -> List[BoundingBox]:
        if not self._is_loaded or self.model is None:
            logger.error("Model not loaded. Call load_model() first.")
            return []
        
        try:
            results = self.model(frame, verbose=False)
            
            boxes = []
            for result in results:
                if result.boxes is None:
                    continue
                    
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    
                    if cls_id in self.target_classes and conf >= self.confidence_threshold:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        boxes.append(BoundingBox(x1, y1, x2, y2, conf, cls_id))
            
            return boxes
            
        except Exception as e:
            logger.error(f"Detection error: {e}")
            return []
    
    def draw_boxes(self, frame: np.ndarray, boxes: List[BoundingBox]) -> np.ndarray:
        output = frame.copy()
        
        for box in boxes:
            color = (0, 255, 0)
            cv2.rectangle(output, (box.x1, box.y1), (box.x2, box.y2), color, 2)
            
            label = f"Person {box.confidence:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            
            cv2.rectangle(output, 
                         (box.x1, box.y1 - label_size[1] - 10),
                         (box.x1 + label_size[0], box.y1),
                         color, -1)
            
            cv2.putText(output, label, (box.x1, box.y1 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            
            cv2.circle(output, box.center, 5, (0, 0, 255), -1)
        
        return output
    
    def is_loaded(self) -> bool:
        return self._is_loaded
