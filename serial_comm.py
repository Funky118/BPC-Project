# Serial communication over RS232 betweem a PC and a graphical interface
# Authors: Dominik Ricanek
#          Prokop Tkadlec
import time
import serial

game_x_size = 799
game_y_size = 599
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
        parameters = packet
        #try:
        #packet = packet.decode()
       # except(UnicodeDecodeError, AttributeError):
          #  print('Bytearray undecodable!')
          #  return -1
        
        if len(packet) != self.packet_size:
            print('Wrong packet size!')
            return -1

        # Packet is a bytearray, no need to Process the packet into a string

        # Send the packet and read the graphical interface response
        self.comm.write(parameters)
        answer = b' '
        while self.comm.inWaiting() == 0:
            pass

        if self.comm.inWaiting() > 0:
            answer = self.comm.read(self.comm.inWaiting())
        
        if answer == b'N':
            print('Chyba pri prenosu!')
            return -1
        elif answer == b'A':
            pass
            #do nothing, communication was succesful
        else:
            print('Unknown acknowladge! ' + str(answer))
            return -2

class RS232(SPI):
    
    def __init__(self, size_x = 0, size_y = 0, port_name = 'COM3', baudrate = 115200):
        super().__init__(port_name, baudrate)
        self.size_x = size_x
        self.size_y = size_y
        self.relative_x = game_x_size/size_x
        self.relative_y = game_y_size/size_y
        self.middle_x = round(game_x_size/2)
        self.middle_y = round(game_y_size/2)

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
        #print(packet)
        self.send_packet(packet)

    def rectfill(self, x1, y1, x2, y2, color):

        packet = bytearray([
                            0x5,
                            bytes(x1)[0], bytes(x1)[1],
                            bytes(y1)[0], bytes(y1)[1],
                            bytes(x2)[0], bytes(x2)[1],
                            bytes(y2)[0], bytes(y2)[1],
                            bytes(color)[0], bytes(color)[1],
                            0, 0, 0, 0,
                            0x55
                           ])
        #print(packet)
        self.send_packet(packet)

    def circlefill(self, x, y, radius, color):
        
        packet = bytearray([
                            0x8,
                            bytes(x)[0], bytes(x)[1],
                            bytes(y)[0], bytes(y)[1],
                            bytes(radius)[0], bytes(radius)[1],
                            bytes(color)[0], bytes(color)[1],
                            0, 0, 0, 0, 0, 0,
                            0x55
                           ])
        #print(packet)
        self.send_packet(packet)

    def clear(self):
        self.rectfill(1, 1, game_x_size, game_y_size, BLACK)
        self.vline(800, 0, game_y_size, WHITE)
        self.vline(game_x_size, 0, game_y_size, WHITE)
        self.comm.flushInput()
        self.comm.flushOutput()
        # Delete the entire screen except borders
        

class ping_pong(RS232):
    def __init__(self, relative_player_position = 0, fps = 30, size_x = 0, size_y = 0, port_name = 'COM3', baudrate = 115200):
        super().__init__(size_x, size_y, port_name, baudrate)
        self.fps = fps
        # Starting position of player bats and the ball (x is 1 because of monitor limitations)
        self.player0_pos = [ int(1+0.01*relative_player_position), self.middle_y]
        self.player1_pos = [ int(-1+game_x_size-0.01*relative_player_position), self.middle_y]
        self.ball_pos = [self.middle_x, self.middle_y]
        # Used in refresh method
        self.ball_prev_pos = [self.middle_x, self.middle_y]
        
    def update_player0(self, pos_y):
        self.player0_pos[1] += int(self.relative_y*pos_y)
        
    def update_player1(self,pos_y):
        self.player1_pos[1] += int(self.relative_y*pos_y)

    def update_ball(self, pos_x, pos_y):

        if (int(self.ball_pos[0]*self.relative_x) + int(self.relative_x*pos_x)) < game_x_size and (int(self.ball_pos[0]*self.relative_x) + int(self.relative_x*pos_x)) > 0:
            if (int(self.ball_pos[1]*self.relative_y) + int(self.relative_y*pos_y)) < game_y_size and (int(self.ball_pos[1]*self.relative_y) + int(self.relative_y*pos_y)) > 0:
                self.ball_prev_pos = self.ball_pos.copy()
                self.ball_pos[0] += int(self.relative_x*pos_x)
                self.ball_pos[1] += int(self.relative_y*pos_y)
        
    def draw_net(self):
        self.vline(self.middle_x, 0, game_y_size, WHITE)
    
    
    def draw_player0(self):
        # Refresh the player0 on the console
        self.rectfill(
                      1, 1,
                      int(1+self.relative_x*10),game_y_size,
                      BLACK)

        # Draw the player0 on the console relative to the game screen
        self.rectfill(
                      self.player0_pos[0], self.player0_pos[1]-int(self.relative_y*50),
                      self.player0_pos[0]+int(self.relative_x*10),self.player0_pos[1]+int(self.relative_y*50),
                      WHITE)

    def draw_player1(self):
        # Refresh the player1 on the console
        self.rectfill(
                      game_x_size, 1,
                      -1 + game_x_size - int(self.relative_x*10),game_y_size,
                      BLACK)

        # Draw the player1 on the console relative to the game screen
        self.rectfill(
                      self.player1_pos[0], self.player1_pos[1]-int(self.relative_y*50),
                      self.player1_pos[0]-int(self.relative_x*10),self.player1_pos[1]+int(self.relative_y*50),
                      WHITE)

    def draw_ball(self):
        # Draw the net overlayed by the ball
        self.draw_net()

        # Delete previous ball
        self.circlefill(
                        #self.ball_prev_pos[0],
                        #self.ball_prev_pos[1],
                        int(self.ball_prev_pos[0]*self.relative_x),
                        int(self.ball_prev_pos[1]*self.relative_y),
                        #it would be an ellipse on disproportunate constole settings, so fuck it
                        int(self.relative_x*5),
                        BLACK)

        # Draw ball
        self.circlefill(
                        #self.ball_pos[0],
                        #self.ball_pos[1],
                        int(self.ball_pos[0]*self.relative_x),
                        int(self.ball_pos[1]*self.relative_y),
                        #it would be an ellipse on disproportunate constole settings, so fuck it
                        int(self.relative_x*5),
                        WHITE)

    def game_start(self):
        # Draw some cool shit and start the game!
        self.open()
        self.comm.flushInput()
        self.comm.flushOutput()
        self.clear()
        #time.sleep(1)
        self.draw_player0()
        #time.sleep(1)
        self.draw_player1()
        #time.sleep(1)
        self.draw_ball()
        #time.sleep(1)

#TODO:
    # Round up coords of the middle of the screen
    # Draw a line down the middle
    # Draw two black rectangles on either side
    # Draw a black dot on balls position

#g = ping_pong(0,30,700,500)
#g.game_start()

#for i in range(10):
#    g.update_player1(-5)
#    g.update_player0(5)
 #   g.update_ball(10,20)
 #   g.draw_game()


