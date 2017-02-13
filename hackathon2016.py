#Ou physics hackathon 2k16.  Authors: Paul Canton, Tim Miller

#Theme: An adventure.  Possibly a game or a story

#Some notes were taking in my windows 10 parition, after installing python there
#Quickly found windows command prompt functional but cumbersome and ill documented
#Difficult to get python and command prompt line to work together, installing packages, etc
#So, here we are in Fedora

#Goals/some things we wanted to learn to apply to our other works:

#Rather than getting data off a webpage as we hoped to learn, we found a package that could 
#play a video from an html link.

#Wanted to learn how to do an interactive plot - like you have in iraf.  An interactive gui were one
#could select parameter space in trebuchets draw and angle of fire was implimented.

#Wanted to learn tocall and run an old (IDL) script, possibly via the command line from within python.
#os.system might be useful for this, but wasn't implimented for this cause.



#Some more background:
#Tim and I wanted to do a game, sieging NH (ie black holes you fall into behind doors, etc).  Quickly found it
#would be complicated to write a lot in a weekend,
#and around our goals of things to learn settled on sieging gittenger hall with a trebuchet which is currently
#being demonlished anyhow. 

#Fun idea: Use monty python clips for triumph or defeat if you hit or miss the building

import math as mth
import os
import time
import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,72)
  #pygame.draw.rect(screen, (0,0,0),
  #                 (0,
  #                  (screen.get_height() / 2) - 10,
  #                  200,20), 0)
  #pygame.draw.rect(screen, (255,255,255),
  #                 (2,
  #                  (screen.get_height() / 2) - 12,
  #                  700,60), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                (0, (screen.get_height() / 2) - 10))
  pygame.display.flip()

def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  display_box(screen, question + ": " + string.join(current_string,""))
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[:-1]
      screen = pygame.display.set_mode((1500,720))
      pygame.display.set_caption('Down With Gittinger Hall!!!')
    elif inkey == K_RETURN and current_string:
      break
    elif inkey <= 60 and inkey != K_RETURN:
      current_string.append(chr(inkey))
    display_box(screen, question + ": " + string.join(current_string,""))
  return string.join(current_string,"")

def load_image(name, colorkey=None): #definition
    fullname = os.path.join('/home/Paul/Desktop/hackathon2016', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class target(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect=load_image('Gittengerhall.JPG',-1)
        


#define tryagain = 1 as to repeat the code block until you destroy gittinger with a hit
tryagain = 1 #give up is false
loose = 0 #loose is the number of shots the trebuchets gotten off, a counter
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

#While loops are useful in cases where a user's input is required - repeat until user does something specific senarios
while tryagain == 1:

    #install pygame to be able to do gui stuff: >> sudo yum install pygame
    #In a later version we got an input gui going... not here
    screen = pygame.display.set_mode((1500,720))
    pygame.display.set_caption('Down With Gittinger Hall!!!')
    inangle = ask(screen, "Enter the launch angle between 0 and 90 degrees ")
    print('You entered ',inangle)
    pygame.display.quit()
#    inangle = input('Enter the launch angle: ')
#    print('You entered ',inangle)

    screen = pygame.display.set_mode((980,720))
    pygame.display.set_caption('Down With Gittinger Hall!!!')
    invelocity = ask(screen, "Enter the initial velocity in m/s ")
    print('You entered ',invelocity)
    pygame.display.quit()
#    invelocity = input('Enter the initial velocity: ')
#    print('You entered ',invelocity)

    #redefining variables just for clarity
    vi = float(invelocity)
    theta = float(inangle)


    #Position of target (building) is exactly 10m high,
    #with a down range distance of 50
    #N.B. yt is the middle point of the buildings height
    xt = 50
    yt = 5

    
    #Position of projectile follows the kinematic EOMs:
    X0 = 0
    Y0 = 15
    vix = vi*mth.cos(theta)
    viy = vi*mth.sin(theta)
    ax = 0
    ay = -9.81

    #d=vt, in x gives the time at which the projectile is down range at the target:
    #that is, when x=xt
    t=(xt-X0)/vix

    #the height at that range is:
    y = viy*t+0.5*ay*t**2+Y0

#    print 'y = ',y

    #launch/fire trebuchet video
    os.system("vlc --play-and-exit --fullscreen --start-time 128 --stop-time 132 trebuchetlaunch.webm")

    #If the projectile is at the height of the target it hits,
    #if not, you get taunted by monty python and the holy grail tips

    if (y > yt-5) and (y < yt+5):
#        print 'play demolition movie'

        #Display a photo of gittenger for a few seconds
        screen = pygame.display.set_mode((960,720)) #screen size set to image size
        Gitter = target()
        allsprites = pygame.sprite.RenderPlain(Gitter)
        #Draw Everything
        allsprites.draw(screen)
        pygame.display.flip()

        os.system("cvlc --play-and-exit --start-time 4 --stop-time 10 shot.mp3")
	pygame.display.quit()
        
#        #add a delay here.  No longer needed as code doesnt finish sound clip in cvlc
#	time.sleep(3)
#	pygame.display.quit()

        os.system("vlc --play-and-exit --fullscreen --start-time 2 --stop-time 30 Nuke.webm")
        os.system("vlc --play-and-exit --fullscreen --start-time 0 --stop-time 7 golfclap.webm")

        tryagain = 0 #break out if they want out

                    
    else:
#        print 'play monty python fail video'
        #Display a photo of gittenger for a few seconds
        screen = pygame.display.set_mode((960,720))
        Gitter = target()
        allsprites = pygame.sprite.RenderPlain(Gitter)
        #Draw Everything
        allsprites.draw(screen)
        pygame.display.flip()

        os.system("cvlc --play-and-exit --start-time 4 --stop-time 10 shot.mp3")
	pygame.display.quit()
        
#        #add a delay here
#	time.sleep(3)
#	pygame.display.quit()
        
        if loose%3 == 0:
            os.system("vlc --play-and-exit --fullscreen --start-time 91 --stop-time 96 frenchtaunter.webm")
        elif loose%3 == 1:
            os.system("vlc --play-and-exit --fullscreen --start-time 106 --stop-time 115 frenchtaunter.webm")
        elif loose%3 == 2:
            os.system("vlc --play-and-exit --fullscreen --start-time 119 --stop-time 123 frenchtaunter.webm")

        loose = loose+1
            
        breakout = 1
        while breakout == 1: #when its false it moves on!
#            giveup = input('Would you like to give up? [1 for y/0 for n]')
            screen = pygame.display.set_mode((1500,720))
    	    pygame.display.set_caption('Down With Gittinger Hall!!!')
    	    giveup = ask(screen, "Would you like to give up? [1 for yes or 0 for no] ")
	    pygame.display.quit()
            if int(float(giveup)) == 1:
                tryagain = 0 #break out if they want out
                breakout = 0
                #if you give up play the bye bye taunter video:
                os.system("vlc --play-and-exit --fullscreen --start-time 168 --stop-time 170 frenchtaunter.webm")
            elif int(float(giveup)) == 0:
                breakout = 0
                # repeat code, try again is still true so outer while loop goes again
                # breakout to 0 gets it out of this while loop
            else:
                screen = pygame.display.set_mode((1920,720))
    	        pygame.display.set_caption('Down With Gittinger Hall!!!')
    	        ask(screen, "You big dummy, enter 1 for yes and 0 for no. Practice: Type 1 or 0 ")
	        pygame.display.quit()
#                print 'You big dummy, enter 1 for y or 0 for n'

screen = pygame.display.set_mode((980,720))
pygame.display.set_caption('Down With Gittinger Hall!!!')
fontobject = pygame.font.Font(None,72)
screen.blit(fontobject.render("Huzzah, hackathon 2k16 was fun!", 1, (255,255,255)),
              (0, (screen.get_height() / 2) - 10))
pygame.display.flip()
time.sleep(5)
pygame.display.quit()
#print 'Huzzah, hackathon 2k16 was fun!'
