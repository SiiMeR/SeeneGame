import pygame
from pygame import *
from random import getrandbits
import dumbmenu as dm
from pygame.locals import *
from time import sleep
from hollow import *

__author__ = 'Siim ja Mari-Liis'


# -*- coding:utf-8 -*-

resolutsioon = (800, 600)
aken = pygame.display.set_mode(resolutsioon, 0, 32)  # akna reso ja bit-depth

taust = pygame.image.load('bgtitle.png')
taust.convert()

tile_group = pygame.sprite.Group()

elusid = 3
seeni = 0
maxseeni = 0

ikoon = pygame.image.load("seen.png")
pygame.display.set_icon(ikoon)

voitja = pygame.image.load('victory.png')
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
            self.image = pygame.transform.scale(pygame.image.load('puravik.png'), (75, 75))  # seenteta ruutude pilt
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y
        self.starttick = pygame.time.get_ticks()
        self.pooratud = False

    def update(self):
        global valmis
        if pygame.time.get_ticks() - self.starttick > 2000 and not self.pooratud:
            self.image = pygame.transform.scale(pygame.image.load("mida.png"), (75, 75))  # kinnikatmise pilt
            self.pooratud = True
            valmis = True

    def poora(self):
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
    global maxseeni
    while True:
        aken.blit(taust,(0,0))

        pygame.key.set_repeat(500,40)
        valik = dm.dumbmenu(aken, ['Alusta',
                                   "Juhised",
                                     'Lahku'], 305, 200, "joystixmonospace.ttf", 35, 0.5, Color(0, 0, 0), Color(0, 0, 0), True, Color(255,150,0)) # viimane Color vahetab outline colorit
        pygame.display.update()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                raise SystemExit
        if valik == 0:
            font = pygame.font.Font("joystixmonospace.ttf", 35)

            aken.blit(taust,(0,0))
            raskusastetekst = "Vali raskusaste"
            raskusastetekstrender = textOutline(font, raskusastetekst, (0,1,0),(255,150,0))
            aken.blit(raskusastetekstrender, (175,100))
            valik2 = dm.dumbmenu(aken, ['Kerge',
                                     'Keskmine',
                                        "Raske",
                                        "Tagasi"], 305, 200, "joystixmonospace.ttf", 35, 0.5, Color(0, 0, 0), Color(0, 0, 0), True, Color(255,150,0))
            if valik2 == 0:
                maxseeni = 4
                return
            elif valik2 == 1:
                maxseeni = 8
                return
            elif valik2 == 2:
                maxseeni = 12
                return
            elif valik2 == 3:
                valik
        elif valik == 1:
            aken.blit(taust,(0,0))

            font = pygame.font.Font("joystixmonospace.ttf", 29)
            juhenditekst  = "Vajuta küsimärkide peale peale,"
            juhenditekst3 = "kus olid kärbseseened(punased)."
            juhenditekst4 = "       Sul on 3 elu."
            juhenditekst5 = "Vajuta F1, et alustada uuesti."

            renderjuhend = textOutline(font, juhenditekst, (0,1,0),(255,150,0))
            #renderjuhend2 = textOutline(font, juhenditekst2, (0,1,0),(255,150,0))
            renderjuhend3 = textOutline(font, juhenditekst3, (0,1,0),(255,150,0))
            renderjuhend4 = textOutline(font, juhenditekst4, (0,1,0),(255,150,0))
            renderjuhend5 = textOutline(font, juhenditekst5, (0,1,0), (255,150,0))

            aken.blit(renderjuhend, (30,250))
            aken.blit(renderjuhend3, (30,300))
            aken.blit(renderjuhend4, (30,350))
            aken.blit(renderjuhend5, (30,400))

            juhend = dm.dumbmenu(aken,["Tagasi"],320,500, "joystixmonospace.ttf", 35,0.5, Color(0,0,0), Color(0,0,0), True, Color(255,150,0))
        elif valik == 2:
            raise SystemExit


def main():

    pygame.init()
    pygame.mixer.init()   # muusika
    display.set_caption("Seenekas")
    timer = time.Clock()
    joonistaruudustik()


    while True:

            elukontroller()
            if seeni == 0:
                voit()

            timer.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == K_F1:
                    alustauuesti()
                if event.type == pygame.MOUSEBUTTONDOWN and valmis:
                    if event.button == 1:
                        hiire_asukoht = event.pos
                        for spr in tile_group:
                           if spr.rect.collidepoint(hiire_asukoht):
                               spr.poora()



                if event.type == QUIT:
                    raise SystemExit

                    pygame.display.flip()
            aken.blit(taustapilt, (0, 0))  #  pane taust ekraanile, alustades koordinaatidelt 0,0

            joonistatekst()
            tile_group.draw(aken)
            tile_group.update()

            pygame.display.flip()


def joonistaruudustik():
    global seeni, maxseeni
    tile_group.empty()
    for i in range(160,600,100):
        for j in range(100,600,100):
            onseen = bool(getrandbits(1))
            if onseen and seeni != maxseeni:
                seeni += 1
                tile_group.add(Tile(i, j, onseen))
            else:
                tile_group.add(Tile(i,j,False))
    aken.blit(taust, (0,0))


def joonistatekst():

    syda = pygame.transform.scale(pygame.image.load('syda.png'), (40, 40))
    font = pygame.font.Font("joystixmonospace.ttf", 30)
    eluluger = "ELUSID : "
    seeneluger = "SEENI  : " + str(seeni)




    elutekst = textOutline(font,eluluger,(125,0,0),(0,1,0))
    seenetekst = textOutline(font,seeneluger,(125,0,0),(0,1,0))
    #elutekst = font.render(eluluger, 1, (125,0,0))
    #seenetekst = font.render(seeneluger, 1, (125,0,0))
    for i in range (0,elusid):
        for j in range(230,230 + (45 * elusid),45):
            aken.blit(syda, (j,10))

    aken.blit(seenetekst, (10,45))
    aken.blit(elutekst, (10,10))


def elukontroller():
    if elusid == 0 or elusid < 0:
        kaotus()


voitja_rect = voitja.get_rect()
kaotaja_rect = kaotaja.get_rect()

def voit():
    pygame.mixer.music.load('V_IT_.ogg')
    pygame.mixer.music.play()
    while True:
        aken.blit(voitja,voitja_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                raise SystemExit


def kaotus():
    pygame.mixer.music.load('gameover.wav')
    pygame.mixer.music.play()

    for aeg in range(1,3):
        aken.blit(kaotaja,kaotaja_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                raise SystemExit
        sleep(1)
    alustauuesti()

def alustauuesti():
    global elusid, seeni, valmis
    font = pygame.font.Font("joystixmonospace.ttf", 27)

    uuestitekst = "Kas soovid uuesti alustada?"

    uuestirender = textOutline(font, uuestitekst, (0,1,0),(255,150,0))
    aken.blit(taust,(0,0))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                raise SystemExit
        aken.blit(uuestirender, (100, 150))
        pygame.display.update()
        pygame.key.set_repeat(500,40)
        valik = dm.dumbmenu(aken, ['Jah',
                                     'Ei'], 340, 250, "joystixmonospace.ttf", 25, 0.5, Color(0, 0, 0), Color(0, 0, 0), True, Color(255,150,0))

        if valik == 0:
            seeni = 0
            elusid = 3
            valmis = False
            pygame.mixer.music.stop()
            main()

        elif valik == 1:
            raise SystemExit


def intro():

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
