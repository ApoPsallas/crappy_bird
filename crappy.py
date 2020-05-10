import pygame
from pygame.transform import *
from pygame.locals import *
import random
from time import sleep
path = './/'
pygame.init()
pygame.mixer.init()
try:
    file = open(path+'high_score.txt', 'r')
    high_score = file.read()
    high_score = int(high_score)
    file.close
except IOError:
    high_score = 0
cr_icon = path+'crappy_icon.jpg'
print(cr_icon)
icon = pygame.image.load(cr_icon)
flap = pygame.mixer.Sound(path+'flap.wav')
punch = pygame.mixer.Sound(path+"hit2.wav")
tick = pygame.mixer.Sound(path+"point2.wav")
score_flag = False
score = 0
final_score = 0
score_font = pygame.font.SysFont("monospace", 30)
white = (255,255,255)
black = (0,0,0)
brown = (160,82,45)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
light_blue = (100,100,255)
yellow = (255,255,0)
grey = (128,128,128)
cloud_img = path+'cloud.png'
bird_up_img = path+'bird_wings_up.png'
bird_down_img = path+'bird_wings_down.png'
cloud = pygame.image.load(cloud_img)
bird_down = pygame.image.load(bird_down_img)
bird_up = pygame.image.load(bird_up_img)
screen_width = 800
screen_height = 600
bird_height = 27
bird_width = 40
block_speed = 10
lead_x = (screen_width/3)-(bird_width/2)
lead_y = (screen_height/2)-(bird_height/2)
lead_x_change = 0
lead_y_change = 0
obstacle_width = 80
obstacle_x = screen_width
obstacle_y = random.randrange(screen_height/2, screen_height-100, 20)
obstacle_height = screen_height - obstacle_y
ground_height = 20
hole = 100
obstacle_speed = 5
cloud_speed = 2
gravity = 2
lift = 0
cloud_x = screen_width
cloud_y = random.randrange(screen_height/4, screen_height-screen_height/4, 100)
FPS = 60
bird = bird_up
angle = 0
check = False
turn_speed = 5
def deleteContent(fd):
    os.ftruncate(fd, 0)
    os.lseek(fd, 0, os.SEEK_SET)
def sound (effect):
    pygame.mixer.Sound.play(effect)
def border(x,y):
  global bird_height
  global bird_width
  if x <= 0:
    x = 0
  if x+bird_width >= screen_width:
    x = screen_width - bird_width
  if y <= 0:
    y = 0
  if y+bird_height >= screen_height:
    y = screen_height - bird_height
  return x, y
def collide(lead_x,lead_y,obstacle_x,obstacle_y):
    global obstacle_width
    global bird_height
    global bird_width
    global hole
    global screen_height
    global ground_height
    flag = False
    if lead_x<obstacle_x+obstacle_width and lead_x+bird_width>obstacle_x:
        if lead_y<obstacle_y-hole or lead_y+bird_height>obstacle_y:
            flag = True
    if lead_y +  bird_height >= screen_height - ground_height:
        flag = True
    return flag
gameDisplay = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Crappy Bird')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

gameExit = False
game_over = False
score_font.set_bold(True)
while not gameExit:

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        gameExit = True
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            sound(flap)
            gravity = -3
            lift = 15
            bird = bird_down
            turn_speed = - 10
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_SPACE:
            bird = bird_up

  gameDisplay.fill(light_blue)
  lead_y += gravity
  if lift < 0:
    gravity = 2
  lead_x,lead_y = border(lead_x,lead_y)
  if cloud_x <= -100 :
    cloud_y = random.randrange(screen_height/4, screen_height-screen_height/4, 100)
    cloud_x = screen_width


  gameDisplay.blit(cloud, (cloud_x,cloud_y ))
  if obstacle_x <= - obstacle_width:
    obstacle_y = random.randrange(screen_height/2, screen_height-100, 20)
    obstacle_x = screen_width
    obstacle_height = screen_height - obstacle_y
    score_flag = False
  pygame.draw.rect(gameDisplay, green,[obstacle_x,obstacle_y,obstacle_width,obstacle_height])
  pygame.draw.rect(gameDisplay, red,[obstacle_x-10,obstacle_y,obstacle_width+20,20])
  pygame.draw.rect(gameDisplay, green,[obstacle_x,0,obstacle_width,obstacle_y-hole])
  pygame.draw.rect(gameDisplay, red,[obstacle_x-10,obstacle_y-hole-20,obstacle_width+20,20])
  pygame.draw.rect(gameDisplay, brown,[0,screen_height-ground_height,screen_width,ground_height])
  gameDisplay.blit(rotate(bird, angle),(lead_x,lead_y))
  score_label = score_font.render('score:'+str(score), 1, (0,0,0))
  gameDisplay.blit(score_label, (0, 0))
  pygame.display.update()
  obstacle_x -= obstacle_speed
  cloud_x -= cloud_speed
  lift -= 1
  # angle -= turn_speed
  # if angle <= -25:
    # angle = -25
    # turn_speed = 10
  # if angle >= 25:
    # angle = 25
    # turn_speed = 10
  game_over = collide(lead_x,lead_y,obstacle_x,obstacle_y)

  if obstacle_x + obstacle_width < lead_x:
    if score_flag == False:
        sound(tick)
        score += 1
        score_flag = True
  if game_over:
    sound(punch)
    obstacle_x = screen_width
    lead_y = (screen_height/2)-(bird_height/2)
    final_score = score
    score = 0
    score_flag = False
    angle = 0

  clock.tick(FPS)
  while game_over:
    if final_score > high_score:
        high_score = final_score
    gameDisplay.fill(red)
    gameDisplay.blit(rotate(bird, 180),((screen_width/2)-bird_width/2,(screen_height/2)-bird_height/2))
    score_label = score_font.render('score:'+str(final_score), 1, (0,0,0))
    gameDisplay.blit(score_label, (10,0))
    high_scorelbl = score_font.render('high score: '+str(high_score), 1, (0,0,0))
    gameDisplay.blit(high_scorelbl,(10,50))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
            game_over = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_over = False
    clock.tick(FPS)

file = open(path+'high_score.txt','w')

file.write(str(high_score))
file.close
pygame.quit()
quit()
