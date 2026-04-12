import cv2
import logging
import io
import threading
from flask import Flask, render_template, jsonify, Response, send_file
from flask_cors import CORS
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

global_frame = None
global_stats = {
    'current_count': 0,
    'peak_count': 0,
    'average_count': 0,
    'wait_time_minutes': 0,
    'status': 'INITIALIZING',
    'trend': 'STABLE',
    'timestamp': datetime.now().isoformat()
}
stats_lock = threading.Lock()


def init_server(analyzer, recommender, camera_handler):
    global analyzer_instance, recommender_instance, camera_instance
    analyzer_instance = analyzer
    recommender_instance = recommender
    camera_instance = camera_handler


def update_stats(stats: dict):
    global global_stats
    with stats_lock:
        global_stats = stats.copy()
        global_stats['timestamp'] = datetime.now().isoformat()


def update_frame(frame):
    global global_frame
    global_frame = frame.copy() if frame is not None else None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/stats')
def get_stats():
    with stats_lock:
        stats = global_stats.copy()
    
    if analyzer_instance:
        recommendation = recommender_instance.get_recommendation(stats.get('current_count', 0))
        stats['recommendation'] = recommendation
    
    return jsonify(stats)


@app.route('/api/stats/history')
def get_stats_history():
    if analyzer_instance:
        history = list(analyzer_instance.count_history)
        return jsonify({
            'history': [{'count': h['count'], 'timestamp': h['timestamp'].isoformat()} for h in history]
        })
    return jsonify({'history': []})


@app.route('/api/frame')
def get_frame():
    if global_frame is None:
        return Response(status=204)
    
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
    ret, buffer = cv2.imencode('.jpg', global_frame, encode_param)
    
    if not ret:
        return Response(status=204)
    
    return Response(buffer.tobytes(), mimetype='image/jpeg')


@app.route('/api/frame/annotated')
def get_annotated_frame():
    if global_frame is None:
        return Response(status=204)
    
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 85]
    ret, buffer = cv2.imencode('.jpg', global_frame, encode_param)
    
    if not ret:
        return Response(status=204)
    
    return Response(buffer.tobytes(), mimetype='image/jpeg')


@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'camera_connected': camera_instance.isOpened() if camera_instance else False
    })


@app.route('/api/config')
def get_config():
    if analyzer_instance:
        return jsonify({
            'max_threshold': analyzer_instance.max_threshold,
            'min_threshold': analyzer_instance.min_threshold,
            'roi_points': analyzer_instance.roi_points.tolist() if hasattr(analyzer_instance.roi_points, 'tolist') else analyzer_instance.roi_points,
            'avg_service_time': analyzer_instance.avg_service_time
        })
    return jsonify({})


@app.route('/api/reset', methods=['POST'])
def reset_stats():
    if analyzer_instance:
        analyzer_instance.reset_stats()
        update_stats(analyzer_instance.calculate_stats())
        return jsonify({'status': 'success', 'message': 'Statistics reset'})
    return jsonify({'status': 'error', 'message': 'Analyzer not available'}), 500


def run_server(host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
    logger.info(f"Starting dashboard server on {host}:{port}")
    app.run(host=host, port=port, debug=debug, threaded=True)


if __name__ == '__main__':
    run_server(debug=True)
