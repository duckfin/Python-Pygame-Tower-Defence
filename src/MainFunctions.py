from localdefs import *
from localclasses import *
import pygame

def makeIcons():
    Icon('Fighter') #Icon to select to build a basic tower
    Icon('Archer')
    Icon('Slow')
    Icon('Cannon')
    Icon('Poison')
    print "Icon Object Created"

def tickAndClear(screen,clock,background):
    clock.tick(30)
    screen.blit(background,(0,0))

def workSenders(frametime):
    for sender in senderlist:
        sender.tick(frametime)

def workTowers(screen,frametime):
    for tower in towerlist:
        tower.takeTurn(frametime,screen)
        pygame.draw.line(screen, (0,0,0), (tower.rect.left,tower.rect.top-2), (tower.rect.right,tower.rect.top-2), 3)
        pygame.draw.line(screen, (255,0,0), (tower.rect.left,tower.rect.top-2), (tower.rect.left+(tower.hp*1.0/tower.maxhp*1.0)*tower.rect.width,tower.rect.top-2), 3)

def dispExplosions(screen):
    #Display any explosions in the queue, then remove them.
    for rect in explosions:
        screen.blit(imgLoad('explosion.png'),rect)
        explosions.remove(rect)

def dispText(screen,wavenum):
    #This displays the basic status at the top left.
    font = pygame.font.Font(None,20)
    text = font.render("Money: %d | Wave: %d | %d :Health" % (player.money,wavenum,player.health),1,(0,0,0))
    textpos = text.get_rect(left=10,top=5)
    screen.blit(text,textpos)

def workEnemies(screen,frametime):
    #Let the enemies do their thing. Move, draw to screen, draw health bars.
    for enemy in enemylist:
        enemy.takeTurn(frametime)
        screen.blit(enemy.image,enemy.rect)
        pygame.draw.line(screen, (0,0,0), (enemy.rect.left,enemy.rect.top-2), (enemy.rect.right,enemy.rect.top-2), 3)
        if enemy.poisontimer:
            pygame.draw.line(screen, (0,255,0), (enemy.rect.left,enemy.rect.top-2), (enemy.rect.left+(enemy.health*1.0/enemy.starthealth*1.0)*enemy.rect.width,enemy.rect.top-2), 3)
        else:
            pygame.draw.line(screen, (255,0,0), (enemy.rect.left,enemy.rect.top-2), (enemy.rect.left+(enemy.health*1.0/enemy.starthealth*1.0)*enemy.rect.width,enemy.rect.top-2), 3)

def dispStructures(screen):
    for struct in (towerlist):
        screen.blit(struct.image,struct.rect)

def dispNextWave(screen):
    font = pygame.font.Font(None,20)
    text = font.render("Next Wave",1,(0,0,0))
    nexttextpos = text.get_rect(right=scrwid-10,centery=scrhei/2)
    pygame.draw.rect(screen, (255,255,255), nexttextpos.inflate(2,2), 0)
    pygame.draw.rect(screen, (0,0,0), nexttextpos.inflate(2,2), 1)
    screen.blit(text,nexttextpos)
    return nexttextpos

def selectedIcon(screen,selected):
    mouseat = selected.img.get_rect(center=pygame.mouse.get_pos())
    screen.blit(selected.img,mouseat)
    if selected.base == "Tower":
        pygame.draw.circle(screen,(0,0,0),mouseat.center,int(eval(selected.type+"Tower").baserange),2)

def selectedTower(screen,selected):
    font = pygame.font.Font(None,20)
    selected.genButtons(screen)
    for text,rect,cb in selected.buttonlist:
        screen.blit(text,rect)
    pygame.draw.circle(screen,(255,255,255),selected.rect.center,int(selected.range),1)