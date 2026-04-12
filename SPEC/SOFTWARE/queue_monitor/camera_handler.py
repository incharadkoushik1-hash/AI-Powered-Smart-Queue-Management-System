import cv2
import numpy as np
import logging
from typing import Optional, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CameraHandler:
    def __init__(self, config: dict):
        self.config = config
        self.source = config.get('source', 0)
        self.width = config.get('width', 1280)
        self.height = config.get('height', 720)
        self.fps = config.get('fps', 30)
        self.cap = None
        self._is_opened = False
        
    def open(self) -> bool:
        try:
            if isinstance(self.source, int):
                self.cap = cv2.VideoCapture(self.source)
            else:
                self.cap = cv2.VideoCapture(str(self.source))
            
            if not self.cap.isOpened():
                logger.error(f"Failed to open camera source: {self.source}")
                return False
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            
            actual_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            actual_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            actual_fps = self.cap.get(cv2.CAP_PROP_FPS)
            
            logger.info(f"Camera opened: {actual_width}x{actual_height} @ {actual_fps}fps")
            self._is_opened = True
            return True
            
        except Exception as e:
            logger.error(f"Error opening camera: {e}")
            return False
    
    def read(self) -> Optional[np.ndarray]:
        if not self._is_opened or self.cap is None:
            return None
            
        ret, frame = self.cap.read()
        if not ret:
            logger.warning("Failed to read frame from camera")
            return None
            
        return frame
    
    def read_with_encoding(self) -> Tuple[Optional[np.ndarray], Optional[bytes]]:
        frame = self.read()
        if frame is None:
            return None, None
            
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 85]
        ret, buffer = cv2.imencode('.jpg', frame, encode_param)
        
        if not ret:
            return frame, None
            
        return frame, buffer.tobytes()
    
    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            self._is_opened = False
            logger.info("Camera released")
    
    def isOpened(self) -> bool:
        if self.cap is None:
            return False
        return self.cap.isOpened() and self._is_opened
    
    def get_frame_dimensions(self) -> Tuple[int, int]:
        if self.cap is not None and self._is_opened:
            return int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), \
                   int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return self.width, self.height
    
    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
