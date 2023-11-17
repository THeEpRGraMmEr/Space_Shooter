# IMPORT LIBS
import pygame
import pygame.locals
import sys
import random

pygame.init()

# SCREEN AND SIZE
W, H = 600, 700
SCREEN = pygame.display.set_mode((W, H))
pygame.display.set_caption("Space_Shooter")

# CLOCK AND FRAMES
clock = pygame.time.Clock()
fps = 60

# COMMON COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Score
score = 0

# LOADING BACKGROUND
BG_0 = pygame.image.load(r"objects\space.jpg")
BG_1 = pygame.image.load(r"objects\space.jpg")

# LOADING LULU
LULU_for_BG = pygame.image.load(r"objects\bg_lulu.png")
LULU_for_BG.convert()
alien = pygame.image.load(r"objects\shipBlue_manned.png")
pygame.display.set_icon(alien)

# sounds
fire_sound = pygame.mixer.Sound(r"sounds\fire.ogg")
Space_sound = pygame.mixer.music.load(r"sounds\space_sound.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

# RUNNING
RUNNING = True

# BG CORDINATES
bg_x, bg_y = 0, 0
bg_x1, bg_y1 = 0, -H

# LULU_BG cordinates
bg_lulu_x = W/2 - LULU_for_BG.get_width()/2
bg_lulu_y = H/2 - LULU_for_BG.get_height()/2

# LULU PARAMETERS
alien_width, alien_height = 50, 50
alien_speed = 3
no_of_aliens = 10
aliens = []
aliens_speed = []
alien_Bullets = []

# SHIP PARAMETERS
space_ship = pygame.image.load(r"objects\ship.png")
space_ship_width, space_ship_height = 60, 60
space_ship = pygame.transform.scale(space_ship, (space_ship_width, space_ship_height))
space_ship.convert()
space_ship.set_colorkey(WHITE)
space_ship_rect = space_ship.get_rect()
space_ship_rect.center = (W/2 , H - space_ship_height/2)
changex = 0

# DEFINING THE FIRE MOVEMENT
firing_ammo = []
firing_ammo_rect = []
change_speed = 0
index = 0
no_of_bullets = 20


# BACKGROUND LOOP 
def BG_Loop(bg):
    SCREEN.fill(BLACK)
    global bg_y, bg_x, bg_y1, bg_x1
    if bg_y >= H:
        bg_y = (-BG_1.get_height())
    bg_y += 1
    SCREEN.blit(BG_0, (bg_x, bg_y))
    if bg_y1 > H:
        bg_y1 = (-BG_0.get_height())
    bg_y1 += 1
    SCREEN.blit(bg, (bg_x1, bg_y1))
    SCREEN.blit(LULU_for_BG, (bg_lulu_x, bg_lulu_y))

# Draw Text Function
def draw_text(surface, text, color, x, y, font_size):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x), (y)
    surface.blit(text_surface, text_rect)
            
# DEFINING MULTIPLE LULUS
for i in range(no_of_aliens):
    alien = pygame.image.load(r"objects\shipBlue_manned.png")
    alien = pygame.transform.scale(alien, (alien_width, alien_height))
    alien.convert()
    alien_rect = alien.get_rect()
    alien_rect.center = (random.randint(alien_width, W-alien_width), random.randint(-H * 3, 0))
    aliens.append(alien_rect) 
    alien_speed = random.randint(2, 4)
    aliens_speed.append(alien_speed)
    
# fire images
for i in range(no_of_bullets):
    fire = pygame.image.load(r"objects\fire.png")
    fire_width, fire_height = 20, 20
    fire = pygame.transform.scale(fire, (fire_width, fire_height))
    fire.convert
    fire.set_colorkey(WHITE)
    fire_rect = fire.get_rect()
    fire_rect.x = -fire_width
    firing_ammo_rect.append(fire_rect)
    firing_ammo.append(fire)

 # MAIN LOOP 
while RUNNING:
    # Background Loop
    BG_Loop(BG_0)
    
    # LULU'S movements
    for i in range(no_of_aliens):
        aliens[i].y += aliens_speed[i]
        
        if aliens[i].y >= H:
            aliens[i].x = random.randint(0, W - alien_width)
            aliens[i].y = random.randint(-H * 3, -alien_height)
    
        if aliens[i].colliderect(space_ship_rect):
            RUNNING = False

        for j in range(no_of_bullets):
            if aliens[i].colliderect(firing_ammo_rect[j]):
                aliens[i].x = random.randint(0, W - alien_width)
                aliens[i].y = random.randint(-H * 3, -alien_height)
                firing_ammo_rect[j].centerx = -fire_width
                score += 1
        SCREEN.blit(alien, aliens[i])       

    # EVENT-FOR LOOP
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                changex += 5
            if event.key == pygame.K_LEFT:
                changex -= 5
            if event.key == pygame.K_SPACE:
                change_speed = 3
                index += 1
                index %= len(firing_ammo_rect)
                firing_ammo_rect[index].center = space_ship_rect.center
                fire_sound.play()
                fire_sound.set_volume(0.5)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                changex = 0
            if event.key == pygame.K_LEFT: 
                changex = 0
        
    # SPACESHIP MOVEMENT
    space_ship_rect.centerx += changex
    if space_ship_rect.right >= W:
        changex = 0
    if space_ship_rect.left <= 0:
        changex = 0
    
    # FIRING POSITION UPDATE
    firing_ammo_rect[index].centery -= change_speed
    for i in range(no_of_bullets):
        firing_ammo_rect[i].centery -= change_speed
        for j in range(no_of_bullets):
            if firing_ammo_rect[i].centery <= 0:
                firing_ammo_rect[i].centerx = -fire_width 
            SCREEN.blit(firing_ammo[i], firing_ammo_rect[j])
    
    # UPDATING fps 
    if score >= 20:
        fps += 0.008
    SCREEN.blit(space_ship, space_ship_rect)
    draw_text(surface=SCREEN, text= f"score: {score}", color=WHITE,  x=45 , y=10, font_size=30)
    
    pygame.display.flip()
    clock.tick(fps)