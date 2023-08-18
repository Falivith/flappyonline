import pygame, random
import time
from config import make_pos, read_pos
from pygame.locals import *
from network import Network

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800

SPEED = 5
GRAVITY = 2
GAME_SPEED = 5

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500
random.seed(0)
PIPE_GAP = 200
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

class Bird(pygame.sprite.Sprite):

    def __init__(self, color, startPos=(SCREEN_WIDTH/ 2, SCREEN_HEIGHT/ 2)):
        pygame.sprite.Sprite.__init__(self)

        bluebird_images = [
            pygame.image.load('assets/bluebird-upflap.png').convert_alpha(),
            pygame.image.load('assets/bluebird-midflap.png').convert_alpha(),
            pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
        ]

        yellowbird_images = [
            pygame.image.load('assets/yellowbird-upflap.png').convert_alpha(),
            pygame.image.load('assets/yellowbird-midflap.png').convert_alpha(),
            pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
        ]

        self.images = bluebird_images if color == "blue" else yellowbird_images
        self.current_image = 0
        self.image = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = startPos[0] #x
        self.rect[1] = startPos[1] #y

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]
        # Update y
        self.rect[1] += GRAVITY
    
    def bump(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.rect[1] += -SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

class Pipe(pygame.sprite.Sprite):
    def __init__():
        pass
    def __init__(self, inverted=None, xpos=None, ysize=None):
        pygame.sprite.Sprite.__init__(self)
        if xpos is None and inverted is None and ysize is None:
            self.pipe_group = pygame.sprite.Group()
            return
        else:
            self.image = pygame.image.load('assets/pipe-red.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (PIPE_WIDTH,PIPE_HEIGHT))
            
            self.rect = self.image.get_rect()
            self.rect[0] = xpos

            if inverted:
                self.image = pygame.transform.flip(self.image, False, True)
                self.rect[1] = -(self.rect[3] - ysize)
            else:
                self.rect[1] = SCREEN_HEIGHT - ysize

            self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

    def get_random_pipes(self,x=None):
        if x is not None:
            self.xpos = x
        size = random.randint(100, 300)
        print("xpos: ",self.xpos)
        pipe = Pipe(False, self.xpos, size)
        pipe_inverted = Pipe(True, self.xpos, SCREEN_HEIGHT - size - PIPE_GAP)
        return (pipe, pipe_inverted)
    
    def generate_pipes(self):
        for i in range(2):
            self.xpos = SCREEN_WIDTH * i + 800
            pipes = self.get_random_pipes()
            self.pipe_group.add(pipes[0])
            self.pipe_group.add(pipes[1])

    def remove_pipes(self):
        if is_off_screen(self.pipe_group.sprites()[0]):
                self.pipe_group.remove(self.pipe_group.sprites()[0])
                self.pipe_group.remove(self.pipe_group.sprites()[0])

                pipes = self.get_random_pipes(SCREEN_WIDTH * 2)

                self.pipe_group.add(pipes[0])
                self.pipe_group.add(pipes[1])

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos=None):
        pygame.sprite.Sprite.__init__(self)
        if xpos is None:
            self.ground_group = pygame.sprite.Group()
            return
        else:
            self.image = pygame.image.load('assets/base.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

            self.mask = pygame.mask.from_surface(self.image)

            self.rect = self.image.get_rect()
            self.rect[0] = xpos
            self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
        
    def update(self):
        self.rect[0] -= GAME_SPEED
    def generate_ground(self):
        for i in range(2):
            ground = Ground(GROUND_WIDTH * i)
            self.ground_group.add(ground)
    def remove_ground(self):
        if is_off_screen(self.ground_group.sprites()[0]):
                self.ground_group.remove(self.ground_group.sprites()[0])

                new_ground = Ground(GROUND_WIDTH - 20)
                self.ground_group.add(new_ground)

def restart_button():
    pygame.draw.rect(screen, 255, 0, 0, (350, 250, 100, 50))
    fonte = pygame.font.Font(None, 36)
    texto = fonte.render("Restart", True, (255, 255, 255))
    screen.blit(texto, (360, 260))

