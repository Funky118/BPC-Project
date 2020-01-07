# Serial communication over RS232 betweem a PC and a graphical interface
# Authors: Dominik Ricanek
#          Prokop Tkadlec
import time
import serial

game_x_size = 700
game_y_size = 500
WHITE = 0xffff
BLACK = 0x0000

# Splits a hex number into its upper and lower bytes
def bytes(intr):
    return divmod(intr, 0x100)

class SPI:
    
    def __init__(self, port_name = 'COM3', baudrate = 115200 ):

        self.comm = serial.Serial()

        self.comm.port = port_name
        self.comm.baudrate = baudrate
        # Set a timeout between individial bytes
        self.comm.inter_byte_timeout = 0.001

        self.packet_size = 16
    # Open the communication channel
    def open(self):
        self.comm.open()

    # Close the channel
    def close(self):
        self.comm.close()

    # Set up the packet parameters
    def set_packet_params(self, packet_size, inter_byte_timeout):
        self.packet_size = packet_size
        self.comm.inter_byte_timeout = inter_byte_timeout

    # Send a packet of data and avaluate the answer
    def send_packet(self, packet):
        # Flush before anything to avoid making a mess on the buffer
        self.comm.flushInput()
        self.comm.flushOutput()

        try:
            packet = packet.decode()
        except(UnicodeDecodeError, AttributeError):
            print('Bytearray undecodable!')
            return -1
        
        if len(packet) != self.packet_size:
            print('Wrong packet size!')
            return -1

        # Packet is a bytearray, no need to Process the packet into a string

        # Send the packet and read the graphical interface response
        self.comm.write(parameters)
        answer = b' '
        print(self.comm.inWaiting())
        if self.comm.inWaiting() > 0:
            answer = self.comm.read(self.comm.inWaiting())
        
        if answer == b'N':
            print('Chyba pri prenosu!')
            return -1
        elif answer == b'A':
            pass
            #do nothing, communication was succesful
        else:
            print('Unknown acknowladge!')
            return -2

class RS232(SPI):
    
    def __init__(self, size_x = 0, size_y = 0, port_name = 'COM3', baudrate = 115200):
        super().__init__(port_name, baudrate)
        self.size_x = size_x
        self.size_y = size_y
        self.relative_x = size_x/game_x_size
        self.relative_y = size_y/game_y_size
        self.middle_x = round(size_x/2)
        self.middle_y = round(size_y/2)

    def vline(self, x, y1, y2, color):
        
        packet = bytearray([
                            0x3,
                            bytes(x)[0], bytes(x)[1],
                            bytes(y1)[0], bytes(y1)[1],
                            bytes(y2)[0], bytes(y2)[1],
                            bytes(color)[0], bytes(color)[1],
                            0, 0, 0, 0, 0, 0,
                            0x55
                           ])
        print(packet)
        print(self.send_packet(packet))

    def rectfill(self, x1, y1, x2, y2, color):

        packet = bytearray([
                            0x3,
                            bytes(x1)[0], bytes(x1)[1],
                            bytes(y1)[0], bytes(y1)[1],
                            bytes(x2)[0], bytes(x2)[1],
                            bytes(y2)[0], bytes(y2)[1],
                            bytes(color)[0], bytes(color)[1],
                            0, 0, 0, 0,
                            0x55
                           ])
        print(packet)
        print(self.send_packet(packet))

    def circlefill(self, x, y, radius, color):
        
        packet = bytearray([
                            0x3,
                            bytes(x)[0], bytes(x)[1],
                            bytes(y)[0], bytes(y)[1],
                            bytes(radius)[0], bytes(radius)[1],
                            bytes(color)[0], bytes(color)[1],
                            0, 0, 0, 0, 0, 0,
                            0x55
                           ])
        print(packet)
        print(self.send_packet(packet))

    def clear(self):
        # Delete the entire screen
        pass
        

class ping_pong(RS232):
    def __init__(self, relative_player_position = 0, fps = 30, size_x = 0, size_y = 0, port_name = 'COM3', baudrate = 115200):
        super().__init__(size_x, size_y, port_name, baudrate)
        self.fps = fps
        # Starting position of player bats and the ball
        self.player0_pos = [ int(0+0.01*relative_player_position), self.middle_y]
        self.player1_pos = [ int(self.size_x-0.01*relative_player_position), self.middle_y]
        self.ball_pos = [self.middle_x, self.middle_y]
        # Used in refresh method
        self.ball_prev_pos = [self.middle_x, self.middle_y]
        
    def update_player0(self, pos_y):
        self.player0_pos[1] += int(self.relative_y*pos_y)
        
    def update_player1(self,pos_y):
        self.player1_pos[1] += int(self.relative_y*pos_y)

    def update_ball(self, pos_x, pos_y):
        self.ball_prev_pos = self.ball_pos.copy()
        self.ball_pos[0] += int(self.relative_y*pos_x)
        self.ball_pos[1] += int(self.relative_y*pos_y)
        
    def draw_net(self):
        self.vline(self.middle_x, 0, self.size_y, WHITE)
    
    def game_start(self):
        # Draw some cool shit a the game start
        pass

    def draw_game(self):
        # Draw the player0 on the console relative to the game screen
        self.rectfill(
                      self.player0_pos[0], self.player0_pos[1]-int(self.relative_y*50),
                      self.player0_pos[0]+int(self.relative_x*10),self.player0_pos[1]+int(self.relative_y*50),
                      WHITE)
        # Draw the player1 on the console relative to the game screen
        self.rectfill(
                      self.player1_pos[0], self.player1_pos[1]-int(self.relative_y*50),
                      self.player1_pos[0]-int(self.relative_x*10),self.player1_pos[1]+int(self.relative_y*50),
                      WHITE)

        # Draw ball
        self.circlefill(
                        self.ball_pos[0],
                        self.ball_pos[1],
                        #it would be an ellipse on disproportunate constole settings, so fuck it
                        int(self.relative_x*5),
                        WHITE)

                        
    def refresh(self):
        # Round up coords of the middle of the screen
        # Draw a line down the middle
        # Draw two black rectangles on either side
        # Draw a black dot on balls position
        pass
#TODO:
    # Import and implement CRC check
        # Always 0x6C
    # Test on arduino
    # Flush the buffer when getting ACK
    # Change decode to byte.fromhex()
