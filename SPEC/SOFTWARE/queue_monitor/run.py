import cv2
import logging
import signal
import sys
import threading
import time
import argparse
from config.settings import get_settings
from camera_handler import CameraHandler
from detector import PersonDetector
from queue_analyzer import QueueAnalyzer
from alert_manager import AlertManager
from recommender import StaffingRecommender
import dashboard_server

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

running = True
settings = None


def signal_handler(signum, frame):
    global running
    logger.info("Shutdown signal received")
    running = False


def main():
    global running, settings
    
    parser = argparse.ArgumentParser(description='AI Queue Monitoring System')
    parser.add_argument('--config', type=str, help='Path to config.yaml')
    parser.add_argument('--no-alerts', action='store_true', help='Disable alerts')
    args = parser.parse_args()
    
    settings = get_settings()
    
    if args.config:
        settings.load_config(args.config)
    
    if args.no_alerts:
        settings.alerts['led_enabled'] = False
        settings.alerts['buzzer_enabled'] = False
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("=" * 50)
    logger.info("AI Queue Monitoring System")
    logger.info("=" * 50)
    
    logger.info("Initializing camera...")
    camera = CameraHandler(settings.camera)
    if not camera.open():
        logger.error("Failed to open camera. Exiting.")
        sys.exit(1)
    
    logger.info("Loading YOLOv8 model...")
    detector = PersonDetector(settings.detection)
    if not detector.load_model():
        logger.error("Failed to load detection model. Exiting.")
        camera.release()
        sys.exit(1)
    
    logger.info("Initializing queue analyzer...")
    analyzer = QueueAnalyzer(settings.queue, detector)
    
    logger.info("Initializing alert manager...")
    alert_manager = AlertManager(settings.alerts)
    alert_manager.system_ready()
    
    logger.info("Initializing staffing recommender...")
    recommender = StaffingRecommender(settings.recommendations)
    
    logger.info("Starting dashboard server...")
    dashboard_server.init_server(analyzer, recommender, camera)
    server_thread = threading.Thread(
        target=dashboard_server.run_server,
        kwargs={
            'host': settings.server.get('host', '0.0.0.0'),
            'port': settings.server.get('port', 5000),
            'debug': settings.server.get('debug', False)
        }
    )
    server_thread.daemon = True
    server_thread.start()
    
    logger.info(f"Dashboard available at http://localhost:{settings.server.get('port', 5000)}")
    
    logger.info("Starting main processing loop...")
    frame_count = 0
    last_alert_time = time.time()
    alert_cooldown = 10
    
    previous_status = None
    
    while running:
        frame = camera.read()
        
        if frame is None:
            logger.warning("Failed to read frame, retrying...")
            time.sleep(0.1)
            continue
        
        frame_count += 1
        
        if frame_count % 5 == 0:
            boxes = detector.detect(frame)
            
            count = analyzer.count_in_roi(boxes)
            stats = analyzer.calculate_stats()
            
            annotated_frame = analyzer.draw_roi(frame)
            annotated_frame = detector.draw_boxes(annotated_frame, boxes)
            
            dashboard_server.update_frame(annotated_frame)
            dashboard_server.update_stats(stats)
            
            current_time = time.time()
            status = stats['status']
            
            if status != previous_status:
                if status == 'CRITICAL' or status == 'HIGH':
                    if current_time - last_alert_time > alert_cooldown:
                        if status == 'CRITICAL':
                            alert_manager.alert_queue_critical()
                        else:
                            alert_manager.alert_queue_high()
                        last_alert_time = current_time
                elif status in ['NORMAL', 'LOW']:
                    alert_manager.alert_queue_normal()
                
                previous_status = status
        else:
            dashboard_server.update_frame(frame)
        
        if frame_count % 100 == 0:
            logger.info(f"Processed {frame_count} frames - Current queue: {analyzer.current_count}")
    
    logger.info("Shutting down...")
    camera.release()
    alert_manager.cleanup()
    logger.info("Shutdown complete")


if __name__ == '__main__':
    main()
