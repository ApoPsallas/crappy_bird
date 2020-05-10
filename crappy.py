import pygame
from colors import *
from pygame.transform import *
from pygame.locals import *
import random
from time import sleep
from screen import Screen
from bird import Bird
from obstacle import Obstacle
from cloud import Cloud
pygame.init()
pygame.mixer.init()
path = './/'

def init_bird(bird, screen):
  bird.up_img = path+'bird_wings_up.png'
  bird.down_img = path+'bird_wings_down.png'
  bird.down = pygame.image.load(bird.down_img)
  bird.up = pygame.image.load(bird.up_img)
  bird.curr = bird.up
  bird.x_axis = (screen.width/3)-(bird.width/2)
  bird.y_axis = (screen.height/2)-(bird.height/2)
  bird.height = 27
  bird.width = 40

  return bird

def init_obstacle(obstacle,screen):    
  obstacle.width = 80
  obstacle.x_axis = screen.width
  obstacle.y_axis = random.randrange(screen.height/2, screen.height-100, 20)
  obstacle.height = screen.height - obstacle.y_axis
  obstacle.ground_height = 20
  obstacle.hole = 100
  obstacle.speed = 5

  return obstacle

def init_cloud(cloud, screen):
  cloud_img = path+'cloud.png'
  cloud.sprite = pygame.image.load(cloud_img)
  cloud.speed = 2
  cloud.x_axis = screen.width
  cloud.y_axis = random.randrange(screen.height/4, screen.height-screen.height/4, 100)
  
  return cloud

def deleteContent(fd):
  os.ftruncate(fd, 0)
  os.lseek(fd, 0, os.SEEK_SET)

def play_sound (effect):
  pygame.mixer.Sound.play(effect)

def next_position(bird, screen):
  if bird.x_axis <= 0:
    bird.x_axis = 0
  if bird.x_axis+bird.width >= screen.width:
    bird.x_axis = screen.width - bird.width
  if bird.y_axis <= 0:
    bird.y_axis = 0
  if bird.y_axis+bird.height >= screen.height:
    bird.y_axis = screen.height - bird.height
  return bird.x_axis, bird.y_axis

def is_collision(bird, screen, obstacle):
  flag = False
  if bird.x_axis<obstacle.x_axis+obstacle.width and bird.x_axis+bird.width>obstacle.x_axis:
      if bird.y_axis<obstacle.y_axis-obstacle.hole or bird.y_axis+bird.height>obstacle.y_axis:
          flag = True
  if bird.y_axis +  bird.height >= screen.height - obstacle.ground_height:
      flag = True
  return flag

# INITIALIZE GAME
try:
    file = open(path+'high_score.txt', 'r')
    high_score = file.read()
    high_score = int(high_score)
    file.close
except IOError:
    high_score = 0

cr_icon = path+'crappy_icon.jpg'
icon = pygame.image.load(cr_icon)
flap = pygame.mixer.Sound(path+'flap.wav')
punch = pygame.mixer.Sound(path+"hit2.wav")
tick = pygame.mixer.Sound(path+"point2.wav")
score_flag = False
score = 0
final_score = 0
score_font = pygame.font.SysFont("monospace", 30)
game_over_font = pygame.font.SysFont("monospace", 50)
score_font.set_bold(True)
game_over_font.set_bold(True)
FPS = 60
screen = Screen()
screen.init_screen(800, 600)
gameDisplay = pygame.display.set_mode((screen.width,screen.height))
pygame.display.set_caption('Crappy Bird')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

gameExit = False
game_over = False

#Create Entities
bird = Bird()
obstacle = Obstacle()
cloud = Cloud()

bird = init_bird(bird,screen)
obstacle = init_obstacle(obstacle,screen)
cloud = init_cloud(cloud, screen)

gravity = 2
lift = 0

# Game Screen Loop
while not gameExit:

# Player Actions
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        gameExit = True
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            play_sound(flap)
            gravity = -3
            lift = 15
            bird.curr= bird.down
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_SPACE:
            bird.curr= bird.up

# Calculate motion
  if lift < 0:
    gravity = 2
  
  bird.y_axis += gravity
  bird.x_axis,bird.y_axis = next_position(bird,screen)

  if cloud.x_axis <= -100 :
    cloud.y_axis = random.randrange(screen.height/4, screen.height-screen.height/4, 100)
    cloud.x_axis = screen.width

  if obstacle.x_axis <= - obstacle.width:
    obstacle = init_obstacle(obstacle, screen)
    score_flag = False

  if obstacle.x_axis + obstacle.width < bird.x_axis:
    if score_flag == False:
        play_sound(tick)
        score += 1
        score_flag = True

  obstacle.x_axis -= obstacle.speed
  cloud.x_axis -= cloud.speed
  lift -= 1

  game_over = is_collision(bird, screen, obstacle)

  # DRAW ENTITIES
  gameDisplay.fill(light_blue)
  # draw cloud
  gameDisplay.blit(cloud.sprite, (cloud.x_axis,cloud.y_axis ))

  # draw lower obstacle
  pygame.draw.rect(gameDisplay, green,[obstacle.x_axis,obstacle.y_axis,obstacle.width,obstacle.height])

  # draw upper obstacle
  pygame.draw.rect(gameDisplay, green,[obstacle.x_axis,0,obstacle.width,obstacle.y_axis-obstacle.hole])

  #draw ground
  pygame.draw.rect(gameDisplay, brown,[0,screen.height-obstacle.ground_height,screen.width,obstacle.ground_height])

  #draw bird
  gameDisplay.blit(bird.curr,(bird.x_axis,bird.y_axis))

  score_label = score_font.render('score:'+str(score), 1, black)
  gameDisplay.blit(score_label, (0, 0))
  pygame.display.update()

  if game_over:
    play_sound(punch)
    obstacle.x_axis = screen.width
    bird.y_axis = (screen.height/2)-(bird.height/2)
    final_score = score
    score = 0
    score_flag = False

  clock.tick(FPS)

  #Game Over Screen Loop
  while game_over:
    if final_score > high_score:
        high_score = final_score
    gameDisplay.fill(red)
    score_label = score_font.render('score:'+str(final_score), 1, black)
    gameDisplay.blit(score_label, (10,0))
    high_score_label = score_font.render('high score: '+str(high_score), 1, black)
    gameDisplay.blit(high_score_label,(10,50))
    game_over_label = game_over_font.render("GAME OVER", 1, black)
    gameDisplay.blit(game_over_label,((screen.width/3)-20,screen.height/3))
    gameDisplay.blit(rotate(bird.curr, 180),((screen.width/2)-bird.width/2,(screen.height/2)-bird.height/2))
    
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
            game_over = False

        if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_RETURN:
                game_over = False
    clock.tick(FPS)

file = open(path+'high_score.txt','w')

file.write(str(high_score))
file.close
pygame.quit()
quit()
