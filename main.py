# Complete your game here
#Imports
import pygame
import random

pygame.init()

#Window dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

#Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('MOOC 14')

#Framerate
clock = pygame.time.Clock()
FPS = 60

#Game variables
SCROLL_THRESH = 200
GRAVITY = 1
MAX_PLATFORMS = 10
scroll = 0


#Colors
WHITE = (255,255,255)

#Images
robot_image = pygame.image.load('robot.png')

#Player class
class Player():
    def __init__(self, x ,y) -> None:
        self.image = robot_image
        self.width = 40
        self.height = 84
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = (x,y)
        self.vel_y = 0
        self.gravity = True

    def move(self):
        scroll = 0
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx = -10
        
        if key[pygame.K_RIGHT]:
            dx = 10

        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(self.image, (self.rect.x-5, self.rect.y))
        pygame.draw.rect(screen,WHITE,self.rect, 2)

#Player instance
robot = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

#Game loop
while True:

    clock.tick(FPS)
    
    robot.move()

    robot.draw()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    pygame.display.update()