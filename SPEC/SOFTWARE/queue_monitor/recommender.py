import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StaffingRecommender:
    def __init__(self, config: dict):
        self.config = config
        self.staff_per_people = config.get('staff_per_5_people', 1)
        self.max_queue_per_staff = config.get('max_queue_per_staff', 5)
        self.current_staff = config.get('current_staff', 2)
        
    def get_recommendation(self, queue_count: int) -> Dict:
        recommended_staff = self._calculate_optimal_staff(queue_count)
        action = self._get_action(recommended_staff)
        
        return {
            'current_staff': self.current_staff,
            'recommended_staff': recommended_staff,
            'staff_needed': max(0, recommended_staff - self.current_staff),
            'action': action,
            'message': self._get_message(action, recommended_staff, queue_count),
            'queue_level': self._get_queue_level(queue_count)
        }
    
    def _calculate_optimal_staff(self, queue_count: int) -> int:
        if queue_count <= 0:
            return 1
        
        optimal = max(1, queue_count // self.max_queue_per_staff)
        
        if queue_count % self.max_queue_per_staff > 0:
            optimal += 1
            
        return min(optimal, 10)
    
    def _get_action(self, recommended: int) -> str:
        if recommended > self.current_staff + 1:
            return "ADD_STAFF"
        elif recommended == self.current_staff:
            return "MAINTAIN"
        else:
            return "REDUCE"
    
    def _get_queue_level(self, count: int) -> str:
        if count == 0:
            return "EMPTY"
        elif count <= 3:
            return "LIGHT"
        elif count <= 7:
            return "MODERATE"
        elif count <= 12:
            return "HEAVY"
        else:
            return "OVERLOADED"
    
    def _get_message(self, action: str, staff_count: int, queue_count: int) -> str:
        messages = {
            "ADD_STAFF": f"Queue is getting busy ({queue_count} people). Consider adding {max(1, staff_count - self.current_staff)} staff member(s).",
            "MAINTAIN": f"Current staffing ({self.current_staff}) is adequate for {queue_count} people in queue.",
            "REDUCE": f"Queue is light ({queue_count} people). Consider reducing to {staff_count} staff member(s)."
        }
        return messages.get(action, "Staffing is optimal.")
    
    def get_peak_hours_recommendation(self, hourly_data: List[Dict]) -> Dict:
        if not hourly_data:
            return {
                'peak_hours': [],
                'off_peak_hours': [],
                'average_people': 0,
                'recommended_staff_schedule': []
            }
        
        counts = [d.get('count', 0) for d in hourly_data]
        avg_count = sum(counts) / len(counts) if counts else 0
        
        peak_threshold = avg_count * 1.5
        
        peak_hours = [hour for hour, count in enumerate(counts) if count >= peak_threshold]
        off_peak_hours = [hour for hour, count in enumerate(counts) if count < avg_count]
        
        schedule = []
        for hour, count in enumerate(counts):
            optimal = self._calculate_optimal_staff(count)
            schedule.append({
                'hour': hour,
                'expected_count': count,
                'recommended_staff': optimal
            })
        
        return {
            'peak_hours': peak_hours,
            'off_peak_hours': off_peak_hours,
            'average_people': round(avg_count, 1),
            'recommended_staff_schedule': schedule
        }
    
    def get_efficiency_metrics(self, queue_count: int, service_time_avg: float) -> Dict:
        if queue_count == 0:
            efficiency = 100
        elif service_time_avg <= 0:
            efficiency = 50
        else:
            ideal_time = queue_count * 2
            actual_time = service_time_avg
            efficiency = min(100, (ideal_time / actual_time) * 100) if actual_time > 0 else 100
        
        return {
            'current_efficiency': round(efficiency, 1),
            'service_rate': round(service_time_avg / 60, 1),
            'arrival_rate': round(queue_count / 10, 1),
            'status': 'OPTIMAL' if efficiency >= 80 else 'NEEDS_IMPROVEMENT'
        }
