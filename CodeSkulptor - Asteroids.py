# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False
rock_acc = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def angle_increment(self):
        self.angle_vel += .1
   
    def angle_decrement(self):
        self.angle_vel -= .1
    
    def reset_angle(self):
        self.angle_vel = 0
    
    def toggle_thrust(self):
        if self.thrust == True:
            self.thrust = False
            ship_thrust_sound.rewind()
        elif self.thrust == False:
            self.thrust = True
            ship_thrust_sound.play()
    
    #def toggle_thrust(self, on):
        #self.thrust = on
        #if on:
            #ship_thrust_sound.rewind()
            #ship_thrust_sound.play()
        #else:
            #ship_thrust_sound.pause()
    
    def shoot(self):
        global missile_group
        missile_pos = [self.pos[0] + self.radius * self.forward[0], self.pos[1] + self.radius * self.forward[1]]
        missile_vel = [self.vel[0] + 8 * self.forward[0], self.vel[1] + 8 * self.forward[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
        
    def draw(self,canvas):
        if self.thrust == True:
            canvas.draw_image(self.image, (135,45), self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        self.angle += self.angle_vel
        
        self.forward = angle_to_vector(self.angle)
        if self.thrust == True:
            self.vel[0] += (self.forward[0]/10)
            self.vel[1] += (self.forward[1]/10)
            
        self.vel[0] *= .99
        self.vel[1] *= .99
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
            
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        self.age += 1
        if self.age > self.lifespan:
            return True
        else:
            return False
   
    def collide(self, other_object):
        distance = dist(self.pos, other_object.get_position())
        minimum_distance = self.radius + other_object.get_radius()
        if distance < minimum_distance:
            return True
        else:
            return False
        
def click(pos):
    global started, score, lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        lives = 3
        score = 0
        soundtrack.rewind()
        soundtrack.play()
        started = True
        
        
def group_collision(group, other_object):
    for sprite in set(group):
        if sprite.collide(other_object) == True:
            group.remove(sprite)
            return True

def group_group_collision(group, other_group):
    collisions = 0
    for sprite in set(group):
        if group_collision(other_group, sprite) == True:
            group.remove(sprite)
            collisions += 1
    return collisions

def process_sprite_group(canvas, group):
    for sprite in set(group):
        if sprite.update() == True:
            group.remove(sprite)
        sprite.draw(canvas)
        
def draw(canvas):
    global time, started, lives, score, rock_group, missile_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("Score: " + str(score), (700, 30), 27, 'White')
    canvas.draw_text("Lives: " + str(lives), (725, 65), 18, 'Red')

    my_ship.draw(canvas)
    my_ship.update()
    
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    
    if group_collision(rock_group, my_ship) == True:
        lives -= 1
        
    score += group_group_collision(rock_group, missile_group)
    
    if lives <= 0:
        rock_group = set([])
        started = False
    
    if started == False:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

# timer handler that spawns a rock
def rock_spawner():
    global rock_group, rock_acc
    rock_pos = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
    rock_vel = [random.randint(-2, 2) + rock_acc, random.randint(-2, 2) + rock_acc]
    rock_angle_vel = random.choice([-.2,-.1, .1, .2])
    a_rock = Sprite(rock_pos, rock_vel, 0, rock_angle_vel, asteroid_image, asteroid_info)
    collide_distance = dist(rock_pos, my_ship.get_position())
    rock_acc += .05
    if len(rock_group) <= 12 and started == True and collide_distance > 5:
        rock_group.add(a_rock)
    
def key_down(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_decrement()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_increment()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.toggle_thrust()
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def key_up(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.reset_angle()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.reset_angle()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.toggle_thrust()
    
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()