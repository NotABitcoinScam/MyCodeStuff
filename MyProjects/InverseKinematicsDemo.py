import sys, pygame
import time
from pygame.math import Vector2
import math
pygame.init()

info=pygame.display.Info()

size = width, height = info.current_w, info.current_h
center = width, height = info.current_w/2, info.current_h/2
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

l=150
n=3

'''points = list(map(Vector2, [(center), 
                            (center[0]+1*l,center[1]+1*l), 
                            (center[0]+2*l,center[1]+2*l), 
                            (center[0]+3*l,center[1]+3*l), 
                            ((center[0]+4*l,center[1]+4*l))]))'''

points = [pygame.Vector2(center[0],center[1])]
for i in range(n):
    points.append(pygame.Vector2(center[0]+(i+1)*l,center[1]))


target = Vector2(450, 300)
target_speed = Vector2(3, 3)

rel_points = []
angles = []

max_angle = 360 # Adjust for limited angles

for i in range(1, len(points)):
    rel_points.append(points[i] - points[i-1])
    angles.append(0)

def solve_ik(i, endpoint, target):
    if i < len(points) - 2:
        endpoint = solve_ik(i+1, endpoint, target)
    current_point = points[i]

    angle = (endpoint-current_point).angle_to(target-current_point)
    angles[i] += angle#min(max(-360, angle), 360)
    angles[i] = min(max(180-max_angle, (angles[i]+180)%360), 180+max_angle)-180

    return current_point + (endpoint-current_point).rotate(angle)

def render():
    black = 0, 0, 0
    white = 255, 255, 255

    screen.fill(white)
    for i in range(1, len(points)):
        prev = points[i-1]
        cur = points[i]
        #pygame.draw.aaline(screen, black, prev, cur)
        pygame.draw.line(screen, black, prev, cur, 5)
    '''for point in points:
        #pygame.draw.circle(screen, black, (int(point[0]), int(point[1])), 5)
        pass'''
    for i in range(len(points)):
        pygame.draw.circle(screen, (0,0,0), (int(points[i][0]), int(points[i][1])), 5)
        pass
    pygame.draw.circle(screen, black, (int(target[0]), int(target[1])), 10)
    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    solve_ik(0, points[-1], target)
    angle = 0
    for i in range(1, len(points)):
        angle += angles[i-1]
        points[i] = points[i-1] + rel_points[i-1].rotate(angle)

    '''target += target_speed
    if target.x <= 0 or target.x >= width:
        target_speed.x = -target_speed.x
    if target.y <= 0 or target.y >= height:
        target_speed.y = -target_speed.y'''
    target=pygame.mouse.get_pos()

    render()

    pygame.time.wait(int(1000/60))