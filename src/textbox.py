from localdefs import *

class Textbox():
    def __init__(self,ID,x,y,width = 80,size = 18):
        pygame.font.init()
        self.fontr = pygame.font.Font(None,size)
        self.height = self.fontr.get_height()
        self.text = ""
        self.render_text = self.fontr.render(self.text,1,(0,250,0))
        self.pos = (x+2,y+2)
        self.ID = ID
        self.curpos = 1
        self.font = None
        self.Rect = pygame.Rect(x,y,width,self.height + 4)
        self.Brect = pygame.Rect(x-2,y-2,width+4,self.height + 8)
        self.Focus = False

    def Draw(self,canvas):
        pygame.draw.rect(canvas,(250,250,250),self.Rect)
        if self.Focus:
            pygame.draw.rect(canvas,(0,125,0),self.Brect,2)
        else:
            pygame.draw.rect(canvas,(125,125,125),self.Brect,2)
        canvas.blit(self.render_text,self.pos)

    def key_event(self,evt):
        letter = None
        if evt.key == pygame.K_BACKSPACE:
            Tx,cr = self.text , self.curpos
            self.text = Tx[:cr-2] + Tx[cr-1:]
            self.curpos -= 1
            if self.curpos < 1:
                self.curpos = 1
            self.render_text = self.fontr.render(self.text,1,(0,250,0))

        if evt.key > 96 and evt.key < 123:
            letter = chr(evt.key)

        if evt.key > 47 and evt.key < 58:
            letter = chr(evt.key)

        if evt.key == pygame.K_SPACE:
            letter = " "

        if not letter == None:
            Tx,cr = self.text , self.curpos
            self.text = Tx[:cr-1] + letter + Tx[cr-1:]
            self.curpos += 1
            self.render_text = self.fontr.render(self.text,1,(0,250,0))
    def Check(self,key,evt):
        if key == self.ID:
            self.Focus = True
            self.key_event(evt)
        else:
            self.Focus = False
