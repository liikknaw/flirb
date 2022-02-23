import pygame
import os
import sys
import random
import json

# pylint: disable=no-member
pygame.init()
pygame.mixer.pre_init(frequency=44100, size=16,channels=1, buffer=512)

def getHighScore():
    with open('data/save.dat', 'r') as save_file:
        if os.stat('data/save.dat').st_size == 0:
            save_file.close()
            return 0
        else:
            highestScore = json.load(save_file)
            save_file.close()
            return highestScore

#Muuttujia
screen_w = 576
screen_h = 1024
gravity = 0.20
birb_movement = 0
Game_on = True
score = 0
high_score = getHighScore()


birb_icon = pygame.image.load('data/assets/yellowbird-upflap.png')
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Flirb")
pygame.display.set_icon(birb_icon)
clock = pygame.time.Clock()


#Birb
birb_up = pygame.transform.scale2x(pygame.image.load('data/assets/yellowbird-upflap.png').convert_alpha())
birb_down = pygame.transform.scale2x(pygame.image.load('data/assets/yellowbird-downflap.png').convert_alpha())
birb_mid = pygame.transform.scale2x(pygame.image.load('data/assets/yellowbird-midflap.png').convert_alpha())

animFrames = [birb_up, birb_mid, birb_down]
birb_ind = 0

birb_surface = animFrames[birb_ind]
birb_rect = birb_surface.get_rect(center = (100,512))

BIRBFLAP = pygame.USEREVENT +1
pygame.time.set_timer(BIRBFLAP, 200)

#birb_surface = pygame.image.load('data/assets/yellowbird-upflap.png').convert_alpha()
#birb_surface = pygame.transform.scale2x(birb_surface)
#birb_rect = birb_surface.get_rect(center = (100, 512))

def rotateBirb(birb):
    new_birb = pygame.transform.rotozoom(birb, birb_movement*-3, 1)
    return new_birb

def birb_anim():
    new_birb = animFrames[birb_ind]
    new_birb_rect = new_birb.get_rect(center = (100, birb_rect.centery))
    return new_birb, new_birb_rect

#Putket
pipeImg = pygame.image.load('data/assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipeImg)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipePosList = [400, 600, 800, (screen_h-224)]

def makePipe():
    random_pipe = random.choice(pipePosList)
    random_gap = random.choice([250, 400, 600])
    bottom_pipe = pipe_surface.get_rect(midtop = (screen_w, random_pipe))
    top_pipe = pipe_surface.get_rect(midbottom = (screen_w, random_pipe-random_gap))
    return top_pipe, bottom_pipe

def movePipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def drawPipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= screen_h:
            screen.blit(pipe_surface, pipe)
        else:
            flipped_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flipped_pipe, pipe)

def collision_det(pipes):
    for pipe in pipes:
        if(birb_rect.colliderect(pipe)):
            hits.play()
            return False
    
    if(birb_rect.top <= -75 or birb_rect.bottom >= (screen_h-200)):
        return False
    
    return True

#tausta
bgImg = pygame.image.load('data/assets/background-day.png').convert()
bg_surface = pygame.transform.scale(bgImg, (screen_w, screen_h))


#maa
floorImg = pygame.image.load('data/assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floorImg)
floor_x = 0

def draw_floor():
    screen.blit(floor_surface, (floor_x, 900))
    screen.blit(floor_surface, (floor_x + 576, 900))

#Scores
fontti = pygame.font.Font('data/assets/04b_19__.TTF', 80)

game_over_surface = pygame.transform.scale2x(pygame.image.load('data/assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (screen_w/2, screen_h/2))

def show_score(game_state):
    if(game_state == 'main'):
        score_surface = fontti.render((str(int(score))), False, (250,241,210))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)
    elif(game_state == 'game_over'):
        score_surface = fontti.render(str(f'Score: {int(score)}'), False, (250,241,210))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)

        
        high_score_surface = fontti.render(str(f'High Score: {int(high_score)}'), False, (250,241,210))
        high_score_rect = high_score_surface.get_rect(center = (288, 850))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if(score > high_score):
        high_score = score
    return high_score


#Tallennus
def save(highScore):
    with open('data/save.dat', 'r') as save_file:
        if os.stat('data/save.dat').st_size == 0:
            with open('data/save.dat', 'w') as save_file:
                json.dump(highScore, save_file)
                save_file.close()
        else:
            with open('data/save.dat') as save_file:
                highestScore = json.load(save_file)
                if(highScore > highestScore):
                    with open('data/save.dat', 'w') as save_file:
                        json.dump(highScore, save_file)
                        save_file.close()

#Äänet
flaps = pygame.mixer.Sound('data/sounds/sfx_wing.wav')
hits = pygame.mixer.Sound('data/sounds/sfx_hit.wav')
points = pygame.mixer.Sound('data/sounds/sfx_point.wav')
point_counter = 100


#=============================================================G A M E  L O O P=======================================
while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save(int(high_score))
            pygame.quit()
            sys.exit()

        #Keyboard events
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_ESCAPE):
                save(high_score)
                pygame.quit()
                sys.exit()

            if(event.key == pygame.K_SPACE):
                birb_movement = 0
                birb_movement -= 6.5
                flaps.play()

            if(event.key == pygame.K_SPACE and Game_on == False):
                Game_on = True
                pipe_list.clear()
                birb_rect.center = (100, 512)
                birb_movement = 0
                score = 0
                point_counter = 100

            if(event.key == pygame.K_z):
                pipe_list.pop()
                pipe_list.pop()

        if(event.type == SPAWNPIPE):
            pipe_list.extend(makePipe())

        if(event.type == BIRBFLAP):
            if(birb_ind < 2):
                birb_ind += 1
            else:
                birb_ind = 0
            
            birb_surface,birb_rect = birb_anim()

    #Tausta
    screen.blit(bg_surface, (0,0))

    if(Game_on):
        #Birb handles
        birb_movement += gravity
        birb_rot = rotateBirb(birb_surface)
        birb_rect.centery += birb_movement
        screen.blit(birb_rot, birb_rect)
        
        Game_on = collision_det(pipe_list)
    
        #Pipes
        pipe_list = movePipes(pipe_list)
        drawPipes(pipe_list)

        #Score
        score += 0.01
        point_counter -= 1
        show_score('main')
        if(point_counter <= 0):
            points.play()
            point_counter = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        show_score('game_over')

    #Maa
    draw_floor()
    if(floor_x <= -576):
        floor_x = 0
    else:
        floor_x -= 1

    pygame.display.update()
    clock.tick(120)