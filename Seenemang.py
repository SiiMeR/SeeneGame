__author__ = 'Siim ja Mari-Liis'
# -*- coding:utf-8 -*-
import sys
import os
import pygame
import math
from pygame import *
from random import getrandbits


resolutsioon = (800,640)
aken = pygame.display.set_mode(resolutsioon, 0, 32) # akna reso ja bit-depth
taust = Surface((800, 640))
taust.convert()
taust.fill(Color(40, 200, 60))
tile_group = pygame.sprite.Group()
elusid = 3
class Tile(pygame.sprite.Sprite): # klass ruudukeste joonistamiseks
    def __init__(self, x, y, HasShroom):
        pygame.sprite.Sprite.__init__(self)
        self.has_shroom = HasShroom
        if self.has_shroom:
            self.image = pygame.transform.scale(pygame.image.load('seen.bmp'), (75, 75)) # seentega ruutude pilt
        elif not self.has_shroom:
            self.image = pygame.transform.scale(pygame.image.load('selg.jpg'), (75, 75)) # seenteta ruutude pilt
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y
        self.starttick = pygame.time.get_ticks()
        self.pööratud = False

    def update(self):
        if pygame.time.get_ticks() - self.starttick > 2000 and not self.pööratud:
            self.image = pygame.transform.scale(pygame.image.load("selg.jpg"), (75,75)) # kinnikatmise pilt
            self.pööratud = True

    def flip(self):  # ruutude ümberkeeramise funktsioon
        pass

def main():

    pygame.init()         # paneme akna käima
    pygame.mixer.init()   # muusika
    display.set_caption("Seenekas")
    timer = time.Clock()
    joonistaruudustik()


    while True:  # gameloop, mis käib kuni lõppu jõuame
            timer.tick(60)  # maxfps, üle selle programm kunagi ei saa joosta, hoiab jõudlust kokku
            for event in pygame.event.get():  # võimaldab kasutajal väljuda x nuppu kastuades, või väljuda siis, kui programm ütleb seda
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    #ruut = tile(200,200,False)

               #     if ruut.collidepoint(pos):
               #         tile_group.flip()
                if event.type == QUIT:
                    return  # murrab True loopist välja
            aken.blit(taust, (0, 0))  #  pane taust ekraanile, alustades koordinaatidelt 0,0

            joonistatekst()
            tile_group.draw(aken)
            tile_group.update()

            pygame.display.flip()


def joonistaruudustik():
    for i in range(160,600,100):
        for j in range(100,600,100):
            teeseen = bool(getrandbits(1))
            tile_group.add(Tile(i, j, teeseen))
    aken.blit(taust, (0,0))

def joonistatekst():  # kõik tekstid, mida on vaja ekraanile kuvada
    font = pygame.font.SysFont("impact", 30)

    eluluger = "ELUSID : " + " " "süda " * elusid
    tekst = font.render(eluluger, 1, (0,0,0))
    aken.blit(tekst, (10,10))   # pane see tekst ekraanile


main()  # mäng tööle
