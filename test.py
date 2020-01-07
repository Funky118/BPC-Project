import serial
import time

BLACK = 0
WHITE = 0xff

def Refresh():
    pass

# Setting up the port variables
ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM6'
#ser.rtscts = True
#ser.dsrdtr = True
#ser.xonxoff = True
ser.inter_byte_timeout = 0.001
ser.open()

# Test packet
#packet = bytes.fromhex('02002000200060ffff00000000000055')
offset = 0;
packet = bytearray([2, 0, (0x20+offset), 0, 0x20,(0x0060+offset), WHITE, WHITE, 0, 0, 0, 0, 0, 0, 0x55])
prev_packet = bytearray([2, 0, (0x20+offset), 0, 0x20,(0x0060+offset), BLACK, BLACK, 0, 0, 0, 0, 0, 0, 0x55])
for i in range(60):
    ser.write(packet)
    ser.read(ser.inWaiting())
    offset += 10
    packet = bytearray([2, 0, (0x20+offset), 0, 0x20,(0x0060+offset), WHITE, WHITE, 0, 0, 0, 0, 0, 0, 0x55])
    time.sleep(0.1)
    ser.write(prev_packet)
    ser.read(ser.inWaiting())
    prev_packet = bytearray([2, 0, (0x20+offset), 0, 0x20,(0x0060+offset), BLACK, BLACK, 0, 0, 0, 0, 0, 0, 0x55])
    
    
# Write the packet
#ser.write(packet)
print(ser.inWaiting())









# Garbo: 
#   bytes.fromhex('02002000200060ffff00000000000055')
