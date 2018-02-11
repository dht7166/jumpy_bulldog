import pygame
from pygame import *
import glob
import time
import sys


class Terrain(pygame.sprite.Sprite):
    def __init__(self,folder,time,position,width = 1,height = 1):
        self.time = time
        pygame.sprite.Sprite.__init__(self)
        self.folder = folder
        img_list = glob.glob(str(folder)+"\*.png")
        self.image_list = []
        for img in img_list:
            image = pygame.image.load(img).convert()
            image = pygame.transform.scale(image,(200*width,100*height))
            self.image_list.append(image)
        self.image = self.image_list[6]
        self.rect = self.image.get_rect()
        x,y = position
        y = y - 100*(height-1)
        position = (x,y)
        self.rect.topleft = position


    def update(self, cur_time,idle = False):
        if idle:
            self.time = cur_time
        else:
            delta = cur_time-self.time
            offset = round(delta*300,0)
            x,y = self.rect.center
            self.rect.center = (x-offset,y)
            self.time = cur_time