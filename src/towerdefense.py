#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/
#
# Original Coder: Austin Morgan (codenameduckfin@gmail.com)
# Version: 0.6.0
#
# If altering the code, please keep this comment box at least. Also, please
# comment all changes or additions with two pound signs (##), so I can tell what's
# been changed and what hasn't. Adding another comment box below this one with your
# name will insure any additions or changes you made that make it into the next version
# will be credited to you. Preferably, you'd leave your email and a little description
# of your changes, but that's not absolutely needed.
#
# License:
# All code and work contained within this file and folder and package is open for
# use, however please include at least a credit to me and any other coders working
# on this project.
#
#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/
#
# Version 0.7.0
# Things to add/change:
#   More towers.
#   BETTER GRAPHICS!
#   SOUND/MUSIC!
#
#   Make updates more frequently :)
#
#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/

##/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#
##
## Gabriel Lazarini Baptistussi (gabrielbap1@gmail.com)
##
## I just made a small change in localclasses.Enemy.move(), now the enemies
## have a different picture for each direction they are moving.
##
##/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#

import sys
import pygame
from pygame.locals import *
from localdefs import *
from localclasses import *
from abilities import *
from mapmenu import pickMap
from SenderClass import Sender
import MainFunctions
import EventFunctions
import time
from RollFunctions import d

def main():
    pygame.init()
    print "Pygame Initialized"
    pygame.display.set_caption("PyGame Tower Defence Game")
    pygame.mouse.set_visible(1)
    #localdefs: mapvar = Map()
    background = mapvar.loadMap((scrwid,scrhei),pickMap())
    print "Map Object Generated"
    screen = pygame.display.set_mode((scrwid,scrhei))
    print "Display Initialized"
    clock = pygame.time.Clock()
    genEnemyImageArray() #localdefs
    print "Enemy Image Array Generated"
    run=True #Run loop
    wavenum = 0
    selected = None #Nothing is selected

    MainFunctions.makeIcons()
    
    #Openbutton is the white surface on which the Icon sits
    openbutton = pygame.Surface((iconlist[len(iconlist)-1].rect.right+5,25))
    openbuttonrect = pygame.Rect((0,scrhei-25),(iconlist[len(iconlist)-1].rect.right+5,25))
    openbutton.fill((255,255,255))
    print "Begin Play Loop!!!"
    speed = 3
    frametime = speed/30.0
    while run:
        starttime = time.time()

        MainFunctions.tickAndClear(screen, clock, background)

        MainFunctions.workSenders(frametime)

        MainFunctions.workTowers(screen,frametime)

        MainFunctions.dispExplosions(screen)

        MainFunctions.dispText(screen,wavenum)

        MainFunctions.workEnemies(screen,frametime)

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                #If the user left-clicks...
                if event.dict['button']==1:
                    if nexttextpos.collidepoint(event.dict['pos']):
                        wavenum+=1
                        player.health += d(8) + 2
                        for tower in towerlist:
                            if tower.hp < tower.maxhp:
                                tower.hp = min(tower.hp+tower.level,tower.maxhp)
                        if ('wave'+str(wavenum)+'a') in mapvar.mapdict:
                            Sender(wavenum,'a')
                        if ('wave'+str(wavenum)+'b') in mapvar.mapdict:
                            Sender(wavenum,'b')
                        if ('wave'+str(wavenum)+'c') in mapvar.mapdict:
                            Sender(wavenum,'c')
                        if ('wave'+str(wavenum)+'d') in mapvar.mapdict:
                            Sender(wavenum,'d')
                        if all([('wave'+str(wavenum)+letter) not in mapvar.mapdict for letter in ['a','b','c','d']]):
                            if len(enemylist) == 0:
                                background=mapvar.loadMap((scrwid,scrhei),pickMap())
                                screen = pygame.display.set_mode((scrwid,scrhei))
                                wavenum=1
                            else:
                                print "There are still enemies on the screen!"
                                wavenum-=1
                    elif selected:
                        if selected.__class__ == Icon:
                            if event.dict['pos'][1]<scrhei-squsize:
                                if player.money>=eval(selected.type+"Tower").basecost:
                                    if (not any([ttower.rect.collidepoint(event.dict['pos']) for ttower in towerlist])
                                        and not any([p.inflate(25,25).collidepoint(event.dict['pos']) for pathrectlist in mapvar.pathrectlists for p in pathrectlist])):
                                        eval(selected.type+selected.base)(event.dict['pos'])
                                        selected = None
                            else:
                                selected = None
                        elif Tower in selected.__class__.__bases__:
                            EventFunctions.leftSelectedTower(event, selected)
                    else:
                        for object in (towerlist+iconlist):
                            if object.rect.collidepoint(event.dict['pos']):
                                selected = object
                else:
                    selected = None
            keyinput = pygame.key.get_pressed()
            if event.type == QUIT:
                sys.exit()
            if keyinput[K_ESCAPE]:
                sys.exit()
            if keyinput[K_f]:
                screen = pygame.display.set_mode((scrwid,scrhei),FULLSCREEN)
            if keyinput[K_w]:
                screen = pygame.display.set_mode((scrwid,scrhei))

        font = pygame.font.Font(None,20)

        MainFunctions.dispStructures(screen)

        nexttextpos = MainFunctions.dispNextWave(screen)

        if selected and selected.__class__ == Icon:
            MainFunctions.selectedIcon(screen, selected)

        if selected and Tower in selected.__class__.__bases__:
            MainFunctions.selectedTower(screen, selected)

        screen.blit(openbutton,openbuttonrect)
        for icon in iconlist:
            screen.blit(icon.img,icon.rect)
            if icon.rect.collidepoint(pygame.mouse.get_pos()):
                text = font.render("%s Tower (%d)" % (icon.type,eval(icon.type+"Tower").basecost),1,(0,0,0))
                textpos = text.get_rect(left=icon.rect.left,bottom=icon.rect.top-2)
                screen.blit(text,textpos)

        screen.blit(mapvar.baseimg,mapvar.baserect)

        pygame.display.flip()

        frametime = (time.time() - starttime) * speed

main()

#Thanks to everyone who looks over this code, or tests this thing out. Feel free
#to contact me at the email address listed above with any questions, comments, or
#your own set of changes. I've wanted to do a game like this for a while, so I'll
#stay committed as long as it has some interest in the community.

#Have a nice day :)