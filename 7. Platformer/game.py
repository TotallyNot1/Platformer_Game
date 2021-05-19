# Imports
import pygame
import json
import os
import sys
import math

# Window settings
GRID_SIZE = 64
WIDTH = 16 * GRID_SIZE
HEIGHT = 9 * GRID_SIZE
TITLE = "AETHER: THE SEQUEL"
FPS = 60


# Create window
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (0, 150, 255)
LIGHT_GREY = (175, 175, 175)
BLUE_GREY = (41, 55, 67)
GRAY = (220, 220, 220)


# Stages
START = 0
PLAYING = 1
LOSE = 2
LEVEL_COMPLETE = 3

# Load fonts
font_xl = pygame.font.Font(None, 96)
font_lg = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 60)
font_md = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 32)
font_sm = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 24)
font_xs = pygame.font.Font(None, 14)

# Load images
hero_img = pygame.image.load('assets/images/characters/Character.png').convert_alpha()
grass_dirt_img = pygame.image.load('assets/images/tiles/Ground_Block.png').convert_alpha()
block_img = pygame.image.load('assets/images/tiles/Platform_Block.png').convert_alpha()
gem_img = pygame.image.load('assets/images/items/YinYang_Orb.png').convert_alpha()
heart_img = pygame.image.load('assets/images/items/heart.png').convert_alpha()
cloud_img = pygame.image.load('assets/images/characters/Air_Attacker.png').convert_alpha()
spikeball_img = pygame.image.load('assets/images/characters/Enemy.png').convert_alpha()
spikeman_img = pygame.image.load('assets/images/characters/Test#2.png').convert_alpha()
laser_img = pygame.image.load('assets/images/characters/Laser.png').convert_alpha()
flag_img = pygame.image.load('assets/images/tiles/Top.png').convert_alpha()
pole_img = pygame.image.load('assets/images/tiles/Base.png').convert_alpha()
traps_img = pygame.image.load('assets/images/characters/Bomb_img.png').convert_alpha()
# Load sounds
laser_snd = pygame.mixer.Sound('assets/sounds/Laser.wav')

#Music
start_music = 'assets/music/theme2.wav'
stage_theme = 'assets/music/Metal_Empire.wav'
victory_theme = 'assets/music/Credits_theme.wav'
lose_music = 'assets/music/Pyramid_Dance.wav'
# Game classes
class Entity(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()
        
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.centerx = x * GRID_SIZE + GRID_SIZE// 2
        self.rect.centery = y * GRID_SIZE + GRID_SIZE// 2

        self.vx = 0
        self.vy = 0
        
    def apply_gravity(self):
        self.vy += gravity

        if self.vy > terminal_velocity:
            self.vy = terminal_velocity
        
class Hero(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        #self.vx = self.speed
        self.speed = 5
        self.jump_power = 15
        self.vx = 0
        self.vy = 0

        self.hearts = 3
        self.gems = 0
        self.score = 0
        self.hurt_timer = 0
        self.shoot_clock = 0
        
    def move_to(self, x, y):
        self.rect.centerx = x * GRID_SIZE + GRID_SIZE // 2
        self.rect.centery = y * GRID_SIZE + GRID_SIZE // 2
        
    def move_right(self):
        
        self.vx = self.speed
    	
    def move_left(self):
        self.vx = -1 * self.speed
        
    def stop(self):
        self.vx = 0 
    
    def jump(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2
        if len(hits) > 0:
            self.vy = -1 * self.jump_power
            
    def shoot(self):
        if self.shoot_clock <= 0:
            laser = Laser(laser_img)
            bullet.rect.centerx = self.rect.centerx
            bullet.rect.centery = self.rect.centery
            laser.theta = laser.find_theta(self)
            self.lasers.add(laser)
                        
            self.shoot_clock = 20

            laser_snd.play()
            
    '''def apply_momentum(self):
        self.vx += momentum
        
        if self.vx > friction:
            self.vx = friction'''
    
    def check_enemies(self):
        hits = pygame.sprite.spritecollide(self, enemies, False)

        for enemy in hits:
            if self.hurt_timer ==0:
                self.hearts -= 1
                self.hurt_timer = 1.0 * FPS
                print(self.hearts)
                print("oof!")
                
            if self.rect.x < enemy.rect.x:
                self.rect.right = enemy.rect.left
            elif self.rect.x > enemy.rect.x:
                self.rect.left = enemy.rect.right

            if self.rect.y < enemy.rect.y:
                self.rect.bottom = enemy.rect.top
            elif self.rect.y > enemy.rect.y:
                self.rect.bottom = enemy.rect.top

        if self.hurt_timer > 0:
            self.hurt_timer -= 1

            if self.hurt_timer < 0:
                self.hurt_timer = 0
            
    def move_and_check_platforms(self):
        self.rect.x += self.vx

        hits = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hits:
            if self.vx > 0:
                self.rect.right = hit.rect.left
                
            if self.vx < 0:
                self.rect.left = hit.rect.right
                
        self.rect.y += self.vy
        
        hits = pygame.sprite.spritecollide(self, platforms, False)
        
        for hit in hits:
            if self.vy > 0:
                self.rect.bottom = hit.rect.top
            elif self.vy < 0:
                self.rect.top = hit.rect.bottom
            self.vy = 0
                
    def check_world_edges(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > world_width:
            self.rect.right = world_width

    def check_items(self):
        hits = pygame.sprite.spritecollide(self, items, True)

        for item in hits:
            item.apply(self)
    def reached_goal(self):
        return pygame.sprite.spritecollideany(self, goal)
                
    def update(self):
        self.apply_gravity()
        self.move_and_check_platforms()
        self.check_world_edges()
        self.check_items()
        self.check_enemies()
        self.reached_goal()

        self.shoot_clock -= 1

        
class Laser(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.speed = 30
        self.theta = None
        self.dis_dis = None
        self.velocity = []

    def shoot(self):
        SHOOT_SOUND.play()

    def find_theta(self, hero):
        offset_x, offset_y = game.calculate_offset()
        pos = pygame.mouse.get_pos()
        dis_x = (pos[0] + (-1*offset_x)) - self.rect.centerx
        dis_y = pos[1] - self.rect.centery
        self.dis_dis = math.sqrt((dis_x**2 + dis_y**2))

        self.theta = math.asin(dis_y/self.dis_dis)

        self.find_velocity(hero)

    def find_velocity(self, hero):
        if not hero.facing_right:
            vx = math.cos(self.theta) * -1 * self.speed
        else:
            vx = math.cos(self.theta) * self.speed
        vy = math.sin(self.theta) * self.speed
        self.velocity = [vx, vy]

    def check_walls_and_blocks(self):
        hit_list = pygame.sprite.spritecollide(self, level.main_tiles, False)

        for hit in hit_list:
            if self.velocity[0] > 0:
                self.kill()
            elif self.velocity[0] < 0:
                self.kill()
            self.velocity[0] = 0

        hit_list = pygame.sprite.spritecollide(self, level.main_tiles, False)

        for hit in hit_list:
            if self.velocity[1] > 0:
                self.kill()
            elif self.velocity[1] < 0:
                self.kill()
                self.velocity[1] = 0


    def update(self, level):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        self.check_walls_and_blocks(level)

        if self.rect.left > level.width or self.rect.right < 0:
            self.kill()

        
class Platform(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        
        
class Gem(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        
    def apply(self, character):
        character.gems += 1
        character.score += 10
        print(character.gems)
        
        
class Enemy(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.vx = -2
        self.vy = 0
        self.heart = 2

    def reverse (self):
        self.vx *= -1
        
    def move_and_check_platforms(self):
        self.rect.x += self.vx

        hits = pygame.sprite.spritecollide(self, platforms, False)
        must_reverse = False
        for hit in hits:
            if self.vx > 0:
                self.rect.right = hit.rect.left
                must_reverse = True
            if self.vx < 0:
                self.rect.left = hit.rect.right
                must_reverse = True
                
        if must_reverse:
            self.reverse()
            
        self.rect.y += self.vy
        
        hits = pygame.sprite.spritecollide(self, platforms, False)
        
        for hit in hits:
            if self.vy > 0:
                self.rect.bottom = hit.rect.top
            elif self.vy < 0:
                self.rect.top = hit.rect.bottom
                
            self.vy = 0
            
    def check_world_edges(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.reverse()
        elif self.rect.right > world_width:
            self.rect.right = world_width
            self.reverse()
            
    def check_platform_edges(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2
        
        must_reverse = True
        
        for platform in hits:
            if self.vx < 0 and platform.rect.left <= self.rect.left:
                must_reverse = False
            elif self.vx > 0 and platform.rect.right >= self.rect.right:
                must_reverse = False

        if must_reverse:
            self.reverse()

    def check_lasers(self, lasers):
        hit_list = pygame.sprite.spritecollide(self, lasers, True)
        for hit in hit_list:
            self.kill()
            
class Spikeball(Enemy):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        
        self.heart = 2
    def update(self):
        hits = pygame.sprite.spritecollide(self, lasers, True)

        for laser in hits:
          self.heart -= 1

        if self.heart <= 0:
            self.kill()
            
        self.apply_gravity()
        self.move_and_check_platforms()
        self.check_world_edges()
        self.check_lasers

class Spikeman(Enemy):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.heart = 2
    def update(self):
        hits = pygame.sprite.spritecollide(self, lasers, True)

        for laser in hits:
          self.heart -= 1

        if self.heart <= 0:
            self.kill()
            
        self.apply_gravity()
        self.move_and_check_platforms()
        self.check_world_edges()
        self.check_platform_edges()
        self.check_lasers

class Cloud(Enemy):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.heart = 2
    def update(self):
        hits = pygame.sprite.spritecollide(self, lasers, True)

        for laser in hits:
          self.heart -= 1

        if self.heart <= 0:
            self.kill()
        self.move_and_check_platforms()
        self.check_world_edges()
        self.check_lasers
            
class Flag(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
            
    

        
# Helper functions
def show_start_screen():
    screen.fill(BLACK)
    text = font_xl.render(TITLE, True, WHITE)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2 - 8
    screen.blit(text, rect)

    text = font_sm.render("Press Any Key To start", True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, HEIGHT // 2 + 8
    screen.blit(text, rect)
    
def show_lose_screen():
    screen.fill(BLACK)
    text = font_lg.render("Game Over", True, WHITE)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2 - 8
    screen.blit(text, rect)

    text = font_sm.render("Press 'r' to play again", True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH // 2, HEIGHT // 2 + 8
    screen.blit(text, rect)

def show_level_complete_screen():
    text = font_lg.render("Level complete", True, WHITE)
    rect = text.get_rect()
    rect.midbottom = WIDTH // 2, HEIGHT // 2 - 8
    screen.blit(text, rect)


def show_hud():
    text =  font_md.render(str(hero.score), True, WHITE)
    rect = text.get_rect()
    rect.midtop = WIDTH //2, 16
    screen.blit(text, rect)

    screen.blit(gem_img, [WIDTH - 100, 14])
    text =  font_md.render('x' + str(hero.gems), True, WHITE)
    rect = text.get_rect()
    rect.topleft = WIDTH - 60, 24
    screen.blit(text, rect)

    for i in range(hero.hearts):
        x = i * 36 + 16 
        y = 16
        screen.blit(heart_img, [x, y])
def draw_grid(offset_x=0, offset_y=0):
    for x in range(0, WIDTH + GRID_SIZE, GRID_SIZE):
        adj_x = x - offset_x % GRID_SIZE
        pygame.draw.line(screen, GRAY, [adj_x, 0], [adj_x, HEIGHT], 1)

    for y in range(0, HEIGHT + GRID_SIZE, GRID_SIZE):
        adj_y = y - offset_y % GRID_SIZE
        pygame.draw.line(screen, GRAY, [0, adj_y], [WIDTH, adj_y], 1)

    for x in range(0, WIDTH + GRID_SIZE, GRID_SIZE):
        for y in range(0, HEIGHT + GRID_SIZE, GRID_SIZE):
            adj_x = x - offset_x % GRID_SIZE + 4
            adj_y = y - offset_y % GRID_SIZE + 4
            disp_x = x // GRID_SIZE + offset_x // GRID_SIZE
            disp_y = y // GRID_SIZE + offset_y // GRID_SIZE
            
            point = '(' + str(disp_x) + ',' + str(disp_y) + ')'
            text = font_xs.render(point, True, GRAY)
            screen.blit(text, [adj_x, adj_y])
    
#setup
def start_game():
    global hero, stage
    hero = Hero(0, 0, hero_img)
    stage = START

    pygame.mixer.music.load(start_music)
    pygame.mixer.music.play(-1)
def start_level():
    global player, platforms, items, lasers, enemies, goal, all_sprites
    global gravity, terminal_velocity
    global world_width, world_height
    
    player = pygame.sprite.GroupSingle()
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    items = pygame.sprite.Group()
    lasers = pygame.sprite.Group()
    goal = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    traps = pygame.sprite.Group()
    
    # load level file here
    with open('assets/levels/world-1.json') as f:
        data = json.load(f)
        
    world_width = data['width'] * GRID_SIZE
    world_height = data['height'] * GRID_SIZE
    
    hero.move_to(data['start'][0], data['start'][1])
    player.add(hero)
    
    for i, loc in enumerate(data['flag_locs']):
        if i == 0:
            goal.add( Flag(loc[0], loc[1], flag_img) )
        else:
            goal.add( Flag(loc[0], loc[1], pole_img) )

    for loc in data['grass_locs']:
        platforms.add(Platform(loc[0], loc[1], grass_dirt_img))
        
    for loc in data['block_locs']:
        platforms.add(Platform(loc[0], loc[1], block_img))

    for loc in data['spikeball_locs']:
        enemies.add(Spikeball(loc[0], loc[1], spikeball_img))

    for loc in data['spikeman_locs']:
        enemies.add(Spikeman(loc[0], loc[1], spikeman_img))

    for loc in data['cloud_locs']:
        enemies.add(Cloud(loc[0], loc[1], cloud_img))
        
    for loc in data['gem_locs']:
        items.add(Gem(loc[0], loc[1], gem_img))

    def load_lasers(self):
        self.lasers = pygame.sprite.Group()

    gravity = data['gravity']
    terminal_velocity = data['terminal_velocity']
    momentum = data['momentum']
    friction = data['friction']

    all_sprites.add(player, platforms, items, enemies, goal)
    
# Game loop
running = True
grid_on = False

start_game()
start_level()

while running:
    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                grid_on = not grid_on
            
            elif stage == START:
                stage = PLAYING
                pygame.mixer.music.load(stage_theme)
                pygame.mixer.music.play(-1)
                
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    hero.jump()
                elif event.key == pygame.K_z:
                    hero.shoot()
            
            elif stage == LOSE:
                if event.key == pygame.K_r:
                    start_game()
                    start_level()
                pygame.mixer.music.load(lose_music)
                pygame.mixer.music.play(-1)

                
    pressed = pygame.key.get_pressed()
    
    if stage == PLAYING:
        if pressed[pygame.K_LEFT]:
            hero.move_left()
        elif pressed[pygame.K_RIGHT]:
            hero.move_right()
        else:
            hero.stop()

    
    
    # Game logic
    if stage == PLAYING:
        all_sprites.update()
        
        if hero.hearts == 0:
            stage = LOSE
        elif hero.reached_goal():
            stage = LEVEL_COMPLETE
            pygame.mixer.music.load(victory_theme)
            pygame.mixer.music.play(-1)
            countdown = 2 * FPS
            
        elif stage == LEVEL_COMPLETE:
            countdown -= 1
            if countdown <= 0:
                start_level()
                stage = PLAYING
            
    if hero.rect.centerx < WIDTH // 2:
        offset_x = 0
    elif hero.rect.centerx > world_width - WIDTH // 2:
        offset_x = world_width - WIDTH
    else:
        offset_x = hero.rect.centerx - WIDTH // 2
    
    # Drawing code
    screen.fill(BLUE_GREY)

    for sprite in all_sprites:
        screen.blit(sprite.image, [sprite.rect.x - offset_x, sprite.rect.y])
        
    show_hud()

    if stage == START:
        show_start_screen()
    elif stage == LOSE:
        show_lose_screen()
    elif stage == LEVEL_COMPLETE:
        show_level_complete_screen()

    if grid_on:
        draw_grid(offset_x)
        
    # Update screen
    pygame.display.update()


    # Limit refresh rate of game loop 
    clock.tick(FPS)


# Close window and quit
pygame.quit()

