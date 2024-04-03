# Jump from platform to platform while a ghost is chasing you
# Use arrow keys to move and space to jump

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
game_over = False
fade_counter = 0
high_score = 0
game_info = True

#Colors
WHITE = (255,255,255)
BG = (31,31,31)
PLATFORM = (100, 100 ,0)
BLACK = (0,0,0)

#Define fonts
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)

#Images
robot_image = pygame.image.load('robot.png').convert_alpha()
platform_image = pygame.image.load('door.png').convert_alpha()
monster_image = pygame.image.load('monster.png').convert_alpha()

#Function for outputting text on screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    text_rect = img.get_rect(center=(SCREEN_WIDTH // 2, y))
    screen.blit(img, text_rect)

#Function for drawing info panel
def draw_panel():
    pygame.draw.rect(screen, BLACK, (0,0,SCREEN_WIDTH, 30))
    pygame.draw.line(screen, WHITE, (0,30), (SCREEN_WIDTH, 30), 2)
    img = font_small.render('SCORE: ' + str(score), True, WHITE)
    screen.blit(img, (0,0))

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
        #Check collission with enemy
        for enemy in enemy_group:
            if enemy.rect.colliderect(self.rect):
                #Ghosts pushes the player down the platform if it collides with the player
                dy += 5
        
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

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = monster_image
        self.width = 40
        self.height = 84
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.direction = random.choice([-1, 1])
        if self.direction == 1:
            self.rect.center = (SCREEN_WIDTH, SCREEN_HEIGHT + 50)
        else:
            self.rect.center = (0, SCREEN_HEIGHT + 50)

    #Ghost chaces the player
    def update(self, scroll):
        self.rect.y += scroll
        if robot.rect.y > self.rect.y:
            self.rect.y += 3
        if robot.rect.x > self.rect.x:
            self.rect.x += 3
        if robot.rect.y < self.rect.y:
            self.rect.y -= 3
        if robot.rect.x < self.rect.x:
            self.rect.x -= 3

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
enemy_group = pygame.sprite.Group()

#Starting platform
platform = Platform(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50, 200, False)
platform_group.add(platform)

#Game loop
while True:

    clock.tick(FPS)

    if game_info:
        pygame.draw.rect(screen, BLACK, (0,0,SCREEN_WIDTH, SCREEN_HEIGHT))
        draw_text('ESCAPE THE HAUNTED CAVE', font_big, WHITE, SCREEN_WIDTH // 2, 220)
        draw_text('USE ARROW KEYS TO MOVE AND SPACE TO JUMP', font_small, WHITE, SCREEN_WIDTH // 2, 275)
        draw_text('PRESS SPACE TO START', font_big, WHITE, SCREEN_WIDTH // 2, 400)

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            game_info = False

    elif game_over == False:

        scroll = robot.move()

        draw_bg()

        #Generate platforms
        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(60, 80)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(95, 105)
            p_type = random.randint(1, 2)
            if p_type == 1 and score > 1000:
                p_moving = True
            else:
                p_moving = False
            platform = Platform(p_x, p_y, p_w, p_moving)
            platform_group.add(platform)

        #Update platforms
        platform_group.update(scroll)

        #Generate enemies
        if score > 0:
            if len(enemy_group) == 0:
                enemy = Enemy()
                enemy_group.add(enemy)

        enemy_group.update(scroll)

        #Update score
        if scroll > 0:
            score += scroll

        #Draw line at previous high score
        if high_score > 0:
            pygame.draw.line(screen, WHITE, (0, score - high_score + SCROLL_THRESH), (SCREEN_WIDTH, score - high_score + SCROLL_THRESH), 3)
            draw_text('HIGH SCORE', font_small, WHITE, SCREEN_WIDTH - 130, score - high_score + SCROLL_THRESH - 20)

        #Draw sprites
        platform_group.draw(screen)
        enemy_group.draw(screen)
        robot.draw()

        #Draw panel
        draw_panel()

        #Check game over
        if robot.rect.top > SCREEN_HEIGHT:
            game_over = True
        
    else:
        if fade_counter < SCREEN_WIDTH:
            fade_counter += 15
            for y in range(0, 6, 2):
                pygame.draw.rect(screen, BLACK, (0, y * 200, fade_counter, 200))
                pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - fade_counter, (y+1) * 200, SCREEN_WIDTH, 200))
        else:
            draw_text('GAME OVER!', font_big, WHITE, SCREEN_WIDTH // 2, 220)
            draw_text('SCORE: ' + str(score), font_big, WHITE, SCREEN_WIDTH // 2, 275)
            draw_text('PRESS SPACE TO PLAY AGAIN', font_big, WHITE, SCREEN_WIDTH // 2, 400)
        #Update high score
        if score > high_score:
            high_score = score

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            #Reset variables
            game_over = False
            scroll = 0
            score = 0
            fade_counter = 0
            #Reposition robot
            robot.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
            #Reset platforms
            platform_group.empty()
            #Reset enemies
            enemy_group.empty()
            #Create starting platform
            platform = Platform(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50, 200, False)
            platform_group.add(platform)    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    pygame.display.update()