import pygame, random
import time
from config import make_pos, read_pos
from flappy import Pipe,Ground,Bird,Button,screen, SCREEN_HEIGHT,SCREEN_WIDTH
from pygame.locals import *
from network import Network

pygame.display.set_caption("Flappy Bird Online")
pygame.init()

bird_group = pygame.sprite.Group()

def initGame(n):
    clock = pygame.time.Clock()
    pipes = Pipe()
    ground = Ground()
    
    BACKGROUND = pygame.image.load('assets/background-day.png')
    BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    pipes.generate_pipes()
    ground.generate_ground()

    startPos = n.getPos()
    bird_group.empty()

    print("StartPos", startPos)

    bird1 = Bird("blue", (205, 405))
    bird2 = Bird("yellow", (205, 405))

    bird_group.add(bird1)
    bird_group.add(bird2)

    while True:
        clock.tick(60)
        pygame.display.update()

        pos_str_tuple = make_pos((bird1.rect[0], bird1.rect[1]))

        print("Envio: ",  pos_str_tuple)
        recv_str_tuple = n.send(pos_str_tuple)
        p2_pos = read_pos(recv_str_tuple)

        print("Recebi: ", p2_pos)

        bird2.rect[0] = p2_pos[0]
        bird2.rect[1] = p2_pos[1]

        bird_group.update()

        for event in pygame.event.get():
            if event.type ==   QUIT:
                pygame.quit()

        bird1.bump()

        ground.ground_group.update()
        pipes.pipe_group.update()

        screen.blit(BACKGROUND, (0, 0))

        pipes.remove_pipes()
        ground.remove_ground()

        bird_group.draw(screen)
        pipes.pipe_group.draw(screen)
        ground.ground_group.draw(screen)

        pygame.display.update()

        if (pygame.sprite.groupcollide(bird_group, ground.ground_group, False, False, pygame.sprite.collide_mask) or
                pygame.sprite.groupcollide(bird_group, pipes.pipe_group, False, False, pygame.sprite.collide_mask)):
            # Game over
            bird_group.empty()
            ground.ground_group.empty()
            pipes.pipe_group.empty()
            time.sleep(1)
            return
        
def start():
    bg = pygame.image.load("assets/background-day.png").convert_alpha()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    start_img = pygame.image.load('assets/start_btn.png').convert_alpha()
    exit_img = pygame.image.load('assets/exit_btn.png').convert_alpha()

    start_button = Button(100, 200, start_img, 0.8)
    exit_button = Button(115, 380, exit_img, 0.8)

    n = Network()

    run = True

    while run:

        screen.blit(bg, (0, 0))
        
        if start_button.draw(screen):

            print("Waiting")

            while n.ready() == "Not":
                time.sleep(0.1)
                pass

            print("Started")

            initGame(n)

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