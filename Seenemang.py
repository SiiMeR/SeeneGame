import pygame
from pygame import *
from random import getrandbits
import dumbmenu as dm
from pygame.locals import *
from time import sleep

__author__ = 'Siim ja Mari-Liis'


# -*- coding:utf-8 -*-

resolutsioon = (800, 600)
aken = pygame.display.set_mode(resolutsioon, 0, 32)  # akna reso ja bit-depth

taust = Surface((800, 600))
taust.convert()

tile_group = pygame.sprite.Group()

elusid = 3
seeni = 0

ikoon = pygame.image.load("seen.png")
pygame.display.set_icon(ikoon)

võitja = pygame.image.load('victory.png')
kaotaja = pygame.image.load('loss.png')
taustapilt = pygame.image.load("plats.png")

valmis = False

punane = 255, 0, 0
roheline = 0, 255, 0
sinine = 0, 0, 255



class Tile(pygame.sprite.Sprite):  # klass ruudukeste jaoks
    def __init__(self, x, y, HasShroom):
        pygame.sprite.Sprite.__init__(self)
        self.has_shroom = HasShroom
        if self.has_shroom:
            self.image = pygame.transform.scale(pygame.image.load('seen.png'), (75, 75))  # seentega ruutude pilt
        elif not self.has_shroom:
            self.image = pygame.transform.scale(pygame.image.load('selg.jpg'), (75, 75))  # seenteta ruutude pilt
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y
        self.starttick = pygame.time.get_ticks()
        self.pööratud = False

    def update(self):
        global valmis
        if pygame.time.get_ticks() - self.starttick > 2000 and not self.pööratud:
            self.image = pygame.transform.scale(pygame.image.load("selg.jpg"), (75, 75))  # kinnikatmise pilt
            self.pööratud = True
            valmis = True

    def poora(self):  # ruutude ümberkeeramise funktsioon
        global elusid, seeni

        if self.has_shroom:
            seeni -= 1
            self.kill()
            pauk1 = pygame.mixer.Sound('blast1.wav')
            pauk1.set_volume(.3)
            pauk1.play()
        elif not self.has_shroom:
            elusid -= 1
            valevalik = pygame.mixer.Sound('wrong.ogg')
            valevalik.play()


def menu():
    ekraan = pygame.display.set_mode(resolutsioon)
    while True:
        ekraan.fill(Color(255, 255, 0))
        pygame.display.update()
        pygame.key.set_repeat(500,40)
        valik = dm.dumbmenu(ekraan, ['Alusta mängu',
                                     'Lõpeta mäng'], 300, 250, "comicsansms", 32, 0.5, Color(0, 0, 0), Color(0, 0, 0))

        if valik == 0:
            return
        elif valik == 1:
            pygame.quit()
            exit()


def main():

    pygame.init()         # paneme akna käima
    pygame.mixer.init()   # muusika
    display.set_caption("Seenekas")
    timer = time.Clock()
    joonistaruudustik()

    while True:  # gameloop, mis käib kuni lõppu jõuame
            elukontroller()
            if seeni == 0:
                võit()
            timer.tick(60)  # maxfps, üle selle programm kunagi ei saa joosta, hoiab jõudlust kokku
            for event in pygame.event.get():  # võimaldab kasutajal väljuda x nuppu kastuades, või väljuda siis, kui programm ütleb seda
                if event.type == pygame.KEYDOWN and event.key == K_F1:
                    alustauuesti()
                if event.type == pygame.MOUSEBUTTONDOWN and valmis:
                    if event.button == 1:
                        hiire_asukoht = event.pos
                        for spr in tile_group:
                           if spr.rect.collidepoint(hiire_asukoht):
                               spr.poora()



                if event.type == QUIT:
                    return  # murrab True loopist välja
            aken.blit(taustapilt, (0, 0))  #  pane taust ekraanile, alustades koordinaatidelt 0,0

            joonistatekst()
            tile_group.draw(aken)
            tile_group.update()

            pygame.display.flip()


def joonistaruudustik():
    global seeni
    tile_group.empty()
    for i in range(160,600,100):
        for j in range(100,600,100):
            onseen = bool(getrandbits(1))
            if onseen:
                seeni += 1
            tile_group.add(Tile(i, j, onseen))
    aken.blit(taust, (0,0))


def joonistatekst():  # kõik tekstid, mida on vaja ekraanile kuvada

    font = pygame.font.Font("joystixmonospace.ttf", 29)

    seeneluger = "SEENI  : " + str(seeni)
    eluluger = "ELUSID : " + "SÜDA " * elusid

    elutekst = font.render(eluluger, 1, (125,0,0))
    seenetekst = font.render(seeneluger, 1, (125,0,0))

    aken.blit(seenetekst, (10,45))
    aken.blit(elutekst, (10,10))


def elukontroller():
    if elusid == 0 or elusid < 0:
        kaotus()


võitja_rect = võitja.get_rect()
kaotaja_rect = kaotaja.get_rect()


def võit():
    pygame.mixer.music.load('V_IT_.ogg')
    pygame.mixer.music.play()
    while True:
        aken.blit(võitja,võitja_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()


def kaotus():
    pygame.mixer.music.load('youlose.ogg')
    pygame.mixer.music.play()

    for aeg in range(1,3):
        aken.blit(kaotaja,kaotaja_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
        sleep(1)
    alustauuesti()

def alustauuesti():
    global elusid, seeni
    font = pygame.font.SysFont("comicsansms", 40)
    uuestitekst = "Kas soovid uuesti alustada?"
    uuestirender = font.render(uuestitekst, 1, (0,0,0))
    aken.fill(Color(255, 255, 0))
    while True:
        aken.blit(uuestirender, (150, 150))

        pygame.display.update()
        pygame.key.set_repeat(500,40)
        valik = dm.dumbmenu(aken, ['Jah',
                                     'Ei'], 340, 250, "comicsansms", 32, 0.5, Color(0, 0, 0), Color(0, 0, 0))

        if valik == 0:
            seeni = 0
            elusid = 3
            main()

        elif valik == 1:
            pygame.quit()
            exit()


def intro():   # ma loodan et sony mind maha ei löö // tegelt on see ajutine video algul

    pygame.mixer.quit()
    movie = pygame.movie.Movie('startupm.mpg')
    screen = pygame.display.set_mode(movie.get_size())
    movie_screen = pygame.Surface(movie.get_size()).convert()
    movie.set_display(movie_screen)
    movie.play()

    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                movie.stop()
                playing = False
        if not movie.get_busy():
            return

        screen.blit(movie_screen,(0,0))
        pygame.display.update()

#intro()
menu()
main()
alustauuesti()