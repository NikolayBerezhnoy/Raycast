import math
import pygame
import maps
import time
import pyautogui

FPS = 140

width = 1200
height = 800

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

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("game")
MOVE_TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_TIMER, 1)

CAMERA_TIMER = pygame.USEREVENT + 2
pygame.time.set_timer(CAMERA_TIMER, 30)

running = True

mx0, my0 = pygame.mouse.get_pos()

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
    
    #+ view_angle to math_angle
    # if math_angle >= 0:
    #     math_angle += view_angle / 2
    # else:
    #     math_angle -= view_angle / 2

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
                    if gray_scale > 255: 
                        gray_scale = 255
                    pygame.draw.rect(screen, (gray_scale, gray_scale, gray_scale),
                                    ((width/view_angle)*(current_angle-turn_angle), (height/2)-height/(2*distance)+offset,
                                        width/100, height/distance), 0)
                    pygame.draw.rect(screen, (112, 156, 122),
                                    ((width/view_angle)*(current_angle-turn_angle), (height/2)-height/(2*distance)+offset + height/distance,
                                        width/100, height), 0)

                    break
                if maps.map1[x][y] == "#":#Obstacle
                    #print(distance, current_angle)
                    gray_scale = 1200 / distance
                    if gray_scale > 255: 
                        gray_scale = 255
                    pygame.draw.rect(screen, (gray_scale, gray_scale, 255),
                                    ((width/view_angle)*(current_angle-turn_angle), (height / 2)-height/(2/3*distance)+offset,
                                        width/100, 3* height / distance), 0)
                    pygame.draw.rect(screen, (112, 156, 122),
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
        pygame.draw.line(screen, (0, 255, 0), [width / 2, height / 10 * 4.5], [width / 2, height / 10 * 5.5], 2)
        pygame.draw.line(screen, (0, 255, 0), [width / 10 * 4.5, height / 2], [width / 10 * 5.5, height / 2], 2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pygame.draw.line(screen, (255, 0, 0), [width/3*2, height], [width / 2, height / 2], 10)
            elif event.button == 3:
                scope = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pass
            elif event.button == 3:
                scope = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if -(round(math.sin(math.radians(math_angle)), 3)) > 0:
                    move_x = 0.01
                else:
                    move_x = -0.01
                if round(math.cos(math.radians(math_angle)), 3) > 0:
                    move_y = 0.01
                else:
                    move_y = -0.01

            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if -(round(math.sin(math.radians(math_angle)), 3)) > 0:
                    move_x = -0.01
                else:
                    move_x = 0.01
                if round(math.cos(math.radians(math_angle)), 3) > 0:
                    move_y = -0.01
                else:
                    move_y = 0.01
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                #move_angle = -3
                pass
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                #move_angle = 3
                pass

        if event.type == CAMERA_TIMER:
                turn_angle += move_angle
        if event.type == MOVE_TIMER or 1:
                if maps.map1[round(p_x + move_x)][round(p_y + move_y)] == ".": #No collision
                    p_x += move_x
                    p_y += move_y

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                move_x, move_y = 0, 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                move_x, move_y = 0, 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                #move_angle = 0
                pass
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                #move_angle = 0
                pass
    
    clock.tick(FPS)
    pygame.display.flip()