import network
import socket
import time
import struct

class NtpClient:
    def __init__(self, ntp_host):
        self.host = ntp_host
        self.NTP_DELTA = 2208988800
        
    def set_time(self):
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1B
        addr = socket.getaddrinfo(self.host, 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.settimeout(1)
            res = s.sendto(NTP_QUERY, addr)
            msg = s.recv(48)
        finally:
            s.close()
        val = struct.unpack("!I", msg[40:44])[0]
        t = val - self.NTP_DELTA    
        tm = time.gmtime(t)
        machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))

if __name__ == "__main__":
    from Wifi import Wifi
    wifi_connection = Wifi()
    ip_address = wifi_connection.connect()
    print(f'Current time: {time.localtime()}')
    ntp_client = NtpClient('pool.ntp.org')
    ntp_client.set_time()
    print(f'Current time: {time.localtime()}')
    