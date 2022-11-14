from RSFSJTN01 import RSFSJTN01
from BME280Reader import BME280Reader
from Wifi import Wifi
from NtpClient import NtpClient
from picozero import pico_temp_sensor
import socket

class WeatherServer:
    def __init__(self, ntp_host, port, bme280_sda, bme280_scl, wind_speed_pin):
        # Connect to Wifi
        self.wifi_connection = Wifi()
        self.ip = self.wifi_connection.connect()
        # Set the time from the provided NTP server
        self.ntp_host = ntp_host
        self.ntp_client = NtpClient(self.ntp_host)
        # Set the listening port for incoming requests
        self.port = port
        # Set up the BME280
        self.bme280_sda = bme280_sda
        self.bme280_scl = bme280_scl
        self.bme280_reader = BME280Reader(self.bme280_sda, self.bme280_scl)
        # Set up the wind speed detector
        self.wind_speed_pin = wind_speed_pin
        self.wind_speed_sensor = RSFSJTN01(self.wind_speed_pin)
        # Set up the internal server
        address = (self.ip, self.port)
        self.connection = socket.socket()
        self.connection.bind(address)
        self.connection.listen(1)
        
    def get_data(self):
        pico_temp = pico_temp_sensor.temp
        (temp,pressure,humidity) = self.bme280_reader.get_values()
        wind_speed = self.wind_speed_sensor.get_wind_speed()
        #Template JSON
        data = f"""{{
"pico_temperature": "{pico_temp}",
"temperature": "{temp}",
"pressure": "{pressure}",
"humidity": "{humidity}",
"wind_speed": "{wind_speed}"
}}"""
        response = f"""HTTP/1.1 200 OK
Content-Type: application/json; encoding=utf8
Content-Length: {len(data)}

{data}"""
        print(response)
        return str(response)
        
    def serve(self):
        while True:
            print(self.connection)
            client = self.connection.accept()[0]
            print(client)
            request = client.recv(1024)
            request = str(request)
            print(request)
            try:
                request = request.split()[1]
                print(request)
            except IndexError:
                pass
            client.send(self.get_data())
            client.close()
            
# Use to test
if __name__ == "__main__":
    try:
        weather_server = WeatherServer('pool.ntp.org', 80, 20, 21, 2)
        while True:
            weather_server.serve()
    except KeyboardInterrupt:
        machine.reset()