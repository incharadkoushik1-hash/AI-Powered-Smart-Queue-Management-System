import yaml
import os
import logging
from typing import Any, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings:
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self.load_config()
    
    def load_config(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__), 
                'config.yaml'
            )
        
        try:
            with open(config_path, 'r') as f:
                self._config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            self._config = self._get_default_config()
        except yaml.YAMLError as e:
            logger.error(f"Error parsing config: {e}")
            self._config = self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        return {
            'camera': {
                'source': 0,
                'width': 1280,
                'height': 720,
                'fps': 30
            },
            'detection': {
                'model_path': 'yolov8n.pt',
                'confidence': 0.5,
                'classes': [0]
            },
            'queue': {
                'roi_points': [[200, 150], [1080, 150], [1080, 570], [200, 570]],
                'max_threshold': 10,
                'min_threshold': 3,
                'history_size': 100,
                'avg_service_time': 120
            },
            'shelves': [
                {'id': 1, 'name': 'Shelf A', 'bbox': [50, 100, 400, 200], 'category': 'beverages'},
                {'id': 2, 'name': 'Shelf B', 'bbox': [450, 100, 800, 200], 'category': 'snacks'},
            ],
            'shelf_detection': {
                'enabled': True,
                'low_threshold': 30,
                'empty_threshold': 10,
                'scan_interval': 10
            },
            'alerts': {
                'led_enabled': True,
                'buzzer_enabled': True,
                'alert_duration': 2
            },
            'server': {
                'host': '0.0.0.0',
                'port': 5000,
                'debug': False
            },
            'recommendations': {
                'staff_per_5_people': 1,
                'max_queue_per_staff': 5,
                'current_staff': 2
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_section(self, section: str) -> Dict:
        return self._config.get(section, {})
    
    @property
    def camera(self) -> Dict:
        return self._config.get('camera', {})
    
    @property
    def detection(self) -> Dict:
        return self._config.get('detection', {})
    
    @property
    def queue(self) -> Dict:
        return self._config.get('queue', {})
    
    @property
    def alerts(self) -> Dict:
        return self._config.get('alerts', {})
    
    @property
    def server(self) -> Dict:
        return self._config.get('server', {})
    
    @property
    def recommendations(self) -> Dict:
        return self._config.get('recommendations', {})
    
    @property
    def shelf_detection(self) -> Dict:
        return self._config.get('shelf_detection', {})


def get_settings() -> Settings:
    return Settings()
