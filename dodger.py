import pygame
from pygame.locals import *
import sys
import random

#------------ INIT ------------#
pygame.joystick.init()
pygame.font.init()
pygame.init()

WIDTH = 480
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dodger')

clock = pygame.time.Clock()

#joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
#js = joysticks[0]
#js.init()

#------------ COLORS ------------#
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#------------ FUNCTIONS ------------#
def name_input():
  global player_name
  title_font = pygame.font.Font('PressStart2P.ttf', 28)
  font = pygame.font.Font('PressStart2P.ttf', 24)
  selection = 0
  in_menu = True

  title_render = title_font.render('NEW HIGH SCORE', True, WHITE)
  screen.blit(title_render, (WIDTH/2 - title_render.get_width()/2, 120))

  letters = ('abcdefghijklmnopqrstuvwxyz')
  name = ""
  name_index = 0

  while in_menu:

      # Event Loop
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()

        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_RETURN:
              print('enter pressed')
              if selection == 27:
                player_name = name
                in_menu = False
                return
              else:
                if len(name) < 8:
                  name += letters[selection]

          if event.key == pygame.K_DOWN:
            print('down pressed')
            if selection < 17:
              selection += 9
            else:
              selection = 27

          if event.key == pygame.K_UP:
            print('up pressed')
            if selection > 8:
              selection -= 9
            elif selection == 27:
              selection = 26

          if event.key == pygame.K_RIGHT:
            print('right pressed')
            if selection < 25 and selection not in [8, 17, 27]:
              selection += 1

          if event.key == pygame.K_LEFT:
            print('left pressed')
            if selection > 0 and selection not in [9, 18, 27]:
              selection -= 1
          
      # Update
      line_text = ""

      for i in range(len(name)):
        line_text += name[i]
        if i != 7:
          line_text += " "

      if len(line_text) < 15:
        if selection < 26:
          line_text += letters[selection] + " "

      while len(line_text) < 16:
        if len(line_text) != 15:
          line_text += "_"
        if len(line_text) != 16:
          line_text += " "

      lines_render = font.render(line_text, True, WHITE)
      
      letter_renders = []
      for i in range(len(letters)):
        if i == selection:
          render = font.render(letters[i], True, RED)
        else:
          render = font.render(letters[i], True, WHITE)
        letter_renders.append(render)
      
      submit_render = font.render('SUBMIT', True, WHITE)
      if selection == 27:
        submit_render = font.render('SUBMIT', True, RED)

      # Draw
      screen.fill(BLACK)
  
      screen.blit(title_render, (WIDTH/2 - title_render.get_width()/2, 50))
      screen.blit(lines_render, (WIDTH/2 - lines_render.get_width()/2, 125))

      count = 0
      x_offset = 50
      y_offset = 225
      for render in letter_renders:
        screen.blit(render, (x_offset, y_offset))
        count += 1
        x_offset += render.get_width() + 20
        if count % 9 == 0:
          x_offset = 50
          y_offset += render.get_height() + 20
          count = 0

      screen.blit(submit_render, (300, 400))

      # Load
      pygame.display.flip()
      clock.tick(60)

def game_over():
  global game_state, player_score, player_name, leaderboard_names, leaderboard_scores
  game_state = 'dead'
  new_record = False

  # update scores
  index = 0
  for score in leaderboard_scores:
    if player_score > score:
      name_input()
      leaderboard_scores.insert(index, player_score)
      leaderboard_names.insert(index, player_name)
      leaderboard_scores.pop()
      leaderboard_names.pop()
      new_record = True
      break
    index += 1

  save_leaderboard()
  if new_record:
    leaderboard()

def load_leaderboard():
  global leaderboard_names, leaderboard_scores
  file = 'leaderboard.txt'

  with open(file) as f:
    line = f.readline()
    while line:
      line = line.strip().split()
      leader = line[0]
      score = int(line[1])
      leaderboard_names.append(leader)
      leaderboard_scores.append(score)
      line = f.readline()

def save_leaderboard():
  global leaderboard_names, leaderboard_scores
  file = open('leaderboard.txt', 'w')

  for i in range(len(leaderboard_names)):
    text = f"{leaderboard_names[i]} {leaderboard_scores[i]}\n"
    file.write(text)
  file.close()

def spawn_enemy():
  enemy = Enemy()
  enemy.x = random.randint(0, 480 - enemy.width)
  enemy_list.append(enemy)

def draw_score():
  global player_score, game_state
  font = pygame.font.Font('PressStart2P.ttf', 14)
  render = font.render('Score = 0', True, WHITE)
  render2 = font.render('Play again? Press enter.', True, WHITE)
  render = font.render('Score = ' + str(player_score), True, WHITE)
  
  screen.blit(render, (10, 420))

  if game_state == 'dead':
    screen.blit(render2, (10, 450))

def main_menu():
  global game_state, enemy_list, player_score
  title_font = pygame.font.Font('PressStart2P.ttf', 36)
  font = pygame.font.Font('PressStart2P.ttf', 24)
  selection = 1
  in_menu = True

  while in_menu:

      # Event Loop
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()

        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_RETURN:
              print('enter pressed')
              if selection == 1:
                print('play')
                game_state = 'playing'
                enemy_list = []
                player_score = 0
                in_menu = False
                return

              elif selection == 2:
                print('leaderboard')
                in_menu = False
                leaderboard()
                return

              elif selection == 3:
                print('credits')
                in_menu = False
                credits()
                return

              elif selection == 4:
                print('quit')
                pygame.quit()
                sys.exit()

          if event.key == pygame.K_DOWN:
            print('down pressed')
            selection += 1
            if selection > 4:
                selection = 1

          if event.key == pygame.K_UP:
            print('up pressed')
            selection -= 1
            if selection < 1:
                selection = 4
          
      # Update

      # Draw
      screen.fill(BLACK)

      title_render = title_font.render('DODGER', True, WHITE)
      screen.blit(title_render, (WIDTH/2 - title_render.get_width()/2, 120))
  
      line_text = ['PLAY', 'LEADERBOARD', 'CREDITS', 'QUIT']
      y = 240
      for line in line_text:
        render = font.render(line, True, WHITE)
        if line_text.index(line) + 1 == selection:
          render = font.render(line, True, RED)
        screen.blit(render, (WIDTH/2 - render.get_width()/2, y))
        y += 40

      # Load
      pygame.display.flip()
      clock.tick(60)

def credits():
  title_font = pygame.font.Font('PressStart2P.ttf', 24)
  font = pygame.font.Font('PressStart2P.ttf', 20)
  selection = 1
  in_menu = True

  screen.fill(BLACK)
  
  title_render = title_font.render('CREDITS', True, WHITE)
  screen.blit(title_render, (WIDTH/2 - title_render.get_width()/2, 60))

  class_text = ['Made by 2019-2020', 'Raspberry Pi Class:']
  students = ['Frasher Gray', 'Kevin Meek', 'Zyler Mardis', 'Cullen Nagle']
  
  y = 140
  for line in class_text:
    render = font.render(line, True, WHITE)
    x = WIDTH/2 - render.get_width()/2
    screen.blit(render, (x, y))
    y += 40

  for student in students:
    render = font.render(student, True, GRAY)
    x = WIDTH/2 - render.get_width()/2
    screen.blit(render, (x, y))
    y += 40

  back_render = font.render('BACK TO MAIN MENU', True, RED)
  screen.blit(back_render, (WIDTH/2 - back_render.get_width()/2, 420))
  
  while in_menu:

    # Event Loop
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          print('enter pressed')
          main_menu()
          in_menu = False
          return
      
    # Update
    
    # Draw

    # Load
    pygame.display.flip()
    clock.tick(60)

def pause():
  title_font = pygame.font.Font('PressStart2P.ttf', 36)
  font = pygame.font.Font('PressStart2P.ttf', 24)
  selection = 1
  in_menu = True

  while in_menu:

    # Event Loop
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          print('escape pressed')
          break

        if event.key == pygame.K_DOWN:
          print('down pressed')
          selection += 1
          if selection > 2:
            selection = 1
        
        if event.key == pygame.K_UP:
          print('up pressed')
          selection -= 1
          if selection < 1:
              selection = 2
        
        if event.key == pygame.K_RETURN:
          if selection == 1:
            return
          if selection == 2:
            print('quit')
            in_menu = False
            main_menu()
            return
  
    # Update

    # Draw
    pygame.draw.rect(screen, BLUE, (100, 80, 280, 300))
    
    title_render = title_font.render('Pause', True, WHITE)
    resume_render = font.render('Resume', True, WHITE)
    quit_render = font.render('Quit', True, WHITE)

    if selection == 1:
        resume_render = font.render('Resume', True, RED)
    
    elif selection == 2:
        quit_render = font.render('Quit', True, RED)

    x = WIDTH/2 - title_render.get_width()/2
    screen.blit(title_render, (x, 120))

    x = WIDTH/2 - resume_render.get_width()/2
    screen.blit(resume_render, (x, 220))

    x = WIDTH/2 - quit_render.get_width()/2
    screen.blit(quit_render, (x, 300))

    # Load
    pygame.display.flip()
    clock.tick(60)

def leaderboard():
  title_font = pygame.font.Font('PressStart2P.ttf', 24)
  font = pygame.font.Font('PressStart2P.ttf', 20)
  selection = 1
  in_menu = True
  leaders = []
  scores = []

  file = 'leaderboard.txt'
  with open(file) as f:
    line = f.readline()
    while line:
      line = line.strip().split()
      print(f"line: {line}")
      leader = line[0]
      score = line[1]
      print(f"leader: {leader}")
      print(f"score: {score}")
      leaders.append(leader)
      scores.append(score)
      line = f.readline()

  screen.fill(BLACK)
  render = title_font.render('LEADERBOARD', True, WHITE)
  screen.blit(render, (WIDTH/2 - render.get_width()/2, 60))

  y = 140
  while len(leaders) > 0:
    text = f"{leaders.pop(0)}"
    render = font.render(text, True, WHITE)
    screen.blit(render, (40, y))
    text = f"{scores.pop(0)}"
    render = font.render(text, True, WHITE)
    screen.blit(render, (360, y))
    y += 40
  
  render = font.render('BACK TO MAIN MENU', True, RED)
  screen.blit(render, (WIDTH/2 - render.get_width()/2, 420))

  while in_menu:

    # Event Loop
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          print('enter pressed')
          in_menu = False
          main_menu()
          return
        
    # Update

    # Draw
    
    # Load
    pygame.display.flip()
    clock.tick(60)

#------------ CLASSES ------------#
class Player():
  width = 50
  height = 50
  x = WIDTH / 2 - width / 2
  y = 350
  color = (255, 0, 255)
  rect = pygame.Rect(x, y, width, height)
  direction = 0
  velocity = 3

  def is_collided_with(self, enemy_list):
    for enemy in enemy_list:
      if self.rect.colliderect(enemy.rect):
        print('collision')
        return True
    return False

  def update(self):
    self.x += self.velocity * self.direction
    if self.x < 0:
      self.x = 0
    if self.x > 480 - self.width:
      self.x = 480 - self.width

  def draw(self):
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    pygame.draw.rect(screen, self.color, self.rect)

class Enemy():
  width = 25
  height = 25
  x = 0
  y = 0
  color = (0, 255, 0)
  rect = pygame.Rect(x, y, width, height)
  direction = 1
  velocity = 3

  def update(self):
    self.y += self.direction * self.velocity

  def draw(self):
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    pygame.draw.rect(screen, self.color, self.rect)

#------------ OBJECTS ------------#
player = Player()
player_score = 0
player_name = ''

enemy = Enemy()
enemy_list = []
enemy_spawn_time = 1000
timer_check = False
event_id = pygame.USEREVENT + 1
pygame.time.set_timer(event_id, enemy_spawn_time)

game_state = 'playing'

leaderboard_names = []
leaderboard_scores = []
load_leaderboard()
print(f"leaderboard_names: {leaderboard_names}")
print(f"leaderboard_scores: {leaderboard_scores}")

#------------ Game Loop ------------#

main_menu()

while True:
  
  # Event Loop
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()

    if event.type == pygame.JOYAXISMOTION:
      if js.get_axis(0) == -1:
        print('move left')
        player.direction = -1
      if js.get_axis(0) == 0:
        print('stop moving')
        player.direction = 0
      if js.get_axis(0) > 0.9:
        print('move right')
        player.direction = 1
        
    if event.type == pygame.JOYBUTTONDOWN:
      if event.key == js.get_button(1):
          print('a pressed')
          if game_state == 'dead':
            print('restart')
            game_state = 'playing'
            enemy_list = []
            player_score = 0
            enemy_spawn_time = 1000

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT or event.key == pygame.K_a:
        print('move left')
        player.direction = -1
      if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        print('move right')
        player.direction = 1
      if event.key == pygame.K_RETURN:
        if game_state == 'dead':
          print('restart')
          game_state = 'playing'
          enemy_list = []
          player_score = 0
          enemy_spawn_time = 1000
      if event.key == pygame.K_ESCAPE:
        print('pause')
        pause()

    if event.type == pygame.KEYUP:
      print('stop moving')
      player.direction = 0
    
    if event.type == event_id:
      if game_state == 'playing':
        print('spawn enemy')
        spawn_enemy()

  # Update
  if game_state == "playing":
    
    if player_score % 5 == 0 and timer_check == True:
      if enemy_spawn_time >= 150:
        enemy_spawn_time -= 50
      pygame.time.set_timer(event_id, enemy_spawn_time)
      print(f'enemy_spawn_time: {enemy_spawn_time}')
      timer_check = False

    if player.is_collided_with(enemy_list):
      game_over()
    else:
      player.update()
      for enemy in enemy_list:
        enemy.update()
        if enemy.y > 400 - enemy.width:
          enemy_list.remove(enemy)
          player_score += 1
          timer_check = True

  # Draw
  screen.fill(BLACK)
  pygame.draw.line(screen, WHITE, (0, 350 + player.height+1), (WIDTH, 350 + player.height+1), 3)
  player.draw()
  for enemy in enemy_list:
    enemy.draw()
  draw_score()

  # Load
  pygame.display.flip()
  clock.tick(60)