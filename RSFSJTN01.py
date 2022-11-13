from machine import Pin
import time
import _thread

class RSFSJTN01:
    def __init__(self, input_pin_number):
        self.wind_speed = 0
        self.count = 0
        self.input_pin_number = input_pin_number
        _thread.start_new_thread(self.reset_thread, ())
        self.input_pin = Pin(self.input_pin_number, Pin.IN, Pin.PULL_DOWN)
        self.input_pin.irq(trigger=Pin.IRQ_FALLING, handler=self.pulse_detected)
    
    def pulse_detected(self,p):
        self.count = self.count + 1

    def reset_thread(self):
        while True:
            # convert number of clicks to m/s (* 8.75 to get cm/s, divide by 100 to get m/s)
            # then convert to mph where 1m/s = 2.23694mph
            self.wind_speed = ((self.count * 8.75) / 100) * 2.23694
            self.count = 0
            time.sleep(1)
        
    def get_wind_speed(self):
        return self.wind_speed
    
# This can be used to test the class. Spin up an instance and call it every second to get wind speed
if __name__ == "__main__":
    device = RSFSJTN01(2)
    while True:
        print(f'Returned wind speed: {device.get_wind_speed()}mph')
        time.sleep(1)