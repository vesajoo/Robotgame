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
score = 0

#Colors
WHITE = (255,255,255)
BG = (35,15,0)
PLATFORM = (100, 100 ,0)

#Images
robot_image = pygame.image.load('robot.png').convert_alpha()
platform_image = pygame.image.load('door.png').convert_alpha()

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

        # Gravity
        if self.gravity:
            self.vel_y += GRAVITY
            dy += self.vel_y

        #Check that player doesnt go off the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        #Check collision with platforms
        for platform in platform_group:
            #Collision in y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #Check if above the platform
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.vel_y = 0
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.gravity = False
                        #Move player with platform if it is moving
                        if platform.moving:
                            dx += platform.direction * platform.speed
                        if key[pygame.K_SPACE]:
                            self.vel_y = -20
                            self.gravity = True
            else:
                self.gravity = True
        
        #Check if player bounced to top of screen
        if self.rect.top <= SCROLL_THRESH:
            #If player is jumping
            if self.vel_y < 0:
                scroll = -dy

        #Update rect position
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
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1, 3)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        #Move platform from side to side if it is a moving platform
        if self.moving == True:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed
        #Change direction if it has moved fully
        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
            self.move_counter = 0
        #Update vertical position
        self.rect.y += scroll
        #Check if platform has gone off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

#Player instance
robot = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)

#Sprite groups
platform_group = pygame.sprite.Group()

#Starting platform
platform = Platform(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50, 200, False)
platform_group.add(platform)

#Game loop
while True:

    clock.tick(FPS)

    scroll = robot.move()

    draw_bg()

    #Generate platforms
    if len(platform_group) < MAX_PLATFORMS:
        p_w = random.randint(60, 80)
        p_x = random.randint(0, SCREEN_WIDTH - p_w)
        p_y = platform.rect.y - random.randint(100, 120)
        p_type = random.randint(1, 2)
        if p_type == 1 and score > 1000:
            p_moving = True
        else:
            p_moving = False
        platform = Platform(p_x, p_y, p_w, p_moving)
        platform_group.add(platform)

    #Update platforms
    platform_group.update(scroll)

    #Update score
    if scroll > 0:
        score += scroll

    #Draw sprites
    platform_group.draw(screen)
    robot.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    pygame.display.update()