import pygame
from random import randint
from serial_comm import ping_pong
BLACK = (0,0,0)

class Ball(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
 
        # Draw the ball (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.velocity = [randint(2,4),randint(-4,4)]
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]


    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-4,4)

    def update_console(self, ping_pong):
        ping_pong.update_ball(self.velocity[0], self.velocity[1])


