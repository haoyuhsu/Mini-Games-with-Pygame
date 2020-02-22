# This is a flappy bird Game

import pygame, sys, random, time
from math import atan, degrees, pi

# Initialize Seed
random.seed()

class Bird:
    def __init__(self):
        self.x = 50            # bird x-pos
        self.y = width/2       # bird y-pos
        self.gravity = 1       # Gravity Constant
        self.lift = 25         # Lifting Force
        self.velocity = 0      # Initial Velocity
    def show(self):
    	angle = degrees(atan(-self.velocity/15)+pi/18)   # get the horizontal angle (Based on velocity)
    	pic = pygame.transform.rotate(img, angle)        # rotate the image to the angle
    	# 因為是以圖片左上角座標黏貼 故把鳥的位置定在圖片的中心點去做調整
    	# Adjust the coordinate to top-left of the image and blit
    	playSurface.blit(pic, (int(self.x-img_width/2), int(self.y-img_hieght/2)))
    def update(self):
        self.velocity += self.gravity   # Gravity change velocity
        self.velocity *= 0.9            # damping (same as air resistance)
        self.y += self.velocity         # velocity change y-pos
        if (self.y > height):   # Top boundary
            self.y = height
            self.velocity = 0
        if (self.y < 0):        # Low boundary
            self.y = 0
            self.velocity = 0
    def up(self):
        self.velocity += -self.lift     # Lift the bird

class Pipe:
    def __init__(self, level):
        self.top = random.randrange(height/2)  # get the upper pipe length
        self.gap = 150 - level*10              # gap between two pipes, decrease in higher level
        self.x = width                         # pipe x-pos (initial)
        self.w = 30                            # pipe width
        self.speed = 3                         # pipe moving speed
        self.color = green                     # pipe color
        self.collide = False                   # pipe collide with bird or not
    def hit(self, bird):
        if (bird.y < self.top or bird.y > self.top + self.gap):  # if Bird y-pos outside the gap
            if (bird.x > self.x and bird.x < self.x + self.w):   # Bird x-pos lies in the width of pipe
                self.collide = True            # set collision factor True
                return True
        self.collide = False                   # set collision factor False
        return False
    def show(self):
        # get upper pipe position (top-left), width, length
        upPipe = pygame.Rect((self.x, 0), (self.w, self.top))
        # get lower pipe positon (top-left), width, length
        downPipe = pygame.Rect((self.x, self.top + self.gap), (self.w, height - self.top - self.gap))
        if (self.collide):
            self.color = red   # change pipe color to red when collide
        else:
            self.color = green
        pygame.draw.rect(playSurface, self.color, upPipe, 0)     # Draw the upper pipe
        pygame.draw.rect(playSurface, self.color, downPipe, 0)   # Draw the lower pipe
    def update(self):
        self.x -= self.speed      # update pipe x-pos
    def offscreen(self):
        # check if pipe is off the screen
        if (self.x < -self.w):
            return True
        else:
            return False

def KeyPressed():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(-1)
        elif event.type == pygame.KEYDOWN:
            # when 'space' is pressed 
            if event.key == pygame.K_SPACE:
                bird.up()      # lift the bird up
                sound1.play()  # play the jumping sound

def showScore(choice):
    # choose a font, implement some text to it (Create a Surface)
    sFont = pygame.font.SysFont('monaco', 22)
    Ssurf = sFont.render('Score : {0}'.format(score), True, black)
    # get the rect of the surface
    Srect = Ssurf.get_rect()
    # choose the score text position
    if choice == True:
        Srect.midtop = (200, 200)
    else:
        Srect.midtop = (350, 20)
    # blit the text surface, use Srect as the location of the surface
    playSurface.blit(Ssurf, Srect)

def gameOver():
    myFont = pygame.font.SysFont('monaco', 72)
    GOsurf = myFont.render('Game Over!', True, red)
    GOrect = GOsurf.get_rect()        # Get the Rect of the Surface
    GOrect.midtop = (200, 130)        # Set the Position (Rect)
    playSurface.blit(GOsurf, GOrect)  # blit GOsurf on playSurface at GOrect position
    pygame.display.flip()
    pygame.mixer.music.pause()        # pause the background music
    sound_end.play()                  # play the gameover soundeffect
    time.sleep(5)
    pygame.quit()
    sys.exit()

check_errors = pygame.init()
if (check_errors[1] > 0):
    print("(!) Had {0} initializing errors,exiting... ".format(check_errors[1]))
    sys.exit(-1)
else:
    print("(+) Pygame successfully initialized!")

# Initialize Mixer
pygame.mixer.init()

# Setting Background Music
pygame.mixer.music.load('GrasslandsTheme.ogg')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

# Adding 'Jump' Soounds
sound1 = pygame.mixer.Sound('jump.wav')
sound1.set_volume(0.1)
# Adding 'End' Sounds
sound_end = pygame.mixer.Sound('fail.wav')
sound_end.set_volume(0.2)

# Screen Parameters
width = 400
height = 500

# Screen
playSurface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird!!')

# Setting Colors
white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)
green = pygame.Color(0, 255, 0)
red = pygame.Color(255, 0, 0) 

# FPS Controller
fpsController = pygame.time.Clock()

frame_rate = 50

# Image size
img_width = 70
img_hieght = 70
# load in and rescale an image
img = pygame.image.load('bird.png')
img = pygame.transform.scale(img, (img_width, img_hieght))

# Create a bird class and a pipe List
bird = Bird()
pipeList = []

# Initialize the game parameters
score = 0
gameover = False

while True:
	# Background
    playSurface.fill(white)

    # Pipes
    for i in range (len(pipeList)-1):  # -1: avoid list index out of range
        if (pipeList[i].hit(bird)):
            gameover = True
        if (pipeList[i].offscreen()):
            pipeList.pop(i)      # pop it out of pipeList to save memory
            score += 1           # count the score
        pipeList[i].show()
        pipeList[i].update()

    # level up by 1 (20 points)
    level = int(score/20)

    # Control the frequency of the pipe appearance
    frameCount = int(pygame.time.get_ticks()/1000*frame_rate)
    # pipe shows up every 50 frames
    if (frameCount % 50 == 0 ):
        pipeList.append(Pipe(level))

    # Detect the keyboard control
    KeyPressed()
    
    # Bird
    bird.show()
    bird.update()

    # Score
    showScore(gameover)

    # Game Over function
    if (gameover == True):
        gameOver()

    pygame.display.flip()            # update the full display Surface to the screen
    fpsController.tick(frame_rate)   # run under certain framerate