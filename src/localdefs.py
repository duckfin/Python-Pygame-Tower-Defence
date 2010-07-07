import math
import os
import sys
import pygame
import threading
import time
from sys import exit as sysexit
from pygame.locals import *

scrwid = 800 #Screen width.
scrhei = 600 #Screen height. Uses 4:3 ratio.
squsize = 20 #Square size.
class Map():
    def __init__(self):
        self.current = 1
        self.pathrectlist = None
        self.pointmovelist = None
        self.endrect = None
        self.mapdict = dict()
        self.pointmovelists = list()
        self.pathrectlists = list()
    def getmovelist(self):
        movelists = list()
        movelistnum = -1
        f = open(os.path.join('mapfiles',str(self.current),'movefile.txt'))
        line = f.readline().strip().split(',')
        self.basepoint = (int(line[0]),int(line[1]))

        for line in f.readlines():
            line = line.strip().split(',')
            if int(line[0])<0 or int(line[1])<0 or int(line[0])>(scrwid/squsize) or int(line[1])>(scrhei/squsize):
                movelists.append(list())
                movelistnum+=1
            movelists[movelistnum].append((int(line[0]),int(line[1])))

        for movelist in movelists:
            movelist.append(self.basepoint)
            pointmovelist = list([(point[0]*squsize+int(squsize/2.0),point[1]*squsize+int(squsize/2.0)) for point in movelist])
            pointmovelist.append((scrwid+squsize,scrhei+squsize))
            pathrectlist = list([pygame.Rect(pointmovelist[ind],(pointmovelist[ind+1][0]-pointmovelist[ind][0],pointmovelist[ind+1][1]-pointmovelist[ind][1])) for ind in range(len(pointmovelist)-2)])
            for rec in pathrectlist:
                rec.normalize()
            self.pointmovelists.append(pointmovelist)
            self.pathrectlists.append(pathrectlist)
            print "Move List Generated"
    def getmapproperties(self):
        def mapPropertiesGen(self):
            f = open(os.path.join('mapfiles',str(self.current),'mapproperties.txt'))
            for line in f.readlines():
                line = line.strip().split('=')
                linepro = line[1].strip().split(',')
                yield line[0],[float(each) for each in linepro]
        self.mapdict = dict(mapPropertiesGen(self))
        print "Map Properties Created"
    def backgroundGen(self,bgsize):
        print "Generating Background"

        grassbmp = imgLoad(os.path.join('backgroundimgs','Grass.bmp'))
        grassroadbmp = imgLoad(os.path.join('backgroundimgs','GrasRoad.bmp'))

        dsq = imgLoad(os.path.join('backgroundimgs','desertsquare.jpg'))
        dpc = imgLoad(os.path.join('backgroundimgs','desertpathcorner.png'))
        dpc = grassroadbmp.subsurface(pygame.Rect((80,1),(20,20)))
        dpcft = pygame.transform.flip(dpc, False, True)
        dpctf = pygame.transform.flip(dpc, True, False)
        dpctt = pygame.transform.flip(dpc, True, True)
        dpi = imgLoad(os.path.join('backgroundimgs','desertpathinter.png'))
        dp = imgLoad(os.path.join('backgroundimgs','desertpath.png'))
        dpr = pygame.transform.rotate(dp,90)

        dsq = grassbmp.subsurface(pygame.Rect((40,41),(20,20)))

        grvr = grassroadbmp.subsurface(pygame.Rect((0,41),(20,20)))
        grvl = grassroadbmp.subsurface(pygame.Rect((80,41),(20,20)))
        grht = grassroadbmp.subsurface(pygame.Rect((40,1),(20,20)))
        grhb = grassroadbmp.subsurface(pygame.Rect((40,81),(20,20)))

        background = imgLoad(os.path.join('mapfiles',str(self.current),'background.jpg'))
        for pathnum in range(len(self.pointmovelists)):
            pathrectlist = self.pathrectlists[pathnum]
            pointmovelist = self.pointmovelists[pathnum]
            for rec in [pygame.Rect(x,y,squsize,squsize) for x in range(0,scrwid,squsize) for y in range(0,scrhei,squsize)]:
                if any([rec.collidepoint(point) for point in pointmovelist]):
                    reccollides = list([rect for rect in pathrectlist if rect.colliderect(rec)])
                    if len(reccollides)==2:
                        if reccollides[0].height==0:
                            if reccollides[0].right==reccollides[1].centerx:
                                if reccollides[0].centery<reccollides[1].centery:
                                    background.blit(dpc,rec)
                                else:
                                    background.blit(dpcft,rec)
                            else:
                                if reccollides[0].centery<reccollides[1].centery:
                                    background.blit(dpctf,rec)
                                else:
                                    background.blit(dpctt,rec)
                        elif reccollides[0].width==0:
                            if reccollides[0].top==reccollides[1].centery:
                                if reccollides[0].centerx<reccollides[1].centerx:
                                    background.blit(dpctf,rec)
                                else:
                                    background.blit(dpc,rec)
                            else:
                                if reccollides[0].centerx<reccollides[1].centerx:
                                    background.blit(dpctt,rec)
                                else:
                                    background.blit(dpcft,rec)
                    if len(list([1 for pml in self.pointmovelists for point in pml if rec.collidepoint(point)]))==2:
                        background.blit(grassroadbmp.subsurface(pygame.Rect((10,11),(10,10))),rec.move(0,-squsize/2+10))
                        background.blit(grassroadbmp.subsurface(pygame.Rect((40+10,81),(10,10))),rec.move(10,-squsize/2+10))
                        background.blit(grhb,rec.move(0,squsize/2))
                elif len(list([rect for rect in pathrectlist if rect.colliderect(rec)]))==2:
                    background.blit(dpi,rec)
                else:
                    collideindex = rec.collidelist(pathrectlist)
                    if collideindex!=-1:
                        if pathrectlist[collideindex].height==0:
                            background.blit(grht,rec.move(0,-squsize/2))
                            background.blit(grhb,rec.move(0,squsize/2))
                        else:
                            background.blit(grvr,rec.move(-squsize/2,0))
                            background.blit(grvl,rec.move(squsize/2,0))
        self.baseimg = imgLoad(os.path.join('backgroundimgs','base.png'))
        self.baserect = self.baseimg.get_rect(center=(self.basepoint[0]*squsize+(0.5*squsize),self.basepoint[1]*squsize+(0.5*squsize)))
        print "Background Generated"
        return background
    def loadMap(self,bgsize,mapname):
        self.current = mapname
        if os.path.exists(os.path.join('mapfiles',str(self.current))):
            self.getmovelist()
            self.getmapproperties()
            return self.backgroundGen(bgsize)
        else:
            print "You Won!!!"
            sysexit(1)

mapvar = Map()

def optionsGen():
    f = open('options.txt')
    for line in f.readlines():
        line = line.strip().split('=')
        yield line
optiondict = dict(optionsGen())
for key in optiondict:
    optiondict[key] = int(optiondict[key])

class Player():
    def __init__(self):
        self.health = int(optiondict['playerhealth'])
        self.money = 150
        self.interest = 1.00
        self.hpt = 0.0
        self.attackmod = 1.00
        self.rangemod = 1.00
        self.name = "player"
        self.abilities = list()
    def addHpt(self,val):
        self.hpt+=val
    def addInterest(self,val):
        self.interest+=val
    def incAtt(self,per):
        self.attackmod*=per
    def incRng(self,per):
        self.rangemod*=per

player = Player()

enemylist = list()
towerlist = list()
bulletlist = list()
iconlist = list()
menulist = list()
explosions = list()
senderlist = list()
timerlist = list()

def imgLoad(img):
    file = os.path.join(img)
    image = pygame.image.load(file)
    image.convert_alpha()
    return image

def distance(first,second):
    return (math.sqrt((second.centerx-first.centerx)**2+(second.centery-first.centery)**2))

class SlowTimer():
    def __init__(self,percent,time):
        self.percent = percent
        self.time = time

class PoisonTimer(threading.Thread):
    def __init__(self,enemy,damage,seconds):
        threading.Thread.__init__(self)
        self.runtime = seconds
        self.dam = damage
        self.target = enemy
        enemy.poisontimer=self
        self.kill = False
    def run(self):
        sec = self.runtime*1.0
        while(sec>0):
            sec-=0.1
            time.sleep(0.1)
            if self.target.poisontimer == self or self.kill == True:
                if self.target.health>0:
                    self.target.health-=self.dam
                    if self.target.health<=0:
                        self.target.die()
                        return
                else:
                    return
            else:
                return
        if self.target.poisontimer == self:
            self.target.poisontimer = None

enemyimagearray = list()
def genEnemyImageArray():
    enemyimage = imgLoad(os.path.join('enemyimgs','enemy.png'))
    enemyimagearray.append(enemyimage)
    enemyimagearray.append(pygame.transform.rotate(enemyimage,90))
    enemyimagearray.append(pygame.transform.flip(enemyimage,True,False))
    enemyimagearray.append(pygame.transform.rotate(enemyimage,-90))