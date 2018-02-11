import pygame
from pygame import *
import time
import sys
import character
import terrain
import random
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)


fps = pygame.time.Clock()
screen = pygame.display.set_mode((1024,768),HWACCEL)
pygame.mouse.set_pos(100,100)
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()
lost_game = pygame.mixer.Sound("sound/lost.wav")
background_sound = pygame.mixer.Sound("sound/background_sound_lvl1.wav")
background_sound.set_volume(0.2)
def main_game():
    background_sound.play(loops=-1,maxtime=0,fade_ms=5000)
    background = pygame.image.load("image/background0.png").convert()
    background = pygame.transform.scale(background,(1024,768))
    screen.blit(background,(0,0))
    terrain_render = pygame.sprite.RenderPlain()
    current_pos = 0
    for i in range(10):
        new_terrain = terrain.Terrain("image\PNG Grass",time.clock(),(current_pos,650),height = 2)
        current_pos = new_terrain.rect.right
        terrain_render.add(new_terrain)
    terrain_render.draw(screen)
    bulldog = character.Dog((500,350))
    character_render = pygame.sprite.RenderPlain(bulldog)
    character_render.draw(screen)
    pygame.display.update()


    while 1:
        fps.tick(120)
        if bulldog.rect.right<0 or bulldog.rect.top>768:
            background_sound.stop()
            lost_game.play()
            time.sleep(lost_game.get_length()-0.2)
            sys.exit(0)
        event = pygame.event.poll()
        if event.type == QUIT:
            sys.exit(0)
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit(0)
        if not pygame.mouse.get_focused():
            terrain_render.update(time.clock(),True)
            continue
        screen.blit(background,(0, 0))
        character_render.update(time.clock(),terrain_render,event)
        character_render.draw(screen)

        terrain_render.update(time.clock())
        for terr in terrain_render:
            gg = terr.rect
            if gg[0]+gg[2]<0:
                terrain_render.remove(terr)

        while len(terrain_render.sprites())<15:
            current_pos = 0
            jump = 0
            for ter in terrain_render:
                current_pos = max(current_pos,ter.rect.right)
            height = 1
            jump = random.choice([0,200])
            if jump:
                height= random.randint(2,3)
            else:
                height = random.randint(1,4)
            new_terrain = terrain.Terrain("image\PNG Grass",time.clock(),(current_pos+jump,650),height = height)
            terrain_render.add(new_terrain)
        terrain_render.draw(screen)
        pygame.draw.rect(screen,(0,0,0),bulldog.top)
        pygame.display.flip()


main_game()