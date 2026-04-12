import logging
import time
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlertManager:
    def __init__(self, config: dict):
        self.config = config
        self.led_enabled = config.get('led_enabled', True)
        self.buzzer_enabled = config.get('buzzer_enabled', True)
        self.alert_duration = config.get('alert_duration', 2)
        self.gpio_available = False
        
        self.green_led_pin = 17
        self.red_led_pin = 27
        self.buzzer_pin = 22
        
        self._init_gpio()
        
    def _init_gpio(self):
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            
            GPIO.setup(self.green_led_pin, GPIO.OUT)
            GPIO.setup(self.red_led_pin, GPIO.OUT)
            GPIO.setup(self.buzzer_pin, GPIO.OUT)
            
            GPIO.output(self.green_led_pin, GPIO.LOW)
            GPIO.output(self.red_led_pin, GPIO.LOW)
            GPIO.output(self.buzzer_pin, GPIO.LOW)
            
            self.gpio = GPIO
            self.gpio_available = True
            logger.info("GPIO initialized successfully")
            
        except ImportError:
            logger.warning("RPi.GPIO not available. Running in simulation mode.")
            self.gpio = None
        except Exception as e:
            logger.error(f"Failed to initialize GPIO: {e}")
            self.gpio = None
    
    def set_led(self, color: str, state: bool):
        if not self.led_enabled:
            return
            
        if self.gpio_available and self.gpio:
            try:
                pin = self.green_led_pin if color.lower() == 'green' else self.red_led_pin
                import RPi.GPIO as GPIO
                GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
                logger.debug(f"LED {color}: {'ON' if state else 'OFF'}")
            except Exception as e:
                logger.error(f"Failed to set LED: {e}")
        else:
            logger.debug(f"[SIMULATION] LED {color}: {'ON' if state else 'OFF'}")
    
    def beep(self, duration: float = 0.5):
        if not self.buzzer_enabled:
            return
            
        if self.gpio_available and self.gpio:
            try:
                import RPi.GPIO as GPIO
                GPIO.output(self.buzzer_pin, GPIO.HIGH)
                time.sleep(duration)
                GPIO.output(self.buzzer_pin, GPIO.LOW)
                logger.debug(f"Buzzer beep for {duration}s")
            except Exception as e:
                logger.error(f"Failed to beep buzzer: {e}")
        else:
            logger.debug(f"[SIMULATION] Buzzer beep for {duration}s")
    
    def beep_pattern(self, pattern: list):
        for duration in pattern:
            if duration > 0:
                self.beep(duration)
            time.sleep(abs(duration) if duration != 0 else 0.3)
    
    def alert_queue_high(self):
        logger.warning("HIGH QUEUE ALERT TRIGGERED")
        
        self.set_led('green', False)
        self.set_led('red', True)
        
        self.beep_pattern([0.5, 0.2, 0.5, 0.2, 0.5])
    
    def alert_queue_critical(self):
        logger.error("CRITICAL QUEUE ALERT TRIGGERED")
        
        self.set_led('green', False)
        self.set_led('red', True)
        
        self.beep_pattern([1.0, 0.3, 1.0, 0.3, 1.0])
    
    def alert_queue_normal(self):
        logger.info("Queue status: NORMAL")
        
        self.set_led('red', False)
        self.set_led('green', True)
    
    def alert_queue_low(self):
        logger.info("Queue status: LOW")
        
        self.set_led('red', False)
        self.set_led('green', True)
    
    def system_ready(self):
        self.set_led('green', True)
        self.set_led('red', False)
        logger.info("System ready indicator")
    
    def system_error(self):
        self.set_led('green', False)
        self.set_led('red', True)
        self.beep_pattern([0.1, 0.1, 0.1])
        logger.error("System error indicator")
    
    def cleanup(self):
        if self.gpio_available and self.gpio:
            try:
                import RPi.GPIO as GPIO
                GPIO.cleanup()
                logger.info("GPIO cleaned up")
            except Exception as e:
                logger.error(f"Failed to cleanup GPIO: {e}")
    
    def __del__(self):
        self.cleanup()
