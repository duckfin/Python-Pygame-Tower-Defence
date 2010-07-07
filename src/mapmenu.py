import os.path
from localdefs import *
from menu import *

def pickMap():
    maplist = [d for d in os.listdir(os.path.join('mapfiles')) if
                os.path.isdir(os.path.join('mapfiles',d))]
    font = pygame.font.Font(None,20)
    mapobjectlist = list()
    for map in maplist:
        if os.path.isfile(os.path.join('mapfiles',map,'description.txt')):
            text = font.render("Map '%s': %s" % (map,open(os.path.join('mapfiles',map,'description.txt')).readline().strip()),1,(255,255,255))
        else:
            text = font.render("Map '%s'" % (map),1,(255,255,255))
        textpos = text.get_rect(left=5,top=5+25*len(mapobjectlist))
        mapobjectlist.append((text,textpos,map))
    screen = pygame.display.set_mode((max([tp.width for t,tp,m in mapobjectlist])+25,10+25*len(maplist)))
    background = pygame.Surface(screen.get_size())
    background.fill((0,0,0))
    while 1:
        screen.blit(background,(0,0))
        for t,tp,m in mapobjectlist:
            screen.blit(t,tp)
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                for t,tp,m in mapobjectlist:
                    if tp.collidepoint(event.dict['pos']):
                        return str(m)
            keyinput = pygame.key.get_pressed()
            if event.type == QUIT:
                sys.exit()
            if keyinput[K_ESCAPE]:
                sys.exit()
        pygame.display.flip()