from localdefs import senderlist,mapvar
from localclasses import Enemy

class Sender():
    def __init__(self,wave,letter):
        self.wavenum = wave
        self.enemycounter = 1.0
        self.letter = letter
        self.enemiesgone = 0
        senderlist.append(self)
    def tick(self,frametime):
        self.enemycounter -= frametime
        if self.enemycounter<=0:
            if self.enemiesgone<mapvar.mapdict['wave'+str(self.wavenum)+self.letter][0]:
                Enemy(self.wavenum,self.letter)
                self.enemiesgone+=1
            else:
                senderlist.remove(self)
            self.enemycounter = 1.0
