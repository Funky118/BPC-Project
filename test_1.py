import serial
import time

BLACK = 0
WHITE = 0xff

# Setting up the port variables
ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM6'
#ser.rtscts = True
#ser.dsrdtr = True
#ser.xonxoff = True
ser.inter_byte_timeout = 0.001
ser.open()
ser.flushInput()
ser.flushOutput()

# Test packet
#packet = bytes.fromhex('02002000200060ffff00000000000055')
offset = 0
offset2 = 0
playfield = bytearray([4, 0, 0, 0, 0, 0, 0x79, 0, 0x39, WHITE, WHITE, 0, 0, 0, 0, 0x55])

packet = bytearray([8, 0, (0x20+offset), 0, (0x10+offset2), 0, 0x20, WHITE, WHITE, 0, 0, 0, 0, 0, 0, 0x55])
prev_packet = bytearray([8, 0, (0x20+offset), 0, (0x10+offset2), 0, 0x20, BLACK, BLACK, 0, 0, 0, 0, 0, 0, 0x55])
while(0x20+offset2)<255:
    ser.write(playfield)
    ser.read(1)
    ser.write(packet)
    ser.read(ser.inWaiting())
    offset += 10
    packet = bytearray([8, 0, (0x20+offset), 0, (0x10+offset2), 0, 0x20, WHITE, WHITE, 0, 0, 0, 0, 0, 0, 0x55])
    time.sleep(0.01)
    ser.write(prev_packet)
    ser.read(ser.inWaiting())
    prev_packet = bytearray([8, 0, (0x20+offset), 0, (0x10+offset2), 0, 0x20, BLACK, BLACK, 0, 0, 0, 0, 0, 0, 0x55])
    if(0x60+offset)>=255:
        offset = 0
        offset2 += 10
    
# Write the packet
#ser.write(packet)
print(ser.inWaiting())


#Notes:
    #Coordinates need two bytes









# Garbo: 
#   bytes.fromhex('02002000200060ffff00000000000055')
