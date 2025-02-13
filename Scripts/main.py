import os
import sys
import math
import pygame
import maps
import random
import time
import pyautogui

pygame.init()

######################################
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100
        self.speed = 0.01

    def update(self):
        pass

    
class Square:
    def __init__(self, x, y):
        size = random.randint(1, 15)
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = random.uniform(6, 7)
        self.angle = random.uniform(180, 360) 
        self.dx = self.speed * math.cos(math.radians(self.angle))
        self.dy = self.speed * math.sin(math.radians(self.angle))
        self.lifetime = random.randint(5, 15) 

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.lifetime -= 1

    def is_alive(self):
        return self.lifetime > 0
########################

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GRASS = (203, 203, 203)
GREY = (224, 224, 224)

FPS = 140

width = 1200
height = 800

player_speed = 0.015
p_x = 1
p_y = 1
offset = 0
turn_angle = -360
view_angle = 100
math_angle = turn_angle
raycast_step = 1
ray_len = 50
move_x, move_y = 0, 0
move_angle = 0
scope = False

clock = pygame.time.Clock()

screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)


pygame.display.set_caption("game")
MOVE_TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_TIMER, 1)

CAMERA_TIMER = pygame.USEREVENT + 2
pygame.time.set_timer(CAMERA_TIMER, 30)


dog_surf = pygame.image.load(os.path.join('Images', "gun.png"))
dog_surf.set_colorkey((255, 255, 255))
dog_rect = dog_surf.get_rect(bottomright=(width, height))

gun_scope_surf = pygame.image.load(os.path.join('Images', "gun_scope.png"))
gun_scope_surf.set_colorkey((255, 255, 255))
gun_scope_rect = gun_scope_surf.get_rect(bottomright=(width, height))

running = True

mx0, my0 = pygame.mouse.get_pos()
update_move_dir_fd = False
update_move_dir_bk = False
update_move_dir_lt = False
update_move_dir_rt = False

squares = []#particles

while running:
    #convert angle
    if turn_angle < -360 and turn_angle >= -720:
        math_angle = -(turn_angle + 360)
    if turn_angle >= -360 and turn_angle <= 0:
        math_angle = -(360 + turn_angle)
    if math_angle < 0:
        math_angle = 360 + math_angle
    math_angle -= view_angle / 2

    if math_angle < 0:
        math_angle = 360 + math_angle
    math_angle += 90
    #correct angle
    if turn_angle >= 0 and turn_angle <= 10:
        turn_angle = -360
    if turn_angle <= -720 and turn_angle <= -740:
        turn_angle = -360 
        
    width, height = screen.get_size()
    screen.fill((0, 0, 0))
    #pygame.draw.rect(screen, (255, 0, 0), (10, 10, 100, 10), 0)

    #raycast
    for current_angle in range(turn_angle, view_angle + raycast_step, raycast_step):
        for distance in range(1, ray_len):
            if current_angle >= 0 and current_angle <= 90 or 1:
                try:
                    x = round(p_x + (math.sin(math.radians(current_angle))) * distance)
                    y = round(p_y + (math.cos(math.radians(current_angle))) * distance)
                    a = maps.map1[x][y]
                except:
                    break

                x = round(p_x + (math.sin(math.radians(current_angle))) * distance)
                y = round(p_y + (math.cos(math.radians(current_angle))) * distance)
                #print(round(x), round(y))

                if maps.map1[x][y] == "^":#Walls
                    #print(distance, current_angle)
                    gray_scale = 1200 / distance
                    if gray_scale > 100: 
                        gray_scale = 100
                    pygame.draw.rect(screen, (gray_scale, gray_scale, gray_scale),
                                    ((width/view_angle)*(current_angle-turn_angle), (height/2)-height/(2*distance)+offset,
                                        width/100, height/distance), 0)
                    pygame.draw.rect(screen, GRASS,
                                    ((width/view_angle)*(current_angle-turn_angle), (height/2)-height/(2*distance)+offset + height/distance,
                                        width/100, height), 0)

                    break
                if maps.map1[x][y] == "#":#Obstacle
                    #print(distance, current_angle)
                    gray_scale = 1200 / distance
                    if gray_scale > 100: 
                        gray_scale = 100
                    pygame.draw.rect(screen, (255, gray_scale, gray_scale),#Object
                                    ((width/view_angle)*(current_angle-turn_angle), (height / 2)-height/(2/3*distance)+offset,
                                        width/100, 3* height / distance), 0)
                    pygame.draw.rect(screen, GRASS,#Grass
                                    ((width/view_angle)*(current_angle-turn_angle), (height/2)-height/(2*distance)+offset + height/distance,
                                        width/100, height), 0)

                    break

    #print(move_x, move_y)
    mx, my=pygame.mouse.get_pos()
    print(math_angle)
    offset = height - my - height / 3

    if mx0 != mx:
        if mx < mx0:
            move_angle = -3
        else:
            move_angle = 3
    else:
        move_angle = 0

    mx0, my0 = pygame.mouse.get_pos()

    if scope:
        #print(gun_scope)
        #pygame.draw.line(screen, (0, 255, 0), [width / 2, height / 10 * 4.5], [width / 2, height / 10 * 5.5], 2)
        #pygame.draw.line(screen, (0, 255, 0), [width / 10 * 4.5, height / 2], [width / 10 * 5.5, height / 2], 2)
        scale = pygame.transform.scale(
        gun_scope_surf, (gun_scope_surf.get_width() // 1,
               gun_scope_surf.get_height() // 1))
        scale_rect = scale.get_rect(bottomright=(width / 2 + 200, height))
        screen.blit(scale, scale_rect)

    else:
        scale = pygame.transform.scale(
        dog_surf, (dog_surf.get_width() // 1,
               dog_surf.get_height() // 1))
        scale_rect = scale.get_rect(bottomright=(width + 50, height))
        screen.blit(scale, scale_rect)
    
    move_x, move_y = 0, 0
    slow = 1

    if update_move_dir_fd:
        move_y = player_speed * math.sin(math.radians(math_angle))
        move_x = player_speed * math.cos(math.radians(math_angle))
        slow = 4

    if update_move_dir_bk:
        move_y = -player_speed * math.sin(math.radians(math_angle))
        move_x = -player_speed * math.cos(math.radians(math_angle))
        slow = 4


    if update_move_dir_rt:
        move_y += player_speed * math.sin(math.radians(math_angle - 90)) / slow
        move_x += player_speed * math.cos(math.radians(math_angle - 90)) / slow

    if update_move_dir_lt:
        move_y += player_speed * math.sin(math.radians(math_angle + 90)) / slow
        move_x += player_speed * math.cos(math.radians(math_angle + 90)) / slow

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx_shoot, my_shoot = pygame.mouse.get_pos()
                for _ in range(25):  # Particles
                    squares.append(Square(width / 2, height * 0.55))

            elif event.button == 3:
                scope = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pass
            elif event.button == 3:
                scope = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                update_move_dir_fd = True

                move_y = player_speed * math.sin(math.radians(math_angle))
                move_x = player_speed * math.cos(math.radians(math_angle))

            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                update_move_dir_bk = True

                move_y = -player_speed * math.sin(math.radians(math_angle))
                move_x = -player_speed * math.cos(math.radians(math_angle))
                
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                update_move_dir_lt = True

                
  
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                update_move_dir_rt = True

        if event.type == CAMERA_TIMER:
                turn_angle += move_angle
        if event.type == MOVE_TIMER or 1:
                if maps.map1[round(p_x + move_x)][round(p_y + move_y)] == ".": #No collision
                    p_x += move_x
                    p_y += move_y

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                update_move_dir_fd = False
                move_x, move_y = 0, 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                update_move_dir_bk = False
                move_x, move_y = 0, 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                update_move_dir_lt = False
                move_x, move_y = 0, 0

            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                update_move_dir_rt = False
                move_x, move_y = 0, 0
    

    for square in squares[:]:#Update particles
            square.update()
            if not square.is_alive():
                squares.remove(square)
    for square in squares:
            pygame.draw.rect(screen, random.choice([RED, GREY, YELLOW, GREY, YELLOW]), square.rect)


    clock.tick(FPS)
    pygame.display.flip()