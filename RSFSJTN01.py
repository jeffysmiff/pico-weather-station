from machine import Pin
import time
import _thread

class RSFSJTN01:
    def __init__(self, input_pin_number):
        self.wind_speed = 0
        self.count = 0
        self.input_pin_number = input_pin_number
        self.last_time=time.time_ns()
        self.input_pin = Pin(self.input_pin_number, Pin.IN, Pin.PULL_DOWN)
        self.input_pin.irq(trigger=Pin.IRQ_FALLING, handler=self.pulse_detected)
    
    def pulse_detected(self,p):
        self.count = self.count + 1

    def get_wind_speed(self):
        curr_time_ns = time.time_ns()
        # convert ns to s
        time_delta = (curr_time_ns - self.last_time) / 1000000000.0
        # multiply counted pulses by 8.75cm/s and divide by number of secs since last calc
        # then divide by 100 to get m/s and multiply by 2.23694 to get mph
        wind_speed = (((self.count * 8.75) / time_delta ) / 100) * 2.23694
        self.count = 0
        self.last_time = curr_time_ns
        return wind_speed
    
# This can be used to test the class. Spin up an instance and call it every second to get wind speed
if __name__ == "__main__":
    device = RSFSJTN01(2)
    while True:
        time.sleep(1)
        print(f'Returned wind speed: {device.get_wind_speed()}mph')
