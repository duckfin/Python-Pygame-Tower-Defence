import os
import sys
from pygame.locals import *
from localdefs import *
from RollFunctions import d

CRcost = list([170,350,550,750,1000,1350,1750,2200,2850,3650,4650])
CRxp = list([400,600,800,1200,1600,2400,3200,4800,6400,9600,12800])

class Enemy():
    def __init__(self,wave,letter):
        self.image = enemyimagearray[0]
        self.curnode = 0
        self.distance = 0
        if letter=='a':
            self.movelist = mapvar.pointmovelists[0][:]
        elif letter=='b':
            self.movelist = mapvar.pointmovelists[1][:]
        elif letter=='c':
            self.movelist = mapvar.pointmovelists[2][:]
        elif letter=='d':
            self.movelist = mapvar.pointmovelists[3][:]
        self.rect = self.image.get_rect(center=(self.movelist[self.curnode]))
        enemylist.append(self)
        self.CR = int(mapvar.mapdict['wave'+str(wave)+letter][1])
        self.cost = CRcost[self.CR]/mapvar.mapdict['wave'+str(wave)+letter][0]
        self.health = d(8,mapvar.mapdict['wave'+str(wave)+letter][2])
        self.speed = mapvar.mapdict['wave'+str(wave)+letter][4]
        self.starthealth = self.health
        self.startspeed = self.speed
        self.route = 1
        self.range = 2*squsize
        self.slowtimers = list()
        self.slowpercent = 1.0
        self.holdcentx = self.rect.centerx*1.0
        self.holdcenty = self.rect.centery*1.0
        self.poisontimer = None
        self.armorClass = 10 + mapvar.mapdict['wave'+str(wave)+letter][3]
        self.dr = 0
        self.xp = CRxp[self.CR]/mapvar.mapdict['wave'+str(wave)+letter][0]
        self.damageDie = mapvar.mapdict['wave'+str(wave)+letter][6]
        self.damageDieAmt = mapvar.mapdict['wave'+str(wave)+letter][5]
        self.damageMod = mapvar.mapdict['wave'+str(wave)+letter][7]
        self.attackMod = mapvar.mapdict['wave'+str(wave)+letter][8]
        self.targetTimer = self.startTargetTimer = 1.0
    def takeTurn(self,frametime):
        self.workSlowTimers(frametime)
        self.move(frametime)
        self.targetTimer -= frametime
        if self.targetTimer<=0:
            self.target()
            self.targetTimer=self.startTargetTimer
    def target(self):
        for tower in towerlist:
            if distance(self.rect,tower.rect)<=self.range:
                self.attackTower(tower)
                tower.checkHealth()
                return tower.rect.center
        return 0
    def attackTower(self,tower):
        roll = d(20)
        attackRoll = self.attackMod + roll
        if attackRoll >= tower.armorClass or roll == 20:
            self.hitTower(tower)
            if roll == 20:
                self.hitTower(tower)
    def hitTower(self,tower):
        damageDone = (self.damage() - tower.dr)
        tower.hp -= damageDone
    def damage(self):
        return d(self.damageDie,self.damageDieAmt) + self.damageMod
    def workSlowTimers(self,frametime):
        for st in self.slowtimers[:]:
            st.time -= frametime
            if st.time<=0:
                self.slowtimers.remove(st)
    def move(self,frametime):
        slowlist = [st.percent for st in self.slowtimers]
        slowlist.append(1)
        slowpercent = min(slowlist)
        moveamt = slowpercent*frametime
        for i in range(int(self.speed)):
            if mapvar.baserect.colliderect(self.rect):
                self.attack()
                return
            if self.rect.collidepoint(self.movelist[self.curnode+1]):
                self.curnode+=1
            if self.movelist[self.curnode+1][0]>self.rect.centerx:
                self.distance+=moveamt
                self.holdcentx+=moveamt
                self.image = enemyimagearray[0]
                self.rect.centerx = int(self.holdcentx)
            elif self.movelist[self.curnode+1][0]<self.rect.centerx:
                self.distance+=moveamt
                self.holdcentx-=moveamt
                self.image = enemyimagearray[2]
                self.rect.centerx = int(self.holdcentx)
            elif self.movelist[self.curnode+1][1]>self.rect.centery:
                self.distance+=moveamt
                self.holdcenty+=moveamt
                self.image = enemyimagearray[3]
                self.rect.centery = int(self.holdcenty)
            elif self.movelist[self.curnode+1][1]<self.rect.centery:
                self.distance+=moveamt
                self.holdcenty-=moveamt
                self.image = enemyimagearray[1]
                self.rect.centery = int(self.holdcenty)
    def checkHealth(self):
        if self.health<=0:
            self.die()
    def attack(self):
        player.health -= (d(self.damageDie,self.damageDieAmt) + self.damageMod)
        enemylist.remove(self)
        if self.poisontimer:
            self.poisontimer.kill = True
        if player.health<=0:
            print "You Lost!"
            sys.exit(1)
        return
    def die(self):
        explosions.append(self.rect)
        if self in enemylist:
            enemylist.remove(self)
        player.money+=(self.cost)
        xpper = self.xp/(1.0*len(towerlist))
        for tower in towerlist:
            tower.xp += xpper

levelxp = list([0,1300,3300,6000,10000,15000,23000,34000,50000,71000,105000])
levelprice = list([75,500,1500,3000,5250,8000,11750,16500,23000,31000])

class Tower():
    def __init__(self,cent):
        self.level = 1
        self.targetTimer = 0
        player.money-=self.cost
        self.upgradeCost = 0
        self.critMin = 20
        self.rect = self.image.get_rect(center=cent)
        towerlist.append(self)
        self.totalspent = self.cost
        self.abilities = list()
        self.buttonlist = list()
        self.calcUpgrade()
        self.xp = 0
        self.dr = 0
        self.armorClass = 10
    def upgrade(self):
        pass
    def genButtons(self,screen):
        font = pygame.font.Font(None,20)
        self.buttonlist = list()
        text = font.render("Sell: %d(%d)" % (int(self.totalspent/2),player.money+int(self.totalspent/2)),1,(255,255,255))
        selltextpos = text.get_rect(right=scrwid-10,bottom=scrhei-10)
        pygame.draw.rect(screen, (255,0,0), selltextpos.inflate(2,2), 0)
        pygame.draw.rect(screen, (0,0,0), selltextpos.inflate(2,2), 1)
        self.buttonlist.append((text,selltextpos,self.sell))
        text = font.render("Upgrade to level %d: %d gold, (%d/%d)" % (self.level+1,self.upgradeCost,self.xp,self.upgradeXp),1,(255,0,0))
        textpos = text.get_rect(right=scrwid-10,bottom=self.buttonlist[-1][1].top-10)
        pygame.draw.rect(screen, (255,255,255), textpos.inflate(2,2), 0)
        pygame.draw.rect(screen, (0,0,0), textpos.inflate(2,2), 1)
        self.buttonlist.append((text,textpos,self.upgrade))
    def calcUpgrade(self):
        self.upgradeXp = levelxp[self.level]
        self.upgradeCost = levelprice[self.level]
    def takeTurn(self,frametime,screen):
        self.targetTimer -= frametime
        if self.targetTimer<=0:
            enemypoint = self.target()
            #If the tower shot an enemy, highlight the tower and restart
            #the turncounter.
            if enemypoint:
                temp = self.image.copy()
                temp.fill((255,255,255))
                screen.blit(temp,self.rect)
                self.targetTimer=self.startTargetTimer
                #Enemypoint will be 1 if a slow tower hits (not yet implemented)
                #otherwise, if the option is turned on, draw a line from the
                #tower to the enemy it hit.
                if enemypoint is not 1 and optiondict['targetlines']:
                    pygame.draw.line(screen,(255,255,255),self.rect.center,enemypoint)
    def target(self):
        for enemy in sorted(enemylist,key=(lambda x: x.distance),reverse=True):
            if distance(self.rect,enemy.rect)<=self.range:
                self.attackEnemy(enemy)
                enemy.checkHealth()
                return enemy.rect.center
        return 0
    def attackEnemy(self,enemy):
        penalty = 0
        while(self.bab-penalty>=1):
            roll = d(20)
            attackRoll = self.bab-penalty + self.attackMod + roll
            if attackRoll >= enemy.armorClass or roll == 20:
                self.hitEnemy(enemy)
                if roll >= self.critMin:
                    self.hitEnemy(enemy)
            penalty += 5
    def hitEnemy(self,enemy):
        damageDone = (self.damage() - enemy.dr)
        enemy.health -= damageDone
    def sell(self):
        player.money+=(self.totalspent/2.0)
        towerlist.remove(self)
    def checkHealth(self):
        if self.hp<=0:
            self.die()
    def die(self):
        explosions.append(self.rect)
        if self in towerlist:
            towerlist.remove(self)

class FighterTower(Tower):
    basecost = 75
    baserange = 2*squsize
    def __init__(self,cent):
        self.cost = self.basecost
        self.range = self.baserange
        self.bab = 1
        self.attackMod = 5
        self.damageMod = 12
        self.startTargetTimer = 1.0
        self.critMin = 19
        self.image = imgLoad(os.path.join('towerimgs','Basic','1.png'))
        self.xp = 0
        self.hp = self.maxhp = 10 + 3
        self.armorClass = 18
        Tower.__init__(self,cent)
    def damage(self):
        return d(6,2) + self.damageMod
    def upgrade(self):
        if player.money>=self.upgradeCost and self.xp>=self.upgradeXp:
            player.money-=self.upgradeCost
            self.level += 1
            self.bab = self.level
            self.maxhp += d(10,1) + 3
            self.hp = self.maxhp
            if self.level == 2:
                self.damageMod += 2
            if self.level == 4:
                self.damageMod += 3
            if self.level == 5:
                self.attackMod += 1
                self.damageMod += 1
            if self.level == 6:
                self.attackMod += 1
                self.damageMod += 1
                self.range += 1*squsize
            if self.level == 8:
                self.critMin -= 2
            if self.level == 9:
                self.attackMod += 1
                self.damageMod += 1
            self.calcUpgrade()

class ArcherTower(Tower):
    basecost = 75
    baserange = 2*squsize
    def __init__(self,cent):
        self.cost = self.basecost
        self.range = self.baserange
        self.bab = 1
        self.attackMod = 7
        self.damageMod = 10
        self.startTargetTimer = 1.0
        self.critMin = 19
        self.image = imgLoad(os.path.join('towerimgs','Basic','1.png'))
        self.xp = 0
        self.hp = self.maxhp = 10 + 3
        self.armorClass = 18
        Tower.__init__(self,cent)
    def damage(self):
        return d(6,2) + self.damageMod
    def upgrade(self):
        if player.money>=self.upgradeCost and self.xp>=self.upgradeXp:
            player.money-=self.upgradeCost
            self.level += 1
            self.bab = self.level
            self.maxhp += d(10,1) + 3
            self.hp = self.maxhp
            if self.level == 2:
                self.startTargetTimer /= 2
                self.attackMod -= 2
            if self.level == 4:
                self.damageMod += 3
            if self.level == 5:
                self.attackMod += 1
                self.damageMod += 1
            if self.level == 6:
                self.attackMod += 1
                self.damageMod += 1
                self.range += 1*squsize
            if self.level == 8:
                self.critMin -= 2
            if self.level == 9:
                self.attackMod += 1
                self.damageMod += 1
            self.calcUpgrade()

class SlowTower(Tower):
    basecost = 50
    baserange = 2*squsize
    def __init__(self,cent):
        self.cost = self.basecost
        self.range = self.baserange
        self.bab = 0
        self.attackMod = 0
        self.damageMod = 2
        self.startTargetTimer = 1.0
        self.slowtime = 1.5
        self.slowamt = 0.75
        self.image = imgLoad(os.path.join('towerimgs','Slow','1.png'))
        Tower.__init__(self,cent)
    def damage(self):
        return self.damageMod
    def hitEnemy(self,enemy):
        enemy.health-=(self.damage()-enemy.dr)
        enemy.slowtimers.append(SlowTimer(self.slowamt,self.slowtime))

class PoisonTower(Tower):
    basecost = 50
    baserange = 2*squsize
    def __init__(self,cent):
        self.cost = self.basecost
        self.range = self.baserange
        self.bab = 0
        self.attackMod = 0
        self.damage = 1
        self.startTargetTimer = 1.0
        self.poisontime = 3
        self.poisonamt = 0.2
        self.image = imgLoad(os.path.join('towerimgs','Poison','1.png'))
        Tower.__init__(self,cent)
    def damage(self):
        return self.damageMod
    def target(self):
        for enemy in sorted(enemylist,key=(lambda x: x.distance),reverse=True):
            if distance(self.rect,enemy.rect)<=self.range and enemy.poisontimer==None:
                self.attackEnemy(enemy)
                enemy.checkHealth()
                return enemy.rect.center
        for enemy in sorted(enemylist,key=(lambda x: x.distance),reverse=True):
            if distance(self.rect,enemy.rect)<=self.range:
                self.attackEnemy(enemy)
                enemy.checkHealth()
                return enemy.rect.center
    def hitEnemy(self,enemy):
        enemy.health-=(self.damage()-enemy.dr)
        t = PoisonTimer(enemy,self.poisonamt,self.poisontime)
        t.start()

class CannonTower(Tower):
    basecost = 50
    baserange = 2*squsize
    def __init__(self,cent):
        self.cost = self.basecost
        self.range = self.baserange
        self.bab = 1
        self.attackMod = 0
        self.damage = 7
        self.startTargetTimer = 1.0
        self.image = imgLoad(os.path.join('towerimgs','Cannon','1.png'))
        Tower.__init__(self,cent)
        self.splashrange = self.range
    def damage(self):
        return self.damageMod
    def attackEnemy(self,enemy,second = False):
        roll = d(20)
        attackRoll = self.attack + roll
        if attackRoll >= enemy.armorClass or roll == 20:
            self.hitEnemy(enemy,second)
            if roll >= self.critMin:
                self.hitEnemy(enemy,second)
    def hitEnemy(self,enemy,second):
        enemy.health-=(self.damage()-enemy.dr)
        if not second:
            for enemy2 in sorted(enemylist,key=(lambda x: x.distance),reverse=True):
                if distance(enemy.rect,enemy2.rect)<=self.splashrange and enemy!=enemy2:
                    self.attackEnemy(enemy2,True)
                    enemy2.checkHealth()
                    return

class Icon():
    def __init__(self,type):
        self.type = type
        self.base = "Tower"
        iconlist.append(self)
        try:
            self.img = imgLoad(os.path.join('towerimgs',type,'1.png'))
        except:
            self.img = imgLoad(os.path.join('towerimgs','Basic','1.png'))
        self.rect = self.img.get_rect(left=len(iconlist)*(25)-20,centery=scrhei-self.img.get_height())
