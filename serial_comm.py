# Serial communication over RS232 betweem a PC and a graphical interface
# Authors: Dominik Ricanek
#          Prokop Tkadlec

import serial

class channel:
    
    def __init__(self, port_name = 'COM3', baudrate = 9600 ):

        self.comm = serial.Serial()

        self.comm.port(port_name)
        self.comm.baudrate(baudrate)

        self.packet_size = 16
        self.end = '55'
    # Open the communication channel
    def open(self):
        self.comm.open()

    # Close the channel
    def close(self):
        self.comm.close()

    # Set up the packet parameters
    def set_params(self, packet_size, end):
        self.packet_size = packet_size
        self.end = end

    # Send a packet of data and avaluate the answer
    def send_packet(self, packet):
        if len(packet) != self.packet_size:
            print('Wrong packet size!')
            return 0

        # Process the packet into a string
        string = packet.decode('hex')

        command = string[0]
        parameters = string[1:]
        end_sign = '55'.decode('hex')

        # Send the packet and read the graphical interface response
        self.comm.write(command + parameters + end_sign)
        if self.comm.inWaiting() > 0:
            answer = self.comm.read(1)
        
        if answer == 'N':
            print('Chyba pri prenosu!')
        elif answer == 'A':
            pass
            #do nothing, communication was succesful
        else:
            print('Unknown acknowladge!')