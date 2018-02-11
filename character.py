import pygame
from pygame import *
import glob


def overlap_y(r1,r2):
    return r1[1]+r1[3]-r2[1]

def overlap_x(r1,r2):
    return r1[0]+r1[2]-r2[0]

class Dog(pygame.sprite.Sprite):
    folder = "image"
    standing = 1

    def __init__(self,position):
        self.sound_jump = pygame.mixer.Sound("sound\jump.wav")
        self.top_offset = 30
        self.time = 0
        self.speed_x = 0
        self.speed_y = -5
        self.jumping = 0
        img_list = glob.glob("image\*gif")
        self.right = []
        self.left = []
        for img in img_list:
            image = pygame.image.load(img)
            image = pygame.transform.scale(image,(100,100))
            self.right.append(image)
            image = pygame.transform.flip(image,True,False)
            self.left.append(image)
        pygame.sprite.Sprite.__init__(self)
        self.value = Dog.standing
        self.image = self.right[self.value]


        self.rect = self.image.get_rect()

        self.bottom = 0
        self.rightmost = 0
        self.top = 0
        self.rect.center = position
        self.update_pos()


    def collide(self,terrain):
        return (terrain.rect.colliderect(self.bottom),terrain.rect.colliderect(self.top),terrain.rect.colliderect(self.rightmost))


    def update_pos(self):
        self.bottom = pygame.Rect(self.rect[0],self.rect.bottom,round(self.rect[2]*0.75 ),1)
        self.top = pygame.Rect(self.rect[0],self.rect.top+self.top_offset,1,1)
        self.rightmost = pygame.Rect(self.rect.right,round((self.rect.top+self.rect.bottom)/2),10,round(self.rect[3]*0.25))

    def jump(self):
        if self.jumping == 0 and self.speed_y!=-5:
            self.speed_y = self.speed_y - 1
        elif self.jumping!=0:
            if(self.speed_y<0):
                self.speed_y = 0
            if self.speed_y<6:
                self.speed_y = self.speed_y + 1
            self.jumping = (self.jumping + 1)%50

    def update(self,cur_time,terrain,event):
        if(cur_time-self.time>0.1):
            self.value = (self.value + 1) % len(self.right)
            self.image = self.right[self.value]
            self.time = cur_time



        # Update physic for character
        x,y = self.rect.center
        self.rect.center = (x+self.speed_x, y - self.speed_y)
        self.update_pos()
        collided = False
        for ter in terrain:
            bt,tp,rm = self.collide(ter)
            o_x = 0
            o_y = 0
            if bt:
                collided = True
                o_y = overlap_y(self.rect,ter.rect)
            if rm:
                o_x = overlap_x(self.rect,ter.rect)
            if tp:
                o_y = -overlap_y(ter.rect,self.rect) + self.top_offset
            x,y = self.rect.center
            self.rect.center = (x-o_x,y-o_y)
            self.update_pos()


        self.jump()

        if event.type == KEYDOWN and self.jumping == 0 and collided:

            self.sound_jump.play()
            self.jumping = 1





