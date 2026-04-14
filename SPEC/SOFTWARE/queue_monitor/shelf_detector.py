import cv2
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ShelfStatus:
    shelf_id: int
    name: str
    status: str
    fill_percentage: float
    alert_needed: bool
    bbox: Tuple[int, int, int, int]


class ShelfDetector:
    def __init__(self, config: dict):
        self.config = config
        self.shelves = config.get('shelves', [])
        self.low_threshold = config.get('low_threshold', 30)
        self.empty_threshold = config.get('empty_threshold', 10)
        self.scan_interval = config.get('scan_interval', 10)
        self._last_scan_frame = None
        self._cached_results = []
        self._reference_saturation = {}
        self._initialized = False
        
    def initialize(self, frame: np.ndarray) -> bool:
        if self._initialized:
            return True
            
        try:
            for shelf in self.shelves:
                bbox = shelf.get('bbox')
                if bbox:
                    x1, y1, x2, y2 = self._validate_bbox(bbox, frame.shape)
                    if x2 > x1 and y2 > y1:
                        region = frame[y1:y2, x1:x2]
                        avg_sat = self._get_avg_saturation(region)
                        self._reference_saturation[shelf.get('id', 0)] = avg_sat
                        logger.info(f"Shelf '{shelf.get('name', 'Unknown')}' reference saturation: {avg_sat:.1f}")
            
            self._initialized = True
            logger.info(f"Shelf detector initialized with {len(self.shelves)} shelves")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize shelf detector: {e}")
            return False
    
    def _validate_bbox(self, bbox: List, frame_shape: Tuple) -> Tuple[int, int, int, int]:
        h, w = frame_shape[:2]
        x1 = max(0, min(bbox[0], w - 1))
        y1 = max(0, min(bbox[1], h - 1))
        x2 = max(x1 + 10, min(bbox[2], w))
        y2 = max(y1 + 10, min(bbox[3], h))
        return x1, y1, x2, y2
    
    def _get_avg_saturation(self, region: np.ndarray) -> float:
        if region.size == 0:
            return 50.0
        
        hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
        s_channel = hsv[:, :, 1]
        return float(np.mean(s_channel))
    
    def analyze_shelf_stock(self, frame: np.ndarray) -> List[ShelfStatus]:
        results = []
        
        for shelf in self.shelves:
            shelf_id = shelf.get('id', 0)
            name = shelf.get('name', f'Shelf {shelf_id}')
            bbox = shelf.get('bbox')
            
            if bbox is None:
                continue
                
            x1, y1, x2, y2 = self._validate_bbox(bbox, frame.shape)
            shelf_region = frame[y1:y2, x1:x2]
            
            fill_pct = self._calculate_fill_percentage(shelf_region, shelf_id)
            status = self._get_status(fill_pct)
            
            results.append(ShelfStatus(
                shelf_id=shelf_id,
                name=name,
                status=status,
                fill_percentage=fill_pct,
                alert_needed=(status in ['LOW STOCK', 'EMPTY']),
                bbox=(x1, y1, x2, y2)
            ))
        
        self._cached_results = results
        return results
    
    def _calculate_fill_percentage(self, shelf_region: np.ndarray, shelf_id: int) -> float:
        if shelf_region.size == 0:
            return 0.0
        
        h, w = shelf_region.shape[:2]
        total_pixels = h * w
        
        gray = cv2.cvtColor(shelf_region, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        hsv = cv2.cvtColor(shelf_region, cv2.COLOR_BGR2HSV)
        s_channel = hsv[:, :, 1]
        _, product_mask = cv2.threshold(s_channel, 40, 255, cv2.THRESH_BINARY)
        
        combined = cv2.bitwise_and(product_mask, edges)
        product_pixels = cv2.countNonZero(combined)
        
        reference = self._reference_saturation.get(shelf_id, 50)
        current_sat = self._get_avg_saturation(shelf_region)
        
        saturation_factor = min(100, (current_sat / max(reference, 1)) * 100)
        
        fill_pct = (product_pixels / max(total_pixels, 1)) * 300
        fill_pct = (fill_pct + saturation_factor) / 2
        fill_pct = min(100.0, max(0.0, fill_pct))
        
        return fill_pct
    
    def _get_status(self, fill_percentage: float) -> str:
        if fill_percentage <= self.empty_threshold:
            return "EMPTY"
        elif fill_percentage <= self.low_threshold:
            return "LOW STOCK"
        else:
            return "FULL"
    
    def get_overall_stats(self, shelf_results: List[ShelfStatus]) -> Dict:
        if not shelf_results:
            return {
                'total_shelves': 0,
                'full_count': 0,
                'low_stock_count': 0,
                'empty_count': 0,
                'alerts_needed': 0,
                'overall_status': 'NO_DATA',
                'shelves': []
            }
        
        full_count = sum(1 for s in shelf_results if s.status == 'FULL')
        low_stock_count = sum(1 for s in shelf_results if s.status == 'LOW STOCK')
        empty_count = sum(1 for s in shelf_results if s.status == 'EMPTY')
        
        overall = 'OK'
        if empty_count > 0:
            overall = 'CRITICAL'
        elif low_stock_count > 0:
            overall = 'WARNING'
        
        return {
            'total_shelves': len(shelf_results),
            'full_count': full_count,
            'low_stock_count': low_stock_count,
            'empty_count': empty_count,
            'alerts_needed': low_stock_count + empty_count,
            'overall_status': overall,
            'shelves': [
                {
                    'id': s.shelf_id,
                    'name': s.name,
                    'status': s.status,
                    'fill_percentage': round(s.fill_percentage, 1),
                    'alert': s.alert_needed
                }
                for s in shelf_results
            ]
        }
    
    def draw_annotations(self, frame: np.ndarray, shelf_results: List[ShelfStatus]) -> np.ndarray:
        output = frame.copy()
        
        for shelf in shelf_results:
            x1, y1, x2, y2 = shelf.bbox
            
            color_map = {
                'FULL': (0, 200, 0),
                'LOW STOCK': (0, 165, 255),
                'EMPTY': (0, 0, 255)
            }
            color = color_map.get(shelf.status, (128, 128, 128))
            
            cv2.rectangle(output, (x1, y1), (x2, y2), color, 2)
            
            label = f"{shelf.name}: {shelf.fill_percentage:.0f}% [{shelf.status}]"
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            thickness = 1
            
            (label_w, label_h), baseline = cv2.getTextSize(label, font, font_scale, thickness)
            
            label_bg_x1 = x1
            label_bg_y1 = y1 - label_h - 10
            label_bg_x2 = x1 + label_w + 10
            label_bg_y2 = y1
            
            if label_bg_y1 < 0:
                label_bg_y1 = y2
                label_bg_y2 = y2 + label_h + 10
            
            cv2.rectangle(output, (label_bg_x1, label_bg_y1), (label_bg_x2, label_bg_y2), color, -1)
            
            text_x = x1 + 5
            text_y = label_bg_y2 - 5 if label_bg_y1 < 0 else y1 - 5
            
            cv2.putText(output, label, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)
        
        return output
    
    def get_cached_results(self) -> List[ShelfStatus]:
        return self._cached_results
