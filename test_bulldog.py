import pygame
from pygame import *
import time
import sys
import character
import terrain
import random


fps = pygame.time.Clock()
screen = pygame.display.set_mode((1024,768),HWACCEL)


def main_game():

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
        if bulldog.rect.left<0 or bulldog.rect.bottom>768:
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
            jump = random.randint(0,200)
            if jump >100:
                height= random.randint(2,4)
            new_terrain = terrain.Terrain("image\PNG Grass",time.clock(),(current_pos+jump,650),height = height)
            terrain_render.add(new_terrain)
        terrain_render.draw(screen)
        pygame.draw.rect(screen,(0,0,0),bulldog.top)
        pygame.display.flip()




main_game()