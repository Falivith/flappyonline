import pygame, random
import time
from pygame.locals import *
from network import Network

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800

SPEED = 2
GRAVITY = 0.2
GAME_SPEED = 2

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 200

pygame.display.set_caption("Flappy Bird Online")

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

    def __init__(self, color, startPos=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)):
        pygame.sprite.Sprite.__init__(self)

        bluebird_images = [
            pygame.image.load('bluebird-upflap.png').convert_alpha(),
            pygame.image.load('bluebird-midflap.png').convert_alpha(),
            pygame.image.load('bluebird-downflap.png').convert_alpha()
        ]

        yellowbird_images = [
            pygame.image.load('yellowbird-upflap.png').convert_alpha(),
            pygame.image.load('yellowbird-midflap.png').convert_alpha(),
            pygame.image.load('yellowbird-downflap.png').convert_alpha()
        ]

        self.images = bluebird_images if color == "blue" else yellowbird_images
        
        self.y = SPEED

        self.current_image = 0

        self.image = pygame.image.load('bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.rect[0] = startPos[0] #x
        self.rect[1] = startPos[1] #y

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]

        self.y += GRAVITY

        # Update y
        self.rect[1] += self.y
    
    def bump(self):
        self.y = -SPEED

class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH,PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
    
    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)

def restart_button():
    pygame.draw.rect(screen, 255, 0, 0, (350, 250, 100, 50))
    fonte = pygame.font.Font(None, 36)
    texto = fonte.render("Restart", True, (255, 255, 255))
    screen.blit(texto, (360, 260))

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

start_img = pygame.image.load('start_btn.png').convert_alpha()
exit_img = pygame.image.load('exit_btn.png').convert_alpha()

BACKGROUND = pygame.image.load('background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

bird_group = pygame.sprite.Group()
bird1 = Bird("blue")
bird_group.add(bird1)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])


clock = pygame.time.Clock()
start_button = Button(100, 200, start_img, 0.8)
exit_button = Button(115, 380, exit_img, 0.8)

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[0])
def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])    

def initGame(n, player):

    startPos = n.getPos()
    bird_group.empty()
    
    bird1 = Bird("blue", (startPos[0], startPos[1]))
    bird2 = Bird("yellow", (startPos[0], startPos[1]))
    
    bird_group.add(bird1)
    bird_group.add(bird2)

    ground_group.empty()

    for i in range(2):
        ground = Ground(GROUND_WIDTH * i)
        ground_group.add(ground)

    pipe_group.empty()

    for i in range(2):
        pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    while True:

        clock.tick(30)

        # Atualização da posição do player 2 no cliente do player 1

        if (player == 0):

            pos_str_tuple = make_pos((bird1.rect[0], bird1.rect[1]))
            print("Tupla criada no cliente:", pos_str_tuple, " Tipo do dado: ", type(pos_str_tuple))
            recv_str_tuple = n.send(pos_str_tuple)
            print("Tupla recebida no cliente:", recv_str_tuple, " Tipo do dado: ", type(recv_str_tuple))
            p2_pos = read_pos(recv_str_tuple)
            print("Nova Posição Pronta:", p2_pos, " Tipo do dado: ", type(p2_pos))

            bird2.rect[0] = p2_pos[0]
            bird2.rect[1] = p2_pos[1]

            bird2.update()

        # Atualização da posição do player 1 no cliente do player 2

        elif (player == 1):

            pos_str_tuple = make_pos((bird2.rect[0], bird2.rect[1]))
            print("Tupla criada no cliente:", pos_str_tuple, " Tipo do dado: ", type(pos_str_tuple))
            recv_str_tuple = n.send(pos_str_tuple)
            print("Tupla recebida no cliente:", recv_str_tuple, " Tipo do dado: ", type(recv_str_tuple))
            p1_pos = read_pos(recv_str_tuple)
            print("Nova Posição Pronta:", p1_pos, " Tipo do dado: ", type(p1_pos))

            bird1.rect[0] = p1_pos[0]
            bird1.rect[1] = p1_pos[1]

            bird1.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if player == 0:
                        bird1.bump()
                    else:
                        bird2.bump()

        screen.blit(BACKGROUND, (0, 0))

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])

            new_ground = Ground(GROUND_WIDTH - 20)
            ground_group.add(new_ground)

        if is_off_screen(pipe_group.sprites()[0]):
            pipe_group.remove(pipe_group.sprites()[0])
            pipe_group.remove(pipe_group.sprites()[0])

            pipes = get_random_pipes(SCREEN_WIDTH * 2)

            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])

        bird_group.update()
        ground_group.update()
        pipe_group.update()

        bird_group.draw(screen)
        pipe_group.draw(screen)
        ground_group.draw(screen)

        pygame.display.update()

        if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
                pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
            # Game over
            bird_group.empty()
            ground_group.empty()
            pipe_group.empty()
            time.sleep(1)
            return

def start():

    n = Network()
    print(f"Posição do Player  <{n.player}> : <{n.getPos()}>")
    run = True

    while run:

        screen.fill((202, 228, 241))

        if start_button.draw(screen):
            initGame(n, int(n.player))

        if exit_button.draw(screen):
            pygame.quit()

        #event handler
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

start()
