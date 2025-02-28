import os
import random
import math
import pygame
import json
from os import listdir
from os.path import isfile, join

pygame.init()  # initialize the pygame module

# A caption for display (at the top of the window)
pygame.display.set_caption("SIXTIES")

# Define a few global variables
WIDTH, HEIGHT = 1000, 600
FPS = 60
PLAYER_VEL = 10  # Player velocity
HEARTS = 5
LEVEL_TIME = 300  # 5 minutes
LEVEL = 1
SAVE_FILE = "savegame.txt"

# Set up pygame window
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Load pixel font
PIXEL_FONT = pygame.font.Font("assets/Fonts/font.otf", 50)
SMALL_PIXEL_FONT = pygame.font.Font("assets/Fonts/font.otf", 35)

# Function that flips the image (of character's status) or is called 'sprite'.
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


# Function that loads the sprite sheets for the character.
# Within the character, we can pick what sheet we want to use, what animations we want to loop through.
# Notice: with dir1 and dir2, we can load other images that aren't just the characters and this will be
#  very dynamic.
def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)  # path to the images we're going to be loading
    images = [f for f in listdir(path) if isfile(join(path, f))]  # loads every file inside the dir

    all_sprites = {}  # key = animation style, value = all the images in that animation

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        # convert.alpha() loads a transparent background image

        # Get all the sprites in the image
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            # draw an animation frame from image onto the surface of exact size
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)  # 32 is the depth
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)  # 'blit' means 'draw'
            sprites.append(pygame.transform.scale2x(surface))  # double size: 64 by 64

            # Want a multi-directional animation, add two keys to our dictionary 'sprites'
            #  for every one of the animations
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


# Function that gets our blocks
def get_block(size, terrain_type="Terrain"):
    # Always use the single terrain spritesheet
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    # Map terrain_type to a column index (assuming one row of tiles)
    tile_map = {"Terrain": 0, "Terrain2": 1, "Terrain3": 2}
    col = tile_map.get(terrain_type, 0)
    # Define the rect based on the tile's column (row 0)
    rect = pygame.Rect(col * size, 0, size, size)
    # Create a new surface for the block
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

# Character Selection Interface
def character_selection():
    selected_character = None
    text = PIXEL_FONT.render("Select Your Character", True, (0, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

    # List of character names
    characters = ["MaskDude", "NinjaFrog", "PinkMan", "VirtualGuy"]

    # Create character buttons
    character_buttons = []
    button_width = 200
    button_height = 50
    button_gap = 20
    total_height = (button_height + button_gap) * len(characters) - button_gap

    # Create Rect objects for each character button
    for i, char in enumerate(characters):
        x = (WIDTH - button_width) // 2
        y = (HEIGHT - total_height) // 2 + i * (button_height + button_gap)
        button_rect = pygame.Rect(x, y, button_width, button_height)
        character_buttons.append((button_rect, char))  # Add button Rect and character name to list

    # Main loop for character selection
    while not selected_character:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in character_buttons:
                    if button[0].collidepoint(event.pos):
                        selected_character = button[1]

        # Clear screen
        window.fill((173, 216, 230))

        # Display text
        window.blit(text, text_rect)

        # Draw character buttons
        for button in character_buttons:
            pygame.draw.rect(window, (0, 255, 0), button[0])
            button_text = SMALL_PIXEL_FONT.render(button[1], True, (255, 255, 255))
            window.blit(button_text, button_text.get_rect(center=button[0].center))

        pygame.display.update()

    return selected_character


# Function to display the main game screen
def main_game_screen():
    title_text = PIXEL_FONT.render("SIXTIES", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

    button_width = 500  # Increased from 200
    button_height = 75  # Increased from 50
    button_color = (255, 140, 0)  # Orange
    button_hover_color = (255, 165, 0)  # Darker orange

    play_btn = Button(WIDTH//2 - button_width//2, HEIGHT//2, 
                     button_width, button_height, 
                     "Play", PIXEL_FONT, button_color, button_hover_color)
    
    settings_btn = Button(WIDTH//2 - button_width//2, HEIGHT//2 + button_height + 20,
                         button_width, button_height,
                         "Settings", PIXEL_FONT, button_color, button_hover_color)
    
    help_btn = Button(WIDTH//2 - button_width//2, HEIGHT//2 + 2 * (button_height + 20),
                      button_width, button_height,
                      "Help", PIXEL_FONT, button_color, button_hover_color)

    background_image = pygame.image.load("assets/Background/background.png").convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    while True:
        window.blit(background_image, (0, 0))
        window.blit(title_text, title_rect)
        play_btn.update()
        settings_btn.update()
        help_btn.update()

        play_btn.draw(window)
        settings_btn.draw(window)
        help_btn.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if play_btn.is_clicked(event):
                return "play"
            elif settings_btn.is_clicked(event):
                return "settings"
            elif help_btn.is_clicked(event):
                return "help"

        pygame.display.update()

def draw_button(window, rect, text):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        rect.inflate_ip(10, 10)
    else:
        rect.inflate_ip(-10, -10)
    pygame.draw.rect(window, (0, 255, 0), rect)
    button_text = SMALL_PIXEL_FONT.render(text, True, (255, 255, 255))
    window.blit(button_text, button_text.get_rect(center=rect.center))

class Button:
    def __init__(self, x, y, width, height, text, font, base_color, hover_color, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.color = base_color

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        window.blit(text_surface, text_surface.get_rect(center=self.rect.center))

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def update(self):
        if self.is_hovered():
            self.color = self.hover_color
        else:
            self.color = self.base_color

    def is_clicked(self, event):
        return self.is_hovered() and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

class ImageButton:
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, window):
        window.blit(self.image, self.rect.topleft)

    def is_clicked(self, event):
        return self.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

# Inheriting from this pygame class for our Player
class Player(pygame.sprite.Sprite):
    COLOUR = (255, 0, 0)
    GRAVITY = 9.8
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
    ANIMATION_DELAY = 3
    INITIAL_JUMP_VELOCITY = -16  # Initial jump velocity

    def __init__(self, x, y, width, height):
        super().__init__()
        self.sprite = None
        self.rect = pygame.Rect(x, y, width, height)  # on rectangle to make it easier to move and collide
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0  # tell us how long the character has been in the air for...
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.hearts = HEARTS
        self.start_time = pygame.time.get_ticks()
        self.checkpoint = None
        self.active_powerup = None
        self.powerup_start_time = 0
        self.powerup_duration = 0
        self.powerup_glow_timer = 0
        self.powerup_glow_pulse = False
        self.default_vel = PLAYER_VEL
        self.default_gravity = self.GRAVITY
        self.level = 1  # Track the current level
        self.PLAYER_VEL = PLAYER_VEL # Store initial player velocity
        self.GRAVITY = 9.8 # Store initial gravity
        self.acceleration = 0.5
        self.friction = 0.3
        self.hit_registered = False

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = - vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    # loop is called once every frame (1 iteration of the while loop)
    # This is going to move our character in the correct direction and handle things like updating
    #   the animation and all the stuff that we constantly need to do for our character
    def loop(self, fps):
        # Apply gravity
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1

        if self.rect.top > HEIGHT:
            self.make_hit()
            self.respawn()

        if pygame.time.get_ticks() - self.start_time > LEVEL_TIME * 1000:
            self.hearts = 0  # Time's up, player fails

        self.update_sprite()

        # Handle powerup effects
        if self.active_powerup:
            current_time = pygame.time.get_ticks()
            time_elapsed = current_time - self.powerup_start_time

            if time_elapsed >= self.powerup_duration - 2000:
                self.powerup_glow_timer += 1
                if self.powerup_glow_timer % 30 == 0:
                    self.powerup_glow_pulse = not self.powerup_glow_pulse

            if time_elapsed >= self.powerup_duration:
                self.deactivate_powerup()

    # update our sprite every single frame
    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:  # means moving up
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.x_vel != 0:
            sprite_sheet = "run"
        elif self.y_vel > self.GRAVITY * 2:  # not > 0 because y_vel is always > 0 due to gravity
            sprite_sheet = "fall"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)  # make sprite dynamic
        self.sprite = sprites[sprite_index]
        self.animation_count += 1

    def draw(self, win, offset_x):
        sprite_to_draw = self.sprite
        if self.active_powerup:
            glow_color = self.get_powerup_glow_color()
            if glow_color:
                if self.powerup_glow_pulse:
                    surface = pygame.Surface(self.sprite.get_size(), pygame.SRCALPHA)
                    surface.fill(glow_color + (128,))  # Adjust alpha for pulse effect
                    sprite_to_draw = self.sprite.copy()
                    sprite_to_draw.blit(surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                else:
                    surface = pygame.Surface(self.sprite.get_size(), pygame.SRCALPHA)
                    surface.fill(glow_color + (64,))  # Adjust alpha for constant glow
                    sprite_to_draw = self.sprite.copy()
                    sprite_to_draw.blit(surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        win.blit(sprite_to_draw, (self.rect.x - offset_x, self.rect.y))

    # Constantly update the rectangle that bounds our character based on the sprite that we're showing
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        # A mask is a mapping of all the pixels that exist in the sprite
        #  This mask allows us to perform pixel perfect collision because we can overlap it with another
        #  mask and make sure that  we only say two objects collide if pixels (not the rectangular box)
        #  are colliding.
        self.mask = pygame.mask.from_surface(self.sprite)

    # Character lands on an object: character stops...
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0  # comment this later..........

    # Character hits head (collide with bottom of an object)
    def hit_head(self):
        self.fall_count = 0
        self.y_vel *= -0.8

    # Character jumps
    def jump(self):
        if self.jump_count < 2:
            self.y_vel = self.INITIAL_JUMP_VELOCITY
            self.animation_count = 0
            self.jump_count += 1
            self.fall_count = 0  # reset to remove any gravity accumulated

    # Character get hit (ex. by fire...)
    def make_hit(self):
        if not self.hit_registered:
            self.hearts -= 1
            self.hit_registered = True
        self.hit = True

    def respawn(self):
        if self.checkpoint:
            self.rect.x, self.rect.y = self.checkpoint.rect.x, self.checkpoint.rect.y
        else:
            self.rect.x, self.rect.y = 100, 100
        self.y_vel = 0
        self.x_vel = 0
        self.hit_registered = False
        return 0

    def set_checkpoint(self, checkpoint):
        self.checkpoint = checkpoint

    def reset_checkpoint(self):
        self.checkpoint = None

    def activate_powerup(self, powerup):
        self.active_powerup = powerup
        self.powerup_start_time = pygame.time.get_ticks()
        self.powerup_duration = powerup.duration
        if powerup.powerup_type == "speed_boost":
            self.default_vel = self.PLAYER_VEL
            self.PLAYER_VEL = self.default_vel * 3  # Substantially increased speed boost
        elif powerup.powerup_type == "jump_boost":
            self.default_gravity = self.GRAVITY
            self.GRAVITY = self.default_gravity * 0.5  # Significantly enhanced jump
        elif powerup.powerup_type == "extra_life":
            self.hearts += 3  # Overpowered extra lives

    def deactivate_powerup(self):
        if self.active_powerup:
            if self.active_powerup.powerup_type == "speed_boost":
                self.PLAYER_VEL = self.default_vel
            elif self.active_powerup.powerup_type == "jump_boost":
                self.GRAVITY = self.default_gravity
        self.active_powerup = None
        self.powerup_start_time = 0
        self.powerup_duration = 0
        self.powerup_glow_timer = 0
        self.powerup_glow_pulse = False

    def get_powerup_glow_color(self):
        if self.active_powerup:
            return self.active_powerup.glow_color
        return None

# Class for all the objects, inherit from this class for specific objects
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()  # Initialize the superclass
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # pygame.SRCALPHA supports transparent images
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


# Class for blocks
class Block(Object):
    def __init__(self, x, y, size, terrain_type="Terrain"):  # A block is a square, just need one dimension
        super().__init__(x, y, size, size)
        block = get_block(size, terrain_type)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


# Class for fire (trap)
class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop_fire(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):  # so that animation_count doesn't get too large
            self.animation_count = 0


# Class for door (end point)
class Door(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "door")
        # Create a custom door surface
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        # Draw door frame
        pygame.draw.rect(self.image, (139, 69, 19), (0, 0, width, height))  # Brown frame
        pygame.draw.rect(self.image, (101, 67, 33), (5, 5, width-10, height-10))  # Darker inner
        # Add door handle
        pygame.draw.circle(self.image, (255, 215, 0), (width-15, height//2), 5)  # Gold handle
        self.mask = pygame.mask.from_surface(self.image)


# Class for NPC
class NPC(Object):
    ANIMATION_DELAY = 3
    GRAVITY = 1
    NPC_VEL = 5  # NPCs have their own velocity, independent of player

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "npc")
        self.sprites = load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)
        self.animation_count = 0
        self.direction = random.choice(["left", "right"])
        self.x_vel = 0
        self.y_vel = 0
        self.fall_count = 0
        self.jump_count = 0
        self.is_alive = True
        self.update_sprite()  # Initialize sprite here
        
        # Set initial offset to ensure proper placement on platforms
        self.rect.y += 1  # Small offset to prevent being partially in the floor

    def update_sprite(self):
        sprite_sheet = "run"
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.sprites[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.mask = pygame.mask.from_surface(self.image)
        
    # Updated loop method with independent physics and better collision detection
    def loop(self, fps, objects, player):
        # Set base velocity - independent of player's velocity
        base_speed = self.NPC_VEL
        self.x_vel = -base_speed if self.direction == "left" else base_speed

        # Apply gravity
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)

        # Store original position for collision detection
        original_x = self.rect.x
        original_y = self.rect.y

        # Horizontal movement and collision
        self.rect.x += self.x_vel
        horizontal_collision = False
        for obj in objects:
            if obj is not self and isinstance(obj, Block) and self.rect.colliderect(obj.rect):
                horizontal_collision = True
                if self.x_vel > 0:
                    self.rect.right = obj.rect.left
                elif self.x_vel < 0:
                    self.rect.left = obj.rect.right
                self.direction = "left" if self.direction == "right" else "right"
                break
        
        # Vertical movement and collision
        self.rect.y += self.y_vel
        vertical_collision = False
        for obj in objects:
            if obj is not self and isinstance(obj, Block) and self.rect.colliderect(obj.rect):
                vertical_collision = True
                if self.y_vel > 0:  # Landing on top of a block
                    self.rect.bottom = obj.rect.top
                    self.fall_count = 0
                    self.y_vel = 0
                elif self.y_vel < 0:  # Hitting the bottom of a block
                    self.rect.top = obj.rect.bottom
                    self.y_vel = 0
                break

        # Check if enemy is about to walk off the platform
        if not horizontal_collision:  # Only check if we didn't collide horizontally
            # Create a check rectangle based on direction
            if self.direction == "left":
                check_rect = pygame.Rect(self.rect.left - 10, self.rect.bottom + 1, 5, 10)
            else:
                check_rect = pygame.Rect(self.rect.right + 5, self.rect.bottom + 1, 5, 10)

            on_platform = False
            for obj in objects:
                if obj is not self and isinstance(obj, Block) and check_rect.colliderect(obj.rect):
                    on_platform = True
                    break
                    
            if not on_platform:
                # Reverse direction if about to walk off
                self.direction = "left" if self.direction == "right" else "right"
                # Reset position to before movement to prevent getting stuck
                self.rect.x = original_x

        self.fall_count += 1
        self.update_sprite()

    def update(self, player):
        if self.is_alive and self.rect.colliderect(player.rect):
            # Check if player is above the enemy (jumping on it)
            if player.rect.bottom <= self.rect.top + 10 and player.y_vel > 0:
                self.die()
                player.y_vel = -10  # Bounce player up
            else:
                player.make_hit()
                player.hearts = max(player.hearts - 1, 0)  # Reduce hearts by 1 but not below 0

    def die(self):
        self.is_alive = False
        # Don't call self.kill() here since we're managing objects in a list, not using sprite groups

# Class for Checkpoint
class Checkpoint(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "checkpoint")
        self.checkpoint_sprites = load_sprite_sheets("Items", "Checkpoints/Checkpoint", 64, 64, False)
        self.image = self.checkpoint_sprites["Checkpoint (Flag Idle)(64x64)"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.active = False

    def activate(self):
        self.active = True
        self.image = self.checkpoint_sprites["Checkpoint (Flag Out)(64x64)"][0]

# Class for PowerUp
class PowerUp(Object):
    def __init__(self, x, y, powerup_type):
        super().__init__(x, y, 32, 32, "powerup")
        self.powerup_type = powerup_type
        self.powerup_sprites = load_sprite_sheets("Items", "Fruits", 32, 32, False)
        self.image = self.get_powerup_image(powerup_type)
        self.mask = pygame.mask.from_surface(self.image)
        self.duration = 5000  # 5 seconds
        self.glow_color = self.get_powerup_glow_color(powerup_type)

    def get_powerup_image(self, powerup_type):
        if powerup_type == "speed_boost":
            return self.powerup_sprites["Apple"][0]
        elif powerup_type == "jump_boost":
            return self.powerup_sprites["Bananas"][0]
        elif powerup_type == "extra_life":
            return self.powerup_sprites["Cherries"][0]
        else:
            return self.powerup_sprites["Kiwi"][0]

    def get_powerup_glow_color(self, powerup_type):
        if powerup_type == "speed_boost":
            return (255, 255, 0)  # Yellow
        elif powerup_type == "jump_boost":
            return (0, 255, 255)  # Cyan
        elif powerup_type == "extra_life":
            return (255, 0, 255)  # Magenta
        else:
            return (0, 255, 0)  # Green

# Function to fade out
def fade_out(window):
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(0, 256):
        fade.set_alpha(alpha)
        window.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(2)

# Function to fade in
def fade_in(window):
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(255, -1, -1):
        fade.set_alpha(alpha)
        window.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(1)

# Returns a list that contains all the background tiles aht we need to draw
def get_background(name):  # name = colour of background
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()  # don't care about '_' values??
    tiles = []

    # Loop through how many tiles that need to be created in the x and y direction
    for i in range(WIDTH // width + 1):
        for j in range (HEIGHT // height + 1):
            pos = (i * width, j * height)  # position of the top left corner of the current
                                           #   tile that I'm adding to the tiles list in pygame
            tiles.append(pos)

    return tiles, image


# Draw function
def draw(window, background, bg_image, player, objects, offset_x, level):
    for tile in background:  # looping through every tile and then draw bg_image at that position
        window.blit(bg_image, tile)  #   which will fill the entire screen with bg_image

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    font = pygame.font.SysFont(None, 35)
    hearts_text = font.render(f"Hearts: {player.hearts}", True, (255, 0, 0))
    time_left = max(0, LEVEL_TIME - (pygame.time.get_ticks() - player.start_time) // 1000)
    timer_text = font.render(f"Time: {time_left}s", True, (0, 0, 0))
    level_text = font.render(f"Level: {level}", True, (0, 0, 0))
    window.blit(hearts_text, (10, 10))
    window.blit(timer_text, (10, 50))
    window.blit(level_text, (WIDTH - 100, 10))

    # Draw powerup display
    if player.active_powerup:
        powerup_text = font.render(f"Powerup: {player.active_powerup.powerup_type}", True, player.active_powerup.glow_color)
        powerup_time_left = max(0, player.powerup_duration - (pygame.time.get_ticks() - player.powerup_start_time)) // 1000
        powerup_timer_text = font.render(f"Time Left: {powerup_time_left}s", True, player.active_powerup.glow_color)
        window.blit(powerup_text, (10, 90))
        window.blit(powerup_timer_text, (10, 130))

    pygame.display.update()


# Function that handles vertical collision
def handle_vertical_collision(player, objects, dy):  # dy = displacement in y
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:  # if character moves down, colliding with the top of the obj
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


#  Function that handles horizontal collision
def collide(player, objects, dx):
    player.move(dx, 0)  # move the character
    player.update()  # update the mask
    collided_obj = None
    for obj in objects:
        if obj.name != "door" and pygame.sprite.collide_mask(player, obj):  # check collide if moving in that direction
            collided_obj = obj
            break

    player.move(-dx, 0)  # move the character back after the check for collision
    player.update()  # update the mask again
    return collided_obj


# Inside this function, check for keys being pressed on the keyboard to
#   move the character (and check for collision)
def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0  # ensure that character only moves to certain direction when we hold the certain key
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_a] and not collide_left:
        player.move_left(PLAYER_VEL)  # move the character to the left by its velocity
    if keys[pygame.K_d] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    objects_to_remove = []  # Create a list to store objects that need to be removed
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()
        if obj and obj.name == "checkpoint":
            obj.activate()
            player.set_checkpoint(obj)
        if obj and obj.name == "powerup" and obj in objects:  # Check if the object is still in the list
            player.activate_powerup(obj)
            objects_to_remove.append(obj)  # Add to removal list instead of removing immediately
    
    # Remove objects after iteration is complete
    for obj in objects_to_remove:
        if obj in objects:  # Double-check the object is still in the list
            objects.remove(obj)

def generate_level(level):
    random.seed(level)
    block_size = 96
    terrain_types = ["Terrain", "Terrain2", "Terrain3"]
    terrain_type = random.choice(terrain_types)
    powerup_types = ["speed_boost", "jump_boost", "extra_life"]

    # Generate floor blocks with gaps
    floor = []
    for i in range(-WIDTH // block_size, (WIDTH * 5) // block_size):
        if random.choice([True, False]):  # Randomly create gaps
            floor.append(Block(i * block_size, HEIGHT - block_size, block_size, terrain_type))

    # Generate left and right borders
    left_border = [Block(-block_size, HEIGHT - block_size * (i + 1), block_size, terrain_type) for i in range(HEIGHT // block_size)]
    right_border = [Block((WIDTH * 5) // block_size * block_size, HEIGHT - block_size * (i + 1), block_size, terrain_type) for i in range(HEIGHT // block_size)]

    # Generate random platforms and fire
    objects = floor.copy()
    objects.extend(left_border)
    objects.extend(right_border)

    # Ensure a platform under the spawn point
    spawn_platform = Block(100, HEIGHT - block_size * 2, block_size, terrain_type)
    objects.append(spawn_platform)

    npc_spawn_chance = min(0.1 * level, 0.5)  # Increase NPC spawn chance with level
    # Ensure at least one NPC in the first few levels
    if level <= 3:
        npc_x = random.randint(5, 10) * block_size
        npc_y = HEIGHT - block_size * random.randint(2, 6) - 64
        npc = NPC(npc_x, npc_y, 32, 32)
        objects.append(npc)

    for i in range(5, (WIDTH * 5) // block_size, random.randint(10, 20)):
        platform_length = random.randint(3, 10)
        platform_height = random.randint(2, 6)
        platform = [Block(i * block_size + j * block_size, HEIGHT - block_size * platform_height, block_size, terrain_type)
                    for j in range(platform_length)]
        objects.extend(platform)

        # Add fire with increasing frequency
        if random.random() < min(0.05 * level, 0.2):
            fire = Fire(i * block_size, HEIGHT - block_size * platform_height - 64, 16, 32)
            fire.on()
            objects.append(fire)

        # Add checkpoints
        if i % (20 * block_size) == 0:
            checkpoint = Checkpoint(i * block_size, HEIGHT - block_size * 2, 64, 64)
            objects.append(checkpoint)

        # Add NPCs with increasing frequency
        if random.random() < npc_spawn_chance:
            npc = NPC(i * block_size, HEIGHT - block_size * platform_height - 64, 32, 32)
            objects.append(npc)

        # Add power-ups
        if random.random() < 0.1:
            powerup_type = random.choice(powerup_types)
            powerup = PowerUp(i * block_size, HEIGHT - block_size * platform_height - 64, powerup_type)
            objects.append(powerup)

    # Add invisible block at the bottom of the screen
    invisible_block = Block(HEIGHT, WIDTH * 5000, block_size, terrain_type)
    objects.append(invisible_block)

    # Add end point (door) with platform underneath
    door_x = (WIDTH * 5) // block_size * block_size - block_size
    door_y = HEIGHT - block_size * 2
    door = Door(door_x, door_y, 64, 128)
    for i in range(3):
        objects.append(Block(door_x - i * block_size, door_y + 128, block_size, terrain_type))

    return objects, invisible_block, door

# Function to save game progress
def save_game(player, level):
    data = {
        "hearts": player.hearts,
        "level": level,
        "checkpoint_x": player.checkpoint.rect.x if player.checkpoint else None,
        "checkpoint_y": player.checkpoint.rect.y if player.checkpoint else None,
        "active_powerup": player.active_powerup.powerup_type if player.active_powerup else None,
        "powerup_start_time": player.powerup_start_time,
        "powerup_duration": player.powerup_duration
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

# Function to load game progress
def load_game(player):
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            player.hearts = data["hearts"]
            level = data["level"]
            checkpoint_x = data["checkpoint_x"]
            checkpoint_y = data["checkpoint_y"]
            active_powerup = data["active_powerup"]
            powerup_start_time = data["powerup_start_time"]
            powerup_duration = data["powerup_duration"]

            if checkpoint_x is not None and checkpoint_y is not None:
                player.checkpoint = Checkpoint(checkpoint_x, checkpoint_y, 64, 64)
            else:
                player.reset_checkpoint()

            if active_powerup:
                powerup_type = active_powerup
                powerup = PowerUp(0, 0, powerup_type)  # Create a dummy powerup object
                player.activate_powerup(powerup)
                player.powerup_start_time = powerup_start_time
                player.powerup_duration = powerup_duration

            return level
    except FileNotFoundError:
        return 1

# Function to restart the game
def restart_game():
    global run_game
    run_game = False

def draw_pause_modal(window):
    modal_width, modal_height = 400, 300
    modal_rect = pygame.Rect((WIDTH - modal_width) // 2, (HEIGHT - modal_height) // 2, modal_width, modal_height)
    pygame.draw.rect(window, (0, 0, 0), modal_rect)
    pygame.draw.rect(window, (255, 255, 255), modal_rect, 5)

    leave_button = Button(modal_rect.centerx - 100, modal_rect.centery - 50, 200, 50, "Leave", PIXEL_FONT, (255, 0, 0), (200, 0, 0))
    buy_coins_button = Button(modal_rect.centerx - 100, modal_rect.centery + 20, 200, 50, "Buy Coins", PIXEL_FONT, (0, 255, 0), (0, 200, 0))

    leave_button.update()
    buy_coins_button.update()

    leave_button.draw(window)
    buy_coins_button.draw(window)

    return leave_button, buy_coins_button

def settings_screen():
    title_text = PIXEL_FONT.render("Settings", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))

    wasd_button = Button(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 50, "WASD Controls", PIXEL_FONT, (0, 255, 0), (0, 200, 0))
    arrows_button = Button(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 50, "Arrow Controls", PIXEL_FONT, (0, 255, 0), (0, 200, 0))
    back_button = Button(WIDTH // 2 - 150, HEIGHT // 2 + 150, 300, 50, "Back", PIXEL_FONT, (255, 0, 0), (200, 0, 0))

    controls = "wasd"  # Default controls

    while True:
        window.fill((173, 216, 230))
        window.blit(title_text, title_rect)
        wasd_button.update()
        arrows_button.update()
        back_button.update()

        wasd_button.draw(window)
        arrows_button.draw(window)
        back_button.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if wasd_button.is_clicked(event):
                controls = "wasd"
            elif arrows_button.is_clicked(event):
                controls = "arrows"
            elif back_button.is_clicked(event):
                return controls

        pygame.display.update()

def help_screen():
    title_text = PIXEL_FONT.render("Help", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))

    controls_text = SMALL_PIXEL_FONT.render("Controls: WASD or Arrow Keys", True, (0, 0, 0))
    controls_rect = controls_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    back_button = Button(WIDTH // 2 - 150, HEIGHT // 2 + 150, 300, 50, "Back", PIXEL_FONT, (255, 0, 0), (200, 0, 0))

    while True:
        window.fill((173, 216, 230))
        window.blit(title_text, title_rect)
        window.blit(controls_text, controls_rect)
        back_button.update()
        back_button.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if back_button.is_clicked(event):
                return

        pygame.display.update()

# Main function (start the game)
def main():
    global run_game
    run_game = True
    character_selected = False
    selected_character = None
    controls = "wasd"  # Default controls

    clock = pygame.time.Clock()
    pause_button = ImageButton(WIDTH - 60, 10, "assets/Menu/Buttons/Play.png")
    game_paused = False

    while run_game:
        screen = main_game_screen()
        if screen == "play":
            if not character_selected:
                selected_character = character_selection()
                character_selected = True
            player = Player(100, 100, 50, 50)
            level = 1
            while player.hearts > 0:
                objects, invisible_block, door = generate_level(level)
                offset_x = 0
                scroll_area_width = 300
                background, bg_image = get_background("Blue.png")
                run = True
                while run:
                    clock.tick(FPS)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                            run_game = False
                            break

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE and player.jump_count < 2:
                                player.jump()

                        if pause_button.is_clicked(event):
                            game_paused = not game_paused

                    if game_paused:
                        leave_button, buy_coins_button = draw_pause_modal(window)
                        for event in pygame.event.get():
                            if leave_button.is_clicked(event):
                                run_game = False
                                run = False
                            elif buy_coins_button.is_clicked(event):
                                # Implement buy coins functionality
                                pass
                        pygame.display.update()
                        continue

                    player.loop(FPS)
                    handle_move(player, objects)
                    draw(window, background, bg_image, player, objects, offset_x, level)
                    pause_button.draw(window)

                    if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or \
                            ((player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                        offset_x += player.x_vel

                    # Check if player falls off the bottom of the screen
                    if player.rect.top > HEIGHT:
                        player.hit = True
                        offset_x = player.respawn()
                        objects, invisible_block, door = generate_level(level)
                        

                    # Check if player collides with the invisible block
                    if player.rect.colliderect(invisible_block.rect):
                        player.hit = True

                    # Reset the level if player is hit
                    if player.hit:
                        offset_x = player.respawn()  # deducts a heart and resets player's position
                        objects, invisible_block, door = generate_level(level)
                        background, bg_image = get_background("Blue.png")
                        player.hit = False # Reset hit status
                        run = True  # Continue the level
                        continue

                    # Check if player reaches the door
                    if player.rect.colliderect(door.rect):
                        fade_out(window)
                        level += 1
                        player = Player(100, 100, 50, 50)
                        player.hearts = HEARTS  # Reset hearts
                        player.level = level  # Update player's level
                        objects, invisible_block, door = generate_level(level)
                        offset_x = 0
                        background, bg_image = get_background("Blue.png")
                        fade_in(window)

                    # Check if player is dead
                    if player.hearts <= 0:
                        font = pygame.font.SysFont(None, 75)
                        text = font.render("Game Over", True, (255, 0, 0))
                        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
                        window.blit(text, text_rect)

                        restart_button = Button(WIDTH // 2 - 150, HEIGHT // 2 - 30, 300, 50, "Restart Level", PIXEL_FONT, (0, 255, 0), (0, 200, 0))
                        menu_button = Button(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 50, "Main Menu", PIXEL_FONT, (255, 0, 0), (200, 0, 0))

                        restart_button.update()
                        menu_button.update()

                        restart_button.draw(window)
                        menu_button.draw(window)

                        pygame.display.update()

                        waiting = True
                        while waiting:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    quit()
                                # ----- Modified restart button branch -----
                                if restart_button.is_clicked(event):
                                    save_game(player, level)  # Save progress before restarting
                                    player.hearts = HEARTS
                                    objects, invisible_block, door = generate_level(level)
                                    offset_x = 0
                                    waiting = False  # Exit waiting loop to resume gameplay
                                # ----------------------------------------------
                                if menu_button.is_clicked(event):
                                    run = False
                                    waiting = False
                                    player.hearts = HEARTS  # Reset hearts when going to main menu
                                    level = 1           # Reset level when going to main menu
                                    character_selected = False  # Return to character selection
                                    break
                        if not run:
                            break  # Break out to return to the main game screen
                        continue  # Proceed with the restarted level

                    # Reset the level if player is hit
                    if player.hit:
                        offset_x = player.respawn()  # deducts a heart and resets player's position
                        objects, invisible_block, door = generate_level(level)
                        background, bg_image = get_background("Blue.png")
                        run = False  # exit inner loop to restart level
                        continue

                    # Update NPCs using the new move method.
                    for obj in objects:
                        if isinstance(obj, NPC) and obj.is_alive:  # Only update if the NPC is alive
                            obj.loop(FPS, objects, player)
                            obj.update(player)  # Call update separately to check player collision
                            # Check for player jumping on NPC (this is already handled in the NPC.update method)
                            if not obj.is_alive:  # If the enemy just died
                                powerup_types = ["speed_boost", "jump_boost", "extra_life"]
                                powerup_type = random.choice(powerup_types)
                                powerup = PowerUp(obj.rect.x, obj.rect.y, powerup_type)
                                objects.append(powerup)
                                objects.remove(obj)  # Remove the dead NPC from the objects list

                break  # return to main menu or restart gameplay
        elif screen == "settings":
            controls = settings_screen()
        elif screen == "help":
            help_screen()

# start
main()
