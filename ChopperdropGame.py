import pygame as pg
import sys
import os
import random

width = 1000
height = 600
size = (width,height)

#Tworze budynki
#tworze funckje pomocnicze
def LoadIm(name,UseColorKey = False):
    full_name = os.path.join('mojagra\\', name)
    image = pg.image.load(full_name)
    if UseColorKey is True:
        colorkey = image.get_at((0,0)) 
        image.set_colorkey(colorkey,RLEACCEL)
    return image
#funckaj usuwa losowy element listy
def random_remove(list1):
    a=random.randint(0,len(list1)-1)
    list1.remove(list1[a])
#klasa budynku
class Building(pg.sprite.Sprite):
    def __init__(self,h):
        pg.sprite.Sprite.__init__(self)
        self.image = LoadIm('budynek.png')            
        self.rect = self.image.get_rect()
        self.y=570
        self.rect.center = (h,self.y)
        self.h=h
    def new_level(self,howMany):
        x=self.y-60*howMany
        self.y=x
        self.rect.center = (self.h,self.y)
#Tworze klase samolotu
class Plane(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = LoadIm('samolot1.png')
        self.rect = self.image.get_rect()
        self.rect.centerx=0
        self.rect.centery=50
        self.x_velocity = 10
        self.y_velocity = 0
    def update(self):
        self.rect.move_ip((self.x_velocity, self.y_velocity))            
        if self.rect.midleft[0] > width:
            r=int(self.rect.centery)+15
            self.rect.midright=(0,r)
class Bomb(pg.sprite.Sprite):
    def __init__(self, start):
        pg.sprite.Sprite.__init__(self)
        self.image = LoadIm('bomb.png')       
        self.rect = self.image.get_rect()
        self.rect.center = start   
        self.x_velocity = 0
        self.y_velocity = 4
    def update(self):
        if self.rect.centery > 600:
            self.kill()
        else:
            self.rect.move_ip((self.x_velocity, self.y_velocity))
        
#class Menu(pg.sprite.Sprite):
   # def __init__(self):        
        
 
 #Wlasciwy program

          

mylist = []     
pg.init()
#tlo
window=pg.display.set_mode(size)
pg.display.set_caption('Chopper Drop ')
pg.display.flip()
        
background = pg.image.load(os.path.join('mojagra\\', 'proba.png'))
screen = pg.display.get_surface()
screen.blit(background,(0,0))
pg.display.flip()

#budynki

mylist1=[]
lista1=[]
i=25
while i<width:
    lista1.append(i)
    i+=50
lista=[]
lista.append(random.randint(0,18))
while len(lista)<=3:
    x=random.randint(0,18)
    if x in lista:
        pass
    else:
        lista.append(x)
mylist=[]
for j in range(19):
    mylist.append(j)

for z in lista:
    mylist.remove(z)
build=pg.sprite.RenderClear()
dict1={}
for i in mylist:
    dict1["build%s"%(mylist.index(i))]=Building(lista1[i])
    build.add(dict1["build%s"%(mylist.index(i))])
    
   
random_remove(mylist)

   
for t in range(1,5):
    random_remove(mylist)
        
    for k in mylist:
        dict1["build%s%s"%(t,mylist.index(k))] = Building(lista1[k])
        dict1["build%s%s"%(t,mylist.index(k))].new_level(t)
        
        build.add(dict1["build%s%s"%(t,mylist.index(k))])
           

          
#Samolot
bombSprite = pg.sprite.RenderClear()
planeSprite = pg.sprite.RenderClear()
plane=Plane()
planeSprite.add(plane)

              
pg.display.flip()



pg.display.flip()
counter = 0
prevRecty = 0
clock=pg.time.Clock()
run=True
#Petla zamyka program gdy nacisniemy QUIT
while run is True:
    clock.tick(40)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_SPACE:
                actRecty = plane.rect.center[1]
                if prevRecty ==  actRecty:
                    counter+=1
                else:
                    counter =0                
                if counter <=1:
                    bombSprite.add(Bomb(plane.rect.midbottom))
            
                prevRecty = actRecty
                        
    
    planeSprite.update()
    bombSprite.update()
    
    for hit in pg.sprite.groupcollide(build, bombSprite,True,True):
        pass
    
    for hit in pg.sprite.groupcollide(build, planeSprite,False,True):
        pass
    
    if bool(build) == False: #or bool(planeSprite) == False:
        sys.exit() 
        
    if bool(planeSprite) == False:
        background = pg.image.load(os.path.join('mojagra\\', 'gameover.png'))
        screen = pg.display.get_surface()
        screen.blit(background,(0,0))
        pg.display.flip()        
        
        
    pg.display.flip()
    build.clear(window, background)
    build.draw(window)    
    planeSprite.clear(window,background)
    planeSprite.draw(window)
    bombSprite.clear(window, background)
    bombSprite.draw(window)    

    pg.display.flip()
    pg.display.flip()