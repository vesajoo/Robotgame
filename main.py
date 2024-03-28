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
BG = (35,15,0)
PLATFORM = (100, 100 ,0)

#Images
robot_image = pygame.image.load('robot.png').convert_alpha()

#Draw background
def draw_bg():
    pygame.draw.rect(screen, BG, (0,0,SCREEN_WIDTH, SCREEN_HEIGHT))

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
        #Reset variables
        scroll = 0
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx = -10
        
        if key[pygame.K_RIGHT]:
            dx = 10

        #Gravity
        if self.gravity:
            self.vel_y += GRAVITY
            dy += self.vel_y

        #Check that player doesnt go off the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

    def draw(self):
        screen.blit(self.image, (self.rect.x-5, self.rect.y))
        pygame.draw.rect(screen,WHITE,self.rect, 2)


#Platfrom class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.moving = moving
        



#Player instance
robot = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
#Starting platform


#Game loop
while True:

    clock.tick(FPS)

    robot.move()

    draw_bg()

    robot.draw()

    platform = pygame.draw.rect(screen, PLATFORM, (SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT- 10, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100), 5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    pygame.display.update()