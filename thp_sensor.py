# Ignore warnings in VS Code
# type: ignore

import board
import busio
import time

from adafruit_bme280 import basic as adafruit_bme280

class ThpSensor():
    def __init__(self, offsetSeconds):
        self.offset = offsetSeconds
        
        # Create a sensor object using the board's default I2C bus
        self.i2c = busio.I2C(board.GP1, board.GP0)
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(self.i2c)
        
        # Set the location's pressure (hPa) at sea level
        self.bme280.sea_level_pressure = 1013.25
    
    
    def get_temperature_f(self):
        return self.bme280.temperature * 1.8 + 32
    
    
    def get_temperature_c(self):
        return self.bme280.temperature
    
    
    def get_humidity(self):
        return self.bme280.relative_humidity
    
    
    def get_pressure(self):
        return self.bme280.pressure
    
    
    def get_altitude(self):
        return self.bme280.altitude
    
    
    def format_time(self, datetime):
        return "{:04}-{:02}-{:02}T{:02}:{:02}:{:02}.000+00:00".format(
            datetime.tm_year,
            datetime.tm_mon,
            datetime.tm_mday,
            datetime.tm_hour,
            datetime.tm_min,
            datetime.tm_sec
        )
    
    
    def generate_telemetry(self):
        utc_timestamp = int(time.time() + self.offset)
        formatted_timestamp = self.format_time(time.localtime(utc_timestamp))
        return [
            {
                "Timestamp": formatted_timestamp,
                "Key": "temperature",
                "Value": self.get_temperature_f()
            },
            {
                "Timestamp": formatted_timestamp,
                "Key": "humidity",
                "Value": self.get_humidity()
            }
        ]