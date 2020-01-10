import math
import random
import pygame
from pygame.locals import *
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
keys = [False, False, False, False]
playerpos = [100, 100]
acc = [0, 0]
arrows = []
badtimer = 10
badtimer1 = 0
badguys = [[640, 100]]
healthvalue = 194
pygame.mixer.init()
rabbit_img = pygame.image.load("resources/images/dude.png")
grass_img = pygame.image.load("resources/images/grass.png")
castle_img = pygame.image.load("resources/images/castle.png")
arrow_img = pygame.image.load('resources/images/bullet.png')
badguy_img1 = pygame.image.load("resources/images/badguy.png")
badguy_img = badguy_img1
healthbar_img = pygame.image.load("resources/images/healthbar.png")
health_img = pygame.image.load("resources/images/health.png")
gameover_img = pygame.image.load("resources/images/gameover.png")
youwin_img = pygame.image.load("resources/images/youwin.png")
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)
running = True
exitcode = False
while running:
    screen.fill(0)
    for x in range(width//grass_img.get_width()+1):
        for y in range(height//grass_img.get_height()+1):
            screen.blit(grass_img, (x*100, y*100))
    screen.blit(castle_img, (0, 30))
    screen.blit(castle_img, (0, 135))
    screen.blit(castle_img, (0, 240))
    screen.blit(castle_img, (0, 345))
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1]-(playerpos[1]+32), position[0]-(playerpos[0]+26))
    playerrot = pygame.transform.rotate(rabbit_img, 360-angle*57.29)
    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
    screen.blit(playerrot, playerpos1)
    for bullet in arrows:
        index = 0
        velx = math.cos(bullet[0])*10
        vely = math.sin(bullet[0])*10
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
            arrows.pop(index)
        index += 1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow_img, 360-projectile[0]*57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))
    if badtimer == 0:
        badguys.append([640, random.randint(50, 430)])
        badtimer = 100 -(badtimer1*2)
        if badtimer1 >= 35:
            badtimer1 = 35
        else:
            badtimer1 += 5
    index_badguy = 0
    for badguy in badguys:
        if badguy[0] < -64:
             badguys.pop(index_badguy)
        badguy[0] -= 7
        badrect = pygame.Rect(badguy_img.get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        if badrect.left < 64:
            hit.play()
            healthvalue -= random.randint(5, 20)
            badguys.pop(index_badguy)
        index_arrow = 0
        for bullet in arrows:
            bulletrect = pygame.Rect(arrow_img.get_rect())
            bulletrect.left = bullet[1]
            bulletrect.top = bullet[2]
            if badguys:
                if badrect.colliderect(bulletrect):
                    enemy.play()
                    acc[0] += 1
                    badguys.pop(index_badguy)
                    arrows.pp(index_arrow)
            index_arrow += 1
        index_badguy += 1
    for badguy in badguys:
        screen.blit(badguy_img, badguy)
    font = pygame.font.Font(None, 24)
    survivedtext = font.render(str((90000-pygame.time.get_ticks())//60000)+":"+
                               str((90000-pygame.time.get_ticks())//1000%60).zfill(2), True, (0,0,0))
    textRect = survivedtext.get_rect()
    textRect.topright=[635,5]
    screen.blit(survivedtext, textRect)
    screen.blit(healthbar_img, (5, 5))
    for health1 in range(healthvalue):
        screen.blit(health_img, (health1+8, 8))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True
            if event.type == pygame.KEYUP:
                if event.key == K_w:
                    keys[0] = False
            elif event.key == K_a:
                keys[1] = Falsew
            elif event.key == K_s:
                keys[2] = False
            elif event.key == K_d:
                keys[3] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot.play()
            position = pygame.mouse.get_pos()
            acc[1] += 1
            arrows.append([math.atan2(position[1]-(playerpos1[1]+32), position[0]-(playerpos1[0]+26)),
                           playerpos1[0]+32, playerpos1[1]+26])
    if keys[0]:
        playerpos[1] -= 5
    elif keys[2]:
        playerpos[1] += 5
    if keys[1]:
        playerpos[0] -= 5
    elif keys[3]:
        playerpos[0] += 5
    badtimer -= 1
    if pygame.time.get_ticks() >= 90000:
        running = False
        exitcode = True
    if healthvalue <= 0:
        running = False
        exitcode = False
    if acc[1] != 0:
        accuracy = acc[0]*1.0/acc[1]*100
        accuracy = ("%.2f" % accuracy)
    else:
        accuracy = 0
if exitcode == False:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(gameover_img, (0, 0))
    screen.blit(text, textRect)
else:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: "+accuracy+"%", True, (0,255,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(youwin_img, (0,0))
    screen.blit(text, textRect)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.flip()
