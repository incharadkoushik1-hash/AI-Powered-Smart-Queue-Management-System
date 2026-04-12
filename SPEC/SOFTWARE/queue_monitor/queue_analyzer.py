import cv2
import numpy as np
import logging
from typing import List, Tuple, Optional, Dict
from collections import deque
from datetime import datetime, timedelta
from detector import BoundingBox

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueueAnalyzer:
    def __init__(self, config: dict, detector=None):
        self.config = config
        self.detector = detector
        self.roi_points = np.array(config.get('roi_points', [[100, 100], [500, 100], [500, 400], [100, 400]]), np.int32)
        self.max_threshold = config.get('max_threshold', 10)
        self.min_threshold = config.get('min_threshold', 3)
        self.history_size = config.get('history_size', 100)
        self.count_history = deque(maxlen=self.history_size)
        self.avg_service_time = config.get('avg_service_time', 120)
        self.last_update = datetime.now()
        self.current_count = 0
        self.peak_count = 0
        self.total_count = 0
        
    def set_roi(self, points: List[List[int]]):
        self.roi_points = np.array(points, np.int32)
        logger.info(f"ROI updated: {points}")
        
    def is_point_in_roi(self, point: Tuple[int, int]) -> bool:
        x, y = point
        return cv2.pointPolygonTest(self.roi_points, (x, y), False) >= 0
    
    def count_in_roi(self, boxes: List[BoundingBox]) -> int:
        count = 0
        in_roi_boxes = []
        
        for box in boxes:
            if self.is_point_in_roi(box.center):
                count += 1
                in_roi_boxes.append(box)
        
        self.current_count = count
        self.count_history.append({
            'count': count,
            'timestamp': datetime.now()
        })
        
        if count > self.peak_count:
            self.peak_count = count
            
        self.total_count += count
        
        return count
    
    def calculate_wait_time(self, count: int) -> float:
        if count <= self.min_threshold:
            return 0
        return (count - self.min_threshold) * (self.avg_service_time / 60)
    
    def get_queue_status(self, count: int) -> str:
        if count >= self.max_threshold:
            return "CRITICAL"
        elif count >= self.max_threshold * 0.7:
            return "HIGH"
        elif count >= self.min_threshold:
            return "NORMAL"
        else:
            return "LOW"
    
    def get_trend(self) -> str:
        if len(self.count_history) < 5:
            return "STABLE"
            
        recent = list(self.count_history)[-5:]
        counts = [h['count'] for h in recent]
        
        if counts[-1] > counts[0] + 2:
            return "INCREASING"
        elif counts[-1] < counts[0] - 2:
            return "DECREASING"
        else:
            return "STABLE"
    
    def calculate_stats(self) -> Dict:
        now = datetime.now()
        time_diff = (now - self.last_update).total_seconds()
        self.last_update = now
        
        wait_time = self.calculate_wait_time(self.current_count)
        status = self.get_queue_status(self.current_count)
        trend = self.get_trend()
        
        avg_count = 0
        if len(self.count_history) > 0:
            avg_count = sum(h['count'] for h in self.count_history) / len(self.count_history)
        
        return {
            'current_count': self.current_count,
            'peak_count': self.peak_count,
            'average_count': round(avg_count, 1),
            'wait_time_minutes': round(wait_time, 1),
            'status': status,
            'trend': trend,
            'max_threshold': self.max_threshold,
            'min_threshold': self.min_threshold,
            'total_people': self.total_count,
            'timestamp': now.isoformat()
        }
    
    def draw_roi(self, frame: np.ndarray) -> np.ndarray:
        output = frame.copy()
        
        color = (255, 0, 0)
        thickness = 2
        
        cv2.polylines(output, [self.roi_points], True, color, thickness)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        text_color = (255, 255, 255)
        bg_color = (0, 0, 139)
        
        text = f"Queue: {self.current_count}"
        text_size, _ = cv2.getTextSize(text, font, font_scale, 2)
        
        x, y = self.roi_points[0]
        y = y - 10 if y > 50 else y + text_size[1] + 20
        
        cv2.rectangle(output, 
                     (x - 5, y - text_size[1] - 5),
                     (x + text_size[0] + 5, y + 5),
                     bg_color, -1)
        
        cv2.putText(output, text, (x, y), font, font_scale, text_color, 2)
        
        return output
    
    def reset_stats(self):
        self.current_count = 0
        self.peak_count = 0
        self.total_count = 0
        self.count_history.clear()
        logger.info("Statistics reset")
